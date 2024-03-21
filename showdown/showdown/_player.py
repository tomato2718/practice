__all__ = ["BotPlayer", "RealPlayer"]

from abc import ABC, abstractmethod

from ._card import DummyCard
from ._game import Card


class Player(ABC):
    name: str
    exchanged: bool
    deck: set[Card]

    def __init__(self, name: str) -> None:
        self.name = name
        self.exchanged = False

    def set_deck(self, __deck: set[Card]) -> None:
        self.deck = __deck

    @abstractmethod
    def choose_player_to_exchange_card(
        self,
        players: list[str],
    ) -> int: ...

    @abstractmethod
    def action(self) -> Card: ...

    @abstractmethod
    def want_exchange(self) -> bool: ...


class BotPlayer(Player):
    def choose_player_to_exchange_card(
        self,
        players: list[str],
    ) -> int: ...

    def want_exchange(self) -> bool:
        return False

    def action(self) -> Card:
        if self.deck:
            return self.deck.pop()
        else:
            return DummyCard()


class RealPlayer(Player):
    def set_deck(self, __deck: set[Card]) -> None:
        print("你持有的手牌為：")
        super().set_deck(__deck)
        print(self._get_sorted_deck())

    def _get_sorted_deck(self) -> list[str]:
        sorted_deck = sorted(list(self.deck), key=lambda x: x.weight)
        return [card.name for card in sorted_deck]

    def choose_player_to_exchange_card(
        self,
        players: list[str],
    ) -> int:
        print({i: j for i, j in enumerate(players)})

        while True:
            input_ = input("請選擇要交換手牌的對象：")
            if input_ not in ("0", "1", "2", "3"):
                print("請輸入玩家編號！")
            elif players[int(input_)] == self.name:
                print("不能與自己交換手牌")
            else:
                break
        return int(input_)

    def want_exchange(self) -> bool:
        while (res := input("你是否要交換手牌 (y/n)？")) not in ("y", "n"):
            print("請輸入 y 或 n。")
        return res == "y"

    def action(self) -> Card:
        if not self.deck:
            print("你沒有能出的手牌，將會跳過此回合")
            return DummyCard()

        print("請選擇要出的手牌：")
        output_deck = {
            str(index): card for index, card in enumerate(self._get_sorted_deck())
        }
        while (target := input(f"{output_deck}：")) not in output_deck:
            print("請選擇擁有的手牌")

        for card in self.deck:
            if card.name == output_deck[target]:
                break
        self.deck.remove(card)
        return card
