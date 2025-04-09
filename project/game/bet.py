import random
from typing import List
from enum import Enum
from dataclasses import dataclass, field


class ColorTypes(Enum):
    """
    Enumeration representing the possible colors of pockets on a roulette wheel.

    Attributes:
        Black (str): Represents the color black.
        Red (str): Represents the color red.
        Green (str): Represents the color green.
    """

    Black: str = "black"
    Red: str = "red"
    Green: str = "green"


class BetTypes(Enum):
    """
    Enumeration representing the types of bets that can be placed in a roulette game.

    Attributes:
        Single (int): Represents a bet on a single number, with a payout ratio of 36:1.
        Color (int): Represents a bet on a color (red or black), with a payout ratio of 2:1.
        Dozen (int): Represents a bet on a dozen numbers, with a payout ratio of 3:1.
    """

    Single: int = 36
    Color: int = 2
    Dozen: int = 3


@dataclass
class Bet:
    """
    Data class representing a bet in a roulette game.

    Attributes:
        numbers (List[int]): A list of numbers on which the bet is placed. Default is an empty list.
        color (ColorTypes): The color on which the bet is placed. Default is ColorTypes.Green.
        amount (List[int]): A list of amounts bet on each number or color. Default is an empty list.
        bet_type (BetTypes): The type of bet being placed. Default is BetTypes.Color.
    """

    numbers: List[int] = field(default_factory=list)
    color: ColorTypes = ColorTypes.Green
    amount: List[int] = field(default_factory=list)
    bet_type: BetTypes = BetTypes.Color
