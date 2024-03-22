from showdown.showdown.game._card import Card, _Colors, _Ranks


class TestCard:
    @staticmethod
    def test_calculate_weight():
        COLOR: list[_Colors] = ["梅花", "方塊", "紅心", "黑桃"]
        RANK: list[_Ranks] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        last_weight = -1
        for rank in RANK:
            for color in COLOR:
                weight = Card._calculate_weight(color, rank)
                assert weight > last_weight
                last_weight = weight