from board import print_board, make_move, is_full
from utils import check_winner
from minimax import best_move

def main():
    board = [0] * 9
    player, ai = 1, 2  # X is 1, O is 2
    turn = player  # Player goes first

    print("Tic Tac Toe — You are X (1), AI is O (2)")
    
    while True:
        print_board(board)
        if check_winner(board):
            winner = check_winner(board)
            print(f"Player {'X' if winner == 1 else 'O'} wins!")
            break
        if is_full(board):
            print("It's a tie!")
            break

        if turn == player:
            move = int(input("Enter your move (1-9): ")) - 1
            if not make_move(board, move, player):
                print("Invalid move. Try again.")
                continue
        else:
            move = best_move(board, ai, player)
            make_move(board, move, ai)
            print(f"AI chose position {move + 1}")

        turn = ai if turn == player else player

if __name__ == "__main__":
    main()
