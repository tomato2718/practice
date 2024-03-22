from collections import defaultdict
from json import dumps

from ._cardstack import CardStack
from ._card import ShowdownCard
from ._deck import Deck
from .interface import ShowdownPlayer


class Game:
    _card_stack: CardStack
    _score_board: dict[str, int]
    _players: list[ShowdownPlayer]
    _players_name: list[str]
    _exchanged: dict[int, list[tuple[ShowdownPlayer, ShowdownPlayer]]]

    def __init__(self) -> None:
        self._card_stack = CardStack()
        self._score_board = dict()
        self._players = list()
        self._players_name = list()
        self._exchanged = defaultdict(list)

    def add_player(self, __player: ShowdownPlayer) -> None:
        if len(self._players) == 4:
            raise Exception("There's already 4 players.")
        self._score_board[__player.name] = 0
        self._players.append(__player)
        self._players_name.append(__player.name)

    def start(self) -> None:
        if len(self._players) < 4:
            raise Exception("There's not yet 4 players.")
        print("遊戲即將開始")
        self._shuffle_card_stack()
        self._deal_cards()
        self._start_game()

    def _shuffle_card_stack(self) -> None:
        print("正在洗牌")
        self._card_stack.shuffle()

    def _deal_cards(self) -> None:
        print("正在發牌")
        for player in self._players:
            deck = Deck([self._card_stack.draw() for _ in range(13)])
            player.set_deck(deck)

    def _start_game(self) -> None:
        print("遊戲開始")
        for round in range(1, 14):
            self._start_round(round)
        self._find_winner()

    def _start_round(self, __round: int) -> None:
        print(f"現在是第 {__round} 回合：")
        plays: dict[str, ShowdownCard] = {}
        for player in self._players:
            print(f"輪到 {player.name} 行動")
            self._ask_for_exchange(player, round=__round)
            plays[player.name] = self._ask_for_play(player)
        self._find_current_round_winner(plays)
        self._check_return_deck(__round)

    def _ask_for_exchange(self, __player: ShowdownPlayer, round: int) -> None:
        if __player.exchanged is False and __player.want_exchange():
            target_index = __player.choose_player_to_exchange_card(self._players_name)
            target_player = self._players[target_index]
            print(f"玩家 {__player.name} 要求與玩家 {target_player.name} 交換手牌")
            self._exchange_deck(
                __player,
                target_player,
            )
            __player.exchanged = True
            self._record_exchanged(
                round=round,
                players=(__player, target_player),
            )

    @staticmethod
    def _exchange_deck(player1: ShowdownPlayer, player2: ShowdownPlayer) -> None:
        player1.deck, player2.deck = player2.deck, player1.deck

    def _record_exchanged(
        self,
        round: int,
        players: tuple[ShowdownPlayer, ShowdownPlayer],
    ) -> None:
        self._exchanged[round].append(players)

    def _ask_for_play(self, __player: ShowdownPlayer) -> ShowdownCard:
        card = __player.action()
        return card

    def _check_return_deck(self, __round: int) -> None:
        exchange_delay = 3
        for player1, player2 in self._exchanged[__round - exchange_delay]:
            print(f"玩家 {player1.name} 和 玩家 {player2.name} 將手牌換回")
            self._exchange_deck(player1, player2)

    def _find_current_round_winner(self, plays: dict[str, ShowdownCard]) -> None:
        for player, card in plays.items():
            print(f"{player} 出的是 {card.name}")
        winner, _ = max(plays.items(), key=lambda x: x[1].weight)
        print(f"此回合獲勝的是 {winner} !")
        self._score_board[winner] += 1

    def _find_winner(self):
        # TODO: 有可能平手
        print("遊戲結束！")
        print(dumps(self._score_board, indent=2))
        max_score = max(self._score_board.values())
        winner_list = []
        for player, score in self._score_board.items():
            if score == max_score:
                winner_list.append(player)
        winner = " 和 ".join(winner_list)
        print(f"獲勝的是：{winner}，一共獲得了 {max_score} 分")
