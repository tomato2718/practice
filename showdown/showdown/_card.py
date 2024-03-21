__all__ = [
    "CardImp",
    "CardStack",
    "DummyCard",
]

from typing import Literal, TypeAlias
from random import shuffle

_Colors: TypeAlias = Literal["黑桃", "紅心", "方塊", "梅花"]
_Ranks: TypeAlias = Literal[
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
]

COLOR: dict[_Colors, int] = {
    "黑桃": 4,
    "紅心": 3,
    "方塊": 2,
    "梅花": 1,
}

RANK: dict[_Ranks, int] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class CardImp:
    name: str
    weight: int

    def __init__(self, color: _Colors, rank: _Ranks):
        self.name = color + rank
        self.weight = self._calculate_weight(color, rank)

    @staticmethod
    def _calculate_weight(color: _Colors, rank: _Ranks) -> int:
        weight = RANK[rank] * 4 + COLOR[color]
        return weight


class DummyCard:
    name = ""
    weight = -1


class CardStack:
    _stack: list[CardImp]

    def __init__(self) -> None:
        self._stack = []
        for color in COLOR:
            for rank in RANK:
                self._stack.append(CardImp(color=color, rank=rank))

    def shuffle(self) -> None:
        shuffle(self._stack)

    def draw(self) -> CardImp:
        if self._stack:
            return self._stack.pop()
        else:
            raise Exception("Card stack is empty.")
