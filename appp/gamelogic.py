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
