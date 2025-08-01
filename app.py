from flask import Flask, jsonify

from game.logic import create_game, generate_orcs

app = Flask(__name__)

game_state = create_game()


@app.route("/game")
def get_game():
    """Return the current state of the game."""
    # Generate new orcs each round
    game_state["orcs"] = generate_orcs()
    return jsonify(
        {
            "players": [player.__dict__ for player in game_state["players"]],
            "orcs": [orc.__dict__ for orc in game_state["orcs"]],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
