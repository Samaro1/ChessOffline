from gamelogic import (
    create_initial_board,
    validate_move,
    apply_move,
    find_king,
    is_square_attacked,
    initial_game_state
)

# =========================
# ASSERT HELPERS
# =========================

def assert_true(condition, message):
    if not condition:
        raise AssertionError("FAILED: " + message)

def assert_false(condition, message):
    if condition:
        raise AssertionError("FAILED: " + message)


# =========================
# PAWN TESTS
# =========================

def test_pawn_forward():
    board = create_initial_board()
    state = initial_game_state()

    assert_true(
        validate_move(board, "e2", "e3", state),
        "Pawn should move forward one square"
    )


def test_pawn_blocked():
    board = create_initial_board()
    state = initial_game_state()

    board["e3"] = "N"

    assert_false(
        validate_move(board, "e2", "e3", state),
        "Pawn cannot move into occupied square"
    )


def test_pawn_capture():
    board = create_initial_board()
    state = initial_game_state()

    board["d3"] = "p"

    assert_true(
        validate_move(board, "e2", "d3", state),
        "Pawn should capture diagonally"
    )


# =========================
# KNIGHT / SLIDERS
# =========================

def test_knight_jump():
    board = create_initial_board()
    state = initial_game_state()

    board["b2"] = "P"  # blocking square

    assert_true(
        validate_move(board, "b1", "c3", state),
        "Knight must jump over pieces"
    )


def test_rook_blocked():
    board = create_initial_board()
    state = initial_game_state()

    assert_false(
        validate_move(board, "a1", "a4", state),
        "Rook cannot jump over pawn"
    )


def test_bishop_diagonal():
    board = create_initial_board()
    state = initial_game_state()

    board["d2"] = None
    board["e3"] = None

    assert_true(
        validate_move(board, "c1", "f4", state),
        "Bishop moves diagonally"
    )


# =========================
# KING / CHECK
# =========================

def test_king_into_check():
    board = create_initial_board()
    state = initial_game_state()

    board = {}
    for f in "abcdefgh":
        for r in "12345678":
            board[f + r] = None

    board["e1"] = "K"
    board["e6"] = "r"

    assert_false(
        validate_move(board, "e1", "e2", state),
        "King cannot move into check"
    )


# =========================
# EN PASSANT
# =========================

def test_en_passant():
    board = {}
    for f in "abcdefgh":
        for r in "12345678":
            board[f + r] = None

    # kings MUST exist
    board["e1"] = "K"
    board["e8"] = "k"

    # pawns
    board["e5"] = "P"
    board["d5"] = "p"

    state = initial_game_state()
    state["moves"].append({
        "from": "d7",
        "to": "d5",
        "piece": "p"
    })

    assert_true(
        validate_move(board, "e5", "d6", state),
        "En passant should be allowed"
    )



# =========================
# CASTLING
# =========================

def test_castling():
    board = create_initial_board()
    state = initial_game_state()

    board["f1"] = None
    board["g1"] = None

    assert_true(
        validate_move(board, "e1", "g1", state),
        "King-side castling should be legal"
    )


# =========================
# RUNNER
# =========================

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