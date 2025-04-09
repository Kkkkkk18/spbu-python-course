import random
from project.game.bet import ColorTypes
from dataclasses import dataclass


@dataclass
class Pocket:
    """
    Data class that implements a pocket on a roulette wheel.

    Attributes
    ----------
    num : int
        The number in the pocket. Default is 0.
    color : ColorTypes
        The color of the pocket. Default is ColorTypes.Green.
    """

    num: int = 0
    color: ColorTypes = ColorTypes.Green


class RouletteTable:
    """
    Represents a roulette table with a wheel of pockets.

    Attributes
    ----------
    _pockets_num : int
        The number of pockets on the roulette wheel.
    _pockets : List[Pocket]
        A list of Pocket objects representing the pockets on the wheel.
    """

    def __init__(self):
        """Initialize the roulette table and set appropriate values to pockets on the wheel."""
        self._pockets_num = 37
        self._pockets = [Pocket()]

        numbers_of_same_color = (10, 18, 28)

        flag = True
        for i in range(1, self._pockets_num):
            if flag:
                self._pockets.append(Pocket(i, ColorTypes.Red))
            else:
                self._pockets.append(Pocket(i, ColorTypes.Black))

            if i not in numbers_of_same_color:
                flag = not flag

    @property
    def pockets_num(self) -> int:
        """Return number of pockets in wheel"""
        return self._pockets_num

    def spin(self) -> Pocket:
        """Simulate spinning the wheel and return the winning pocket."""
        return random.choice(self._pockets)
