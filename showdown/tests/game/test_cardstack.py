from showdown.showdown.game._cardstack import CardStack
from showdown.showdown.game._card import Card


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
