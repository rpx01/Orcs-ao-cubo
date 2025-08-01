class Player:
    def __init__(self, name):
        self.name = name
        self.mana = 10
        self.deck = ["Bola de Fogo", "Raio Gélido", "Mísseis Mágicos"]

    def to_dict(self):
        return {
            "name": self.name,
            "mana": self.mana,
            "deck": self.deck
        }
