# import chess.engine
# import chess

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


turn = 1
board = create_initial_board()
moves = []
game_on = True

while game_on:

    if turn % 2 != 0:
        move = input("User, Input your move?\n")
    else:
        move = input("Bot/Admin, input your move?\n")

    try:
        source_square, target_square = move.split(" ")
    except ValueError:
        print("Not enough values to unpack")
        continue

    try:
        src = board[source_square]
        target = board[target_square]
    except KeyError:
        print("Invalid source square and or target square")
        continue

    if src is None:
        print("Invalid source square or move from")
        continue

    if turn % 2 != 0 and not src.isupper():
        print("You dont have the authority to move this piece")
        continue

    if turn % 2 == 0 and not src.islower():
        print("You dont have the authority to move this piece")
        continue

    # save move state before board mutation 
    one_move = {
        "from": source_square,
        "to": target_square,
        "moved": src,
        "captured": target
    }
    moves.append(one_move)

    # ---- apply move ----
    board[source_square] = None
    board[target_square] = src

    turn += 1
