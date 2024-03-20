import pytest

from showdown.showdown._card import Card, CardStack


class TestCard:
    @staticmethod
    def test_calculate_weight():
        heartA = Card._calculate_weight("紅心", "A")
        heart2 = Card._calculate_weight("紅心", "2")
        spade2 = Card._calculate_weight("黑桃", "2")

        assert heartA > spade2 > heart2


class TestCardStack:
    @staticmethod
    def test_init():
        card_stack = CardStack()

        assert len(card_stack._stack) == 52

    @staticmethod
    def test_draw():
        card_stack = CardStack()

        for i in range(52):
            card = card_stack.draw()
            assert isinstance(card, Card)
            assert len(card_stack._stack) == 51 - i

        with pytest.raises(Exception):
            card_stack.draw()
