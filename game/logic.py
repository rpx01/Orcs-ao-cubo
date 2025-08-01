from typing import Dict, List

from models.player import Player
from models.orc import Orc


def generate_orcs() -> List[Orc]:
    """Generate a list of three random orcs."""
    return [Orc.random_orc() for _ in range(3)]


def create_game() -> Dict[str, List]:
    """Initialize the game state with players and orcs."""
    players = [Player.create("Player 1"), Player.create("Player 2")]
    orcs = generate_orcs()
    return {"players": players, "orcs": orcs}
