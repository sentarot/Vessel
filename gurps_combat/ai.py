"""
GURPS AI Controller Module
Implements AI decision-making for computer-controlled combatants.
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple
from enum import Enum
import random

from .character import Character, HitLocation
from .maneuvers import (
    Maneuver, ManeuverOption, ManeuverType, MANEUVERS,
    get_available_maneuvers, get_available_defenses
)


class AIPersonality(Enum):
    """AI behavior styles."""
    AGGRESSIVE = "aggressive"    # Prefers all-out attacks, high risk
    DEFENSIVE = "defensive"      # Prefers defensive options, low risk
    BALANCED = "balanced"        # Mix of offense and defense
    BERSERKER = "berserker"      # Always all-out attack, never retreat
    TACTICAL = "tactical"        # Uses feints, evaluates, targets locations
    COWARD = "coward"            # Runs away when hurt, very defensive


@dataclass
class AIState:
    """Tracks AI decision-making state."""
    personality: AIPersonality
    evaluate_count: int = 0      # How many times we've evaluated current target
    consecutive_misses: int = 0  # Track missed attacks to adjust strategy
    consecutive_hits: int = 0    # Track successful attacks
    last_maneuver: Optional[str] = None
    target: Optional[Character] = None


class AIController:
    """
    AI controller for computer-controlled combatants.
    Makes decisions about maneuvers and defenses based on personality and situation.
    """

    def __init__(self, character: Character, personality: AIPersonality = AIPersonality.BALANCED):
        self.character = character
        self.state = AIState(personality=personality)

    def choose_maneuver(self, enemies: List[Character],
                        allies: List[Character] = None) -> Tuple[ManeuverOption, Optional[Character], Optional[str], Optional[HitLocation]]:
        """
        Choose a maneuver for this turn.
        Returns (maneuver, target, attack_mode, target_location).
        """
        # Get available maneuvers
        available = get_available_maneuvers(self.character)

        # Find valid targets
        valid_enemies = [e for e in enemies if e.is_conscious()]
        if not valid_enemies:
            return MANEUVERS["do_nothing"], None, None, None

        # Choose target (for now, the most wounded enemy or random)
        target = self._choose_target(valid_enemies)
        self.state.target = target

        # Choose maneuver based on personality and situation
        maneuver = self._select_maneuver(available, target)

        # Choose attack mode if applicable
        attack_mode = self._choose_attack_mode(maneuver)

        # Choose target location
        target_location = self._choose_target_location(maneuver, target)

        return maneuver, target, attack_mode, target_location

    def _choose_target(self, enemies: List[Character]) -> Character:
        """Select a target from available enemies."""
        if not enemies:
            return None

        personality = self.state.personality

        if personality == AIPersonality.TACTICAL:
            # Target most wounded enemy
            return min(enemies, key=lambda e: e.status.current_hp / e.max_hp)

        elif personality == AIPersonality.COWARD:
            # Target weakest looking enemy (lowest HP)
            return min(enemies, key=lambda e: e.max_hp)

        elif personality == AIPersonality.BERSERKER:
            # Target closest/first enemy, never switch
            if self.state.target and self.state.target in enemies:
                return self.state.target
            return enemies[0]

        else:
            # Random or stick with current target
            if self.state.target and self.state.target in enemies and random.random() < 0.7:
                return self.state.target
            return random.choice(enemies)

    def _select_maneuver(self, available: List[ManeuverOption],
                         target: Character) -> ManeuverOption:
        """Select a maneuver based on personality and situation."""
        personality = self.state.personality
        hp_ratio = self.character.status.current_hp / self.character.max_hp
        target_hp_ratio = target.status.current_hp / target.max_hp if target else 1.0

        # Filter to attack maneuvers for convenience
        attacks = [m for m in available if m.maneuver_type in (
            ManeuverType.ATTACK, ManeuverType.ALL_OUT_ATTACK,
            ManeuverType.COMMITTED_ATTACK, ManeuverType.DEFENSIVE_ATTACK,
            ManeuverType.MOVE_AND_ATTACK
        )]

        # Berserker always goes all-out
        if personality == AIPersonality.BERSERKER:
            return random.choice([
                MANEUVERS["all_out_attack_determined"],
                MANEUVERS["all_out_attack_strong"],
                MANEUVERS["all_out_attack_double"]
            ])

        # Coward runs or defends when hurt
        if personality == AIPersonality.COWARD:
            if hp_ratio < 0.5:
                return random.choice([
                    MANEUVERS["all_out_defense_increased"],
                    MANEUVERS["defensive_attack"]
                ])
            elif hp_ratio < 0.75:
                return MANEUVERS["defensive_attack"]

        # Defensive personality
        if personality == AIPersonality.DEFENSIVE:
            if hp_ratio < 0.5:
                return MANEUVERS["all_out_defense_increased"]
            if random.random() < 0.3:
                return MANEUVERS["defensive_attack"]
            return MANEUVERS["attack"]

        # Aggressive personality
        if personality == AIPersonality.AGGRESSIVE:
            if target_hp_ratio < 0.3:
                # Go for the kill
                return MANEUVERS["all_out_attack_strong"]
            if hp_ratio > 0.7:
                return random.choice([
                    MANEUVERS["all_out_attack_determined"],
                    MANEUVERS["committed_attack_determined"],
                    MANEUVERS["attack"]
                ])
            return MANEUVERS["committed_attack_determined"]

        # Tactical personality
        if personality == AIPersonality.TACTICAL:
            # Build up evaluate bonus before attacking
            if self.state.evaluate_count < 2 and random.random() < 0.4:
                self.state.evaluate_count += 1
                return MANEUVERS["evaluate"]

            # Use feint occasionally
            if self.state.consecutive_misses >= 2 and random.random() < 0.5:
                return MANEUVERS["feint"]

            # Reset evaluate count after attacking
            self.state.evaluate_count = 0

            # Smart attack choice
            if target_hp_ratio < 0.3:
                return MANEUVERS["committed_attack_strong"]
            if hp_ratio < 0.5:
                return MANEUVERS["defensive_attack"]
            return MANEUVERS["attack"]

        # Balanced personality (default)
        weights = {
            "attack": 40,
            "all_out_attack_determined": 15 if hp_ratio > 0.5 else 5,
            "all_out_attack_strong": 10 if target_hp_ratio < 0.5 else 5,
            "committed_attack_determined": 15,
            "defensive_attack": 10 if hp_ratio < 0.7 else 5,
            "evaluate": 5
        }

        maneuver_names = list(weights.keys())
        maneuver_weights = list(weights.values())
        chosen = random.choices(maneuver_names, weights=maneuver_weights, k=1)[0]

        return MANEUVERS[chosen]

    def _choose_attack_mode(self, maneuver: ManeuverOption) -> Optional[str]:
        """Choose which attack mode to use (Swing vs Thrust, etc.)."""
        weapon = self.character.equipped_weapon
        if weapon is None:
            return None

        if len(weapon.attacks) == 1:
            return weapon.attacks[0].name

        # Generally prefer swing (more damage) unless low on HP
        personality = self.state.personality
        hp_ratio = self.character.status.current_hp / self.character.max_hp

        swing_attacks = [a for a in weapon.attacks if a.damage_base == "sw"]
        thrust_attacks = [a for a in weapon.attacks if a.damage_base == "thr"]

        # Aggressive/berserker prefers high damage
        if personality in (AIPersonality.AGGRESSIVE, AIPersonality.BERSERKER):
            if swing_attacks:
                return swing_attacks[0].name

        # Defensive/coward might prefer thrust (usually faster recovery)
        if personality in (AIPersonality.DEFENSIVE, AIPersonality.COWARD):
            if thrust_attacks:
                return thrust_attacks[0].name

        # Default: swing for more damage when healthy, thrust when hurt
        if hp_ratio > 0.5 and swing_attacks:
            return swing_attacks[0].name
        elif thrust_attacks:
            return thrust_attacks[0].name
        elif swing_attacks:
            return swing_attacks[0].name

        return weapon.attacks[0].name

    def _choose_target_location(self, maneuver: ManeuverOption,
                                target: Character) -> Optional[HitLocation]:
        """Choose a specific hit location for called shots."""
        personality = self.state.personality

        # Only tactical AI uses called shots
        if personality != AIPersonality.TACTICAL:
            return None

        # Don't called shot with all-out attacks (need the hit)
        if maneuver.maneuver_type == ManeuverType.ALL_OUT_ATTACK:
            return None

        # Random chance to attempt called shot
        if random.random() > 0.3:
            return None

        # Check target's armor
        target_head_dr = target.get_dr(HitLocation.HEAD)
        target_torso_dr = target.get_dr(HitLocation.TORSO)

        # Target head if less armored
        if target_head_dr < target_torso_dr:
            return HitLocation.HEAD

        # Target vitals (torso with bonus damage) implied by torso hit
        # Target legs to reduce mobility
        if random.random() < 0.3:
            return HitLocation.LEG

        return None

    def choose_defense(self, available_defenses: List[str],
                       attack_margin: int) -> Tuple[str, bool]:
        """
        Choose which defense to use and whether to retreat.
        Returns (defense_type, should_retreat).
        """
        personality = self.state.personality
        hp_ratio = self.character.status.current_hp / self.character.max_hp

        # Can't retreat if already did this turn
        can_retreat = not self.character.status.retreated

        # Calculate effective defense values
        defense_values = {}
        for defense in available_defenses:
            if defense == "dodge":
                base = self.character.get_effective_dodge()
            elif defense == "parry":
                base = self.character.get_effective_parry()
            elif defense == "block":
                base = self.character.get_effective_block()
            else:
                continue
            defense_values[defense] = base

        # Find best defense
        best_defense = max(defense_values, key=defense_values.get)
        best_value = defense_values[best_defense]

        # Determine if we should retreat
        should_retreat = False
        if can_retreat:
            # Retreat if defense is uncertain
            if personality == AIPersonality.COWARD:
                should_retreat = True
            elif personality == AIPersonality.BERSERKER:
                should_retreat = False
            elif best_value < 12:  # Less than 75% success chance
                should_retreat = True
            elif hp_ratio < 0.5:  # Desperate
                should_retreat = True

        return best_defense, should_retreat

    def notify_attack_result(self, hit: bool, damage: int = 0):
        """Update AI state based on attack result."""
        if hit:
            self.state.consecutive_hits += 1
            self.state.consecutive_misses = 0
        else:
            self.state.consecutive_misses += 1
            self.state.consecutive_hits = 0

    def get_personality_description(self) -> str:
        """Get a description of this AI's personality."""
        descriptions = {
            AIPersonality.AGGRESSIVE: "Fights aggressively, pressing the attack",
            AIPersonality.DEFENSIVE: "Fights cautiously, prioritizing defense",
            AIPersonality.BALANCED: "Fights with a mix of offense and defense",
            AIPersonality.BERSERKER: "Attacks recklessly with no regard for safety",
            AIPersonality.TACTICAL: "Fights intelligently, using feints and targeting weak points",
            AIPersonality.COWARD: "Fights hesitantly, retreating when hurt"
        }
        return descriptions.get(self.state.personality, "Unknown fighting style")


def create_ai_opponent(name: str, level: str = "average",
                       personality: AIPersonality = None) -> Tuple[Character, AIController]:
    """
    Create a complete AI opponent with character and controller.
    """
    from .character import CharacterBuilder

    # Choose random personality if not specified
    if personality is None:
        personality = random.choice([
            AIPersonality.AGGRESSIVE,
            AIPersonality.DEFENSIVE,
            AIPersonality.BALANCED,
            AIPersonality.TACTICAL
        ])

    # Choose random archetype
    archetype = random.choice(["warrior", "rogue", "brute"])

    if archetype == "warrior":
        character = CharacterBuilder.create_warrior(name, level)
    elif archetype == "rogue":
        character = CharacterBuilder.create_rogue(name, level)
    else:
        character = CharacterBuilder.create_brute(name, level)

    controller = AIController(character, personality)

    return character, controller
