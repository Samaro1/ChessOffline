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

turn = 1
board = create_initial_board()
moves = []
game_on = True

while game_on:

    move = get_move(turn)

    source_square, target_square = parse_move(move)
    if not source_square or not target_square:
        print("Not enough values to unpack")
        continue

    src, target = fetch_pieces(board, source_square, target_square)
    if src is None and target is None:
        print("Invalid source square and or target square")
        continue

    if src is None:
        print("Invalid source square or move from")
        continue

    if not validate_turn(src, turn):
        print("You dont have the authority to move this piece")
        continue

    if capturing_own_piece(src, target):
        print("Your piece already exists here")
        continue

    # save move state before mutation
    save_move(moves, source_square, target_square, src, target)

    # apply move
    apply_move(board, source_square, target_square, src)

    # promotion hook will be here
    if check_promotion(src, target_square):
    # ask user what to promote to
        piece = get_promotion_piece(src)
    # replace board[target_square]
        apply_promotion(board,target_square,piece)
    turn += 1
