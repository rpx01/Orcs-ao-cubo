from flask import Flask, render_template, jsonify, request
from models.player import Player
from game.logic import generate_orcs, player_attack
from models.orc import Orc

app = Flask(__name__)


def initial_state():
    """Função para gerar o estado inicial do jogo."""
    player = Player("Jogador 1")
    return {
        "player": player,
        "orcs": generate_orcs(1),
        "round": 1,
        "score": 0,
        "game_over": False,
    }


# --- Estado do Jogo ---
game_state = initial_state()
# --------------------


def check_game_over(player, orcs):
    """Verifica se o jogo terminou."""
    if not orcs:
        return False  # Não pode ser fim de jogo se não há orcs

    min_mana_cost = min(card.mana_cost for card in player.deck)
    return player.mana < min_mana_cost


@app.route("/")
def game():
    return render_template("game.html")


@app.route("/api/state")
def state():
    return jsonify(
        {
            "player": game_state["player"].to_dict(),
            "orcs": [orc.to_dict() for orc in game_state["orcs"]],
            "round": game_state["round"],
            "score": game_state["score"],
            "game_over": game_state["game_over"],
        }
    )


@app.route("/api/attack", methods=["POST"])
def attack():
    if game_state["game_over"]:
        return jsonify({"result": "game_over"}), 400

    data = request.get_json()
    card_name = data["card_name"]
    orc_name = data["orc_name"]

    card = next((c for c in game_state["player"].deck if c.name == card_name), None)
    orc = next((o for o in game_state["orcs"] if o.name == orc_name), None)

    if card and orc:
        result = player_attack(game_state["player"], orc, card)

        if result == "orc_defeated":
            game_state["score"] += orc.points
            game_state["orcs"].remove(orc)

            if not game_state["orcs"]:
                game_state["round"] += 1
                game_state["player"].mana = 10
                game_state["orcs"] = generate_orcs(game_state["round"])

        game_state["game_over"] = check_game_over(
            game_state["player"], game_state["orcs"]
        )

        return jsonify(
            {
                "result": result,
                "player": game_state["player"].to_dict(),
                "orcs": [o.to_dict() for o in game_state["orcs"]],
                "round": game_state["round"],
                "score": game_state["score"],
                "game_over": game_state["game_over"],
            }
        )

    return jsonify({"result": "error"}), 400


@app.route("/api/restart", methods=["POST"])
def restart():
    """Rota para reiniciar o jogo."""
    global game_state
    game_state = initial_state()
    return jsonify({"result": "restarted"})


if __name__ == "__main__":
    app.run(debug=True)
