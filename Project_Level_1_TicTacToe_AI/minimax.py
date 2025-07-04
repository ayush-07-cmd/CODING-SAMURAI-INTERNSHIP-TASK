from utils import check_winner
from board import is_full

def minimax(board, is_maximizing, ai, human):
    winner = check_winner(board)
    if winner == ai:
        return 1
    elif winner == human:
        return -1
    elif is_full(board):
        return 0

    best = -float('inf') if is_maximizing else float('inf')
    for i in range(9):
        if board[i] == 0:
            board[i] = ai if is_maximizing else human
            score = minimax(board, not is_maximizing, ai, human)
            board[i] = 0
            best = max(best, score) if is_maximizing else min(best, score)
    return best

def best_move(board, ai, human):
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == 0:
            board[i] = ai
            score = minimax(board, False, ai, human)
            board[i] = 0
            if score > best_score:
                best_score = score
                move = i
    return move
