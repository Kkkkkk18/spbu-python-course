import pytest
from project.game.strategy import AggressiveStrategy, BasicStrategy, OptimalStrategy
from project.game.roulette import RouletteGame
from project.game.table import RouletteTable
from project.game.players import Bot
from project.game.bet import Bet


def test_spin_wheel():
    wheel = RouletteTable()
    assert wheel.pockets_num == 37

    with pytest.raises(AttributeError):
        wheel.pockets_num = 26


@pytest.mark.parametrize(
    "strategy, bet_type",
    [
        (AggressiveStrategy(), 36),
        (BasicStrategy(), 2),
        (OptimalStrategy(), 3),
    ],
)
def test_game_strategy(strategy, bet_type):
    wheel = RouletteTable()
    bot = Bot(strategy, 100)
    bot.place_bet(1, 100, wheel.pockets_num)

    assert bot.last_bet.bet_type.value == bet_type
    assert sum(bot.last_bet.amount) <= bot.balance


def test_game_bot():
    bot = Bot(AggressiveStrategy(), balance=100)

    assert bot.balance == 100
    bot.balance -= 20
    assert bot.balance == 80

    with pytest.raises(AttributeError):
        bot.last_bet = Bet()


@pytest.fixture
def roulette():
    bot1 = Bot(AggressiveStrategy(), 100)
    bot2 = Bot(BasicStrategy(), 100)
    bot3 = Bot(OptimalStrategy(), 100)
    bots = [bot1, bot2, bot3]
    return RouletteGame(bots)


def test_game_roulette(roulette):
    win, lose = roulette.run_game()

    assert roulette.current_round == roulette.rounds_num
    assert len(win) + len(lose) == len(roulette.bots)


def test_game_play_round(roulette):
    assert roulette.current_round == 0

    roulette.play_round(1, 100)

    assert roulette.current_round == 1
