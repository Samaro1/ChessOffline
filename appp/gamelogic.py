# =========================
# BOARD SETUP & RENDERING
# =========================

def create_initial_board():
    board = {}
    files = "abcdefgh"
    ranks = "12345678"

    white_back = "RNBQKBNR"
    black_back = "rnbqkbnr"

    for r in ranks:
        for i, f in enumerate(files):
            sq = f + r
            if r == "2":
                board[sq] = "P"
            elif r == "7":
                board[sq] = "p"
            elif r == "1":
                board[sq] = white_back[i]
            elif r == "8":
                board[sq] = black_back[i]
            else:
                board[sq] = None
    return board


def print_board(board):
    print()
    for r in "87654321":
        row = []
        for f in "abcdefgh":
            piece = board[f + r]
            row.append(piece if piece else ".")
        print(r, " ".join(row))
    print("  a b c d e f g h\n")


# =========================
# MOVE HISTORY / STATE
# =========================

def initial_game_state():
    return {
        "turn": "white",
        "moves": [],
        "king_moved": {"white": False, "black": False},
        "rook_moved": {
            "white": {"a": False, "h": False},
            "black": {"a": False, "h": False},
        }
    }


# =========================
# BASIC HELPERS
# =========================

def is_white(piece):
    return piece and piece.isupper()

def is_black(piece):
    return piece and piece.islower()

def opponent(color):
    return "black" if color == "white" else "white"


# =========================
# PIECE MOVE VALIDATION
# =========================

def validate_pawn(board, src, tgt, piece, last_move):
    sf, sr = src[0], int(src[1])
    tf, tr = tgt[0], int(tgt[1])
    df = ord(tf) - ord(sf)
    dr = tr - sr

    direction = 1 if piece == "P" else -1
    start_rank = 2 if piece == "P" else 7

    if df == 0:
        if dr == direction and board[tgt] is None:
            return True
        if sr == start_rank and dr == 2 * direction:
            mid = sf + str(sr + direction)
            if board[mid] is None and board[tgt] is None:
                return True

    if abs(df) == 1 and dr == direction:
        if board[tgt] and board[tgt].isupper() != piece.isupper():
            return True

        if last_move:
            last_from = last_move["from"]
            last_to = last_move["to"]
            last_piece = last_move["piece"]

            if last_piece.lower() == "p":
                if abs(int(last_from[1]) - int(last_to[1])) == 2:
                    if last_to[0] == tf and last_to[1] == src[1]:
                        return True

    return False


def validate_knight(src, tgt):
    df = abs(ord(src[0]) - ord(tgt[0]))
    dr = abs(int(src[1]) - int(tgt[1]))
    return (df, dr) in [(1, 2), (2, 1)]


def validate_slider(board, src, tgt, directions):
    sf, sr = src[0], int(src[1])
    tf, tr = tgt[0], int(tgt[1])

    for df, dr in directions:
        f = ord(sf) + df
        r = sr + dr
        while 0 < r <= 8 and ord("a") <= f <= ord("h"):
            sq = chr(f) + str(r)
            if sq == tgt:
                return True
            if board[sq] is not None:
                break
            f += df
            r += dr
    return False


def validate_king(src, tgt):
    df = abs(ord(src[0]) - ord(tgt[0]))
    dr = abs(int(src[1]) - int(tgt[1]))
    return df <= 1 and dr <= 1


# =========================
# CHECK / ATTACK LOGIC
# =========================

def find_king(board, color):
    target = "K" if color == "white" else "k"
    for sq, p in board.items():
        if p == target:
            return sq
    return None


def is_square_attacked(board, square, by_color, last_move):
    for src, piece in board.items():
        if piece is None:
            continue

        if by_color == "white" and not is_white(piece):
            continue
        if by_color == "black" and not is_black(piece):
            continue

        if piece.lower() == "p":
            if validate_pawn(board, src, square, piece, last_move):
                return True
        elif piece.lower() == "n":
            if validate_knight(src, square):
                return True
        elif piece.lower() == "b":
            if validate_slider(board, src, square, [(1,1),(-1,1),(1,-1),(-1,-1)]):
                return True
        elif piece.lower() == "r":
            if validate_slider(board, src, square, [(1,0),(-1,0),(0,1),(0,-1)]):
                return True
        elif piece.lower() == "q":
            if validate_slider(board, src, square, [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]):
                return True
        elif piece.lower() == "k":
            if validate_king(src, square):
                return True
    return False


def is_in_check(board, color, last_move):
    king_sq = find_king(board, color)
    return is_square_attacked(board, king_sq, opponent(color), last_move)


# =========================
# CASTLING
# =========================

def validate_castling(board, src, tgt, color, state, last_move):
    if state["king_moved"][color]:
        return False

    rank = "1" if color == "white" else "8"

    if src != "e" + rank:
        return False

    if tgt == "g" + rank:
        rook_file = "h"
        path = ["f", "g"]
    elif tgt == "c" + rank:
        rook_file = "a"
        path = ["d", "c", "b"]
    else:
        return False

    if state["rook_moved"][color][rook_file]:
        return False

    for f in path:
        if board[f + rank] is not None:
            return False

    for f in ["e"] + path:
        if is_square_attacked(board, f + rank, opponent(color), last_move):
            return False

    return True


def apply_castling(board, src, tgt):
    rank = src[1]
    if tgt[0] == "g":
        board["f" + rank] = board["h" + rank]
        board["h" + rank] = None
    else:
        board["d" + rank] = board["a" + rank]
        board["a" + rank] = None

    board[tgt] = board[src]
    board[src] = None


# =========================
# MAIN MOVE VALIDATION
# =========================

def validate_move(board, src, tgt, state):
    piece = board[src]
    if piece is None:
        return False

    color = "white" if is_white(piece) else "black"
    last_move = state["moves"][-1] if state["moves"] else None

    if board[tgt] and board[tgt].isupper() == piece.isupper():
        return False

    if piece.lower() == "p":
        valid = validate_pawn(board, src, tgt, piece, last_move)
    elif piece.lower() == "n":
        valid = validate_knight(src, tgt)
    elif piece.lower() == "b":
        valid = validate_slider(board, src, tgt, [(1,1),(-1,1),(1,-1),(-1,-1)])
    elif piece.lower() == "r":
        valid = validate_slider(board, src, tgt, [(1,0),(-1,0),(0,1),(0,-1)])
    elif piece.lower() == "q":
        valid = validate_slider(board, src, tgt, [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)])
    elif piece.lower() == "k":
        if validate_castling(board, src, tgt, color, state, last_move):
            return True
        valid = validate_king(src, tgt)
    else:
        return False

    if not valid:
        return False

    snapshot = board.copy()
    board[tgt] = board[src]
    board[src] = None

    illegal = is_in_check(board, color, last_move)
    board.update(snapshot)

    return not illegal


# =========================
# APPLY EN PASSANR
# =========================
def apply_en_passant(board, src, tgt, piece):
    """
    Removes the pawn captured via en passant.
    """
    direction = 1 if piece == "P" else -1
    captured_rank = int(tgt[1]) - direction
    captured_square = tgt[0] + str(captured_rank)

    board[captured_square] = None

# =========================
# APPLY MOVE
# =========================

def apply_move(board, src, tgt, state):
    piece = board[src]
    color = "white" if is_white(piece) else "black"

    if piece.lower() == "k" and abs(ord(src[0]) - ord(tgt[0])) == 2:
        apply_castling(board, src, tgt)
        state["king_moved"][color] = True
    else:
        board[tgt] = board[src]
        board[src] = None

    if piece.lower() == "k":
        state["king_moved"][color] = True
    if piece.lower() == "r":
        state["rook_moved"][color][src[0]] = True

    state["moves"].append({
        "from": src,
        "to": tgt,
        "piece": piece
    })

    state["turn"] = opponent(state["turn"])


# =========================
# GAME LOOP (CLI)
# =========================

def run_cli():
    board = create_initial_board()
    state = initial_game_state()

    while True:
        print_board(board)
        move = input(f"{state['turn']} move (e2 e4): ").split()

        if len(move) != 2:
            print("Invalid input format")
            continue

        src, tgt = move
        if src not in board or tgt not in board:
            print("Invalid square")
            continue

        piece = board[src]
        if piece is None:
            print("No piece on source square")
            continue

        if state["turn"] == "white" and not is_white(piece):
            print("White to move")
            continue
        if state["turn"] == "black" and not is_black(piece):
            print("Black to move")
            continue

        if not validate_move(board, src, tgt, state):
            print("Illegal move")
            continue

        apply_move(board, src, tgt, state)


if __name__ == "__main__":
    run_cli()
