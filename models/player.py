from models.card import get_initial_deck


class Player:
    def __init__(self, name):
        self.name = name
        self.mana = 10
        self.deck = get_initial_deck()

    def to_dict(self):
        return {
            "name": self.name,
            "mana": self.mana,
            "deck": [card.to_dict() for card in self.deck],
        }
