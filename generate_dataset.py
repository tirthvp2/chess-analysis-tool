# generate_dataset.py
import chess
import chess.pgn
import numpy as np
import pandas as pd
from stockfish import Stockfish


def board_to_matrix(board):
    """Convert a chess board to a 3D matrix (8x8x14) for the neural network."""
    board3d = np.zeros((14, 8, 8), dtype=np.int8)
    squares_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def square_to_index(square):
        letter = chess.square_name(square)
        return 8 - int(letter[1]), squares_index[letter[0]]

    # Pieces (1-6 for White, 7-12 for Black)
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1

    # Legal moves for White and Black (channels 13 and 14)
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


def generate_dataset(pgn_file, stockfish_path, num_games=1000):
    stockfish = Stockfish(path=stockfish_path)
    stockfish.set_depth(10)  # Faster evaluation

    positions = []
    outcomes = []  # 1: White wins, 0: Draw, -1: Black wins

    with open(pgn_file, 'r', encoding='utf-8') as f:
        for _ in range(num_games):
            game = chess.pgn.read_game(f)
            if game is None:
                break

            # Get game outcome
            result = game.headers.get("Result", "*")
            if result == "1-0":
                outcome = 1
            elif result == "0-1":
                outcome = -1
            elif result == "1/2-1/2":
                outcome = 0
            else:
                continue  # Skip games with no result

            # Play through the game and collect positions
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
                # Use Stockfish to evaluate the position
                stockfish.set_fen_position(board.fen())
                eval = stockfish.get_evaluation()
                if eval["type"] == "cp":
                    score = eval["value"]
                    # Skip extreme scores (e.g., checkmate)
                    if abs(score) > 1000:
                        continue
                else:
                    continue

                # Convert board to matrix
                matrix = board_to_matrix(board)
                positions.append(matrix.flatten())  # Flatten for the neural network
                outcomes.append(outcome)

    # Save to a CSV file
    df = pd.DataFrame(positions)
    df["outcome"] = outcomes
    df.to_csv("data/chess_dataset.csv", index=False)
    print(f"Generated dataset with {len(positions)} positions.")


if __name__ == "__main__":
    stockfish_path = r"D:/StockFish/stockfish/stockfish-windows-x86-64-avx2.exe"
    pgn_file = r"D:/Chess Analysis Tool/chess-analysis-tool/data/games.pgn"
    generate_dataset(pgn_file, stockfish_path, num_games=1000)
