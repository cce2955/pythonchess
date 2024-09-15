# Python Chess Game

![Chess Board](https://github.com/user-attachments/assets/3e026986-4c47-4dbc-a0c8-4e4d947c04fc))


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

Welcome to the **Python Chess Game**! This project is a fully functional chess game implemented in Python, adhering to standard chess rules, including special moves like castling, en passant, and pawn promotion. Designed with a modular architecture, the game is both maintainable and extensible, making it an excellent learning tool for Python enthusiasts and chess aficionados alike.

## Features

- **Comprehensive Piece Movements:** Implements all standard chess pieces (`Pawn`, `Knight`, `Bishop`, `Rook`, `Queen`, `King`) with their unique movement rules.
- **Special Moves:** Supports castling, en passant captures, and pawn promotion.
- **Game States:** Detects and handles check, checkmate, and stalemate conditions.
- **User Interaction:** Interactive command-line interface allowing players to input moves using algebraic notation (e.g., `e2`, `e4`).
- **Unit Testing:** Extensive test suite using Python's `unittest` framework to ensure the reliability and correctness of game mechanics.

## Installation

### Prerequisites

- **Python 3.6+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/python-chess-game.git
    cd python-chess-game
    ```

2. **Create a Virtual Environment:**

    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv .venv
    ```

3. **Activate the Virtual Environment:**

    - **Windows:**

        ```bash
        .venv\Scripts\activate
        ```

    - **macOS/Linux:**

        ```bash
        source .venv/bin/activate
        ```

4. **Dependencies:**

    None, uses standard python library

## Usage

To start the chess game, run the `game.py` script:

```bash
python game.py
```
How to Play
Selecting a Piece:

Enter the position of the piece you want to move using algebraic notation (e.g., e2).
Selecting a Destination:

After selecting a piece, a list of possible moves will be displayed.
Enter the desired destination position (e.g., e4).
Special Commands:

Quit the Game: Type quit at any prompt to exit the game.
Pawn Promotion:

When a pawn reaches the opposite end of the board, you will be prompted to choose a piece for promotion (Q for Queen, R for Rook, B for Bishop, N for Knight).
Example Gameplay
```bash
  a b c d e f g h
8 r n b q k b n r 8
7 p p p p p p p p 7
6                 6
5                 5
4                 4
3                 3
2 P P P P P P P P 2
1 R N B Q K B N R 1
  a b c d e f g h
white's turn
Enter the position of the piece to move (e.g., 'e2'): a2
Possible moves: a3, a4
Enter the position to move to (e.g., 'e4'): a4
  a b c d e f g h
8 r n b q k b n r 8
7 p p p p p p p p 7
6                 6
5                 5
4 P               4
3                 3
2   P P P P P P P 2
1 R N B Q K B N R 1
  a b c d e f g h
black's turn
Enter the position of the piece to move (e.g., 'e2'): e8
No legal moves available for this piece. Please choose another piece.
  a b c d e f g h
8 r n b q k b n r 8
7 p p p p p p p p 7
6                 6
5                 5
4 P               4
3                 3
2   P P P P P P P 2
1 R N B Q K B N R 1
  a b c d e f g h
black's turn
Enter the position of the piece to move (e.g., 'e2'): g8
Possible moves: f6, h6
Enter the position to move to (e.g., 'e4'): h6
  a b c d e f g h
8 r n b q k b   r 8
7 p p p p p p p p 7
6               n 6
5                 5
4 P               4
3                 3
2   P P P P P P P 2
1 R N B Q K B N R 1
  a b c d e f g h
white's turn
Enter the position of the piece to move (e.g., 'e2'):```
