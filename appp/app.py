from flask import Flask, request, jsonify
from gamemanager import GameManager, validate_move,apply_move
from gamelogic import resolve_game_end

games= {}
app = Flask(__name__)
manager = GameManager()

@app.route("/game", methods=["POST"])
def create_game():
    result = manager.create_game()
    return jsonify(result)

@app.route("/game/<game_id>/join", methods=["POST"])
def join_game(game_id):
    result = manager.join_game(game_id)

    if result is None:
        return jsonify({"error": "Game not found"}), 404
    if result == "full":
        return jsonify({"error": "Game already full"}), 400

    return jsonify(result)

@app.route("/game/<game_id>", methods=["GET"])
def get_game(game_id):
    state = manager.get_game_state(game_id)
    if not state:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(state)

@app.route("/game/<game_id>/move", methods=["POST"])
def move(game_id):
    data = request.json
    player_id = data.get("player_id")
    src = data.get("from")
    tgt = data.get("to")

    result = manager.make_move(game_id, player_id, src, tgt)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result)

@app.route("/game/<game_id>/replay", methods=["GET"])
def game_replay(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    return jsonify({
        "moves": game["state"]["moves"],
        "result": game["state"].get("result", "ongoing")
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)


@app.route("/game/<game_id>/move", methods=["POST"])
def make_move(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    board = game["board"]
    state = game["state"]

    if state["game_over"]:
        return jsonify({"error": "Game already finished"}), 400

    data = request.json
    src = data.get("from")
    tgt = data.get("to")

    if not validate_move(board, src, tgt, state):
        return jsonify({"error": "Illegal move"}), 400

    apply_move(board, src, tgt, state)

    result = resolve_game_end(board, state)
    if result:
        return jsonify({
            "status": result,
            "turn": state["turn"]
        })

    return jsonify({
        "status": "ok",
        "turn": state["turn"]
    })
