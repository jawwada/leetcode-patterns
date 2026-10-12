---
rank: 48
slug: tic_tac_toe
---

Design the referee for tic-tac-toe on an n × n board. Two players alternate valid moves on empty cells, and `move(row, col, player)` returns the player who has just filled a whole row, column or diagonal with their marks, or 0 if nobody has. On a 3 × 3 board the moves (0, 0) by player 1, (0, 2) by 2, (2, 2) by 1, (1, 1) by 2, (2, 0) by 1 and (1, 0) by 2 return 0, and the seventh, player 1 at (2, 1), returns 1: the bottom row is full of X.

The brute force stores the board and after each move scans the new mark's row, column and diagonals, `O(n)` per move and `O(n²)` memory. But a line wins only when all n of its cells hold one player's mark, and that question fits in one number per line, a signed counter. Player 1 adds +1 and player 2 adds -1 to every line through the cell they take, so each counter is the difference between the two players' marks on its line. A line of n cells reaches `n` only when every cell holds player 1's mark and `-n` only when every cell holds player 2's; once both players have marked a line it can reach neither, which is exactly the rule that a mixed line is dead.

A cell lies on one row and one column, on the main diagonal when `row = col`, and on the anti-diagonal when `row + col = n - 1`. Only those two diagonals have n cells, so the shorter diagonals that N-Queens (#113) names by `r - c` and `r + c` can never win here. A move can complete only lines through its own cell, and only for the player who made it, so checking its row, its column and the two diagonals is the whole win check.

```text
player 1 = X adds +1, player 2 = O adds -1 to each line through the cell
move (r, c, p)    rows           cols           diagonal  anti  returns
(0, 0, 1)         [1, 0, 0]      [1, 0, 0]          1      0      0
(0, 2, 2)         [0, 0, 0]      [1, 0, -1]         1     -1      0
(2, 2, 1)         [0, 0, 1]      [1, 0, 0]          2     -1      0
(1, 1, 2)         [0, -1, 1]     [1, -1, 0]         1     -2      0
(2, 0, 1)         [0, -1, 2]     [2, -1, 0]         1     -1      0
(1, 0, 2)         [0, -2, 2]     [1, -1, 0]         1     -1      0
(2, 1, 1)         [0, -2, 3]     [1, 0, 0]          1     -1      1

          col 0  col 1  col 2    rows[r]
row 0       X      .      O         0     X and O: dead, never 3 or -3
row 1       O      O      .        -2
row 2       X      X      X         3     = n: player 1 wins
cols[c]     1      0      0      diagonal X O X = 1, anti O O X = -1
```

```pseudo
CLASS TicTacToe
    FUNCTION Init(n)
        self.n ← n
        self.rows ← array of n zeros      // player 1 adds +1, player 2 adds -1
        self.cols ← array of n zeros
        self.diagonal ← 0                 // cells with row = col
        self.anti_diagonal ← 0            // cells with row + col = n - 1

    FUNCTION Move(row, col, player)
        sign ← 1
        IF player = 2
            sign ← -1
        self.rows[row] ← self.rows[row] + sign
        self.cols[col] ← self.cols[col] + sign
        IF row = col
            self.diagonal ← self.diagonal + sign
        IF row + col = self.n - 1         // not ELSE IF: the center is on both
            self.anti_diagonal ← self.anti_diagonal + sign
        IF abs(self.rows[row]) = self.n OR abs(self.cols[col]) = self.n
            RETURN player
        IF abs(self.diagonal) = self.n OR abs(self.anti_diagonal) = self.n
            RETURN player
        RETURN 0
```

Each move updates and tests at most four counters, so it costs `O(1)`, and the referee keeps `2n + 2` numbers instead of the `n²` cells of a board. Reach for signed counters whenever the question is whether a whole row, column or group has become uniform while cells only ever fill up. Find Winner on a Tic Tac Toe Game (LC 1275) replays a list of moves through the same counters and reports a draw when all nine cells fill without a winner, and Valid Tic-Tac-Toe State (LC 794) asks whether a board could arise in a real game, which comes down to the mark counts and who moved last. For k in a row on a bigger board, as in Gomoku, the counters stop working, because a winning run can sit anywhere along a longer line; walk outward from the new mark in the four directions instead, `O(k)` per move. The classic mistake is `ELSE IF` for the anti-diagonal. The center of an odd board lies on both diagonals, so when player 2 takes (0, 2), (1, 1) and (2, 0) the anti-diagonal counter misses the center, stops at -2, and the win goes unreported.

*Practice:* LC 348 Design Tic-Tac-Toe · LC 1275 Find Winner on a Tic Tac Toe Game · LC 794 Valid Tic-Tac-Toe State
