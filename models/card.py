from dataclasses import dataclass
import random


@dataclass
class Card:
    """Simple card used in the player's deck."""
    name: str
    value: int

    @staticmethod
    def random_card() -> "Card":
        """Generate a card with a random name and value."""
        names = ["Slash", "Shield", "Heal", "Fireball", "Lightning"]
        return Card(name=random.choice(names), value=random.randint(1, 5))
