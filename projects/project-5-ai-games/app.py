import random
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "replace-this-with-an-environment-secret"

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return "draw" if all(board) else None


def minimax(board, maximizing):
    result = winner(board)
    if result == "O":
        return 1
    if result == "X":
        return -1
    if result == "draw":
        return 0

    scores = []
    mark = "O" if maximizing else "X"
    for i, cell in enumerate(board):
        if cell:
            continue
        board[i] = mark
        scores.append(minimax(board, not maximizing))
        board[i] = ""
    return max(scores) if maximizing else min(scores)


def computer_move(board):
    choices = []
    best = -2
    for i, cell in enumerate(board):
        if cell:
            continue
        board[i] = "O"
        score = minimax(board, False)
        board[i] = ""
        if score > best:
            best = score
            choices = [i]
        elif score == best:
            choices.append(i)
    return random.choice(choices) if choices else None


def commentary(result):
    messages = {
        "X": ["Nice line — you got me.", "Clean win. Well played."],
        "O": ["The computer found the opening.", "That board was mine this round."],
        "draw": ["No winner this time.", "Perfectly balanced board."],
        None: ["Your move.", "Think two moves ahead."],
    }
    return random.choice(messages[result])


@app.post("/new")
def new_game():
    session["board"] = [""] * 9
    return jsonify(board=session["board"], message="New game started")


@app.post("/move")
def move():
    board = session.get("board", [""] * 9)
    payload = request.get_json(silent=True) or {}
    index = payload.get("index")
    if not isinstance(index, int) or index not in range(9) or board[index]:
        return jsonify(error="Invalid move"), 400
    if winner(board):
        return jsonify(error="Game is already over"), 400

    board[index] = "X"
    result = winner(board)
    if not result:
        ai_index = computer_move(board)
        if ai_index is not None:
            board[ai_index] = "O"
        result = winner(board)

    session["board"] = board
    return jsonify(board=board, winner=result, message=commentary(result))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
