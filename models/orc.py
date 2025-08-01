import random

class Orc:
    def __init__(self, name, life, points):
        self.name = name
        self.life = life
        self.points = points

    def to_dict(self):
        return {
            "name": self.name,
            "life": self.life,
            "points": self.points
        }

def random_orc():
    names = ["Orc Guerreiro", "Orc Xamã", "Orc Gigante"]
    name = random.choice(names)
    return Orc(name, random.randint(3, 6), random.randint(1, 3))
