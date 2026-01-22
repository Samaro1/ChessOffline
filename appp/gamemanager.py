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
        self.games = {}  # game_id to game_data

    def create_game(self):
        game_id = str(uuid.uuid4())
        self.games[game_id] = {
            "board": create_initial_board(),
            "state": initial_game_state()
        }
        return game_id

    def get_game(self, game_id):
        return self.games.get(game_id)

    def make_move(self, game_id, src, tgt):
        game = self.get_game(game_id)
        if not game:
            return {"error": "game_not_found"}

        board = game["board"]
        state = game["state"]

        if not validate_move(board, src, tgt, state):
            return {"error": "illegal_move"}

        apply_move(board, src, tgt, state)

        # endgame checks
        if check_checkmate(board, state):
            state["status"] = "checkmate"
        elif is_stalemate(board, state):
            state["status"] = "stalemate"

        return {"ok": True}
