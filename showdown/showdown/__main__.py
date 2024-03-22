from .game import Game
from ._player import BotPlayer, RealPlayer

def main():
    game = Game()
    game.add_player(BotPlayer("foo"))
    game.add_player(BotPlayer("bar"))
    game.add_player(BotPlayer("baz"))
    game.add_player(RealPlayer("YOU"))
    game.start()

if __name__ == "__main__":
    main()