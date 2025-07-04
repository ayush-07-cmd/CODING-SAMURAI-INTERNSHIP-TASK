def check_winner(board):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for line in wins:
        if board[line[0]] == board[line[1]] == board[line[2]] != 0:
            return board[line[0]]
    return None
