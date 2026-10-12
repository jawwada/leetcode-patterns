---
rank: 89
slug: game_of_life
---

Each cell of a board is live (`1`) or dead (`0`), and all cells change at once. A live cell with two or three live neighbors among its eight survives, a dead cell with exactly three live neighbors comes alive, and every other cell is dead in the next generation. Compute the next board in place. The board with rows `010`, `001`, `111`, `000` becomes `000`, `101`, `011`, `010`.

The easy solution reads neighbors from a copy of the board and writes into the original, for `O(m n)` extra space. Writing into the board directly fails, because the rules are simultaneous: once a cell has been overwritten, a neighbor scanned later counts its new state instead of its old one. The fix is to give every cell room for both generations. Only bit 0 of each cell is in use, so bit 1 is free. During the first pass, bit 0 keeps the current state for every reader, and each cell's next state goes into bit 1: `cell | 2` marks it live next, and a cell left alone is dead next. Every neighbor count reads `cell & 1`, which ignores bit 1 whether or not that neighbor has been visited yet. A second pass then shifts each value right by one, so bit 1 drops into bit 0 and the present is forgotten.

Read each value as two binary digits with the future on the left: `2` is a dead cell coming alive, `1` a live cell dying. The rules collapse into one test, since a cell is live next exactly when it has three live neighbors, or when it is live and has two.

```text
cell = 2 × next + current:  0 dead → dead    1 live → dead
                            2 dead → live    3 live → live

board     live neighbors    after pass 1    after pass 2 (>> 1)
0 1 0     1 1 2             0 1 0           0 0 0
0 0 1     3 5 3             2 0 3           1 0 1
1 1 1     1 3 2             1 3 3           0 1 1
0 0 0     2 3 2             0 2 0           0 1 0
```

```pseudo
FUNCTION CountLiveNeighbors(board, row, col)
    live ← 0
    FOR near_row FROM max(0, row - 1) TO min(len(board) - 1, row + 1)
        FOR near_col FROM max(0, col - 1) TO min(len(board[0]) - 1, col + 1)
            IF near_row = row AND near_col = col
                CONTINUE                    // a cell is not its own neighbor
            live ← live + (board[near_row][near_col] & 1)   // bit 0: now
    RETURN live

FUNCTION GameOfLife(board)
    FOR row FROM 0 TO len(board) - 1
        FOR col FROM 0 TO len(board[0]) - 1
            live ← CountLiveNeighbors(board, row, col)
            alive ← board[row][col] & 1
            IF live = 3 OR (alive = 1 AND live = 2)
                board[row][col] ← board[row][col] | 2    // bit 1: live next
    FOR row FROM 0 TO len(board) - 1
        FOR col FROM 0 TO len(board[0]) - 1
            board[row][col] ← board[row][col] >> 1       // keep only the next
```

Each cell reads at most eight neighbors, so the two passes cost `O(m n)` time with `O(1)` extra space. The signal is a grid that must change all at once and in place, with values small enough to leave spare bits. The same move, keeping extra information inside the input instead of in a copy, solves Set Matrix Zeroes, which marks the rows and columns to clear in the matrix's own first row and column. On an infinite board, keep a set of live cells instead: each live cell adds one to a count for each of its eight neighbors in a map, and the next set holds the cells counted three times plus the live cells counted twice, so a generation costs time in proportion to the live cells. The classic mistake is testing `cell = 1` instead of reading bit 0 when counting neighbors: a cell already marked `3`, live now and live next, stops counting as live, and the 2 by 2 block of live cells, which never changes, loses its bottom row.

*Practice:* LC 289 Game of Life · LC 73 Set Matrix Zeroes
