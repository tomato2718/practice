__all__ = [
    "ShowdownCard",
    "Card",
    "DummyCard",
    "COLOR",
    "RANK",
]

from typing import Literal, TypeAlias
from abc import ABC

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

class ShowdownCard(ABC):
    weight: int
    name: str

class Card(ShowdownCard):
    def __init__(self, color: _Colors, rank: _Ranks):
        self.name = color + rank
        self.weight = self._calculate_weight(color, rank)

    @staticmethod
    def _calculate_weight(color: _Colors, rank: _Ranks) -> int:
        weight = RANK[rank] * 4 + COLOR[color]
        return weight


class _DummyCard(ShowdownCard):
    name = "pass"
    weight = -1

DummyCard = _DummyCard()