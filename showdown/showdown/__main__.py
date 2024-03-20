from ._game import Game
from ._card import CardStack

def main():
    card_stack = CardStack()
    game = Game(card_stack=card_stack)
    game.start()

if __name__ == "__main__":
    main()