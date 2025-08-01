from flask import Flask, render_template, jsonify, request
from models.player import Player
from game.logic import player_attack, advance_orcs
from models.orc import random_orc
import random

app = Flask(__name__)


def initial_state():
    """Função para gerar o estado inicial do jogo com o mapa."""
    player = Player("Jogador 1")
    game_map = {str(i): [[], [], []] for i in range(1, 7)}
    game_map["1"][0].append(random_orc(1))
    return {
        "player": player,
        "map": game_map,
        "round": 1,
        "score": 0,
        "game_over": False,
        "log": ["O jogo começou! Um orc apareceu na região 1."],
    }


# --- Estado do Jogo ---
game_state = initial_state()
# --------------------


@app.route("/")
def game():
    return render_template("game.html")


@app.route("/api/state")
def state():
    serialized_map = {
        lane: [[o.to_dict() for o in area] for area in areas]
        for lane, areas in game_state["map"].items()
    }
    return jsonify(
        {
            "player": game_state["player"].to_dict(),
            "map": serialized_map,
            "round": game_state["round"],
            "score": game_state["score"],
            "game_over": game_state["game_over"],
            "log": game_state["log"],
        }
    )


@app.route("/api/attack", methods=["POST"])
def attack():
    if game_state["game_over"]:
        return jsonify({"result": "game_over"}), 400

    data = request.get_json()
    card_name = data["card_name"]
    orc_id = data["orc_id"]
    lane = data["lane"]
    area = data["area"]

    card = next((c for c in game_state["player"].deck if c.name == card_name), None)
    orc_list = game_state["map"][lane][area]
    orc = next((o for o in orc_list if o.id == orc_id), None)

    if card and orc:
        result = player_attack(game_state["player"], orc, card)
        if result == "orc_defeated":
            game_state["score"] += orc.points
            orc_list.remove(orc)

        serialized_map = {
            lane_num: [[o.to_dict() for o in area_list] for area_list in areas]
            for lane_num, areas in game_state["map"].items()
        }
        return jsonify(
            {
                "result": result,
                "player": game_state["player"].to_dict(),
                "map": serialized_map,
                "round": game_state["round"],
                "score": game_state["score"],
                "game_over": game_state["game_over"],
                "log": game_state["log"],
            }
        )

    return jsonify({"result": "error"}), 400


@app.route("/api/end_turn", methods=["POST"])
def end_turn():
    if game_state["game_over"]:
        return jsonify({"result": "game_over"}), 400

    orcs_at_gate = advance_orcs(game_state["map"])
    if orcs_at_gate:
        game_state["log"].append(
            f"{len(orcs_at_gate)} orcs chegaram à torre! Fim de jogo!"
        )
        game_state["game_over"] = True

    game_state["round"] += 1
    lane_to_spawn = str(random.randint(1, 6))
    new_orc = random_orc(game_state["round"])
    game_state["map"][lane_to_spawn][0].append(new_orc)
    game_state["log"].append(
        f"Um novo {new_orc.name} apareceu na região {lane_to_spawn}."
    )
    game_state["player"].mana = 10

    serialized_map = {
        lane: [[o.to_dict() for o in area] for area in areas]
        for lane, areas in game_state["map"].items()
    }
    return jsonify(
        {
            "player": game_state["player"].to_dict(),
            "map": serialized_map,
            "round": game_state["round"],
            "score": game_state["score"],
            "game_over": game_state["game_over"],
            "log": game_state["log"],
        }
    )


@app.route("/api/restart", methods=["POST"])
def restart():
    """Rota para reiniciar o jogo."""
    global game_state
    game_state = initial_state()
    return jsonify({"result": "restarted"})


if __name__ == "__main__":
    app.run(debug=True)
