import random
from abc import ABC, abstractmethod
from typing import List
from project.game.bet import Bet, BetTypes, ColorTypes


class Strategy(ABC):
    """
    Abstract class that defines the interface for a roulette playing strategy.

    Methods
    -------
    make_bet(balance: int, min_bet: int, max_bet: int, pockets_num: int, last: bool = False) -> Bet
        Abstract method to be implemented by subclasses to define the betting strategy.
    """

    @abstractmethod
    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """
        Make a bet based on the current game state.

        Parameters
        ----------
        balance : int
            The amount of money left.
        min_bet : int
            The minimum bet amount.
        max_bet : int
            The maximum bet amount.
        pockets_num : int
            The number of pockets on the roulette wheel.
        last : bool, optional
            True if the last bet won, default is False.

        Returns
        -------
        Bet
            A Bet object representing the bet to be placed.
        """
        pass


class AggressiveStrategy(Strategy):
    """A strategy that makes bets on a random selection of up to half the pockets on the wheel."""

    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """
        Make a bet on a random selection of up to half the pockets on the wheel.

        Parameters
        ----------
        balance : int
            The amount of money left.
        min_bet : int
            The minimum bet amount.
        max_bet : int
            The maximum bet amount.
        pockets_num : int
            The number of pockets on the roulette wheel.
        last : bool, optional
            True if the last bet won, default is False.

        Returns
        -------
        Bet
            A Bet object representing the bet to be placed.
        """
        if balance < min_bet:
            return Bet()

        chips_num = min(balance // min_bet, pockets_num // 2, max_bet // min_bet)

        bet_numbers = random.sample(range(pockets_num), chips_num)

        bet_amount = [min_bet for _ in range(chips_num)]

        return Bet(numbers=bet_numbers, amount=bet_amount, bet_type=BetTypes.Single)


class BasicStrategy(Strategy):
    """A basic strategy that makes bets on a randomly chosen color."""

    def __init__(self):
        self._last_bet_amount: List[int] = []
        self._last_color: ColorTypes
        self._is_first = True

    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """
        Make a bet on a randomly chosen color.

        Parameters
        ----------
        balance : int
            The amount of money left.
        min_bet : int
            The minimum bet amount.
        max_bet : int
            The maximum bet amount.
        pockets_num : int
            The number of pockets on the roulette wheel.
        last : bool, optional
            True if the last bet won, default is False.

        Returns
        -------
        Bet
            A Bet object representing the bet to be placed.
        """
        if balance < min_bet:
            return Bet()

        bet_color = random.choice(list(ColorTypes))

        bet_amount = [min_bet]

        return Bet(color=bet_color, amount=bet_amount, bet_type=BetTypes.Color)


class OptimalStrategy(Strategy):
    """A strategy that makes bets on one of the dozens on the roulette wheel."""

    def __init__(self):
        self._dozen_number = 3

    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """
        Make a bet on one of the dozens on the roulette wheel.

        Parameters
        ----------
        balance : int
            The amount of money left.
        min_bet : int
            The minimum bet amount.
        max_bet : int
            The maximum bet amount.
        pockets_num : int
            The number of pockets on the roulette wheel.
        last : bool, optional
            True if the last bet won, default is False.

        Returns
        -------
        Bet
            A Bet object representing the bet to be placed.
        """
        if balance < min_bet:
            return Bet()

        num_dozen = random.choice([i + 1 for i in range(self._dozen_number)])

        numbers_bet = pockets_num // self._dozen_number

        bet_numbers = [
            i + 1 for i in range(numbers_bet * (num_dozen - 1), numbers_bet * num_dozen)
        ]
        bet_amount = [
            min_bet * min(balance // min_bet, numbers_bet, max_bet // min_bet)
        ]
        return Bet(numbers=bet_numbers, amount=bet_amount, bet_type=BetTypes.Dozen)
