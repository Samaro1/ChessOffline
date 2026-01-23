import uuid
from gamelogic import (
    create_initial_board,
    initial_game_state,
    validate_move,
    apply_move,
    is_stalemate,
    check_checkmate
)

class GameManager:
    def __init__(self):
        self.games = {}

    def create_game(self):
        game_id = str(uuid.uuid4())
        white_id = str(uuid.uuid4())

        self.games[game_id] = {
            "board": create_initial_board(),
            "state": initial_game_state(),
            "white_id": white_id,
            "black_id": None
        }

        return {
            "game_id": game_id,
            "player_id": white_id,
            "color": "white"
        }

    def join_game(self, game_id):
        game = self.games.get(game_id)
        if not game:
            return None

        if game["black_id"] is not None:
            return "full"

        black_id = str(uuid.uuid4())
        game["black_id"] = black_id

        return {
            "game_id": game_id,
            "player_id": black_id,
            "color": "black"
        }

    def get_game_state(self, game_id):
        game = self.games.get(game_id)
        if not game:
            return None

        return {
            "board": game["board"],
            "turn": game["state"]["turn"],
            "white_connected": game["white_id"] is not None,
            "black_connected": game["black_id"] is not None
        }

    def make_move(self, game_id, player_id, src, tgt):
        game = self.games.get(game_id)
        if not game:
            return {"error": "Game not found"}, 404

        state = game["state"]
        board = game["board"]

        # Determine player color
        if player_id == game["white_id"]:
            player_color = "white"
        elif player_id == game["black_id"]:
            player_color = "black"
        else:
            return {"error": "Invalid player"}, 403

        # Enforce turn
        if state["turn"] != player_color:
            return {"error": "Not your turn"}, 403

        if src not in board or tgt not in board:
            return {"error": "Invalid square"}, 400

        if not validate_move(board, src, tgt, state):
            return {"error": "Illegal move"}, 400

        apply_move(board, src, tgt, state)

        if check_checkmate(board, state):
            return {
                "status": "checkmate",
                "winner": player_color
            }

        if is_stalemate(board, state):
            return {"status": "stalemate"}

        return {"status": "ok"}
