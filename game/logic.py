from models.orc import random_orc

def generate_orcs():
    return [random_orc() for _ in range(3)]
