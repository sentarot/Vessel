"""
GURPS Character Module
Implements character creation and management with GURPS 4th Edition rules.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math

from .dice import calculate_thrust_damage, calculate_swing_damage
from .weapons import Weapon, Armor, WEAPONS, ARMORS, DamageType


class HitLocation(Enum):
    """Body hit locations for targeted attacks."""
    TORSO = "torso"         # Default, no modifier
    HEAD = "head"           # -5 to hit, x4 damage for crushing
    FACE = "face"           # -5 to hit (or -7 for eyes)
    NECK = "neck"           # -5 to hit
    ARM = "arm"             # -2 to hit
    HAND = "hand"           # -4 to hit
    LEG = "leg"             # -2 to hit
    FOOT = "foot"           # -4 to hit
    GROIN = "groin"         # -3 to hit

    @staticmethod
    def get_hit_modifier(location: 'HitLocation') -> int:
        """Return the to-hit modifier for targeting this location."""
        modifiers = {
            HitLocation.TORSO: 0,
            HitLocation.HEAD: -5,
            HitLocation.FACE: -5,
            HitLocation.NECK: -5,
            HitLocation.ARM: -2,
            HitLocation.HAND: -4,
            HitLocation.LEG: -2,
            HitLocation.FOOT: -4,
            HitLocation.GROIN: -3
        }
        return modifiers.get(location, 0)

    @staticmethod
    def random_location() -> 'HitLocation':
        """Roll 3d6 for random hit location."""
        from .dice import roll_3d6
        roll, _ = roll_3d6()

        location_table = {
            (3, 4): HitLocation.HEAD,
            (5,): HitLocation.FACE,
            (6, 7): HitLocation.LEG,      # Right leg
            (8,): HitLocation.ARM,        # Right arm
            (9, 10, 11): HitLocation.TORSO,
            (12,): HitLocation.ARM,       # Left arm
            (13, 14): HitLocation.LEG,    # Left leg
            (15,): HitLocation.HAND,
            (16,): HitLocation.FOOT,
            (17, 18): HitLocation.NECK
        }

        for rolls, location in location_table.items():
            if roll in rolls:
                return location
        return HitLocation.TORSO


class PostureType(Enum):
    """Character postures affecting combat."""
    STANDING = "standing"
    CROUCHING = "crouching"     # -2 to be hit by ranged
    KNEELING = "kneeling"       # -2 to hit in melee, -2 to be hit by ranged
    CRAWLING = "crawling"       # Move at 1/3, -4 to hit, -2 to be hit
    PRONE = "prone"             # -4 to hit, -3 to be hit by ranged


@dataclass
class CharacterStatus:
    """Current combat status of a character."""
    current_hp: int = 10
    current_fp: int = 10
    shock_penalty: int = 0      # Penalty from recent damage
    stunned: bool = False
    prone: bool = False
    posture: PostureType = PostureType.STANDING
    unconscious: bool = False
    dead: bool = False
    major_wound: bool = False   # Failed HT roll from >HP/2 damage
    defense_bonus: int = 0      # Temporary defense bonus (from maneuvers)
    attack_bonus: int = 0       # Temporary attack bonus
    all_out_attack: bool = False
    committed_attack: bool = False
    retreated: bool = False     # Has used retreat this turn


@dataclass
class Character:
    """
    A GURPS character with full combat statistics.
    """
    name: str

    # Primary Attributes (default 10 for humans)
    st: int = 10    # Strength
    dx: int = 10    # Dexterity
    iq: int = 10    # Intelligence
    ht: int = 10    # Health

    # Skills (name -> level)
    skills: Dict[str, int] = field(default_factory=dict)

    # Equipment
    weapons: List[Weapon] = field(default_factory=list)
    armor: List[Armor] = field(default_factory=list)
    equipped_weapon: Optional[Weapon] = None
    equipped_shield: Optional[Weapon] = None

    # Combat status
    status: CharacterStatus = field(default_factory=CharacterStatus)

    # Advantages/Disadvantages affecting combat
    combat_reflexes: bool = False  # +1 to all defenses, +6 to recover from stun
    high_pain_threshold: bool = False  # No shock penalty
    hard_to_kill: int = 0  # Bonus to HT rolls to stay alive

    def __post_init__(self):
        """Initialize derived statistics."""
        self.status.current_hp = self.max_hp
        self.status.current_fp = self.max_fp

        # Add default unarmed combat
        if "Brawling" not in self.skills:
            self.skills["Brawling"] = self.dx

    # Derived Attributes
    @property
    def max_hp(self) -> int:
        """Hit Points, based on ST."""
        return self.st

    @property
    def max_fp(self) -> int:
        """Fatigue Points, based on HT."""
        return self.ht

    @property
    def will(self) -> int:
        """Will, based on IQ."""
        return self.iq

    @property
    def perception(self) -> int:
        """Perception, based on IQ."""
        return self.iq

    @property
    def basic_speed(self) -> float:
        """Basic Speed = (HT + DX) / 4."""
        return (self.ht + self.dx) / 4

    @property
    def basic_move(self) -> int:
        """Basic Move = Basic Speed (rounded down)."""
        return int(self.basic_speed)

    @property
    def dodge(self) -> int:
        """Base Dodge = Basic Speed + 3 (rounded down)."""
        base = int(self.basic_speed) + 3
        if self.combat_reflexes:
            base += 1
        return base

    @property
    def thrust_damage(self) -> str:
        """Thrust damage based on ST."""
        return calculate_thrust_damage(self.st)

    @property
    def swing_damage(self) -> str:
        """Swing damage based on ST."""
        return calculate_swing_damage(self.st)

    def get_skill(self, skill_name: str) -> int:
        """Get effective skill level, defaulting to attribute-based default."""
        if skill_name in self.skills:
            return self.skills[skill_name]

        # Common skill defaults
        defaults = {
            "Brawling": self.dx,
            "Karate": self.dx - 5,
            "Wrestling": self.dx - 5,
            "Broadsword": self.dx - 5,
            "Shortsword": self.dx - 5,
            "Knife": self.dx - 4,
            "Shield": self.dx - 4,
            "Axe/Mace": self.dx - 5,
            "Spear": self.dx - 5,
            "Staff": self.dx - 5,
            "Two-Handed Sword": self.dx - 5,
            "Polearm": self.dx - 5,
            "Rapier": self.dx - 5,
            "Two-Handed Axe/Mace": self.dx - 5,
        }
        return defaults.get(skill_name, self.dx - 6)

    def get_parry(self, weapon: Optional[Weapon] = None) -> int:
        """
        Calculate parry value.
        Parry = 3 + (Skill / 2) + weapon modifier
        """
        if weapon is None:
            weapon = self.equipped_weapon

        if weapon is None:
            # Unarmed parry with Brawling
            skill = self.get_skill("Brawling")
            base_parry = 3 + skill // 2
        else:
            attack = weapon.primary_attack
            skill = self.get_skill(attack.skill)
            base_parry = 3 + skill // 2 + attack.parry_mod

        if self.combat_reflexes:
            base_parry += 1

        return base_parry

    def get_block(self) -> int:
        """
        Calculate block value (requires shield).
        Block = 3 + (Shield Skill / 2) + Defense Bonus
        """
        if self.equipped_shield is None:
            return 0

        skill = self.get_skill("Shield")
        base_block = 3 + skill // 2 + self.equipped_shield.db

        if self.combat_reflexes:
            base_block += 1

        return base_block

    def get_dr(self, location: HitLocation = HitLocation.TORSO) -> int:
        """Get Damage Resistance for a body location."""
        total_dr = 0
        loc_str = location.value

        for armor_piece in self.armor:
            if loc_str in armor_piece.locations:
                total_dr += armor_piece.dr

        return total_dr

    def get_attack_skill(self, weapon: Optional[Weapon] = None, attack_name: Optional[str] = None) -> int:
        """Get the effective attack skill."""
        if weapon is None:
            weapon = self.equipped_weapon

        if weapon is None:
            # Unarmed attack
            return self.get_skill("Brawling")

        attack = weapon.get_attack(attack_name) if attack_name else weapon.primary_attack
        return self.get_skill(attack.skill)

    def calculate_damage(self, weapon: Optional[Weapon] = None, attack_name: Optional[str] = None) -> Tuple[str, DamageType]:
        """
        Calculate damage string for an attack.
        Returns (damage_string, damage_type).
        """
        if weapon is None:
            weapon = self.equipped_weapon

        if weapon is None:
            # Unarmed: thrust-1 crushing
            return self._apply_damage_mod(self.thrust_damage, -1), DamageType.CRUSHING

        attack = weapon.get_attack(attack_name) if attack_name else weapon.primary_attack

        if attack.damage_base == "thr":
            base = self.thrust_damage
        else:  # "sw"
            base = self.swing_damage

        return self._apply_damage_mod(base, attack.damage_mod), attack.damage_type

    def _apply_damage_mod(self, base_damage: str, mod: int) -> str:
        """Apply a modifier to a damage string."""
        if mod == 0:
            return base_damage

        # Parse existing modifier
        if "+" in base_damage:
            parts = base_damage.split("+")
            dice_part = parts[0]
            existing_mod = int(parts[1])
        elif "-" in base_damage and base_damage.count("-") == 1:
            # Handle "1d-2" format
            idx = base_damage.index("-")
            dice_part = base_damage[:idx]
            existing_mod = -int(base_damage[idx+1:])
        else:
            dice_part = base_damage
            existing_mod = 0

        new_mod = existing_mod + mod

        if new_mod > 0:
            return f"{dice_part}+{new_mod}"
        elif new_mod < 0:
            return f"{dice_part}{new_mod}"
        else:
            return dice_part

    def take_damage(self, damage: int, damage_type: DamageType, location: HitLocation = HitLocation.TORSO) -> Dict:
        """
        Apply damage to the character.
        Returns a dict with damage report.
        """
        from .weapons import get_damage_multiplier

        dr = self.get_dr(location)
        penetrating = max(0, damage - dr)

        # Apply damage type multiplier to penetrating damage
        if penetrating > 0:
            multiplier = get_damage_multiplier(damage_type)
            injury = int(penetrating * multiplier)
        else:
            injury = 0

        # Special: crushing to head does x4 for knockdown purposes
        is_major_wound = injury > self.max_hp // 2

        # Apply injury
        old_hp = self.status.current_hp
        self.status.current_hp -= injury

        # Apply shock (unless High Pain Threshold)
        if not self.high_pain_threshold and injury > 0:
            self.status.shock_penalty = min(4, injury)

        result = {
            "raw_damage": damage,
            "damage_type": damage_type.value,
            "location": location.value,
            "dr": dr,
            "penetrating": penetrating,
            "injury": injury,
            "hp_before": old_hp,
            "hp_after": self.status.current_hp,
            "shock": self.status.shock_penalty,
            "major_wound": is_major_wound
        }

        # Check for death/unconsciousness
        self._check_health_status(result, is_major_wound, location)

        return result

    def _check_health_status(self, result: Dict, major_wound: bool, location: HitLocation):
        """Check for stun, unconsciousness, and death."""
        hp = self.status.current_hp
        max_hp = self.max_hp

        # Major wound check
        if major_wound:
            result["requires_ht_check"] = True
            result["ht_check_type"] = "major_wound"

        # At 0 HP or below: make HT roll each turn to stay conscious
        if hp <= 0:
            result["requires_ht_check"] = True
            result["ht_check_type"] = "consciousness"

        # At -HP: make HT roll or die
        if hp <= -max_hp:
            result["requires_ht_check"] = True
            result["ht_check_type"] = "death"

        # At -5xHP: automatic death
        if hp <= -5 * max_hp:
            self.status.dead = True
            result["dead"] = True

    def heal(self, amount: int):
        """Heal HP."""
        self.status.current_hp = min(self.max_hp, self.status.current_hp + amount)

    def rest(self, minutes: int = 10):
        """Recover FP from rest."""
        if minutes >= 10:
            fp_recovered = minutes // 10
            self.status.current_fp = min(self.max_fp, self.status.current_fp + fp_recovered)

    def start_turn(self):
        """Reset per-turn status at the start of a turn."""
        self.status.shock_penalty = max(0, self.status.shock_penalty - 1)  # Shock reduces each turn
        self.status.defense_bonus = 0
        self.status.attack_bonus = 0
        self.status.all_out_attack = False
        self.status.committed_attack = False
        self.status.retreated = False

    def is_alive(self) -> bool:
        """Check if character is still alive."""
        return not self.status.dead

    def is_conscious(self) -> bool:
        """Check if character is conscious."""
        return self.is_alive() and not self.status.unconscious

    def can_act(self) -> bool:
        """Check if character can take actions."""
        return self.is_conscious() and not self.status.stunned

    def get_effective_dodge(self) -> int:
        """Get current dodge including all modifiers."""
        base = self.dodge

        # Encumbrance would reduce this
        # Posture modifiers
        if self.status.posture == PostureType.PRONE:
            base -= 3

        # Shock penalty
        base -= self.status.shock_penalty

        # Temporary bonuses
        base += self.status.defense_bonus

        # Cannot dodge if all-out attacking
        if self.status.all_out_attack:
            return 0

        return max(3, base)  # Minimum dodge is 3

    def get_effective_parry(self) -> int:
        """Get current parry including all modifiers."""
        base = self.get_parry()

        # Shock penalty
        base -= self.status.shock_penalty

        # Temporary bonuses
        base += self.status.defense_bonus

        # Cannot parry if all-out attacking
        if self.status.all_out_attack:
            return 0

        return max(3, base)

    def get_effective_block(self) -> int:
        """Get current block including all modifiers."""
        base = self.get_block()
        if base == 0:
            return 0

        # Shock penalty
        base -= self.status.shock_penalty

        # Temporary bonuses
        base += self.status.defense_bonus

        # Cannot block if all-out attacking
        if self.status.all_out_attack:
            return 0

        return max(3, base)

    def __str__(self) -> str:
        weapon_name = self.equipped_weapon.name if self.equipped_weapon else "Unarmed"
        return f"{self.name} [HP:{self.status.current_hp}/{self.max_hp} FP:{self.status.current_fp}/{self.max_fp}] ({weapon_name})"


class CharacterBuilder:
    """Helper class for creating characters with templates."""

    @staticmethod
    def create_warrior(name: str, level: str = "average") -> Character:
        """Create a warrior-type character."""
        configs = {
            "weak": {"st": 11, "dx": 11, "iq": 9, "ht": 11, "skill_bonus": 0},
            "average": {"st": 12, "dx": 12, "iq": 10, "ht": 12, "skill_bonus": 2},
            "strong": {"st": 14, "dx": 13, "iq": 10, "ht": 13, "skill_bonus": 4},
            "elite": {"st": 15, "dx": 14, "iq": 11, "ht": 14, "skill_bonus": 6}
        }
        cfg = configs.get(level, configs["average"])

        char = Character(
            name=name,
            st=cfg["st"],
            dx=cfg["dx"],
            iq=cfg["iq"],
            ht=cfg["ht"],
            skills={
                "Broadsword": cfg["dx"] + cfg["skill_bonus"],
                "Shield": cfg["dx"] + cfg["skill_bonus"],
                "Brawling": cfg["dx"] + cfg["skill_bonus"] - 1
            }
        )

        # Equip gear
        char.equipped_weapon = WEAPONS["broadsword"]
        char.equipped_shield = WEAPONS["medium_shield"]
        char.weapons = [char.equipped_weapon, char.equipped_shield]
        char.armor = [ARMORS["mail_shirt"], ARMORS["light_helm"]]

        return char

    @staticmethod
    def create_rogue(name: str, level: str = "average") -> Character:
        """Create a rogue-type character."""
        configs = {
            "weak": {"st": 10, "dx": 12, "iq": 10, "ht": 10, "skill_bonus": 0},
            "average": {"st": 10, "dx": 13, "iq": 11, "ht": 11, "skill_bonus": 2},
            "strong": {"st": 11, "dx": 14, "iq": 12, "ht": 12, "skill_bonus": 4},
            "elite": {"st": 11, "dx": 16, "iq": 13, "ht": 12, "skill_bonus": 6}
        }
        cfg = configs.get(level, configs["average"])

        char = Character(
            name=name,
            st=cfg["st"],
            dx=cfg["dx"],
            iq=cfg["iq"],
            ht=cfg["ht"],
            skills={
                "Rapier": cfg["dx"] + cfg["skill_bonus"],
                "Knife": cfg["dx"] + cfg["skill_bonus"],
                "Brawling": cfg["dx"] + cfg["skill_bonus"] - 1
            },
            combat_reflexes=True
        )

        char.equipped_weapon = WEAPONS["rapier"]
        char.weapons = [char.equipped_weapon, WEAPONS["knife"]]
        char.armor = [ARMORS["leather_armor"]]

        return char

    @staticmethod
    def create_brute(name: str, level: str = "average") -> Character:
        """Create a brute-type character (heavy hitter)."""
        configs = {
            "weak": {"st": 13, "dx": 10, "iq": 8, "ht": 12, "skill_bonus": 0},
            "average": {"st": 15, "dx": 11, "iq": 9, "ht": 13, "skill_bonus": 1},
            "strong": {"st": 17, "dx": 11, "iq": 9, "ht": 14, "skill_bonus": 2},
            "elite": {"st": 19, "dx": 12, "iq": 9, "ht": 15, "skill_bonus": 4}
        }
        cfg = configs.get(level, configs["average"])

        char = Character(
            name=name,
            st=cfg["st"],
            dx=cfg["dx"],
            iq=cfg["iq"],
            ht=cfg["ht"],
            skills={
                "Two-Handed Axe/Mace": cfg["dx"] + cfg["skill_bonus"],
                "Brawling": cfg["dx"] + cfg["skill_bonus"]
            },
            high_pain_threshold=True
        )

        char.equipped_weapon = WEAPONS["great_axe"]
        char.weapons = [char.equipped_weapon]
        char.armor = [ARMORS["scale_armor"], ARMORS["heavy_helm"]]

        return char

    @staticmethod
    def create_custom(name: str, st: int = 10, dx: int = 10, iq: int = 10, ht: int = 10,
                      skills: Optional[Dict[str, int]] = None,
                      weapon: Optional[str] = None,
                      armor: Optional[List[str]] = None) -> Character:
        """Create a fully customized character."""
        char = Character(
            name=name,
            st=st, dx=dx, iq=iq, ht=ht,
            skills=skills or {}
        )

        if weapon and weapon in WEAPONS:
            char.equipped_weapon = WEAPONS[weapon]
            char.weapons = [char.equipped_weapon]

        if armor:
            char.armor = [ARMORS[a] for a in armor if a in ARMORS]

        return char
