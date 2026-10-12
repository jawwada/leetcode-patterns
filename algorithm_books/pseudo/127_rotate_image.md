---
rank: 127
slug: rotate_image
---

Rotate an `n × n` matrix by 90 degrees clockwise in place, without allocating a second matrix. The matrix with rows `1 2 3`, `4 5 6` and `7 8 9` becomes `7 4 1`, `8 5 2`, `9 6 3`: the first row turns into the last column, read from top to bottom.

A rotation is a rule about coordinates: the cell at row `r`, column `c` lands at row `c`, column `n - 1 - r`. Writing `rotated[c][n - 1 - r] ← matrix[r][c]` into a fresh matrix is easy and costs `O(n²)` extra space, so the in-place requirement is the whole problem. The way through is to split the rotation into two moves made only of swaps. The transpose mirrors the matrix across its main diagonal, sending `(r, c)` to `(c, r)`: every cell above the diagonal trades places with its partner below, and the diagonal stays put. Reversing each row mirrors left to right, sending `(r, c)` to `(r, n - 1 - c)`. Together they send `(r, c)` to `(c, r)` and then to `(c, n - 1 - r)`, exactly the rotation.

Picture the matrix as a square card. Flip it over its diagonal, then over its vertical midline, and it has turned a quarter turn clockwise, because two mirror images always compose into a rotation by twice the angle between the mirror lines, here twice 45 degrees. Every swap of the transpose pairs a cell above the diagonal with its mirror below, so the loop visits only the cells with `col > row`.

```text
original            transpose            reverse each row
1  2  3             1  4  7              7  4  1
4  5  6      →      2  5  8       →      8  5  2
7  8  9             3  6  9              9  6  3
cell (r, c)         goes to (c, r)       then to (c, n - 1 - r)

2 at (0, 1)   →   (1, 0)   →   (1, 2)
7 at (2, 0)   →   (0, 2)   →   (0, 0)
5 at (1, 1)   →   (1, 1)   →   (1, 1)    the center never moves
transpose swaps: (0, 1) with (1, 0), (0, 2) with (2, 0), (1, 2) with (2, 1)
```

```pseudo
FUNCTION Rotate(matrix)                     // 90 degrees clockwise, in place
    n ← len(matrix)
    FOR row FROM 0 TO n - 1                 // transpose: mirror on the diagonal
        FOR col FROM row + 1 TO n - 1       // above the diagonal only
            swap(matrix[row][col], matrix[col][row])
    FOR row FROM 0 TO n - 1
        ReverseRow(matrix[row])             // mirror left to right

FUNCTION ReverseRow(cells)
    left ← 0
    right ← len(cells) - 1
    WHILE left < right
        swap(cells[left], cells[right])
        left ← left + 1
        right ← right - 1
```

Each pass touches every cell a constant number of times, so the rotation costs `O(n²)` time and `O(1)` extra space. Counter-clockwise sends `(r, c)` to `(n - 1 - c, r)`: reverse each row and then transpose, or transpose and then reverse the order of the rows. The alternative is the four-way cycle swap: for every cell `(r, c)` on the top side of each ring except its right-hand corner, move the four cells `(r, c) → (c, n - 1 - r) → (n - 1 - r, n - 1 - c) → (n - 1 - c, r)` one step around with a single temporary. It moves each element once instead of about twice, but its index arithmetic is easy to get wrong under pressure. The signals are a grid to rotate, flip or transpose without extra memory; LC 1886 just tries the four quarter turns, and Transpose Matrix, whose matrix need not be square, must build a new array because the shape changes. The classic mistake is starting the inner loop at `0`: every pair is swapped twice, the transpose undoes itself, and the result is the mirror image `3 2 1`, `6 5 4`, `9 8 7`. Reversing the order of the rows instead of each row is the other: it turns the matrix counter-clockwise.

*Practice:* LC 48 Rotate Image · LC 1886 Determine Whether Matrix Can Be Obtained By Rotation · LC 867 Transpose Matrix
