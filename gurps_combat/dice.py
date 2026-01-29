"""
GURPS Dice Rolling Module
Implements the 3d6 resolution system used in GURPS.
"""

import random
from typing import Tuple, List
from dataclasses import dataclass
from enum import Enum


class RollResult(Enum):
    """Result categories for GURPS skill rolls."""
    CRITICAL_SUCCESS = "critical_success"
    SUCCESS = "success"
    FAILURE = "failure"
    CRITICAL_FAILURE = "critical_failure"


@dataclass
class DiceRoll:
    """Represents the result of a dice roll."""
    dice: List[int]
    total: int
    target: int
    result: RollResult
    margin: int  # Positive = success margin, Negative = failure margin

    def __str__(self) -> str:
        dice_str = "+".join(str(d) for d in self.dice)
        return f"Rolled {self.total} ({dice_str}) vs {self.target}: {self.result.value.replace('_', ' ').title()} by {abs(self.margin)}"


def roll_dice(num_dice: int, sides: int = 6) -> List[int]:
    """Roll multiple dice and return individual results."""
    return [random.randint(1, sides) for _ in range(num_dice)]


def roll_3d6() -> Tuple[int, List[int]]:
    """Roll 3d6 and return (total, individual dice)."""
    dice = roll_dice(3, 6)
    return sum(dice), dice


def check_critical(roll: int, target: int) -> RollResult:
    """
    Determine if a roll is a critical success or failure.

    GURPS Critical Rules:
    - Critical Success: Roll of 3-4, or 5 if target >= 15, or 6 if target >= 16
    - Critical Failure: Roll of 18, or 17 if target <= 15, or 10+ over target
    """
    # Critical success checks
    if roll <= 4:
        return RollResult.CRITICAL_SUCCESS
    if roll == 5 and target >= 15:
        return RollResult.CRITICAL_SUCCESS
    if roll == 6 and target >= 16:
        return RollResult.CRITICAL_SUCCESS

    # Critical failure checks
    if roll == 18:
        return RollResult.CRITICAL_FAILURE
    if roll == 17 and target <= 15:
        return RollResult.CRITICAL_FAILURE
    if roll >= target + 10:
        return RollResult.CRITICAL_FAILURE

    # Normal success/failure
    if roll <= target:
        return RollResult.SUCCESS
    return RollResult.FAILURE


def success_roll(target: int) -> DiceRoll:
    """
    Make a success roll against a target number.
    Returns a DiceRoll with full details.
    """
    total, dice = roll_3d6()
    result = check_critical(total, target)
    margin = target - total  # Positive = succeeded by, Negative = failed by

    return DiceRoll(
        dice=dice,
        total=total,
        target=target,
        result=result,
        margin=margin
    )


def margin_of_success(roll: int, target: int) -> int:
    """Calculate margin of success (positive) or failure (negative)."""
    return target - roll


def contest_roll(skill1: int, skill2: int) -> Tuple[DiceRoll, DiceRoll, int]:
    """
    Make a quick contest between two skill levels.
    Returns (roll1, roll2, winner) where winner is 1, 2, or 0 for tie.
    """
    roll1 = success_roll(skill1)
    roll2 = success_roll(skill2)

    # Both succeed or both fail: compare margins
    if (roll1.result in (RollResult.SUCCESS, RollResult.CRITICAL_SUCCESS) and
        roll2.result in (RollResult.SUCCESS, RollResult.CRITICAL_SUCCESS)):
        # Both succeeded - higher margin wins
        if roll1.margin > roll2.margin:
            winner = 1
        elif roll2.margin > roll1.margin:
            winner = 2
        else:
            winner = 0  # Tie
    elif roll1.result in (RollResult.FAILURE, RollResult.CRITICAL_FAILURE) and \
         roll2.result in (RollResult.FAILURE, RollResult.CRITICAL_FAILURE):
        # Both failed - smaller margin of failure wins
        if roll1.margin > roll2.margin:
            winner = 1
        elif roll2.margin > roll1.margin:
            winner = 2
        else:
            winner = 0  # Tie
    elif roll1.result in (RollResult.SUCCESS, RollResult.CRITICAL_SUCCESS):
        winner = 1
    else:
        winner = 2

    return roll1, roll2, winner


def damage_roll(dice_str: str) -> Tuple[int, str]:
    """
    Roll damage based on GURPS dice notation.
    Format: XdY+Z or XdY-Z (e.g., "2d6+2", "1d6-1")
    Returns (damage, roll_description).
    """
    dice_str = dice_str.lower().replace(" ", "")

    # Parse the dice string
    modifier = 0
    if "+" in dice_str:
        parts = dice_str.split("+")
        dice_part = parts[0]
        modifier = int(parts[1])
    elif "-" in dice_str:
        parts = dice_str.split("-")
        dice_part = parts[0]
        modifier = -int(parts[1])
    else:
        dice_part = dice_str

    # Parse number of dice
    if "d" in dice_part:
        num_dice = int(dice_part.split("d")[0]) if dice_part.split("d")[0] else 1
    else:
        # Just a flat number
        return int(dice_part) + modifier, f"{dice_part}"

    # Roll the dice
    dice = roll_dice(num_dice, 6)
    total = sum(dice) + modifier
    total = max(0, total)  # Minimum 0 damage

    dice_desc = "+".join(str(d) for d in dice)
    if modifier > 0:
        desc = f"({dice_desc})+{modifier} = {total}"
    elif modifier < 0:
        desc = f"({dice_desc}){modifier} = {total}"
    else:
        desc = f"({dice_desc}) = {total}"

    return total, desc


def calculate_thrust_damage(st: int) -> str:
    """Calculate thrust damage based on ST (GURPS Basic Set table)."""
    thrust_table = {
        1: "1d-6", 2: "1d-6", 3: "1d-5", 4: "1d-5", 5: "1d-4",
        6: "1d-4", 7: "1d-3", 8: "1d-3", 9: "1d-2", 10: "1d-2",
        11: "1d-1", 12: "1d-1", 13: "1d", 14: "1d", 15: "1d+1",
        16: "1d+1", 17: "1d+2", 18: "1d+2", 19: "2d-1", 20: "2d-1",
        21: "2d", 22: "2d", 23: "2d+1", 24: "2d+1", 25: "2d+2"
    }
    if st < 1:
        st = 1
    if st > 25:
        # For ST > 25, add 1d per 10 ST
        base = "2d+2"
        extra_dice = (st - 25) // 10
        extra_mod = ((st - 25) % 10) // 2
        if extra_dice > 0:
            return f"{2 + extra_dice}d+{2 + extra_mod}"
        return f"2d+{2 + extra_mod}"
    return thrust_table[st]


def calculate_swing_damage(st: int) -> str:
    """Calculate swing damage based on ST (GURPS Basic Set table)."""
    swing_table = {
        1: "1d-5", 2: "1d-5", 3: "1d-4", 4: "1d-4", 5: "1d-3",
        6: "1d-3", 7: "1d-2", 8: "1d-2", 9: "1d-1", 10: "1d",
        11: "1d+1", 12: "1d+2", 13: "2d-1", 14: "2d", 15: "2d+1",
        16: "2d+2", 17: "3d-1", 18: "3d", 19: "3d+1", 20: "3d+2",
        21: "4d-1", 22: "4d", 23: "4d+1", 24: "4d+2", 25: "5d-1"
    }
    if st < 1:
        st = 1
    if st > 25:
        base_dice = 5
        extra = st - 25
        extra_dice = extra // 8
        extra_mod = (extra % 8) // 2 - 1
        return f"{base_dice + extra_dice}d{'+' + str(extra_mod) if extra_mod >= 0 else str(extra_mod)}"
    return swing_table[st]
