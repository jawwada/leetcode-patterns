---
rank: 113
slug: n_queens
---

Place n queens on an n × n chessboard so that no two attack each other along a row, a column or a diagonal, and return every such board as a list of strings, `Q` for a queen and `.` for an empty square. For `n = 4` there are two boards, `[".Q..", "...Q", "Q...", "..Q."]` and its mirror image `["..Q.", "Q...", "...Q", ".Q.."]`.

No two queens may share a row, so place exactly one queen per row, from top to bottom; the search only chooses a column for each row, and the row rule holds by construction. A square is safe when no earlier queen sits in its column, on its diagonal or on its anti-diagonal. Comparing against the earlier queens one by one costs `O(n)` per square; the trick is that every diagonal has a name. Along a down-right diagonal `r - c` stays constant, and along a down-left anti-diagonal `r + c` stays constant, so three sets, `cols`, `diags` and `anti_diags`, answer "is this square attacked?" with three lookups. Placing a queen adds its three names to the sets; backtracking removes them again.

The two grids below are the whole geometry of the problem. Every square carries two diagonal names, and two queens share a diagonal exactly when they share a name. Under them, the first board is built row by row, with the sets as the code holds them after each placement.

```text
r - c: one name per \ diagonal    r + c: one name per / diagonal
  c= 0  1  2  3                     c= 0  1  2  3
r=0  0 -1 -2 -3                   r=0  0  1  2  3
r=1  1  0 -1 -2                   r=1  1  2  3  4
r=2  2  1  0 -1                   r=2  2  3  4  5
r=3  3  2  1  0                   r=3  3  4  5  6

n = 4: row 0 col 0 dead-ends twice, then row 0 col 1 leads to a board
. Q . .   row 0 col 1   cols {1}           r-c {-1}            r+c {1}
. . . Q   row 1 col 3   cols {1, 3}        r-c {-2, -1}        r+c {1, 4}
Q . . .   row 2 col 0   cols {0, 1, 3}     r-c {-2, -1, 2}     r+c {1, 2, 4}
. . Q .   row 3 col 2   cols {0, 1, 2, 3}  r-c {-2, -1, 1, 2}  r+c {1, 2, 4, 5}
```

```pseudo
FUNCTION Draw(queens)
    n ← len(queens)
    board ← empty list
    FOR EACH col IN queens
        board.append("." × col + "Q" + "." × (n - 1 - col))
    RETURN board

FUNCTION Backtrack(n, row, queens, cols, diags, anti_diags, boards)
    IF row = n
        boards.append(Draw(queens))          // every row holds a queen
        RETURN
    FOR col FROM 0 TO n - 1
        IF col IN cols OR (row - col) IN diags OR (row + col) IN anti_diags
            CONTINUE                         // attacked
        queens.append(col)                   // place the queen
        cols.add(col)
        diags.add(row - col)
        anti_diags.add(row + col)
        Backtrack(n, row + 1, queens, cols, diags, anti_diags, boards)
        queens.pop()                         // remove it, undo all four marks
        cols.remove(col)
        diags.remove(row - col)
        anti_diags.remove(row + col)

FUNCTION SolveNQueens(n)
    boards ← empty list
    Backtrack(n, 0, empty list, empty set, empty set, empty set, boards)
    RETURN boards
```

With the column set alone, row r has at most `n - r` free columns, so the tree has at most `n!` leaves and the search is bounded by `O(n · n!)`, plus `O(n²)` to draw each board found; the diagonal sets prune far below that bound, and for n = 8 the search makes only 2,057 calls to find all 92 boards. The extra space is `O(n)` besides the output. When only the number of boards is asked (LC 52), keep the recursion and add 1 at `row = n` instead of drawing. The same idea of constraint sets, one per row, column and 3 × 3 box, drives Sudoku Solver (LC 37), and the three sets can also be three integers used as bitmasks (#137). The classic mistake is naming both diagonal directions with `r - c`: the anti-diagonals then go unchecked, and n = 4 returns 7 boards instead of 2.

*Practice:* LC 51 N-Queens · LC 52 N-Queens II · LC 37 Sudoku Solver
