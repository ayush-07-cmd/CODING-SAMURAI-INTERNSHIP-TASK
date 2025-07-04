from flask import Flask, render_template, request, jsonify
from minimax import best_move
from utils import check_winner

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data["board"]
    player = 1  # Human = X
    ai = 2      # AI = O

    winner = check_winner(board)
    if winner or all(cell != 0 for cell in board):
        return jsonify({"board": board, "status": "end", "winner": winner})

    ai_index = best_move(board, ai, player)
    if ai_index is not None:
        board[ai_index] = ai

    winner = check_winner(board)
    status = "end" if winner or all(cell != 0 for cell in board) else "continue"

    return jsonify({"board": board, "status": status, "winner": winner})

if __name__ == "__main__":
    app.run(debug=True)
