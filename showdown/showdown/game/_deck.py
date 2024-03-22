__all__ = ["Deck"]


from ._card import DummyCard, ShowdownCard


class Deck:
    _deck: list[ShowdownCard]
    dummy_card = DummyCard

    def __init__(self, deck: list[ShowdownCard]) -> None:
        self._deck = sorted(deck, key=lambda x: x.weight)

    def get_choice(self) -> dict[int, str]:
        choice = {index: card.name for index, card in enumerate(self._deck)}
        return choice or {0: self.dummy_card.name}

    def draw(self, card_index: int) -> ShowdownCard:
        if self._deck:
            card = self._deck.pop(card_index)
        else:
            card = self.dummy_card
        return card
