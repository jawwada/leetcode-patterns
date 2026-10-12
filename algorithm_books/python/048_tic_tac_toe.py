"""
Design Tic-Tac-Toe - Row, Column and Diagonal Counters

Two players alternate valid moves on an n x n board; move(row, col, player)
returns the player who has just filled a whole row, column or diagonal, or 0.
n = 3, moves (0,0,1) (0,2,2) (2,2,1) (1,1,2) (2,0,1) (1,0,2) (2,1,1)
-> 0 0 0 0 0 0 1.
"""


# --- algorithm ---
class TicTacToe:
    """One signed counter per row, per column and per long diagonal."""

    def __init__(self, n):
        self.n = n
        self.rows = [0] * n             # player 1 adds +1, player 2 adds -1
        self.cols = [0] * n
        self.diagonal = 0               # cells with row == col
        self.anti_diagonal = 0          # cells with row + col == n - 1

    def move(self, row, col, player):
        """Add the player's sign to each line through the cell; a counter at
        n or -n means a line full of that player's marks. O(1)."""
        sign = 1
        if player == 2:
            sign = -1
        self.rows[row] += sign
        self.cols[col] += sign
        if row == col:
            self.diagonal += sign
        if row + col == self.n - 1:     # not elif: the center is on both
            self.anti_diagonal += sign
        if abs(self.rows[row]) == self.n or abs(self.cols[col]) == self.n:
            return player
        if abs(self.diagonal) == self.n or abs(self.anti_diagonal) == self.n:
            return player
        return 0


# --- try it ---
game = TicTacToe(3)
moves = [(0, 0, 1), (0, 2, 2), (2, 2, 1), (1, 1, 2), (2, 0, 1), (1, 0, 2)]
results = []
for row, col, player in moves:
    results.append(game.move(row, col, player))
print(results)                              # -> [0, 0, 0, 0, 0, 0]
print(game.move(2, 1, 1))                   # -> 1
print(game.rows, game.cols)                 # -> [0, -2, 3] [1, 0, 0]
print(game.diagonal, game.anti_diagonal)    # -> 1 -1
game = TicTacToe(3)
for row, col, player in [(0, 0, 1), (0, 2, 2), (2, 2, 1), (1, 1, 2), (1, 0, 1)]:
    game.move(row, col, player)
print(game.move(2, 0, 2), game.anti_diagonal)   # -> 2 -3
print(TicTacToe(1).move(0, 0, 2))               # -> 2
