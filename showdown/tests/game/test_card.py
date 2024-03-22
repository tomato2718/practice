from showdown.showdown.game._card import Card


class TestCard:
    @staticmethod
    def test_calculate_weight():
        heartA = Card._calculate_weight("紅心", "A")
        heart2 = Card._calculate_weight("紅心", "2")
        spade2 = Card._calculate_weight("黑桃", "2")

        assert heartA > spade2 > heart2
