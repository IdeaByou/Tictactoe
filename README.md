# Tictactoe
Tic-Tac-Toe Game with Minimax Algorithm

Tic-Tac-Toe Game with Minimax Algorithm
Overview
This program is a Python implementation of Tic-Tac-Toe, where a human player competes against an AI using the minimax algorithm. The minimax algorithm allows the AI to play optimally by evaluating the best possible moves for itself and the player. The game runs in a console-based interface where the user can input moves, and the AI responds in turn.

Key Components

Game Board Representation:
The board is represented as a 3x3 grid, typically a list of lists or a one-dimensional list with 9 slots. Each cell may contain an "X", "O", or be empty (usually represented as a space or underscore). "X" represents the human player, and "O" represents the AI.

Player Turn Logic:

The program alternates turns between the player and the AI.
The player chooses an empty cell to place their symbol.
The AI uses the minimax algorithm to determine the best cell to place its symbol.
Minimax Algorithm:

The minimax function evaluates every possible game outcome from the current board state.
Each move is assigned a score based on whether it leads to a win, loss, or draw for the AI.
The algorithm explores all possible moves to either maximize the AI's score or minimize the player’s score.
It returns the optimal move for the AI, ensuring that it cannot lose if it plays perfectly.
Win Condition Check:

After each move, the program checks if there’s a winning line (horizontal, vertical, or diagonal) for either player or if the game has resulted in a draw.
If a win or draw is detected, the game announces the result and ends.
Human-AI Interaction:

The game prompts the human player to select a move.
The AI responds with an optimal move based on the current board state.
