from flask import Flask, request, jsonify
from gamemanager import GameManager

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

def has_insufficient_material(board):
    pieces = [p.lower() for p in board.values() if p]

    # Remove kings
    pieces = [p for p in pieces if p != "k"]

    if not pieces:
        return True  # K vs K

    if len(pieces) == 1 and pieces[0] in ("b", "n"):
        return True  # K+B vs K or K+N vs K

    return False
if __name__ == "__main__":
    app.run(debug=True, port=5001)