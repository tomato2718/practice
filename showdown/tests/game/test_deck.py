import pytest

from showdown.showdown.game._card import Card
from showdown.showdown.game._deck import Deck


class TestDeck:
    @staticmethod
    @pytest.fixture(scope="class")
    def deck() -> Deck:
        return Deck(
            [
                Card("方塊", "2"),
                Card("梅花", "10"),
            ]
        )

    @staticmethod
    def test_get_choice(deck: Deck):
        assert deck.get_choice() == {0: "方塊2", 1: "梅花10"}

        empty_deck = Deck([])

        assert empty_deck.get_choice() == {0: "pass"}

    @staticmethod
    def test_draw(deck: Deck):
        assert len(deck._deck) == 2
        assert deck.draw(0).name == "方塊2"
        assert len(deck._deck) == 1
        assert deck.draw(0).name == "梅花10"
        assert len(deck._deck) == 0
        assert deck.draw(0).name == "pass"
