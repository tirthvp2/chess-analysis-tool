# app.py
from flask import Flask, render_template, request
from chess_analyzer import ChessAnalyzer
from ai_predictor import AIPredictor
import chess
import chess.svg
import numpy as np

app = Flask(__name__)

# Initialize the analyzer and predictor
stockfish_path = r"D:/StockFish/stockfish/stockfish-windows-x86-64-avx2.exe"
analyzer = ChessAnalyzer(stockfish_path)
predictor = AIPredictor()


@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    prediction = None
    board_svg = None
    fen = request.form.get("fen", chess.Board().fen())  # Default to starting position

    if request.method == "POST":
        # Set the position
        try:
            analyzer.set_position(fen)
            board = chess.Board(fen)
            board_svg = chess.svg.board(board, size=400)

            # Get Stockfish analysis
            evaluation = analyzer.get_evaluation()
            best_move = analyzer.get_best_move()
            top_moves = analyzer.get_top_moves(3)
            analysis = {
                "evaluation": evaluation,
                "best_move": best_move,
                "top_moves": top_moves
            }

            # Get AI prediction
            board_matrix = board_to_matrix(board)  # Use the same function as in generate_dataset.py
            outcome, probabilities = predictor.predict(board_matrix)
            prediction = {
                "outcome": outcome,
                "probabilities": {
                    "White Wins": probabilities[2],  # +1
                    "Draw": probabilities[1],        # 0
                    "Black Wins": probabilities[0]   # -1
                }
            }
        except Exception as e:
            analysis = {"error": str(e)}

    return render_template("index.html", fen=fen, analysis=analysis, prediction=prediction, board_svg=board_svg)


# Reuse the board_to_matrix function from generate_dataset.py
def board_to_matrix(board):
    board3d = np.zeros((14, 8, 8), dtype=np.int8)
    squares_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def square_to_index(square):
        letter = chess.square_name(square)
        return 8 - int(letter[1]), squares_index[letter[0]]

    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1

    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[13][i][j] = 1
    board.turn = aux
    return board3d


if __name__ == "__main__":
    app.run(debug=True)
