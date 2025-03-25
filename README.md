# AI-Powered Chess Analysis Tool ♟️

![Chess Analysis Tool](https://img.shields.io/badge/Status-Ongoing-brightgreen)  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![Stockfish](https://img.shields.io/badge/Stockfish-16-orange)  
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-yellow)  
![Flask](https://img.shields.io/badge/Flask-2.x-green)

A powerful tool to analyze chess games, suggest optimal moves, and predict game outcomes using the Stockfish chess engine and a TensorFlow-based machine learning model. Whether you're a chess enthusiast looking to improve your game or a developer interested in AI and chess, this project offers a blend of traditional chess engine analysis with modern machine learning techniques.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview
The AI-Powered Chess Analysis Tool combines the strength of the Stockfish chess engine with a machine learning model to provide in-depth chess game analysis. Users can input a chess position (via FEN), get Stockfish’s evaluation and move suggestions, and see AI-predicted game outcomes (win, draw, or loss probabilities). The tool is accessible through a Flask-based web interface, making it easy to use for players of all levels.

This project was developed as part of my exploration into AI, web development, and system-level programming. It builds on my experience with web projects (like my GitHub Pages site at [tirthvp2.github.io](https://tirthvp2.github.io)) and my interest in low-level programming (e.g., OS development).

## Features
- **Stockfish Analysis**: Evaluate chess positions, get the best move, and see the top 3 move suggestions using the Stockfish engine.
- **AI Outcome Prediction**: Predict game outcomes (win, draw, loss) with a TensorFlow neural network trained on historical chess games.
- **Web Interface**: A user-friendly Flask-based web app to input positions and view analysis.
- **Customizable**: Easily extend the tool to analyze full games, add interactive chessboards, or improve the AI model.
- **Cross-Platform**: Works on Windows, macOS, and Linux with proper setup.

## Tech Stack
- **Python 3.8+**: Core language for scripting and integration.
- **Stockfish 16**: Chess engine for move evaluation and suggestions.
- **TensorFlow 2.x**: Machine learning framework for outcome prediction.
- **python-chess**: Library for chess logic (board representation, move generation).
- **Flask**: Lightweight web framework for the user interface.
- **scikit-learn & joblib**: For label encoding and persistence in the AI model.
- **NumPy & Pandas**: For data processing and model training.

## Installation
Follow these steps to set up the project locally.

### Prerequisites
- Python 3.8 or higher
- Stockfish binary (download from [stockfishchess.org](https://stockfishchess.org/download))
- Git (for cloning the repository)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tirthvp2/chess-analysis-tool.git
   cd chess-analysis-tool
2. **Set Up a Virtual Environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Download and Configure Stockfish**:
   - Download the Stockfish binary for your OS from stockfishchess.org.
   - Update the stockfish_path in app.py and chess_analyzer.py
   ```bash
   stockfish_path = r"C:\Users\YourUsername\stockfish\stockfish-windows-x86-64.exe"  # Windows
   # Or: stockfish_path = "/usr/bin/stockfish"  # Linux
5. **Prepare the Dataset (for AI training)**:
   - Download a PGN file of chess games (e.g., from Lichess: lichess_db_standard_rated_2021-07.pgn.bz2).
   ```bash
   python generate_dataset.py
6. **Train the AI Model**:
   ```bash
   python ai_predictor.py

## Usage
Follow these steps to access the web interface.
### Steps
1. **Run the Flask App**:
   ```bash
   python app.py
2. **Access the Web Interface**:
   Open your browser and go to http://127.0.0.1:5000.


## Contributing
Contributions are welcome! If you’d like to contribute:

1. Fork the repository.
2. Create a new branch (```git checkout -b feature/your-feature```).
3. Make your changes and commit (```git commit -m "Add your feature"```).
4. Push to your branch (```git push origin feature/your-feature```).
5. Open a Pull Request.

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

## License
This project is licensed under the MIT License. See the  file for details.

## Acknowledgements
- Stockfish Team: For providing a powerful open-source chess engine.
- Lichess: For the free PGN game databases used to train the AI model.
- TensorFlow and Flask Communities: For their excellent documentation and support.
- xAI’s Grok: For guidance in debugging and structuring this project.
