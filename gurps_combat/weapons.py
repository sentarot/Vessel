"""
GURPS Weapons and Armor Module
Defines weapons, shields, and armor with their game statistics.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum


class DamageType(Enum):
    """Types of damage in GURPS."""
    CRUSHING = "cr"      # Blunt force
    CUTTING = "cut"      # Slashing (x1.5 to flesh)
    IMPALING = "imp"     # Piercing (x2 to flesh)
    PIERCING = "pi"      # Small piercing (x1)
    BURNING = "burn"     # Fire damage


class WeaponType(Enum):
    """Categories of weapons."""
    UNARMED = "unarmed"
    SWORD = "sword"
    AXE = "axe"
    MACE = "mace"
    POLEARM = "polearm"
    KNIFE = "knife"
    SHIELD = "shield"  # Shield bash
    SPEAR = "spear"
    STAFF = "staff"


@dataclass
class WeaponAttack:
    """Represents a single attack mode of a weapon."""
    name: str
    skill: str              # Skill name used
    damage_type: DamageType
    damage_base: str        # "thr" or "sw" for thrust/swing based
    damage_mod: int         # Modifier to base damage (e.g., +2)
    reach: str              # Reach in hexes (e.g., "1", "1-2", "C")
    parry_mod: int = 0      # Modifier to parry (0, -1, +1, etc.)
    min_st: int = 0         # Minimum ST to use effectively


@dataclass
class Weapon:
    """A weapon with its attacks and properties."""
    name: str
    weapon_type: WeaponType
    attacks: List[WeaponAttack]
    weight: float = 1.0     # Weight in lbs
    cost: int = 0           # Cost in $
    notes: str = ""
    is_shield: bool = False
    db: int = 0             # Defense Bonus (for shields)
    min_st: int = 0         # Minimum ST to use weapon effectively

    @property
    def primary_attack(self) -> WeaponAttack:
        """Return the primary (first) attack mode."""
        return self.attacks[0]

    def get_attack(self, name: str) -> Optional[WeaponAttack]:
        """Get a specific attack mode by name."""
        for attack in self.attacks:
            if attack.name.lower() == name.lower():
                return attack
        return None


@dataclass
class Armor:
    """Armor piece with damage resistance."""
    name: str
    dr: int                 # Damage Resistance
    locations: List[str]    # Body locations covered
    weight: float = 0.0     # Weight in lbs
    cost: int = 0
    notes: str = ""


# Standard weapon definitions
WEAPONS: Dict[str, Weapon] = {
    # Unarmed
    "punch": Weapon(
        name="Punch",
        weapon_type=WeaponType.UNARMED,
        attacks=[
            WeaponAttack("Punch", "Brawling", DamageType.CRUSHING, "thr", -1, "C")
        ],
        weight=0, cost=0
    ),
    "kick": Weapon(
        name="Kick",
        weapon_type=WeaponType.UNARMED,
        attacks=[
            WeaponAttack("Kick", "Brawling", DamageType.CRUSHING, "thr", 0, "C,1", parry_mod=-2)
        ],
        weight=0, cost=0
    ),

    # Swords
    "broadsword": Weapon(
        name="Broadsword",
        weapon_type=WeaponType.SWORD,
        attacks=[
            WeaponAttack("Swing", "Broadsword", DamageType.CUTTING, "sw", 1, "1"),
            WeaponAttack("Thrust", "Broadsword", DamageType.CRUSHING, "thr", 1, "1")
        ],
        weight=3.0, cost=500, min_st=10
    ),
    "shortsword": Weapon(
        name="Shortsword",
        weapon_type=WeaponType.SWORD,
        attacks=[
            WeaponAttack("Swing", "Shortsword", DamageType.CUTTING, "sw", 0, "1"),
            WeaponAttack("Thrust", "Shortsword", DamageType.IMPALING, "thr", 0, "1")
        ],
        weight=2.0, cost=400, min_st=8
    ),
    "greatsword": Weapon(
        name="Greatsword",
        weapon_type=WeaponType.SWORD,
        attacks=[
            WeaponAttack("Swing", "Two-Handed Sword", DamageType.CUTTING, "sw", 3, "1-2"),
            WeaponAttack("Thrust", "Two-Handed Sword", DamageType.IMPALING, "thr", 3, "2")
        ],
        weight=7.0, cost=900, min_st=12
    ),
    "rapier": Weapon(
        name="Rapier",
        weapon_type=WeaponType.SWORD,
        attacks=[
            WeaponAttack("Thrust", "Rapier", DamageType.IMPALING, "thr", 1, "1-2", parry_mod=0)
        ],
        weight=2.75, cost=500, min_st=9
    ),

    # Axes
    "axe": Weapon(
        name="Axe",
        weapon_type=WeaponType.AXE,
        attacks=[
            WeaponAttack("Swing", "Axe/Mace", DamageType.CUTTING, "sw", 2, "1", parry_mod=-1)
        ],
        weight=4.0, cost=50, min_st=11
    ),
    "great_axe": Weapon(
        name="Great Axe",
        weapon_type=WeaponType.AXE,
        attacks=[
            WeaponAttack("Swing", "Two-Handed Axe/Mace", DamageType.CUTTING, "sw", 4, "1-2", parry_mod=-1)
        ],
        weight=8.0, cost=100, min_st=13
    ),

    # Maces
    "mace": Weapon(
        name="Mace",
        weapon_type=WeaponType.MACE,
        attacks=[
            WeaponAttack("Swing", "Axe/Mace", DamageType.CRUSHING, "sw", 3, "1", parry_mod=-1)
        ],
        weight=5.0, cost=50, min_st=12
    ),

    # Knives
    "knife": Weapon(
        name="Large Knife",
        weapon_type=WeaponType.KNIFE,
        attacks=[
            WeaponAttack("Swing", "Knife", DamageType.CUTTING, "sw", -2, "C,1"),
            WeaponAttack("Thrust", "Knife", DamageType.IMPALING, "thr", 0, "C")
        ],
        weight=1.0, cost=40, min_st=6
    ),
    "dagger": Weapon(
        name="Dagger",
        weapon_type=WeaponType.KNIFE,
        attacks=[
            WeaponAttack("Thrust", "Knife", DamageType.IMPALING, "thr", -1, "C", parry_mod=-1)
        ],
        weight=0.25, cost=20, min_st=5
    ),

    # Polearms
    "spear": Weapon(
        name="Spear",
        weapon_type=WeaponType.SPEAR,
        attacks=[
            WeaponAttack("Thrust", "Spear", DamageType.IMPALING, "thr", 2, "1-2*", parry_mod=0),
            WeaponAttack("Thrust (2H)", "Spear", DamageType.IMPALING, "thr", 3, "1-2*", parry_mod=0)
        ],
        weight=4.0, cost=40, min_st=9
    ),
    "halberd": Weapon(
        name="Halberd",
        weapon_type=WeaponType.POLEARM,
        attacks=[
            WeaponAttack("Swing", "Polearm", DamageType.CUTTING, "sw", 5, "2-3*", parry_mod=-2),
            WeaponAttack("Thrust", "Polearm", DamageType.IMPALING, "thr", 3, "2-3*", parry_mod=-2)
        ],
        weight=12.0, cost=150, min_st=13
    ),

    # Staves
    "quarterstaff": Weapon(
        name="Quarterstaff",
        weapon_type=WeaponType.STAFF,
        attacks=[
            WeaponAttack("Swing", "Staff", DamageType.CRUSHING, "sw", 2, "1-2", parry_mod=2),
            WeaponAttack("Thrust", "Staff", DamageType.CRUSHING, "thr", 2, "1-2", parry_mod=2)
        ],
        weight=4.0, cost=10, min_st=7
    ),

    # Shields (can be used as weapons)
    "small_shield": Weapon(
        name="Small Shield",
        weapon_type=WeaponType.SHIELD,
        attacks=[
            WeaponAttack("Bash", "Shield", DamageType.CRUSHING, "thr", 0, "1")
        ],
        weight=8.0, cost=40, is_shield=True, db=1
    ),
    "medium_shield": Weapon(
        name="Medium Shield",
        weapon_type=WeaponType.SHIELD,
        attacks=[
            WeaponAttack("Bash", "Shield", DamageType.CRUSHING, "thr", 0, "1")
        ],
        weight=15.0, cost=60, is_shield=True, db=2
    ),
    "large_shield": Weapon(
        name="Large Shield",
        weapon_type=WeaponType.SHIELD,
        attacks=[
            WeaponAttack("Bash", "Shield", DamageType.CRUSHING, "thr", 0, "1")
        ],
        weight=25.0, cost=90, is_shield=True, db=3
    ),
}


# Standard armor definitions
ARMORS: Dict[str, Armor] = {
    "cloth_armor": Armor(
        name="Cloth Armor",
        dr=1,
        locations=["torso", "arms", "legs"],
        weight=6.0, cost=30
    ),
    "leather_armor": Armor(
        name="Leather Armor",
        dr=2,
        locations=["torso"],
        weight=10.0, cost=100
    ),
    "light_scale": Armor(
        name="Light Scale Armor",
        dr=3,
        locations=["torso"],
        weight=15.0, cost=150
    ),
    "mail_shirt": Armor(
        name="Mail Shirt",
        dr=4,
        locations=["torso"],
        weight=16.0, cost=150,
        notes="Flexible; can be worn under clothing"
    ),
    "mail_hauberk": Armor(
        name="Mail Hauberk",
        dr=4,
        locations=["torso", "arms", "legs"],
        weight=25.0, cost=230
    ),
    "scale_armor": Armor(
        name="Scale Armor",
        dr=4,
        locations=["torso"],
        weight=35.0, cost=420
    ),
    "plate_armor": Armor(
        name="Plate Armor",
        dr=6,
        locations=["torso"],
        weight=30.0, cost=2000
    ),
    "heavy_plate": Armor(
        name="Heavy Plate",
        dr=7,
        locations=["torso", "arms", "legs"],
        weight=45.0, cost=3000
    ),
    "light_helm": Armor(
        name="Light Helm",
        dr=2,
        locations=["head"],
        weight=2.0, cost=25
    ),
    "heavy_helm": Armor(
        name="Heavy Helm",
        dr=4,
        locations=["head"],
        weight=5.0, cost=100
    ),
    "great_helm": Armor(
        name="Great Helm",
        dr=7,
        locations=["head", "face"],
        weight=10.0, cost=340,
        notes="Limits vision"
    ),
    "gauntlets": Armor(
        name="Gauntlets",
        dr=4,
        locations=["hands"],
        weight=2.0, cost=100
    ),
    "boots": Armor(
        name="Heavy Boots",
        dr=2,
        locations=["feet"],
        weight=3.0, cost=50
    ),
}


def get_damage_multiplier(damage_type: DamageType) -> float:
    """
    Get the damage multiplier for penetrating damage.
    Applied after armor reduction.
    """
    multipliers = {
        DamageType.CRUSHING: 1.0,
        DamageType.CUTTING: 1.5,
        DamageType.IMPALING: 2.0,
        DamageType.PIERCING: 1.0,
        DamageType.BURNING: 1.0
    }
    return multipliers.get(damage_type, 1.0)


def create_custom_weapon(name: str, base_weapon: str, **modifications) -> Weapon:
    """Create a modified version of a base weapon."""
    if base_weapon not in WEAPONS:
        raise ValueError(f"Unknown base weapon: {base_weapon}")

    import copy
    weapon = copy.deepcopy(WEAPONS[base_weapon])
    weapon.name = name

    for key, value in modifications.items():
        if hasattr(weapon, key):
            setattr(weapon, key, value)

    return weapon
