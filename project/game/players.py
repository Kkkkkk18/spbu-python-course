import random
from typing import Optional
from project.game.strategy import Strategy
from project.game.bet import Bet, BetTypes, ColorTypes


class Bot:
    """
    The Bot class represents an automated player in the roulette game.

    Attributes:
        name (str): The name of the bot.
        balance (int): The initial balance of the bot.
        _strategy (Strategy): The betting strategy used by the bot.
        _initial_balance (int): The initial balance of the bot, used to track winnings.
        last_result (bool): The result of the last bet (True if won, False otherwise).
        _last_bet (Bet): The last bet made by the bot.

    Methods:
        __init__(strategy: Strategy, balance: int, name: str = ""): Initializes a new bot with a strategy and balance.
        place_bet(min_bet: int, max_bet: int, pockets_num: int) -> None: Places a bet according to the bot's strategy.
        last_bet() -> Bet: Returns the last bet made by the bot.
        balance() -> int: Returns the current balance of the bot.
        balance.setter(value: int): Sets the balance of the bot.
        won() -> bool: Returns True if the bot's balance has increased from the initial balance.
        loss(min_bet: int) -> bool: Returns True if the bot's balance is less than the minimum bet.
    """

    def __init__(self, strategy: Strategy, balance: int, name: str = ""):
        """
         Initializes a new bot.

        Args:
             strategy (Strategy): The betting strategy used by the bot.
             balance (int): The initial balance of the bot.
             name (str, optional): The name of the bot, default is an empty string.
        """
        self._strategy = strategy
        self.name = name
        self.balance = balance
        self._initial_balance = balance
        self.last_result = False
        self._last_bet = Bet()

    def place_bet(self, min_bet: int, max_bet: int, pockets_num: int) -> None:
        """Make bet according to strategy."""
        self._last_bet = self._strategy.make_bet(
            self._balance, min_bet, max_bet, pockets_num, self.last_result
        )

    @property
    def last_bet(self) -> Bet:
        """Returns the last bet made by the bot."""
        return self._last_bet

    @property
    def balance(self) -> int:
        """Returns the current balance of the bot."""
        return self._balance

    @balance.setter
    def balance(self, value):
        """Sets the balance of the bot."""
        self._balance = value

    def won(self) -> bool:
        """Returns True if the bot's balance has increased from the initial balance."""
        return self.balance > self._initial_balance

    def loss(self, min_bet: int) -> bool:
        """Returns True if the bot's balance is less than the minimum bet."""
        return self._balance < min_bet
