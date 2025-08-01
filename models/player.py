from dataclasses import dataclass, field
from typing import List

from .card import Card


@dataclass
class Player:
    """Represents a player in the game."""
    name: str
    mana: int = 10
    deck: List[Card] = field(default_factory=list)

    @staticmethod
    def create(name: str) -> "Player":
        """Create a player with a starter deck and mana."""
        deck = [Card.random_card() for _ in range(5)]
        return Player(name=name, mana=10, deck=deck)
