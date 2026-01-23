from flask import Flask, request, jsonify
from gamemanager import GameManager

app = Flask(__name__)
manager = GameManager()

@app.route("/game", methods=["POST"])
def create_game():
    game_id = manager.create_game()
    return jsonify({"game_id": game_id})

@app.route("/game/<game_id>", methods=["GET"])
def get_game(game_id):
    state = manager.get_game_state(game_id)
    if not state:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(state)

@app.route("/game/<game_id>/move", methods=["POST"])
def move(game_id):
    data = request.json
    src = data.get("from")
    tgt = data.get("to")

    result = manager.make_move(game_id, src, tgt)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
