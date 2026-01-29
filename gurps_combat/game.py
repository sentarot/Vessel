"""
GURPS Combat Game Module
Main game loop and player interface for the tactical combat simulator.
"""

import os
import sys
from typing import Optional, List, Tuple
from dataclasses import dataclass

from .character import Character, CharacterBuilder, HitLocation
from .combat import CombatEngine, CombatState
from .maneuvers import (
    Maneuver, ManeuverOption, ManeuverType, MANEUVERS,
    get_available_maneuvers, get_available_defenses
)
from .weapons import WEAPONS, ARMORS
from .ai import AIController, AIPersonality, create_ai_opponent


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text: str, char: str = "="):
    """Print a formatted header."""
    print(f"\n{char * 60}")
    print(f"  {text}")
    print(f"{char * 60}")


def print_status_bar(player: Character, enemy: Character):
    """Print a status bar showing both combatants."""
    print("\n" + "-" * 60)
    player_status = f"{player.name}: HP {player.status.current_hp}/{player.max_hp}"
    if player.status.shock_penalty > 0:
        player_status += f" [Shock: -{player.status.shock_penalty}]"
    if player.status.stunned:
        player_status += " [STUNNED]"

    enemy_status = f"{enemy.name}: HP {enemy.status.current_hp}/{enemy.max_hp}"
    if enemy.status.shock_penalty > 0:
        enemy_status += f" [Shock: -{enemy.status.shock_penalty}]"
    if enemy.status.stunned:
        enemy_status += " [STUNNED]"

    print(f"  YOU: {player_status}")
    print(f"  FOE: {enemy_status}")
    print("-" * 60)


def get_player_input(prompt: str, valid_options: List[str] = None) -> str:
    """Get validated input from the player."""
    while True:
        try:
            response = input(f"\n{prompt} ").strip().lower()
            if valid_options is None or response in valid_options:
                return response
            print(f"Invalid choice. Options: {', '.join(valid_options)}")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game...")
            sys.exit(0)


def get_number_input(prompt: str, min_val: int, max_val: int) -> int:
    """Get a number input within a range."""
    while True:
        try:
            response = input(f"\n{prompt} [{min_val}-{max_val}]: ").strip()
            num = int(response)
            if min_val <= num <= max_val:
                return num
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game...")
            sys.exit(0)


class GURPSCombatGame:
    """
    Main game class for the GURPS tactical combat simulator.
    """

    def __init__(self):
        self.player: Optional[Character] = None
        self.player_ai: Optional[AIController] = None  # Optional AI assist
        self.enemies: List[Tuple[Character, AIController]] = []
        self.engine: Optional[CombatEngine] = None

    def run(self):
        """Main game loop."""
        clear_screen()
        self.print_title()

        while True:
            choice = self.main_menu()

            if choice == "1":
                self.start_combat()
            elif choice == "2":
                self.show_rules()
            elif choice == "3":
                self.show_credits()
            elif choice == "q":
                print("\nFarewell, warrior!\n")
                break

    def print_title(self):
        """Print the game title."""
        title = """
   ██████╗ ██╗   ██╗██████╗ ██████╗ ███████╗
  ██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔════╝
  ██║  ███╗██║   ██║██████╔╝██████╔╝███████╗
  ██║   ██║██║   ██║██╔══██╗██╔═══╝ ╚════██║
  ╚██████╔╝╚██████╔╝██║  ██║██║     ███████║
   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝
  ╔═══════════════════════════════════════════╗
  ║     TACTICAL COMBAT SIMULATOR v1.0        ║
  ║        Turn-Based Combat System           ║
  ╚═══════════════════════════════════════════╝
        """
        print(title)

    def main_menu(self) -> str:
        """Display main menu and get choice."""
        print("\n  MAIN MENU")
        print("  ---------")
        print("  1. Start Combat")
        print("  2. View Rules")
        print("  3. Credits")
        print("  Q. Quit")

        return get_player_input("Choose:", ["1", "2", "3", "q"])

    def start_combat(self):
        """Start a new combat encounter."""
        clear_screen()
        print_header("CHARACTER CREATION")

        # Create player character
        self.player = self.create_player_character()

        # Create enemy
        clear_screen()
        print_header("CHOOSE YOUR OPPONENT")
        enemy, ai = self.create_enemy()
        self.enemies = [(enemy, ai)]

        # Initialize combat
        self.engine = CombatEngine([self.player, enemy])

        # Run combat
        self.combat_loop(enemy, ai)

    def create_player_character(self) -> Character:
        """Let the player create their character."""
        print("\n  Character Templates:")
        print("  1. Warrior - Balanced fighter with sword and shield")
        print("  2. Rogue - Fast and deadly with rapier")
        print("  3. Brute - Heavy hitter with great axe")
        print("  4. Custom - Build your own")

        choice = get_player_input("Choose template:", ["1", "2", "3", "4"])

        name = input("\n  Enter your character's name: ").strip()
        if not name:
            name = "Hero"

        print("\n  Difficulty (affects your stats):")
        print("  1. Easy (Strong stats)")
        print("  2. Normal (Average stats)")
        print("  3. Hard (Weak stats)")

        diff = get_player_input("Choose difficulty:", ["1", "2", "3"])
        levels = {"1": "strong", "2": "average", "3": "weak"}
        level = levels[diff]

        if choice == "1":
            char = CharacterBuilder.create_warrior(name, level)
        elif choice == "2":
            char = CharacterBuilder.create_rogue(name, level)
        elif choice == "3":
            char = CharacterBuilder.create_brute(name, level)
        else:
            char = self.create_custom_character(name)

        self.display_character(char)
        input("\n  Press Enter to continue...")
        return char

    def create_custom_character(self, name: str) -> Character:
        """Create a custom character with point allocation."""
        print("\n  CUSTOM CHARACTER CREATION")
        print("  Allocate attribute points (10 is human average)")

        st = get_number_input("  Strength (ST)", 8, 18)
        dx = get_number_input("  Dexterity (DX)", 8, 18)
        iq = get_number_input("  Intelligence (IQ)", 8, 18)
        ht = get_number_input("  Health (HT)", 8, 18)

        print("\n  Choose primary weapon:")
        weapons = ["broadsword", "shortsword", "rapier", "axe", "mace", "spear", "quarterstaff", "greatsword"]
        for i, w in enumerate(weapons, 1):
            print(f"  {i}. {WEAPONS[w].name}")

        w_choice = get_number_input("  Weapon", 1, len(weapons))
        weapon = weapons[w_choice - 1]

        print("\n  Choose armor:")
        armors = ["cloth_armor", "leather_armor", "mail_shirt", "scale_armor", "plate_armor"]
        for i, a in enumerate(armors, 1):
            print(f"  {i}. {ARMORS[a].name} (DR {ARMORS[a].dr})")

        a_choice = get_number_input("  Armor", 1, len(armors))
        armor = [armors[a_choice - 1]]

        # Add helm
        print("\n  Add helmet?")
        print("  1. None")
        print("  2. Light Helm (DR 2)")
        print("  3. Heavy Helm (DR 4)")

        h_choice = get_player_input("  Helmet:", ["1", "2", "3"])
        if h_choice == "2":
            armor.append("light_helm")
        elif h_choice == "3":
            armor.append("heavy_helm")

        # Set skill based on weapon
        weapon_skills = {
            "broadsword": "Broadsword",
            "shortsword": "Shortsword",
            "rapier": "Rapier",
            "axe": "Axe/Mace",
            "mace": "Axe/Mace",
            "spear": "Spear",
            "quarterstaff": "Staff",
            "greatsword": "Two-Handed Sword"
        }
        skill_name = weapon_skills.get(weapon, "Broadsword")
        skills = {skill_name: dx + 4, "Brawling": dx + 2}

        char = CharacterBuilder.create_custom(
            name=name, st=st, dx=dx, iq=iq, ht=ht,
            skills=skills, weapon=weapon, armor=armor
        )

        return char

    def create_enemy(self) -> Tuple[Character, AIController]:
        """Create an enemy opponent."""
        print("\n  Enemy Type:")
        print("  1. Random Opponent")
        print("  2. Aggressive Warrior")
        print("  3. Defensive Fighter")
        print("  4. Tactical Master")
        print("  5. Berserker")

        choice = get_player_input("Choose opponent:", ["1", "2", "3", "4", "5"])

        print("\n  Enemy Strength:")
        print("  1. Weak")
        print("  2. Average")
        print("  3. Strong")
        print("  4. Elite")

        strength = get_player_input("Choose strength:", ["1", "2", "3", "4"])
        levels = {"1": "weak", "2": "average", "3": "strong", "4": "elite"}
        level = levels[strength]

        personalities = {
            "1": None,  # Random
            "2": AIPersonality.AGGRESSIVE,
            "3": AIPersonality.DEFENSIVE,
            "4": AIPersonality.TACTICAL,
            "5": AIPersonality.BERSERKER
        }
        personality = personalities[choice]

        names = ["Grimjaw", "Bloodaxe", "Ironhide", "Shadowblade", "Thornback",
                 "Steelfist", "Darkhelm", "Bonecrusher", "Viperstrike", "Doomhammer"]
        import random
        enemy_name = random.choice(names)

        enemy, ai = create_ai_opponent(enemy_name, level, personality)

        print(f"\n  Your opponent: {enemy.name}")
        print(f"  Fighting style: {ai.get_personality_description()}")
        self.display_character(enemy)

        input("\n  Press Enter to begin combat...")
        return enemy, ai

    def display_character(self, char: Character):
        """Display character statistics."""
        print(f"\n  {char.name}")
        print(f"  {'-' * len(char.name)}")
        print(f"  ST: {char.st}  DX: {char.dx}  IQ: {char.iq}  HT: {char.ht}")
        print(f"  HP: {char.max_hp}  FP: {char.max_fp}  Basic Speed: {char.basic_speed}")
        print(f"  Dodge: {char.dodge}  Parry: {char.get_parry()}  Block: {char.get_block()}")
        print(f"  Thrust: {char.thrust_damage}  Swing: {char.swing_damage}")

        if char.equipped_weapon:
            print(f"  Weapon: {char.equipped_weapon.name}")
        if char.equipped_shield:
            print(f"  Shield: {char.equipped_shield.name} (DB +{char.equipped_shield.db})")
        if char.armor:
            armor_str = ", ".join(a.name for a in char.armor)
            print(f"  Armor: {armor_str}")

    def combat_loop(self, enemy: Character, enemy_ai: AIController):
        """Main combat loop."""
        clear_screen()
        print_header(f"COMBAT: {self.player.name} vs {enemy.name}")

        while not self.engine.state.ended:
            current = self.engine.state.get_current_combatant()

            if current == self.player:
                self.player_turn(enemy)
            else:
                self.enemy_turn(enemy, enemy_ai)

            # Check for combat end
            if self.engine.state.check_combat_end():
                break

            # Advance to next turn
            self.engine.state.advance_turn()

            # Small pause between turns
            input("\n  Press Enter to continue...")
            clear_screen()

        # Combat ended
        self.show_combat_result()

    def player_turn(self, enemy: Character):
        """Handle the player's turn."""
        self.engine.start_turn(self.player)

        print_header(f"YOUR TURN - Round {self.engine.state.round_number}")
        print_status_bar(self.player, enemy)

        # Show any status effects
        if self.player.status.shock_penalty > 0:
            print(f"\n  ! You have a -{self.player.status.shock_penalty} shock penalty this turn")

        if self.player.status.stunned:
            print("\n  ! You are STUNNED and cannot act!")
            maneuver = Maneuver(MANEUVERS["do_nothing"])
        else:
            # Choose maneuver
            maneuver = self.choose_player_maneuver(enemy)

        # Execute maneuver
        result = self.engine.execute_maneuver(self.player, maneuver, enemy)

        # Display results
        self.display_combat_result(result)

    def choose_player_maneuver(self, enemy: Character) -> Maneuver:
        """Let player choose their maneuver."""
        print("\n  CHOOSE YOUR ACTION:")
        print("  -------------------")

        maneuvers = [
            ("1", "attack", "Attack - Standard attack, full defenses"),
            ("2", "all_out_attack_determined", "All-Out Attack (Determined) - +4 to hit, NO defenses!"),
            ("3", "all_out_attack_strong", "All-Out Attack (Strong) - +2 damage, NO defenses!"),
            ("4", "committed_attack_determined", "Committed Attack - +2 to hit, -2 defenses"),
            ("5", "defensive_attack", "Defensive Attack - -2 to hit, +1 defense"),
            ("6", "evaluate", "Evaluate - +1 to next attack (stacks to +3)"),
            ("7", "feint", "Feint - Penalize enemy's next defense"),
            ("8", "all_out_defense_increased", "All-Out Defense - +2 to all defenses, no attack"),
        ]

        for key, _, desc in maneuvers:
            print(f"  {key}. {desc}")

        choice = get_player_input("Action:", [str(i) for i in range(1, 9)])

        maneuver_key = maneuvers[int(choice) - 1][1]
        maneuver_option = MANEUVERS[maneuver_key]

        # For attack maneuvers, choose attack mode
        attack_mode = None
        target_location = None

        if maneuver_option.maneuver_type in (ManeuverType.ATTACK, ManeuverType.ALL_OUT_ATTACK,
                                              ManeuverType.COMMITTED_ATTACK, ManeuverType.DEFENSIVE_ATTACK):
            attack_mode = self.choose_attack_mode()
            target_location = self.choose_target_location()

        return Maneuver(maneuver_option, enemy, attack_mode, target_location)

    def choose_attack_mode(self) -> Optional[str]:
        """Let player choose attack mode."""
        weapon = self.player.equipped_weapon
        if weapon is None or len(weapon.attacks) == 1:
            return weapon.attacks[0].name if weapon else None

        print("\n  Attack Mode:")
        for i, attack in enumerate(weapon.attacks, 1):
            dmg_type = "Cutting" if attack.damage_type.value == "cut" else \
                       "Impaling" if attack.damage_type.value == "imp" else "Crushing"
            print(f"  {i}. {attack.name} ({dmg_type})")

        choice = get_number_input("  Choose", 1, len(weapon.attacks))
        return weapon.attacks[choice - 1].name

    def choose_target_location(self) -> Optional[HitLocation]:
        """Let player choose target location (called shot)."""
        print("\n  Target Location (Called Shot):")
        print("  0. Torso (default, no penalty)")
        print("  1. Head (-5 to hit)")
        print("  2. Arm (-2 to hit)")
        print("  3. Leg (-2 to hit)")
        print("  4. Hand (-4 to hit)")

        choice = get_player_input("  Target [0 for default]:", ["0", "1", "2", "3", "4"])

        locations = {
            "0": None,
            "1": HitLocation.HEAD,
            "2": HitLocation.ARM,
            "3": HitLocation.LEG,
            "4": HitLocation.HAND
        }
        return locations[choice]

    def enemy_turn(self, enemy: Character, ai: AIController):
        """Handle the enemy's turn."""
        self.engine.start_turn(enemy)

        print_header(f"{enemy.name.upper()}'S TURN - Round {self.engine.state.round_number}")
        print_status_bar(self.player, enemy)

        if enemy.status.stunned:
            print(f"\n  {enemy.name} is stunned and cannot act!")
            maneuver = Maneuver(MANEUVERS["do_nothing"])
        else:
            # AI chooses action
            maneuver_option, target, attack_mode, target_loc = ai.choose_maneuver([self.player])
            maneuver = Maneuver(maneuver_option, target, attack_mode, target_loc)
            print(f"\n  {enemy.name} uses {maneuver_option.name}!")

        # Execute maneuver
        result = self.engine.execute_maneuver(enemy, maneuver, self.player)

        # Display results
        self.display_combat_result(result)

        # Update AI state
        if result["attacks"]:
            hit = any(a.hit and not (d.defended if result["defenses"] else False)
                      for a, d in zip(result["attacks"], result["defenses"] + [None]))
            damage = sum(d.injury for d in result["damage"]) if result["damage"] else 0
            ai.notify_attack_result(hit, damage)

    def choose_player_defense(self, attack_result) -> Tuple[str, bool]:
        """Let player choose their defense."""
        available = get_available_defenses(self.player)

        if not available:
            print("\n  You cannot defend! (All-Out Attack in effect)")
            return None, False

        print("\n  DEFEND!")
        print("  -------")

        for i, defense in enumerate(available, 1):
            if defense == "dodge":
                value = self.player.get_effective_dodge()
            elif defense == "parry":
                value = self.player.get_effective_parry()
            elif defense == "block":
                value = self.player.get_effective_block()
            print(f"  {i}. {defense.title()} ({value})")

        choice = get_number_input("  Defense", 1, len(available))
        defense = available[choice - 1]

        # Ask about retreat
        retreat = False
        if not self.player.status.retreated:
            retreat_choice = get_player_input("  Retreat for bonus? (y/n):", ["y", "n"])
            retreat = retreat_choice == "y"

        return defense, retreat

    def display_combat_result(self, result: dict):
        """Display the results of combat resolution."""
        for attack in result.get("attacks", []):
            print(f"\n  >> {attack}")

        for defense in result.get("defenses", []):
            print(f"  >> {defense}")

        for damage in result.get("damage", []):
            print(f"\n  >> {damage}")
            for effect in damage.effects:
                print(f"     ! {effect}")

    def show_combat_result(self):
        """Show the final combat result."""
        clear_screen()
        print_header("COMBAT ENDED")

        if self.engine.state.winner == self.player:
            print("""
    ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗██╗
    ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝██║
    ██║   ██║██║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝ ██║
    ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝  ╚═╝
     ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║   ██╗
      ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝
            """)
            print(f"  {self.player.name} is victorious!")
        elif self.engine.state.winner:
            print("""
    ██████╗ ███████╗███████╗███████╗ █████╗ ████████╗
    ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝
    ██║  ██║█████╗  █████╗  █████╗  ███████║   ██║
    ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██║   ██║
    ██████╔╝███████╗██║     ███████╗██║  ██║   ██║
    ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝
            """)
            print(f"  {self.engine.state.winner.name} has defeated you!")
        else:
            print("  The battle ends in mutual defeat...")

        print(self.engine.get_combat_summary())
        input("\n  Press Enter to continue...")

    def show_rules(self):
        """Display GURPS combat rules summary."""
        clear_screen()
        print_header("GURPS COMBAT RULES")

        rules = """
  BASIC MECHANICS
  ---------------
  - Roll 3d6 for all skill checks
  - Success: Roll EQUAL TO or UNDER your skill level
  - Critical Success: Roll of 3-4 (always), 5 if skill >= 15, 6 if skill >= 16
  - Critical Failure: Roll of 18 (always), 17 if skill <= 15

  ATTACK SEQUENCE
  ---------------
  1. Attacker chooses maneuver and makes attack roll
  2. If attack hits, defender may attempt one defense (Dodge, Parry, or Block)
  3. If defense fails, roll damage and apply to target

  MANEUVERS
  ---------
  Attack: Standard attack with full defenses available
  All-Out Attack: Bonuses to hit/damage but NO defenses until next turn
  Committed Attack: Small bonus with minor defense penalty
  Defensive Attack: Small attack penalty for defense bonus
  Evaluate: Study opponent for +1 to hit (max +3)
  Feint: Contest of skills - success penalizes enemy defense

  DEFENSES
  --------
  Dodge: Based on Basic Speed + 3. Works against any attack.
  Parry: Based on weapon skill / 2 + 3. Requires weapon.
  Block: Based on Shield skill / 2 + 3. Requires shield.
  Retreat: +3 to Dodge, +1 to Parry/Block (once per turn)

  DAMAGE
  ------
  - Damage type affects injury multiplier after armor:
    Crushing (cr): x1    Cutting (cut): x1.5    Impaling (imp): x2
  - Damage Resistance (DR) from armor is subtracted first
        """
        print(rules)
        input("\n  Press Enter to continue...")

    def show_credits(self):
        """Display game credits."""
        clear_screen()
        print_header("CREDITS")

        credits = """
  GURPS Tactical Combat Simulator
  --------------------------------
  Based on GURPS 4th Edition by Steve Jackson Games

  GURPS is a trademark of Steve Jackson Games, and its rules
  and calculation descriptions are used here for educational
  and entertainment purposes under fair use.

  This simulator implements core GURPS combat mechanics for
  turn-based tactical combat between a player and AI opponent.

  Features:
  - Full attribute and derived stat calculation
  - Multiple combat maneuvers (Attack, All-Out Attack, Feint, etc.)
  - Three defense types (Dodge, Parry, Block)
  - Damage types with armor penetration
  - Hit locations for called shots
  - AI opponents with different personalities
  - Multiple character archetypes

  Version 1.0
        """
        print(credits)
        input("\n  Press Enter to continue...")


def main():
    """Entry point for the game."""
    game = GURPSCombatGame()
    game.run()


if __name__ == "__main__":
    main()
