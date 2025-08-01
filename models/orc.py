from dataclasses import dataclass
import random


@dataclass
class Orc:
    """Represents an orc enemy."""
    strength: int
    health: int

    @staticmethod
    def random_orc() -> "Orc":
        """Create an orc with random attributes."""
        return Orc(strength=random.randint(1, 10), health=random.randint(1, 10))
