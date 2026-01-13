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
board= create_initial_board()
game_on= True
while game_on:
    if turn % 2 != 0:
        move= input("User, Input your move?\n")
        source_square, target_square= move.split(sep=" ")
        try:
            board[source_square] and board[target_square]
        except KeyError:
            print("Invalid source square and or target square")
            pass
        if board[source_square] == None:
            print("Invalid source square or move from ")
            pass
        else:
            item = board[source_square]
            board[source_square]= None
            board[target_square]= item
            turn += 1

    else:
        move = input("Bot/Admin, input your move?\n")
        source_square, target_square= move.split(sep=" ")
        try:
            board[source_square] and board[target_square]
        except KeyError:
            print("Invalid source square and or target square")
            pass
        if board[source_square] == None:
            print("Invalid source square or move from ")
            pass
        else:
            item = board[source_square]
            board[source_square]= None
            board[target_square]= item
            turn += 1 
    print(board)
    