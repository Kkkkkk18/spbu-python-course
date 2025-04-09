from typing import List, Set, Tuple
from project.game.players import Bot
from project.game.table import RouletteTable, Pocket
from project.game.strategy import ColorTypes


class RouletteGame:

    """
    A class representing a roulette game with multiple bot players.

    Attributes
    ----------
    bots : List[Bot]
        A list of bot players participating in the game.
    rounds_num : int
        The number of rounds to play in the game.
    _verbose : bool
        Flag indicating whether to print game progress to the console.
    _verbose_file : bool
        Flag indicating whether to write game progress to a file.
    _is_over : bool
        Flag indicating whether the game is over.
    current_round : int
        The current round number.
    _file_name : str
        The name of the file to write game progress to.
    _wheel : RouletteTable
        The roulette table with the wheel of pockets.
    _loss : Set[int]
        A set of indices of bots that have lost the game.

    Methods
    -------
    is_game_over() -> None:
        Determine if the game is over and set the _is_over flag to True.
    display_game_state(min_bet: int, winner: Set[int]) -> str:
        Return the current state of the game as a string.
    find_winner(min_bet: int, pocket: Pocket) -> Set[int]:
        Determine the winners of the current round and return their indices.
    run_game(min_bet: int = 1, max_bet: int = 100) -> Tuple[List[Bot], List[Bot]]:
        Start and play the roulette game. Return the winners and losers of the game.
    play_round(min_bet: int, max_bet: int) -> None:
        Play one round of the game.
    pay_off(bot: Bot) -> int:
        Calculate the winning amount for a bot in the current round.
    get_bets(min_bet: int) -> str:
        Return the bets made by bots in the current round as a string.
    write(msg: str) -> None:
        Write a message to a file if _verbose_file flag is True and print it if _verbose flag is True.
    """

    def __init__(
        self,
        bots: List[Bot],
        rounds_num: int = 10,
        verbose: bool = False,
        verbose_file: bool = False,
        *,
        file_name="project/game/example/example.txt",
    ):
        """
        Initialize the RouletteGame with bot players and game settings.

        Parameters
        ----------
        bots : List[Bot]
            A list of bot players participating in the game.
        rounds_num : int, optional
            The number of rounds to play in the game, default is 10.
        verbose : bool, optional
            Flag indicating whether to print game progress to the console, default is False.
        verbose_file : bool, optional
            Flag indicating whether to write game progress to a file, default is False.
        file_name : str, optional
            The name of the file to write game progress to, default is "project/game/example/example.txt".
        """
        self.bots = bots
        self.rounds_num = rounds_num
        self._verbose = verbose
        self._verbose_file = verbose_file
        self._is_over = False
        self.current_round = 0
        self._file_name = file_name
        self._wheel = RouletteTable()
        self._loss: Set[int] = set()

    def is_game_over(self) -> None:
        """Determine if game is over and set _is_over flag to True"""
        if (
            len(self._loss) >= len(self.bots) - 1
            or self.current_round == self.rounds_num
        ):
            self._is_over = True

    def display_game_state(self, min_bet: int, winner: Set[int]) -> str:
        """
        Return current state of game as a string

        Parameters
        ----------
        min_bet : int
            The minimum possible bet.
        winner : Set[int]
            A set of indices of bots that won the current round.

        Returns
        -------
        str
            A string representing the current state of the game.
        """

        msg = "Current game state:\n-------------------\n"
        bot_msg = "    Players: "
        win_msg = "    Winners of the round: "
        lose_msg = "    Bankrupts: "

        for bot in self.bots:
            bot_msg += bot.name + f"(balance={bot.balance}) "

        if all(not bot.loss(min_bet) for bot in self.bots):
            lose_msg += "no bankrupts"
        else:
            for bot in self.bots:
                if bot.loss(min_bet):
                    lose_msg += bot.name + " "

        if len(winner) == 0:
            win_msg += "no winners"
        else:
            for i in winner:
                win_msg += self.bots[i].name + " "
        msg += bot_msg + "\n" + win_msg + "\n" + lose_msg + "\n\n"
        return msg

    def find_winner(self, min_bet: int, pocket: Pocket) -> Set[int]:
        """Determine winners of current round and return their indexes

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        pocket : Pocket
            Winning pocket

        Return
        ------
        Set[int]
        """

        winner: Set[int] = set()
        for i in range(len(self.bots)):
            if not self.bots[i].loss(min_bet):
                # check if color or number matches
                if self.bots[i].last_bet.color == pocket.color:
                    winner.add(i)
                elif pocket.num in self.bots[i].last_bet.numbers:
                    winner.add(i)

        return winner

    def run_game(
        self, min_bet: int = 1, max_bet: int = 100
    ) -> Tuple[List[Bot], List[Bot]]:
        """Start and play roulette game. Return winners and losers of game

        If _verbose flag is True then print process of game.

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        max_bet : int
            Maximum possible bet

        Return
        ------
        Tuple[List[Bot], List[Bot]]
        """
        self.write("Roulette\n\n")
        self.write(f"Minimum bet: {min_bet}\n")
        self.write(f"Maximum bet: {max_bet}\n")
        self.write(f"Number of rounds: {self.rounds_num}\n\n")
        self.write(self.display_game_state(min_bet, set()))

        while not self._is_over:
            self.play_round(min_bet, max_bet)
            self.is_game_over()

        self.write("\nGame is over\n\n")
        game_winners: List[Bot] = []
        game_losers: List[Bot] = []
        # show winners and losers of game
        for bot in self.bots:
            if bot.won():
                game_winners.append(bot)
            else:
                game_losers.append(bot)
            self.write(bot.name + (" won\n" if bot.won() else " lost\n"))

        return (game_winners, game_losers)

    def play_round(self, min_bet: int, max_bet: int) -> None:
        """Play one round of game

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        max_bet : int
            Maximum possible bet

        Return
        ------
        None
        """
        self.write("=== ROUND " + str(self.current_round + 1) + " ===\n\n")
        pocket = self._wheel.spin()

        self.write("The wheel is spinning\n\n")

        # bots make bet
        for i in range(len(self.bots)):
            if not self.bots[i].loss(min_bet):
                self.bots[i].place_bet(min_bet, max_bet, self._wheel.pockets_num)
            else:
                self._loss.add(i)

        self.write(self.get_bets(min_bet))
        self.write(
            f"The winning number and color: {str(pocket.num)} {str(pocket.color.value)}\n\n"
        )

        winners = self.find_winner(min_bet, pocket)

        # collect bets and give the winnings to winners
        for i in range(len(self.bots)):
            self.bots[i].last_result = False
            if not self.bots[i].loss(min_bet):
                self.bots[i].balance -= sum(self.bots[i].last_bet.amount)
                if i in winners:
                    self.bots[i].last_result = True
                    self.bots[i].balance += self.pay_off(self.bots[i])

        self.write(self.display_game_state(min_bet, winners))
        self.current_round += 1

    def pay_off(self, bot: Bot) -> int:
        """Calculate winning amount in current round

        Parameters
        ----------
        bot : Bot
            Bot that has won current round
        pockets_num : int
            Number of pockets in wheel

        Return
        ------
        int
        """

        bet = bot.last_bet
        won = bet.amount[0] * bet.bet_type.value

        return won

    def get_bets(self, min_bet: int) -> str:
        """Return bets made by bots in current round as a string

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        """
        msg = "Bets:\n----"
        for bot in self.bots:
            if not bot.loss(min_bet):
                msg += (
                    "\n    "
                    + bot.name
                    + f" made a bet with {sum(bot.last_bet.amount)} chips on "
                )
                bet = bot.last_bet
                if bet.color != ColorTypes.Green:
                    msg += bet.color.value + " (color)"
                elif len(bet.numbers) != 0:
                    msg += (
                        "".join(map(lambda n: str(n) + " ", bet.numbers))
                        + f"({bet.bet_type.name.lower()})"
                    )

        return msg + "\n\n"

    def write(self, msg: str) -> None:
        """Write msg to file if _verbose_file flag is True and print it if the _verbose flag is True."""
        if self._verbose_file:
            with open(self._file_name, "a") as f:
                f.write(msg)

        if self._verbose:
            print(msg, end="")
