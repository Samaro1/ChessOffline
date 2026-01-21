from flask import Flask, request, jsonify
from gamelogic import (
    create_initial_board,
    initial_game_state,
    validate_move,
    apply_move,
    is_stalemate,
    check_checkmate
)
import uuid


app = Flask(__name__)

games = {}

board = create_initial_board()
state = initial_game_state()

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify({
        "board": board,
        "turn": state["turn"]
    })

@app.route("/game", methods=["POST"])
def create_game():
    game_id = str(uuid.uuid4())

    games[game_id] = {
        "board": create_initial_board(),
        "state": initial_game_state()
    }

    return jsonify({"game_id": game_id})


@app.route("/game/<game_id>", methods=["GET"])
def get_game_state(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    return jsonify({
        "board": game["board"],
        "turn": game["state"]["turn"]
    })

@app.route("/game/<game_id>/move", methods=["POST"])
def make_move(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    board = game["board"]
    state = game["state"]

    data = request.json
    src = data.get("from")
    tgt = data.get("to")

    if src not in board or tgt not in board:
        return jsonify({"error": "Invalid square"}), 400

    if not validate_move(board, src, tgt, state):
        return jsonify({"error": "Illegal move"}), 400

    apply_move(board, src, tgt, state)

    if check_checkmate(board, state):
        return jsonify({"status": "checkmate", "winner": state["turn"]})

    if is_stalemate(board, state):
        return jsonify({"status": "stalemate"})

    return jsonify({"status": "ok"})



if __name__ == "__main__":
    app.run(debug=True)
