from flask import Flask, render_template, jsonify, request
from models.player import Player
from game.logic import generate_orcs, player_attack
from models.orc import Orc

app = Flask(__name__)

# --- Estado do Jogo ---
player = Player("Jogador 1")
orcs = generate_orcs(1)  # Começa com orcs da rodada 1
game_state = {
    "player": player,
    "orcs": orcs,
    "round": 1,
    "score": 0,
}
# ----------------------


@app.route("/")
def game():
    return render_template("game.html")


@app.route("/api/state")
def state():
    # Usamos um dicionário separado para facilitar o envio como JSON
    return jsonify(
        {
            "player": game_state["player"].to_dict(),
            "orcs": [orc.to_dict() for orc in game_state["orcs"]],
            "round": game_state["round"],
            "score": game_state["score"],
        }
    )


@app.route("/api/attack", methods=["POST"])
def attack():
    data = request.get_json()
    card_name = data["card_name"]
    orc_name = data["orc_name"]

    card = next((c for c in game_state["player"].deck if c.name == card_name), None)
    # Procuramos o orc pelo nome E pela vida, para diferenciar orcs com o mesmo nome
    orc = next((o for o in game_state["orcs"] if o.name == orc_name), None)

    if card and orc:
        result = player_attack(game_state["player"], orc, card)

        if result == "orc_defeated":
            # Adiciona os pontos do orc à pontuação e o remove
            game_state["score"] += orc.points
            game_state["orcs"].remove(orc)

            # Se não houver mais orcs, avance para a próxima rodada
            if not game_state["orcs"]:
                game_state["round"] += 1
                game_state["player"].mana = 10  # Restaura a mana do jogador
                game_state["orcs"] = generate_orcs(game_state["round"])

        return jsonify(
            {
                "result": result,
                "player": game_state["player"].to_dict(),
                "orcs": [o.to_dict() for o in game_state["orcs"]],
                "round": game_state["round"],
                "score": game_state["score"],
            }
        )

    return jsonify({"result": "error"}), 400


if __name__ == "__main__":
    app.run(debug=True)
