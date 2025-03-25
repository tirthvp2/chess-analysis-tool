import chess
import chess.engine
from stockfish import Stockfish


class ChessAnalyzer:
    def __init__(self, stockfish_path):
        # Initialize Stockfish with the path to the binary
        self.stockfish = Stockfish(path=stockfish_path)
        # Set Stockfish parameters for better performance
        self.stockfish.update_engine_parameters({
            "Threads": 2,  # Adjust based on your CPU
            "Hash": 2048,  # 2GB hash table
            "Minimum Thinking Time": 30
        })
        self.board = chess.Board()

    def set_position(self, fen=None):
        """Set the board to a specific position using FEN, or reset to initial position."""
        if fen:
            self.board.set_fen(fen)
            self.stockfish.set_fen_position(fen)
        else:
            self.board.reset()
            self.stockfish.set_fen_position(self.board.fen())

    def get_evaluation(self, depth=18):
        """Get Stockfish's evaluation of the current position."""
        self.stockfish.set_fen_position(self.board.fen())
        evaluation = self.stockfish.get_evaluation()
        return evaluation

    def get_best_move(self):
        """Get the best move suggested by Stockfish."""
        self.stockfish.set_fen_position(self.board.fen())
        best_move = self.stockfish.get_best_move()
        return best_move

    def get_top_moves(self, num_moves=3):
        """Get the top N moves suggested by Stockfish."""
        self.stockfish.set_fen_position(self.board.fen())
        top_moves = self.stockfish.get_top_moves(num_moves)
        return top_moves

    def analyze_game(self, pgn):
        """Analyze a full game given in PGN format."""
        import chess.pgn
        import io

        pgn = io.StringIO(pgn)
        game = chess.pgn.read_game(pgn)
        self.board.reset()
        analysis = []

        for move in game.mainline_moves():
            self.board.push(move)
            eval = self.get_evaluation()
            best_move = self.get_best_move()
            analysis.append({
                "move": str(move),
                "evaluation": eval,
                "best_move": best_move
            })
        return analysis
