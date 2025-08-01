import random
import uuid


class Orc:
    def __init__(self, name, life, points):
        self.id = str(uuid.uuid4())
        self.name = name
        self.life = life
        self.points = points

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "life": self.life,
            "points": self.points,
        }


def random_orc(round_number=1):
    names = ["Orc Guerreiro", "Orc Xamã", "Orc Gigante"]
    name = random.choice(names)

    # A vida e os pontos base aumentam com a rodada
    base_life = 3 + round_number
    base_points = 1 + round_number

    # Adiciona uma pequena variação aleatória
    life = random.randint(base_life, base_life + 3)
    points = random.randint(base_points, base_points + 2)

    return Orc(name, life, points)
