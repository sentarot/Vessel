"""
GURPS Combat Maneuvers Module
Implements the various combat maneuvers available in GURPS.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Callable, TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from .character import Character, HitLocation


class ManeuverType(Enum):
    """Types of combat maneuvers."""
    ATTACK = auto()           # Basic attack
    ALL_OUT_ATTACK = auto()   # +4 to hit or +damage, no defenses
    MOVE_AND_ATTACK = auto()  # Move and attack at -4
    COMMITTED_ATTACK = auto() # +2 to hit, limited defenses
    DEFENSIVE_ATTACK = auto() # -2 to hit, +1 to one defense
    FEINT = auto()            # Contest vs defense to set up next attack
    EVALUATE = auto()         # +1 to attacks vs target (stacks 3x)
    ALL_OUT_DEFENSE = auto()  # +2 to one defense or 2 defenses
    CONCENTRATE = auto()      # For spells/special abilities
    READY = auto()            # Change weapon, stand up, etc.
    WAIT = auto()             # Triggered action
    DO_NOTHING = auto()       # Stunned, etc.
    AIM = auto()              # For ranged (+Acc bonus)
    MOVE = auto()             # Full move, no attack


class AllOutAttackType(Enum):
    """Sub-types of All-Out Attack."""
    DETERMINED = "determined"   # +4 to hit
    STRONG = "strong"           # +2 damage or +1 damage per die
    DOUBLE = "double"           # Two attacks
    FEINT = "feint"             # Feint then attack
    LONG = "long"               # +1 reach (or +2 for 2H)


class AllOutDefenseType(Enum):
    """Sub-types of All-Out Defense."""
    INCREASED = "increased"     # +2 to one defense
    DOUBLE = "double"           # Two different defenses vs same attack


class CommittedAttackType(Enum):
    """Sub-types of Committed Attack."""
    DETERMINED = "determined"   # +2 to hit
    STRONG = "strong"           # +1 damage


@dataclass
class ManeuverOption:
    """Represents a specific maneuver choice with its effects."""
    name: str
    maneuver_type: ManeuverType
    description: str
    attack_modifier: int = 0
    damage_modifier: int = 0
    damage_dice_bonus: int = 0  # Extra dice of damage
    defense_modifier: int = 0
    can_defend: bool = True
    defenses_allowed: int = 99  # Number of defenses per turn
    movement_multiplier: float = 1.0  # Fraction of normal move
    extra_attacks: int = 0
    subtype: Optional[str] = None

    def apply_to_attacker(self, character: 'Character'):
        """Apply maneuver effects to the character."""
        character.status.attack_bonus += self.attack_modifier
        character.status.defense_bonus += self.defense_modifier

        if self.maneuver_type == ManeuverType.ALL_OUT_ATTACK:
            character.status.all_out_attack = True
        elif self.maneuver_type == ManeuverType.COMMITTED_ATTACK:
            character.status.committed_attack = True


# Standard maneuver definitions
MANEUVERS = {
    # Basic Attack
    "attack": ManeuverOption(
        name="Attack",
        maneuver_type=ManeuverType.ATTACK,
        description="Make a standard melee attack. You may defend normally."
    ),

    # All-Out Attack variants
    "all_out_attack_determined": ManeuverOption(
        name="All-Out Attack (Determined)",
        maneuver_type=ManeuverType.ALL_OUT_ATTACK,
        description="+4 to hit, but you cannot defend until your next turn.",
        attack_modifier=4,
        can_defend=False,
        subtype=AllOutAttackType.DETERMINED.value
    ),
    "all_out_attack_strong": ManeuverOption(
        name="All-Out Attack (Strong)",
        maneuver_type=ManeuverType.ALL_OUT_ATTACK,
        description="+2 to damage, but you cannot defend until your next turn.",
        damage_modifier=2,
        can_defend=False,
        subtype=AllOutAttackType.STRONG.value
    ),
    "all_out_attack_double": ManeuverOption(
        name="All-Out Attack (Double)",
        maneuver_type=ManeuverType.ALL_OUT_ATTACK,
        description="Make two attacks, but you cannot defend until your next turn.",
        extra_attacks=1,
        can_defend=False,
        subtype=AllOutAttackType.DOUBLE.value
    ),

    # Committed Attack variants
    "committed_attack_determined": ManeuverOption(
        name="Committed Attack (Determined)",
        maneuver_type=ManeuverType.COMMITTED_ATTACK,
        description="+2 to hit, -2 to all defenses, only one defense allowed.",
        attack_modifier=2,
        defense_modifier=-2,
        defenses_allowed=1,
        subtype=CommittedAttackType.DETERMINED.value
    ),
    "committed_attack_strong": ManeuverOption(
        name="Committed Attack (Strong)",
        maneuver_type=ManeuverType.COMMITTED_ATTACK,
        description="+1 to damage, -2 to all defenses, only one defense allowed.",
        damage_modifier=1,
        defense_modifier=-2,
        defenses_allowed=1,
        subtype=CommittedAttackType.STRONG.value
    ),

    # Defensive Attack
    "defensive_attack": ManeuverOption(
        name="Defensive Attack",
        maneuver_type=ManeuverType.DEFENSIVE_ATTACK,
        description="-2 to hit, +1 to your next Parry or Block.",
        attack_modifier=-2,
        defense_modifier=1
    ),

    # Move and Attack
    "move_and_attack": ManeuverOption(
        name="Move and Attack",
        maneuver_type=ManeuverType.MOVE_AND_ATTACK,
        description="Move up to full Move and attack at -4, max skill 9.",
        attack_modifier=-4,
        movement_multiplier=1.0
    ),

    # All-Out Defense variants
    "all_out_defense_increased": ManeuverOption(
        name="All-Out Defense (Increased)",
        maneuver_type=ManeuverType.ALL_OUT_DEFENSE,
        description="+2 to one chosen defense for this turn.",
        defense_modifier=2,
        subtype=AllOutDefenseType.INCREASED.value
    ),
    "all_out_defense_double": ManeuverOption(
        name="All-Out Defense (Double)",
        maneuver_type=ManeuverType.ALL_OUT_DEFENSE,
        description="You may use two different defenses against the same attack.",
        subtype=AllOutDefenseType.DOUBLE.value
    ),

    # Evaluate
    "evaluate": ManeuverOption(
        name="Evaluate",
        maneuver_type=ManeuverType.EVALUATE,
        description="Study your opponent. +1 to attack them next turn (max +3)."
    ),

    # Feint
    "feint": ManeuverOption(
        name="Feint",
        maneuver_type=ManeuverType.FEINT,
        description="Make a Quick Contest of skills. Margin of success penalizes their defense."
    ),

    # Ready
    "ready": ManeuverOption(
        name="Ready",
        maneuver_type=ManeuverType.READY,
        description="Ready a weapon, change stance, stand up, or similar."
    ),

    # Wait
    "wait": ManeuverOption(
        name="Wait",
        maneuver_type=ManeuverType.WAIT,
        description="Specify a trigger. When it occurs, you can interrupt with an action."
    ),

    # Move
    "move": ManeuverOption(
        name="Move",
        maneuver_type=ManeuverType.MOVE,
        description="Move up to your full Move stat. No attacks.",
        movement_multiplier=1.0
    ),

    # Do Nothing
    "do_nothing": ManeuverOption(
        name="Do Nothing",
        maneuver_type=ManeuverType.DO_NOTHING,
        description="You take no action this turn (stunned, recovering, etc.)."
    ),
}


@dataclass
class DefenseOption:
    """Represents a defensive option."""
    name: str
    description: str
    requires_weapon: bool = False
    requires_shield: bool = False
    retreat_bonus: int = 3  # Bonus for retreating while using this defense

    def get_retreat_bonus(self) -> int:
        """Get the bonus for retreating with this defense."""
        return self.retreat_bonus


DEFENSES = {
    "dodge": DefenseOption(
        name="Dodge",
        description="Active defense using agility. Can be used against any attack.",
        retreat_bonus=3
    ),
    "parry": DefenseOption(
        name="Parry",
        description="Deflect attack with weapon. -4 vs flails, cannot parry bullets.",
        requires_weapon=True,
        retreat_bonus=1
    ),
    "block": DefenseOption(
        name="Block",
        description="Stop attack with shield. -2 vs flails.",
        requires_shield=True,
        retreat_bonus=1
    ),
}


class Maneuver:
    """
    Represents a maneuver being executed in combat.
    """

    def __init__(self, option: ManeuverOption, target: Optional['Character'] = None,
                 attack_mode: Optional[str] = None,
                 target_location: Optional['HitLocation'] = None):
        self.option = option
        self.target = target
        self.attack_mode = attack_mode  # e.g., "Swing" or "Thrust"
        self.target_location = target_location  # For called shots
        self.evaluate_bonus = 0  # Accumulated from Evaluate maneuvers
        self.feint_penalty = 0  # Penalty applied to defender from successful Feint

    def get_effective_attack_modifier(self) -> int:
        """Get total attack modifier including all sources."""
        mod = self.option.attack_modifier
        mod += self.evaluate_bonus

        # Called shot penalty
        if self.target_location:
            from .character import HitLocation
            mod += HitLocation.get_hit_modifier(self.target_location)

        return mod

    def get_effective_damage_modifier(self) -> int:
        """Get total damage modifier."""
        return self.option.damage_modifier

    def get_effective_defense_penalty(self) -> int:
        """Get the penalty applied to the defender (from Feint, etc.)."""
        return self.feint_penalty

    def __str__(self) -> str:
        s = f"{self.option.name}"
        if self.target:
            s += f" vs {self.target.name}"
        if self.attack_mode:
            s += f" ({self.attack_mode})"
        if self.target_location:
            s += f" targeting {self.target_location.value}"
        return s


def get_available_maneuvers(character: 'Character', in_melee: bool = True) -> List[ManeuverOption]:
    """
    Get list of maneuvers available to a character.
    """
    available = []

    # Always available
    available.append(MANEUVERS["attack"])
    available.append(MANEUVERS["all_out_attack_determined"])
    available.append(MANEUVERS["all_out_attack_strong"])
    available.append(MANEUVERS["all_out_attack_double"])
    available.append(MANEUVERS["committed_attack_determined"])
    available.append(MANEUVERS["committed_attack_strong"])
    available.append(MANEUVERS["defensive_attack"])
    available.append(MANEUVERS["move_and_attack"])
    available.append(MANEUVERS["all_out_defense_increased"])
    available.append(MANEUVERS["all_out_defense_double"])
    available.append(MANEUVERS["evaluate"])
    available.append(MANEUVERS["feint"])
    available.append(MANEUVERS["ready"])
    available.append(MANEUVERS["wait"])
    available.append(MANEUVERS["move"])

    # Stunned characters can only Do Nothing
    if character.status.stunned:
        return [MANEUVERS["do_nothing"]]

    return available


def get_available_defenses(character: 'Character') -> List[str]:
    """
    Get list of defenses available to a character.
    """
    if character.status.all_out_attack:
        return []  # Cannot defend after all-out attack

    available = ["dodge"]  # Always available

    if character.equipped_weapon is not None:
        available.append("parry")

    if character.equipped_shield is not None:
        available.append("block")

    return available
