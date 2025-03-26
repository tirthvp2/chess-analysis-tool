# test_analyzer.py
from chess_analyzer import ChessAnalyzer

# Replace with your Stockfish path
stockfish_path = r"D:/StockFish/stockfish/stockfish-windows-x86-64-avx2.exe"  # e.g., "/usr/bin/stockfish" on Linux
analyzer = ChessAnalyzer(stockfish_path)

# Test with the starting position
fen = "2k3rr/p1b5/Pp1qp3/1Pp2pp1/3P3p/2PQP1P1/3B1K1P/4RR2 w - - 0 26"
analyzer.set_position(fen)

print("Evaluation:", analyzer.get_evaluation())
print("Best Move:", analyzer.get_best_move())
print("Top 3 Moves:", analyzer.get_top_moves(3))
print("\n")

# Test with a specific position
fen = "1k3r2/ppp3pp/1b1p4/4p3/4P3/8/P2N1r1P/6K1 b - - 3 25"
analyzer.set_position(fen)

print("Evaluation:", analyzer.get_evaluation())
print("Best Move:", analyzer.get_best_move())
print("Top 3 Moves:", analyzer.get_top_moves(3))
