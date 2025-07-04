def print_board(board):
    symbols = [' ', 'X', 'O']
    for i in range(3):
        row = [symbols[board[j]] for j in range(i*3, i*3 + 3)]
        print('|'.join(row))
        if i < 2:
            print("-----")


def is_full(board):
    return all(cell != 0 for cell in board)


def make_move(board, index, player):
    if board[index] == 0:
        board[index] = player
        return True
    return False
