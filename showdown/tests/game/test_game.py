from unittest.mock import MagicMock

import pytest

from showdown.showdown.game._deck import Deck
from showdown.showdown.game._game import Game
from showdown.showdown.game.interface import ShowdownCard, ShowdownPlayer


class TestGame:
    @staticmethod
    @pytest.fixture(scope="function")
    def game() -> Game:
        return Game()

    @staticmethod
    @pytest.fixture(scope="class")
    def MockPlayer() -> type[ShowdownPlayer]:
        class MockPlayer:
            name: str
            exchanged: bool
            deck: Deck

            def __init__(self, __name: str):
                self.name = __name

            def set_deck(self, __deck: Deck) -> None:
                self.deck = __deck

            def choose_player_to_exchange_card(
                self,
                players: list[str],
            ) -> int: ...

            def action(self) -> ShowdownCard: ...

            def want_exchange(self) -> bool: ...

        return MockPlayer

    @staticmethod
    def test_add_player(game: Game, MockPlayer: type[ShowdownPlayer]):
        game.add_player(MockPlayer("foo"))
        game.add_player(MockPlayer("bar"))
        game.add_player(MockPlayer("baz"))
        game.add_player(MockPlayer("qux"))

        with pytest.raises(Exception):
            game.add_player(MockPlayer("fred"))

        assert game._players[0].name == "foo"
        assert game._players[1].name == "bar"
        assert game._players[2].name == "baz"
        assert game._players[3].name == "qux"
        assert game._players_name[0] == "foo"
        assert game._players_name[1] == "bar"
        assert game._players_name[2] == "baz"
        assert game._players_name[3] == "qux"
        assert game._score_board["foo"] == 0
        assert game._score_board["bar"] == 0
        assert game._score_board["baz"] == 0
        assert game._score_board["qux"] == 0

    @staticmethod
    def test_start(game: Game):
        game.add_player(MagicMock())

        with pytest.raises(Exception):
            game.start()

        game.add_player(MagicMock())
        game.add_player(MagicMock())
        game.add_player(MagicMock())

        game._shuffle_card_stack = MagicMock()
        game._deal_cards = MagicMock()
        game._start_game = MagicMock()
        game.start()

        game._shuffle_card_stack.assert_called()
        game._deal_cards.assert_called()
        game._start_game.assert_called()

    @staticmethod
    def test_shuffle_card_stack(game: Game):
        game._card_stack.shuffle = MagicMock()

        game._shuffle_card_stack()

        game._card_stack.shuffle.assert_called()

    @staticmethod
    def test_deal_cards(game: Game, MockPlayer: type[ShowdownPlayer]):
        player1 = MockPlayer("foo")
        player2 = MockPlayer("bar")
        player3 = MockPlayer("baz")
        player4 = MockPlayer("qux")

        player1.set_deck = MagicMock()
        player2.set_deck = MagicMock()
        player3.set_deck = MagicMock()
        player4.set_deck = MagicMock()

        game.add_player(player1)
        game.add_player(player2)
        game.add_player(player3)
        game.add_player(player4)

        game._deal_cards()

        player1.set_deck.assert_called_once()
        player2.set_deck.assert_called_once()
        player3.set_deck.assert_called_once()
        player4.set_deck.assert_called_once()

    @staticmethod
    def test_start_game(game: Game):
        game._start_round = MagicMock()
        game._find_winner = MagicMock()

        game._start_game()

        assert game._start_round.call_count == 13
        assert game._find_winner.call_count == 1

    @staticmethod
    def test_start_round(): ...

    @staticmethod
    def test_ask_for_exchange(game: Game, MockPlayer: type[ShowdownPlayer]):
        game._players_name = MagicMock()
        game._players = MagicMock()

        player1 = MockPlayer("foo")
        player1.exchanged = True
        player1.want_exchange = MagicMock(return_value=True)
        game._exchange_deck = MagicMock()
        game._record_exchanged = MagicMock()

        game._ask_for_exchange(player1, round=1)

        game._exchange_deck.assert_not_called()
        game._record_exchanged.assert_not_called()

        player2 = MockPlayer("bar")
        player2.exchanged = False
        player2.want_exchange = MagicMock(return_value=True)
        game._exchange_deck = MagicMock()
        game._record_exchanged = MagicMock()

        game._ask_for_exchange(player2, round=1)

        game._exchange_deck.assert_called()
        game._record_exchanged.assert_called()

        player3 = MockPlayer("baz")
        player3.exchanged = True
        player3.want_exchange = MagicMock(return_value=False)
        game._exchange_deck = MagicMock()
        game._record_exchanged = MagicMock()

        game._ask_for_exchange(player3, round=1)

        game._exchange_deck.assert_not_called()
        game._record_exchanged.assert_not_called()

        player4 = MockPlayer("bar")
        player4.exchanged = False
        player4.want_exchange = MagicMock(return_value=False)
        game._exchange_deck = MagicMock()
        game._record_exchanged = MagicMock()

        game._ask_for_exchange(player4, round=1)

        game._exchange_deck.assert_not_called()
        game._record_exchanged.assert_not_called()

    @staticmethod
    def test_exchange_deck(game: Game, MockPlayer: type[ShowdownPlayer]):
        player1 = MockPlayer("foo")
        player2 = MockPlayer("bar")

        deck1 = MagicMock()
        deck2 = MagicMock()

        player1.deck = deck1
        player2.deck = deck2

        game._exchange_deck(player1, player2)

        assert player1.deck is not deck1
        assert player1.deck is deck2
        assert player2.deck is not deck2
        assert player2.deck is deck1

    @staticmethod
    def test_record_exchange(game: Game, MockPlayer: type[ShowdownPlayer]):
        player1 = MockPlayer("foo")
        player2 = MockPlayer("bar")
        player3 = MockPlayer("baz")

        game._record_exchanged(1, (player1, player2))
        game._record_exchanged(1, (player2, player3))
        game._record_exchanged(3, (player3, player1))

        assert game._exchanged[1][0] == (player1, player2)
        assert game._exchanged[1][1] == (player2, player3)
        assert game._exchanged[3][0] == (player3, player1)

    @staticmethod
    def test_ask_for_play(game: Game, MockPlayer: type[ShowdownPlayer]):
        player = MockPlayer("foo")
        mock_card = MagicMock()
        player.action = MagicMock(return_value=mock_card)

        card = game._ask_for_play(player)

        player.action.assert_called()
        assert card is mock_card

    @staticmethod
    def test_check_return_deck(game: Game, MockPlayer: type[ShowdownPlayer]):
        game._exchange_deck = MagicMock()
        player1 = MockPlayer("foo")
        player2 = MockPlayer("bar")
        game.add_player(player1)
        game.add_player(player2)

        game._exchanged = {3: [(player1, player2)]}

        game._check_return_deck(6)

        game._exchange_deck.assert_called()

    @staticmethod
    def test_find_current_round_winner(game: Game, MockPlayer: type[ShowdownPlayer]):
        game.add_player(MockPlayer("foo"))
        game.add_player(MockPlayer("bar"))
        game.add_player(MockPlayer("baz"))
        game.add_player(MockPlayer("qux"))

        game._find_current_round_winner(
            {
                "foo": MagicMock(weight=25),
                "bar": MagicMock(weight=31),
                "baz": MagicMock(weight=17),
                "qux": MagicMock(weight=5),
            }
        )

        assert game._score_board["foo"] == 0
        assert game._score_board["bar"] == 1
        assert game._score_board["baz"] == 0
        assert game._score_board["qux"] == 0
