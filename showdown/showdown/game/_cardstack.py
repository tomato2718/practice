__all__ = ["CardStack"]

from random import shuffle

from ._card import Card, COLOR, RANK

class CardStack:
    _stack: list[Card]

    def __init__(self) -> None:
        self._stack = []
        for color in COLOR:
            for rank in RANK:
                self._stack.append(Card(color=color, rank=rank))

    def shuffle(self) -> None:
        shuffle(self._stack)

    def draw(self) -> Card:
        return self._stack.pop()