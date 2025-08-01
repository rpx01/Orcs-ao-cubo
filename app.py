from flask import Flask, render_template, jsonify, request
from models.player import Player
from game.logic import generate_orcs, player_attack
from models.orc import Orc

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


@app.route("/api/attack", methods=["POST"])
def attack():
    data = request.get_json()
    card_name = data["card_name"]
    orc_name = data["orc_name"]

    card = next((c for c in player.deck if c.name == card_name), None)
    orc = next((o for o in orcs if o.name == orc_name), None)

    if card and orc:
        result = player_attack(player, orc, card)
        if result == "orc_defeated":
            orcs.remove(orc)
        return jsonify(
            {
                "result": result,
                "player": player.to_dict(),
                "orcs": [o.to_dict() for o in orcs],
            }
        )

    return jsonify({"result": "error"}), 400

if __name__ == "__main__":
    app.run(debug=True)
