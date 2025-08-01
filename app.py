from flask import Flask, render_template, jsonify
from models.player import Player
from game.logic import generate_orcs

app = Flask(__name__)

# Estado inicial do jogo
player = Player("Jogador 1")
orcs = generate_orcs()

@app.route("/")
def game():
    return render_template("game.html")

@app.route("/api/state")
def state():
    return jsonify({
        "player": player.to_dict(),
        "orcs": [orc.to_dict() for orc in orcs]
    })

if __name__ == "__main__":
    app.run(debug=True)
