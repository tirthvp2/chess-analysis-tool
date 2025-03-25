# test_analyzer.py
from chess_analyzer import ChessAnalyzer

# Replace with your Stockfish path
stockfish_path = r"D:/StockFish/stockfish/stockfish-windows-x86-64-avx2.exe"  # e.g., "/usr/bin/stockfish" on Linux
analyzer = ChessAnalyzer(stockfish_path)

# Test with the starting position
analyzer.set_position()
print("Evaluation:", analyzer.get_evaluation())
print("Best Move:", analyzer.get_best_move())
print("Top 3 Moves:", analyzer.get_top_moves(3))

# Test with a specific position (Scholar's Mate)
#fen = "rnbqkbnr/pppp1ppp/5n2/5p2/5P2/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 2"
fen = "1k3r2/ppp3pp/1b1p4/4p3/4P3/8/P2N1r1P/6K1 b - - 3 25"
analyzer.set_position(fen)
#print("\nScholar's Mate Position:")
print("Evaluation:", analyzer.get_evaluation())
print("Best Move:", analyzer.get_best_move())
print("Top 3 Moves:", analyzer.get_top_moves(3))
