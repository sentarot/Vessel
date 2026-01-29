"""
GURPS Tactical Combat Simulator
A turn-based combat system implementing GURPS 4th Edition rules.
"""

__version__ = "1.0.0"
__author__ = "Vessel Project"

from .dice import roll_3d6, roll_dice, success_roll, margin_of_success, damage_roll
from .character import Character, CharacterBuilder
from .weapons import Weapon, Armor, WEAPONS, ARMORS
from .maneuvers import Maneuver, ManeuverType
from .combat import CombatEngine, CombatState
from .ai import AIController, AIPersonality, create_ai_opponent
from .game import GURPSCombatGame

__all__ = [
    'roll_3d6', 'roll_dice', 'success_roll', 'margin_of_success', 'damage_roll',
    'Character', 'CharacterBuilder',
    'Weapon', 'Armor', 'WEAPONS', 'ARMORS',
    'Maneuver', 'ManeuverType',
    'CombatEngine', 'CombatState',
    'AIController', 'AIPersonality', 'create_ai_opponent',
    'GURPSCombatGame'
]
