__all__ = ["BotPlayer", "RealPlayer"]

from abc import ABC, abstractmethod

from .game import ShowdownCard, Deck


class Player(ABC):
    name: str
    exchanged: bool
    deck: Deck

    def __init__(self, name: str) -> None:
        self.name = name
        self.exchanged = False

    def set_deck(self, __deck: Deck) -> None:
        self.deck = __deck

    @abstractmethod
    def choose_player_to_exchange_card(
        self,
        players: list[str],
    ) -> int: ...

    @abstractmethod
    def action(self) -> ShowdownCard: ...

    @abstractmethod
    def want_exchange(self) -> bool: ...


class BotPlayer(Player):
    def choose_player_to_exchange_card(
        self,
        players: list[str],
    ) -> int: ...

    def want_exchange(self) -> bool:
        return False

    def action(self) -> ShowdownCard:
        card = self.deck.draw(0)
        return card


class RealPlayer(Player):
    def set_deck(self, __deck: Deck) -> None:
        print("你持有的手牌為：")
        print(__deck.get_choice())
        super().set_deck(__deck)

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

    def action(self) -> ShowdownCard:
        print("請選擇要出的手牌：")
        choice = self.deck.get_choice()
        print(choice)
        while True:
            target = input("：")
            if not (target.isdigit() and int(target) in choice):
                print("請選擇擁有的手牌")
            else:
                break
        card = self.deck.draw(int(target))
        return card
