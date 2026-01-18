from gamelogic import (
    create_initial_board,
    validate_move,
    apply_move,
    apply_en_passant,
    apply_castling,
    find_king,
    is_square_attacked,
    initial_game_state
)

def assert_true(condition, message):
    if not condition:
        raise AssertionError("FAILED: " + message)

def assert_false(condition, message):
    if condition:
        raise AssertionError("FAILED: " + message)


def test_pawn_forward():
    board = create_initial_board()
    state = initial_game_state()

    assert validate_move(board, "e2", "e3", state)


def test_pawn_blocked():
    board = create_initial_board()
    board["e3"] = "N"
    assert_false(
        validate_move(board, "e2", "e3"),
        "Pawn cannot move into occupied square"
    )

def test_pawn_capture():
    board = create_initial_board()
    board["d3"] = "p"
    assert_true(
        validate_move(board, "e2", "d3"),
        "Pawn should capture diagonally"
    )

def test_knight_jump():
    board = create_initial_board()
    board["b1"] = "N"
    board["b2"] = "P"
    assert_true(
        validate_move(board, "b1", "c3"),
        "Knight must jump over pieces"
    )

def test_rook_blocked():
    board = create_initial_board()
    assert_false(
        validate_move(board, "a1", "a4"),
        "Rook cannot jump over pawn"
    )

def test_bishop_diagonal():
    board = create_initial_board()
    board["d2"] = None
    board["e3"] = None
    assert_true(
        validate_move(board, "c1", "f4"),
        "Bishop moves diagonally"
    )


def test_king_into_check():
    board = create_initial_board()
    board["e1"] = "K"
    board["e8"] = None
    board["e7"] = None
    board["e6"] = "r"

    assert_false(
        validate_move(board, "e1", "e2"),
        "King cannot move into check"
    )

def test_en_passant():
    board = create_initial_board()
    board.clear()
    board["e5"] = "P"
    board["d5"] = "p"

    last_move = {
        "from": "d7",
        "to": "d5",
        "moved": "p",
        "captured": None
    }

    assert_true(
        validate_move(board, "e5", "d6", last_move),
        "En passant should be allowed"
    )

def test_castling():
    board = create_initial_board()
    board["f1"] = None
    board["g1"] = None

    assert_true(
        validate_move(board, "e1", "g1"),
        "King side castling should be legal"
    )

def run_tests():
    test_pawn_forward()
    test_pawn_blocked()
    test_pawn_capture()
    test_knight_jump()
    test_rook_blocked()
    test_bishop_diagonal()
    test_king_into_check()
    test_en_passant()
    test_castling()
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    run_tests()

