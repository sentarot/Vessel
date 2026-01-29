"""
GURPS Combat Engine Module
Handles the resolution of attacks, defenses, and damage.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable
from enum import Enum, auto
import random

from .dice import success_roll, damage_roll, contest_roll, RollResult
from .character import Character, HitLocation, PostureType
from .weapons import DamageType, get_damage_multiplier
from .maneuvers import (
    Maneuver, ManeuverOption, ManeuverType, MANEUVERS, DEFENSES,
    get_available_defenses
)


class CombatPhase(Enum):
    """Phases of a combat turn."""
    START_ROUND = auto()
    INITIATIVE = auto()
    MANEUVER_SELECTION = auto()
    ATTACK_RESOLUTION = auto()
    DEFENSE_RESOLUTION = auto()
    DAMAGE_RESOLUTION = auto()
    END_ROUND = auto()


@dataclass
class AttackResult:
    """Result of an attack roll."""
    attacker: Character
    defender: Character
    maneuver: Maneuver
    attack_skill: int
    attack_roll: any  # DiceRoll
    hit: bool
    critical_hit: bool = False
    critical_miss: bool = False
    auto_hit: bool = False  # For criticals that bypass defense

    def __str__(self) -> str:
        if self.critical_miss:
            return f"{self.attacker.name} critically misses!"
        if self.critical_hit:
            return f"{self.attacker.name} scores a critical hit!"
        if self.hit:
            return f"{self.attacker.name} hits (rolled {self.attack_roll.total} vs {self.attack_skill})"
        return f"{self.attacker.name} misses (rolled {self.attack_roll.total} vs {self.attack_skill})"


@dataclass
class DefenseResult:
    """Result of a defense roll."""
    defender: Character
    defense_type: str
    defense_value: int
    defense_roll: any  # DiceRoll
    defended: bool
    retreated: bool = False
    critical_defense: bool = False
    critical_failure: bool = False

    def __str__(self) -> str:
        retreat_str = " (retreating)" if self.retreated else ""
        if self.critical_defense:
            return f"{self.defender.name} critically succeeds their {self.defense_type}!"
        if self.critical_failure:
            return f"{self.defender.name} critically fails their {self.defense_type}!"
        if self.defended:
            return f"{self.defender.name} {self.defense_type}s successfully{retreat_str} (rolled {self.defense_roll.total} vs {self.defense_value})"
        return f"{self.defender.name} fails to {self.defense_type}{retreat_str} (rolled {self.defense_roll.total} vs {self.defense_value})"


@dataclass
class DamageResult:
    """Result of damage resolution."""
    attacker: Character
    defender: Character
    raw_damage: int
    damage_roll_desc: str
    damage_type: DamageType
    location: HitLocation
    dr: int
    penetrating: int
    injury: int
    effects: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        s = f"{self.attacker.name} deals {self.raw_damage} {self.damage_type.value} damage "
        s += f"to {self.defender.name}'s {self.location.value}. "
        s += f"DR {self.dr} absorbs {min(self.dr, self.raw_damage)}. "
        if self.injury > 0:
            s += f"{self.defender.name} takes {self.injury} injury!"
        else:
            s += f"No damage penetrates!"
        return s


@dataclass
class CombatState:
    """Current state of the combat."""
    combatants: List[Character]
    turn_order: List[Character] = field(default_factory=list)
    current_turn: int = 0
    round_number: int = 1
    phase: CombatPhase = CombatPhase.START_ROUND
    combat_log: List[str] = field(default_factory=list)
    evaluate_bonuses: Dict[str, Dict[str, int]] = field(default_factory=dict)  # attacker -> {defender: bonus}
    feint_penalties: Dict[str, int] = field(default_factory=dict)  # defender -> penalty
    ended: bool = False
    winner: Optional[Character] = None

    def get_current_combatant(self) -> Optional[Character]:
        """Get the character whose turn it is."""
        if not self.turn_order or self.current_turn >= len(self.turn_order):
            return None
        return self.turn_order[self.current_turn]

    def advance_turn(self):
        """Move to the next combatant's turn."""
        self.current_turn += 1
        if self.current_turn >= len(self.turn_order):
            self.current_turn = 0
            self.round_number += 1
            self.log(f"\n=== ROUND {self.round_number} ===")
            # Reset per-round bonuses
            self.feint_penalties.clear()

    def log(self, message: str):
        """Add a message to the combat log."""
        self.combat_log.append(message)

    def check_combat_end(self) -> bool:
        """Check if combat has ended (one side defeated)."""
        alive = [c for c in self.combatants if c.is_conscious()]
        if len(alive) <= 1:
            self.ended = True
            if alive:
                self.winner = alive[0]
            return True
        return False


class CombatEngine:
    """
    Main combat resolution engine for GURPS tactical combat.
    """

    def __init__(self, combatants: List[Character]):
        self.state = CombatState(combatants=combatants)
        self._determine_initiative()

    def _determine_initiative(self):
        """
        Determine turn order based on Basic Speed.
        Higher Basic Speed goes first. Ties broken by DX, then randomly.
        """
        # Sort by Basic Speed (descending), then DX (descending)
        sorted_combatants = sorted(
            self.state.combatants,
            key=lambda c: (c.basic_speed, c.dx, random.random()),
            reverse=True
        )
        self.state.turn_order = sorted_combatants
        self.state.log(f"=== ROUND {self.state.round_number} ===")
        self.state.log("Turn order: " + ", ".join(c.name for c in sorted_combatants))

    def start_turn(self, character: Character):
        """Begin a character's turn."""
        character.start_turn()
        self.state.log(f"\n--- {character.name}'s Turn ---")
        self.state.log(str(character))

        # Check for stun recovery
        if character.status.stunned:
            self._handle_stun_recovery(character)

    def _handle_stun_recovery(self, character: Character):
        """Handle recovery from stun at start of turn."""
        recovery_target = character.ht
        if character.combat_reflexes:
            recovery_target += 6

        roll = success_roll(recovery_target)
        self.state.log(f"{character.name} attempts to recover from stun: {roll}")

        if roll.result in (RollResult.SUCCESS, RollResult.CRITICAL_SUCCESS):
            character.status.stunned = False
            self.state.log(f"{character.name} recovers from stun!")
        else:
            self.state.log(f"{character.name} remains stunned.")

    def resolve_attack(self, attacker: Character, defender: Character,
                       maneuver: Maneuver) -> AttackResult:
        """
        Resolve an attack roll.
        """
        # Calculate effective skill
        base_skill = attacker.get_attack_skill(attacker.equipped_weapon, maneuver.attack_mode)

        # Apply maneuver modifiers
        effective_skill = base_skill + maneuver.get_effective_attack_modifier()

        # Apply shock penalty
        effective_skill -= attacker.status.shock_penalty

        # Apply evaluate bonus if any
        attacker_name = attacker.name
        defender_name = defender.name
        if attacker_name in self.state.evaluate_bonuses:
            if defender_name in self.state.evaluate_bonuses[attacker_name]:
                eval_bonus = self.state.evaluate_bonuses[attacker_name][defender_name]
                effective_skill += eval_bonus
                maneuver.evaluate_bonus = eval_bonus
                # Clear after use
                del self.state.evaluate_bonuses[attacker_name][defender_name]

        # Move and Attack caps skill at 9
        if maneuver.option.maneuver_type == ManeuverType.MOVE_AND_ATTACK:
            effective_skill = min(effective_skill, 9)

        # Make the roll
        roll = success_roll(effective_skill)

        # Determine result
        critical_hit = roll.result == RollResult.CRITICAL_SUCCESS
        critical_miss = roll.result == RollResult.CRITICAL_FAILURE
        hit = roll.result in (RollResult.SUCCESS, RollResult.CRITICAL_SUCCESS)

        result = AttackResult(
            attacker=attacker,
            defender=defender,
            maneuver=maneuver,
            attack_skill=effective_skill,
            attack_roll=roll,
            hit=hit,
            critical_hit=critical_hit,
            critical_miss=critical_miss,
            auto_hit=critical_hit  # Critical hits may bypass some defenses
        )

        self.state.log(str(result))

        # Handle critical miss effects
        if critical_miss:
            self._handle_critical_miss(attacker)

        return result

    def _handle_critical_miss(self, attacker: Character):
        """Handle the effects of a critical miss."""
        # Roll on critical miss table (simplified)
        roll, _ = random.randint(1, 6), None
        effects = [
            "You drop your weapon!",
            "You stumble; -2 to all defenses until next turn.",
            "You fall down!",
            "Your weapon is stuck or tangled.",
            "You hit yourself! Roll normal damage.",
            "You hit a friend (if any) or yourself!"
        ]
        effect = effects[min(roll - 1, len(effects) - 1)]
        self.state.log(f"Critical miss effect: {effect}")

        # Apply simplified effects
        if "drop" in effect.lower():
            attacker.equipped_weapon = None
        elif "fall" in effect.lower():
            attacker.status.posture = PostureType.PRONE
        elif "stumble" in effect.lower():
            attacker.status.defense_bonus -= 2

    def resolve_defense(self, defender: Character, attack_result: AttackResult,
                        defense_type: str, retreat: bool = False) -> DefenseResult:
        """
        Resolve a defense roll.
        """
        # Get base defense value
        if defense_type == "dodge":
            defense_value = defender.get_effective_dodge()
        elif defense_type == "parry":
            defense_value = defender.get_effective_parry()
        elif defense_type == "block":
            defense_value = defender.get_effective_block()
        else:
            raise ValueError(f"Unknown defense type: {defense_type}")

        # Apply retreat bonus
        if retreat and not defender.status.retreated:
            retreat_bonus = DEFENSES[defense_type].get_retreat_bonus()
            defense_value += retreat_bonus
            defender.status.retreated = True

        # Apply feint penalty
        if defender.name in self.state.feint_penalties:
            defense_value -= self.state.feint_penalties[defender.name]

        # Apply committed attack penalty
        if defender.status.committed_attack:
            defense_value -= 2

        # Critical hit may reduce defense options
        if attack_result.critical_hit:
            defense_value -= 2  # Harder to defend against criticals

        # Make the roll
        roll = success_roll(defense_value)

        defended = roll.result in (RollResult.SUCCESS, RollResult.CRITICAL_SUCCESS)
        critical_defense = roll.result == RollResult.CRITICAL_SUCCESS
        critical_failure = roll.result == RollResult.CRITICAL_FAILURE

        result = DefenseResult(
            defender=defender,
            defense_type=defense_type,
            defense_value=defense_value,
            defense_roll=roll,
            defended=defended,
            retreated=retreat,
            critical_defense=critical_defense,
            critical_failure=critical_failure
        )

        self.state.log(str(result))
        return result

    def resolve_damage(self, attacker: Character, defender: Character,
                       maneuver: Maneuver,
                       location: Optional[HitLocation] = None) -> DamageResult:
        """
        Resolve damage from a successful attack.
        """
        # Determine hit location
        if location is None:
            if maneuver.target_location:
                location = maneuver.target_location
            else:
                location = HitLocation.random_location()

        # Calculate damage
        damage_str, damage_type = attacker.calculate_damage(
            attacker.equipped_weapon, maneuver.attack_mode
        )

        # Apply maneuver damage modifier
        damage_mod = maneuver.get_effective_damage_modifier()
        if damage_mod != 0:
            if "+" in damage_str:
                parts = damage_str.split("+")
                old_mod = int(parts[1])
                damage_str = f"{parts[0]}+{old_mod + damage_mod}"
            elif "-" in damage_str and damage_str.count("-") == 1:
                idx = damage_str.index("-")
                dice_part = damage_str[:idx]
                old_mod = -int(damage_str[idx+1:])
                new_mod = old_mod + damage_mod
                if new_mod >= 0:
                    damage_str = f"{dice_part}+{new_mod}" if new_mod > 0 else dice_part
                else:
                    damage_str = f"{dice_part}{new_mod}"
            else:
                if damage_mod > 0:
                    damage_str = f"{damage_str}+{damage_mod}"
                else:
                    damage_str = f"{damage_str}{damage_mod}"

        # Roll damage
        raw_damage, roll_desc = damage_roll(damage_str)

        # Get DR for location
        dr = defender.get_dr(location)

        # Calculate penetrating damage
        penetrating = max(0, raw_damage - dr)

        # Apply damage type multiplier
        if penetrating > 0:
            multiplier = get_damage_multiplier(damage_type)

            # Head multiplier for crushing
            if location == HitLocation.HEAD and damage_type == DamageType.CRUSHING:
                multiplier = max(multiplier, 4)  # x4 for crushing to head (for knockdown)

            injury = int(penetrating * multiplier)
        else:
            injury = 0

        # Apply injury to defender
        damage_report = defender.take_damage(raw_damage, damage_type, location)

        # Build effects list
        effects = []
        if damage_report.get("major_wound"):
            effects.append("Major wound!")
        if damage_report.get("shock", 0) > 0:
            effects.append(f"Shock penalty: -{damage_report['shock']}")
        if damage_report.get("requires_ht_check"):
            effects.append(f"Requires HT check: {damage_report['ht_check_type']}")
        if damage_report.get("dead"):
            effects.append("FATAL!")

        result = DamageResult(
            attacker=attacker,
            defender=defender,
            raw_damage=raw_damage,
            damage_roll_desc=roll_desc,
            damage_type=damage_type,
            location=location,
            dr=dr,
            penetrating=penetrating,
            injury=injury,
            effects=effects
        )

        self.state.log(str(result))
        for effect in effects:
            self.state.log(f"  - {effect}")

        return result

    def execute_maneuver(self, character: Character, maneuver: Maneuver,
                         defender: Optional[Character] = None) -> Dict:
        """
        Execute a complete maneuver, handling all phases.
        Returns a dictionary with the results.
        """
        results = {
            "maneuver": maneuver,
            "attacker": character,
            "defender": defender,
            "attacks": [],
            "defenses": [],
            "damage": []
        }

        # Apply maneuver effects to character
        maneuver.option.apply_to_attacker(character)

        self.state.log(f"{character.name} uses {maneuver.option.name}")

        # Handle non-attack maneuvers
        if maneuver.option.maneuver_type == ManeuverType.EVALUATE:
            self._handle_evaluate(character, defender)
            return results

        if maneuver.option.maneuver_type == ManeuverType.FEINT:
            self._handle_feint(character, defender)
            return results

        if maneuver.option.maneuver_type in (ManeuverType.ALL_OUT_DEFENSE,
                                              ManeuverType.READY,
                                              ManeuverType.MOVE,
                                              ManeuverType.DO_NOTHING):
            return results

        # Handle attacks
        if defender is None:
            return results

        num_attacks = 1 + maneuver.option.extra_attacks

        for i in range(num_attacks):
            if i > 0:
                self.state.log(f"Second attack:")

            attack_result = self.resolve_attack(character, defender, maneuver)
            results["attacks"].append(attack_result)

            if attack_result.hit:
                # Defender gets to defend (unless critical or all-out attack by defender)
                defense_result = None
                if not attack_result.auto_hit or attack_result.critical_hit:
                    available_defenses = get_available_defenses(defender)
                    if available_defenses:
                        # For now, auto-select best defense
                        defense_result = self._auto_defend(defender, attack_result, available_defenses)
                        results["defenses"].append(defense_result)

                # If defense failed or no defense available, resolve damage
                if defense_result is None or not defense_result.defended:
                    damage_result = self.resolve_damage(character, defender, maneuver)
                    results["damage"].append(damage_result)

            # Check if combat should end
            if self.state.check_combat_end():
                break

        return results

    def _auto_defend(self, defender: Character, attack_result: AttackResult,
                     available_defenses: List[str]) -> DefenseResult:
        """
        Automatically choose and execute the best defense.
        """
        # Calculate effective values for each defense
        best_defense = None
        best_value = -999

        for defense in available_defenses:
            if defense == "dodge":
                value = defender.get_effective_dodge()
            elif defense == "parry":
                value = defender.get_effective_parry()
            elif defense == "block":
                value = defender.get_effective_block()
            else:
                continue

            if value > best_value:
                best_value = value
                best_defense = defense

        # Decide on retreat (if not already used)
        should_retreat = not defender.status.retreated and best_value < 12

        return self.resolve_defense(defender, attack_result, best_defense, should_retreat)

    def _handle_evaluate(self, attacker: Character, target: Optional[Character]):
        """Handle the Evaluate maneuver."""
        if target is None:
            self.state.log(f"{attacker.name} evaluates the battlefield.")
            return

        # Initialize nested dict if needed
        if attacker.name not in self.state.evaluate_bonuses:
            self.state.evaluate_bonuses[attacker.name] = {}

        # Add +1 (max +3)
        current = self.state.evaluate_bonuses[attacker.name].get(target.name, 0)
        new_bonus = min(3, current + 1)
        self.state.evaluate_bonuses[attacker.name][target.name] = new_bonus

        self.state.log(f"{attacker.name} evaluates {target.name}. Attack bonus: +{new_bonus}")

    def _handle_feint(self, attacker: Character, defender: Optional[Character]):
        """Handle the Feint maneuver as a Quick Contest."""
        if defender is None:
            self.state.log(f"{attacker.name} feints at the air.")
            return

        # Quick Contest of weapon skills
        attacker_skill = attacker.get_attack_skill()
        defender_skill = max(
            defender.get_attack_skill(),
            defender.get_skill("Brawling")
        )

        roll1, roll2, winner = contest_roll(attacker_skill, defender_skill)

        self.state.log(f"Feint contest: {attacker.name} {roll1} vs {defender.name} {roll2}")

        if winner == 1:
            # Attacker wins - margin becomes defense penalty
            penalty = roll1.margin - roll2.margin
            penalty = max(0, penalty)
            self.state.feint_penalties[defender.name] = penalty
            self.state.log(f"{defender.name} will have -{penalty} to defenses vs {attacker.name}'s next attack.")
        else:
            self.state.log(f"Feint fails - {defender.name} is not fooled.")

    def handle_ht_check(self, character: Character, check_type: str) -> bool:
        """
        Make an HT check for consciousness, death, etc.
        Returns True if passed.
        """
        target = character.ht + character.hard_to_kill

        # Modifiers based on check type
        if check_type == "consciousness":
            # At 0 HP or below
            pass  # Base HT
        elif check_type == "death":
            # At -HP or below
            pass  # Base HT
        elif check_type == "major_wound":
            # Knockdown/stun check
            if character.high_pain_threshold:
                target += 3

        roll = success_roll(target)
        passed = roll.result in (RollResult.SUCCESS, RollResult.CRITICAL_SUCCESS)

        self.state.log(f"{character.name} makes HT check ({check_type}): {roll}")

        if check_type == "consciousness" and not passed:
            character.status.unconscious = True
            self.state.log(f"{character.name} falls unconscious!")
        elif check_type == "death" and not passed:
            character.status.dead = True
            self.state.log(f"{character.name} dies!")
        elif check_type == "major_wound" and not passed:
            character.status.stunned = True
            self.state.log(f"{character.name} is stunned!")

        return passed

    def get_combat_summary(self) -> str:
        """Get a summary of the current combat state."""
        lines = [f"\n=== Combat Summary (Round {self.state.round_number}) ==="]

        for c in self.state.combatants:
            status = "DEAD" if c.status.dead else "KO" if c.status.unconscious else "Active"
            lines.append(f"  {c.name}: HP {c.status.current_hp}/{c.max_hp}, FP {c.status.current_fp}/{c.max_fp} [{status}]")

        if self.state.ended:
            if self.state.winner:
                lines.append(f"\nVictor: {self.state.winner.name}!")
            else:
                lines.append("\nCombat ended in mutual defeat.")

        return "\n".join(lines)
