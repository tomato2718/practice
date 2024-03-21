from ._game import Game
from ._card import CardStack
from ._player import BotPlayer, RealPlayer

def main():
    card_stack = CardStack()
    game = Game(card_stack=card_stack)
    game.add_player(BotPlayer("foo"))
    game.add_player(BotPlayer("bar"))
    game.add_player(BotPlayer("baz"))
    game.add_player(RealPlayer("qux"))
    game.start()

if __name__ == "__main__":
    main()