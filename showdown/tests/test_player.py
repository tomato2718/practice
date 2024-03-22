import pytest

from showdown.showdown._player import BotPlayer

class TestBotPlayer:
    @staticmethod
    @pytest.fixture(scope="class")
    def player() -> BotPlayer:
        return BotPlayer("foo")

    @staticmethod
    def test_want_exchange(player: BotPlayer):
        assert player.want_exchange() is False