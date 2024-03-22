__all__ = ["ShowdownPlayer"]

from typing import Protocol

from ._deck import Deck
from ._card import ShowdownCard


class ShowdownPlayer(Protocol):
    name: str
    exchanged: bool
    deck: Deck

    def set_deck(self, __deck: Deck) -> None: ...

    def choose_player_to_exchange_card(
        self,
        players: list[str],
    ) -> int: ...

    def action(self) -> ShowdownCard: ...

    def want_exchange(self) -> bool: ...
