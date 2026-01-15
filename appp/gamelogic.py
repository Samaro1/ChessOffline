def create_initial_board():
    board = {}

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

    white_back_rank = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    black_back_rank = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']

    for rank in ranks:
        for i, file in enumerate(files):
            square = file + rank

            if rank == '2':
                board[square] = 'P'
            elif rank == '7':
                board[square] = 'p'
            elif rank == '1':
                board[square] = white_back_rank[i]
            elif rank == '8':
                board[square] = black_back_rank[i]
            else:
                board[square] = None

    return board


def print_board(board):
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

    print()
    for rank in ranks:
        row = []
        for file in files:
            piece = board[file + rank]
            row.append(piece if piece is not None else '.')
        print(rank, ' '.join(row))
    print("  a b c d e f g h\n")


def get_move(turn):
    if turn % 2 != 0:
        return input("User, Input your move?\n")
    else:
        return input("Bot/Admin, input your move?\n")


def parse_move(move):
    try:
        return move.split(" ")
    except ValueError:
        return None, None


def fetch_pieces(board, source_square, target_square):
    try:
        return board[source_square], board[target_square]
    except KeyError:
        return None, None


def validate_turn(src, turn):
    if turn % 2 != 0 and not src.isupper():
        return False
    if turn % 2 == 0 and not src.islower():
        return False
    return True


def capturing_own_piece(src, target):
    if src.isupper() and target is not None and target.isupper():
        return True
    if src.islower() and target is not None and target.islower():
        return True
    return False


def save_move(moves, source_square, target_square, src, target):
    one_move = {
        "from": source_square,
        "to": target_square,
        "moved": src,
        "captured": target
    }
    moves.append(one_move)


def apply_move(board, source_square, target_square, src):
    board[source_square] = None
    board[target_square] = src

def check_promotion(piece, target_square):
    if piece == 'P' and target_square.endswith('8'):
        return True
    if piece == 'p' and target_square.endswith('1'):
        return True
    return False

def get_promotion_piece(pawn):
    if pawn == 'P':
        valid = ['Q', 'R', 'B', 'N']
        default = 'Q'
    else:
        valid = ['q', 'r', 'b', 'n']
        default = 'q'

    choice = input("Promote pawn to (Q, R, B, N) [default Q]: ").strip()

    if choice == "":
        return default

    if choice in valid:
        return choice

    print("Invalid choice, defaulting to Queen")
    return default


def apply_promotion(board, target_square, promotion_piece):
    board[target_square] = promotion_piece

def validate_pawn_move(board, source_square, target_square, piece):
    # split the squares
    src_file = source_square[0]
    src_rank = int(source_square[1])
    tgt_file = target_square[0]
    tgt_rank = int(target_square[1])

    # differences
    file_diff = ord(tgt_file) - ord(src_file)  # +1 right, -1 left
    rank_diff = tgt_rank - src_rank            # +1 up (white), -1 down (black)

    if piece == 'P':  # White pawn
        # Forward 1
        if file_diff == 0 and rank_diff == 1 and board[target_square] is None:
            return True
        # Forward 2 from rank 2
        if file_diff == 0 and rank_diff == 2 and src_rank == 2:
            intermediate_square = src_file + str(src_rank + 1)
            if board[intermediate_square] is None and board[target_square] is None:
                return True
        # Diagonal capture
        if abs(file_diff) == 1 and rank_diff == 1:
            if board[target_square] is not None and board[target_square].islower():
                return True
        return False

    elif piece == 'p':  # Black pawn
        # Forward 1
        if file_diff == 0 and rank_diff == -1 and board[target_square] is None:
            return True
        # Forward 2 from rank 7
        if file_diff == 0 and rank_diff == -2 and src_rank == 7:
            intermediate_square = src_file + str(src_rank - 1)
            if board[intermediate_square] is None and board[target_square] is None:
                return True
        # Diagonal capture
        if abs(file_diff) == 1 and rank_diff == -1:
            if board[target_square] is not None and board[target_square].isupper():
                return True
        return False

def validate_knight_move(board, source_square, target_square, piece):
    # split the squares
    src_file = source_square[0]
    src_rank = int(source_square[1])
    tgt_file = target_square[0]
    tgt_rank = int(target_square[1])

    # differences
    file_diff = abs(ord(tgt_file) - ord(src_file))  # how many columns moved
    rank_diff = abs(tgt_rank - src_rank)           # how many rows moved

    # knight moves must be 2 + 1 positive or negative doesnt matter
    if (file_diff == 2 and rank_diff == 1) or (file_diff == 1 and rank_diff == 2):
        # check capturing own piece
        target = board[target_square]
        if target is None:
            return True
        if piece.isupper() and target.islower():
            return True
        if piece.islower() and target.isupper():
            return True
    return False

def validate_rook_move(board, source_square, target_square, piece):
    src_file = source_square[0]
    src_rank = int(source_square[1])
    tgt_file = target_square[0]
    tgt_rank = int(target_square[1])

    # differences
    file_diff = ord(tgt_file) - ord(src_file)
    rank_diff = tgt_rank - src_rank

    # Rook must move in a straight line
    if file_diff != 0 and rank_diff != 0:
        return False  # moving diagonally is illegal

    # Determine step direction
    step_file = 0
    step_rank = 0
    if file_diff != 0:
        step_file = 1 if file_diff > 0 else -1
    elif rank_diff != 0:
        step_rank = 1 if rank_diff > 0 else -1

    # Check each square along the path (excluding source and target)
    current_file = ord(src_file) + step_file
    current_rank = src_rank + step_rank

    while (current_file != ord(tgt_file) or current_rank != tgt_rank):
        square = chr(current_file) + str(current_rank)
        if board[square] is not None:
            return False  # path is blocked
        current_file += step_file
        current_rank += step_rank

    # Final square: either empty or opponent piece
    target = board[target_square]
    if target is None:
        return True
    if piece.isupper() and target.islower():
        return True
    if piece.islower() and target.isupper():
        return True

    # Cannot capture own piece
    return False

def validate_bishop_move(board, source_square, target_square, piece):
    # split the squares
    src_file = source_square[0]
    src_rank = int(source_square[1])
    tgt_file = target_square[0]
    tgt_rank = int(target_square[1])

    # differences
    file_diff = ord(tgt_file) - ord(src_file)
    rank_diff = tgt_rank - src_rank

    # Bishop must move diagonally
    if abs(file_diff) != abs(rank_diff):
        return False

    # Determine step direction (+1 or -1)
    step_file = 1 if file_diff > 0 else -1
    step_rank = 1 if rank_diff > 0 else -1

    # Start checking from first square after source
    current_file = ord(src_file) + step_file
    current_rank = src_rank + step_rank

    while current_file != ord(tgt_file) and current_rank != tgt_rank:
        square = chr(current_file) + str(current_rank)
        if board[square] is not None:
            return False  # path is blocked
        current_file += step_file
        current_rank += step_rank

    # Final square: empty or opponent piece
    target = board[target_square]
    if target is None:
        return True
    if piece.isupper() and target.islower():
        return True
    if piece.islower() and target.isupper():
        return True

    return False  # cannot capture own piece
def validate_queen_move(board, source_square, target_square, piece):
    src_file = source_square[0]
    src_rank = int(source_square[1])
    tgt_file = target_square[0]
    tgt_rank = int(target_square[1])

    # differences
    file_diff = ord(tgt_file) - ord(src_file)
    rank_diff = tgt_rank - src_rank

    # Check if it's a straight line (rook-like) or diagonal (bishop-like)
    if file_diff == 0 or rank_diff == 0:
        # straight line 
        step_file = 0 if file_diff == 0 else (1 if file_diff > 0 else -1)
        step_rank = 0 if rank_diff == 0 else (1 if rank_diff > 0 else -1)
    elif abs(file_diff) == abs(rank_diff):
        # diagonal 
        step_file = 1 if file_diff > 0 else -1
        step_rank = 1 if rank_diff > 0 else -1
    else:
        # not straight or diagonal → illegal
        return False

    # check path (all squares between source and target)
    current_file = ord(src_file) + step_file
    current_rank = src_rank + step_rank

    while current_file != ord(tgt_file) or current_rank != tgt_rank:
        square = chr(current_file) + str(current_rank)
        if board[square] is not None:
            return False  # path blocked
        current_file += step_file
        current_rank += step_rank

    # final square: empty or opponent piece
    target = board[target_square]
    if target is None:
        return True
    if piece.isupper() and target.islower():
        return True
    if piece.islower() and target.isupper():
        return True

    return False  # cannot capture own piece

def validate_king_move(board, source_square, target_square, piece):
    src_file = source_square[0]
    src_rank = int(source_square[1])
    tgt_file = target_square[0]
    tgt_rank = int(target_square[1])

    # differences
    file_diff = abs(ord(tgt_file) - ord(src_file))
    rank_diff = abs(tgt_rank - src_rank)

    # King can only move 1 square in any direction
    if file_diff > 1 or rank_diff > 1:
        return False

    # Cannot capture own piece
    target = board[target_square]
    if target is None:
        return True
    if piece.isupper() and target.islower():
        return True
    if piece.islower() and target.isupper():
        return True

    return False  # target is own piece

def validate_move(board, source, target, last_move):
    piece = board[source]
    if piece is None:
        return False

    # prevent capturing own piece
    target_piece = board[target]
    if target_piece is not None and piece.isupper() == target_piece.isupper():
        return False

    # ---- PAWN ----
    if piece in ('P', 'p'):
        # en passant has priority over normal pawn capture
        if validate_en_passant(board, source, target, last_move):
            return True
        return validate_pawn_move(board, source, target)

    # ---- KNIGHT ----
    if piece in ('N', 'n'):
        return validate_knight_move(source, target)

    # ---- BISHOP ----
    if piece in ('B', 'b'):
        return validate_bishop_move(board, source, target)

    # ---- ROOK ----
    if piece in ('R', 'r'):
        return validate_rook_move(board, source, target)

    # ---- QUEEN ----
    if piece in ('Q', 'q'):
        return validate_queen_move(board, source, target)

    # ---- KING ----
    if piece in ('K', 'k'):
        # castling checked before normal king move
        if validate_castling(board, source, target):
            return True
        return validate_king_move(source, target)

    return False


def validate_en_passant(board, source, target, last_move):
    if last_move is None:
        return False

    src_piece = board[source]
    if src_piece not in ('P', 'p'):
        return False

    src_file = source[0]
    src_rank = int(source[1])
    tgt_file = target[0]
    tgt_rank = int(target[1])

    last_from = last_move["from"]
    last_to = last_move["to"]
    last_piece = last_move["moved"]

    # last move must be a pawn moving two squares
    if last_piece not in ('P', 'p'):
        return False

    if abs(int(last_from[1]) - int(last_to[1])) != 2:
        return False

    # pawns must be adjacent
    if abs(ord(src_file) - ord(last_to[0])) != 1:
        return False

    # target square must be empty
    if board[target] is not None:
        return False

    # direction logic
    if src_piece == 'P':
        return (
            src_rank == 5 and
            tgt_rank == 6 and
            tgt_file == last_to[0]
        )

    if src_piece == 'p':
        return (
            src_rank == 4 and
            tgt_rank == 3 and
            tgt_file == last_to[0]
        )

    return False

def apply_en_passant(board, source, target):
    captured_square = target[0] + source[1]  # pawn has to be behind target
    board[target] = board[source]
    board[source] = None
    board[captured_square] = None

def validate_castling(board, source, target):
    piece = board[source]
    if piece not in ('K', 'k'):
        return False

    src_file = source[0]
    src_rank = source[1]
    tgt_file = target[0]
    tgt_rank = target[1]

    # king must stay on same rank
    if src_rank != tgt_rank:
        return False

    # king moves exactly two files
    if abs(ord(src_file) - ord(tgt_file)) != 2:
        return False

    # determine rook positions
    if tgt_file > src_file:  # king side
        rook_file = 'h'
        path_files = ['f', 'g']
    else:  # queen side
        rook_file = 'a'
        path_files = ['b', 'c', 'd']

    rook_square = rook_file + src_rank
    rook = board.get(rook_square)

    if rook is None:
        return False

    if piece.isupper() and rook != 'R':
        return False

    if piece.islower() and rook != 'r':
        return False

    # path must be empty
    for f in path_files:
        if board[f + src_rank] is not None:
            return False

    return True

def apply_castling(board, source, target):
    king = board[source]
    rank = source[1]

    if target[0] > source[0]:  # king side
        rook_from = 'h' + rank
        rook_to = 'f' + rank
    else:  # queen side
        rook_from = 'a' + rank
        rook_to = 'd' + rank

    board[target] = king
    board[source] = None
    board[rook_to] = board[rook_from]
    board[rook_from] = None


board = create_initial_board()
moves = []
game_on = True
turn = 'white'

while True:
    move = input("Enter move (e2 e4): ").split()
    if len(move) != 2:
        print("Invalid input format")
        continue

    source, target = move

    if source not in board or target not in board:
        print("Invalid square")
        continue

    piece = board[source]
    if piece is None:
        print("No piece on source square")
        continue

    if turn == 'white' and not piece.isupper():
        print("White to move")
        continue
    if turn == 'black' and not piece.islower():
        print("Black to move")
        continue

    if not validate_move(board, source, target):
        print("Illegal move")
        continue

    board[target] = board[source]
    board[source] = None

    # promotion hook

    turn = 'black' if turn == 'white' else 'white'
    print_board(board)

