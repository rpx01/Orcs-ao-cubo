class Card:
    def __init__(self, name, mana_cost, damage):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage

    def to_dict(self):
        return {
            "name": self.name,
            "mana_cost": self.mana_cost,
            "damage": self.damage,
        }


def get_initial_deck():
    return [
        Card("Bola de Fogo", 3, 4),
        Card("Raio Gélido", 2, 2),
        Card("Mísseis Mágicos", 5, 6),
    ]
