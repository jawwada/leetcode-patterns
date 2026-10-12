---
rank: 56
slug: search_2d_matrix
---

Given a matrix whose rows are sorted from left to right and whose columns are sorted from top to bottom, report whether a target is present. In the matrix with rows `[1, 4, 7, 11, 15]`, `[2, 5, 8, 12, 19]`, `[3, 6, 9, 16, 22]`, `[10, 13, 14, 17, 24]` and `[18, 21, 23, 26, 30]`, the target `5` is present and `20` is not.

Scanning every cell costs `O(m n)`; a binary search per row costs `O(m log n)` and ignores the order down the columns. The trick is to stand in the top-right corner. The top-right value is the largest in its row and the smallest in its column, so one comparison with the target throws away a whole line. If it is bigger than the target, everything below it is bigger still: the column is out, and the walk steps left. If it is smaller, everything to its left is smaller still: the row is out, and the walk steps down. What remains is a smaller matrix with the same kind of corner, so the walk traces a staircase down and to the left until it lands on the target or steps off the board. The bottom-left corner works too, with the moves mirrored; at the top-left or the bottom-right both moves push the value the same way, and one comparison cannot choose between them.

A stronger order allows a faster search. When each row starts above the end of the row before, the rows laid end to end form one sorted array of `m × n` values, and the lower-bound search of #14 runs on it unchanged; only the read changes. Flat position `p` lives in row `floor(p / n)` and column `p mod n` for rows of length `n`, as below on the rows `[1, 3, 5, 7]`, `[10, 11, 16, 20]` and `[23, 30, 34, 60]`.

```text
target 5: found on probe 5         target 20: off the bottom, 9 probes
  1    4 ←  7 ← 11 ← 15             1    4    7   11   15
       ↓                                                ↓
  2   [5]   8   12   19             2    5    8   12   19
                                                        ↓
  3    6    9   16   22             3    6    9   16 ← 22
                                                   ↓
 10   13   14   17   24            10   13   14   17   24
                                                   ↓
 18   21   23   26   30            18 ← 21 ← 23 ← 26   30
                                    ↓

flat p   0  1  2  3  4  5  6  7  8  9 10 11    cell (floor(p / 4), p mod 4)
value    1  3  5  7 10 11 16 20 23 30 34 60    target 3
mid 6 → 16 ≥ 3: hi ← 6    mid 3 → 7 ≥ 3: hi ← 3    mid 1 → 3 ≥ 3: hi ← 1
mid 0 → 1 < 3: lo ← 1     lo = hi = 1: cell (0, 1) holds 3, found
```

```pseudo
FUNCTION StaircaseSearch(matrix, target)
    IF len(matrix) = 0
        RETURN false
    row ← 0
    col ← len(matrix[0]) - 1        // top-right: row's max, column's min
    WHILE row < len(matrix) AND col ≥ 0
        value ← matrix[row][col]
        IF value = target
            RETURN true
        IF value > target
            col ← col - 1           // the rest of this column is bigger still
        ELSE
            row ← row + 1           // the rest of this row is smaller still
    RETURN false

FUNCTION FlattenedSearch(matrix, target)
    IF len(matrix) = 0
        RETURN false
    cols ← len(matrix[0])
    lo ← 0
    hi ← len(matrix) * cols         // half-open [lo, hi) of flat positions
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        value ← matrix[floor(mid / cols)][mid mod cols]   // fold into a cell
        IF value < target
            lo ← mid + 1
        ELSE
            hi ← mid
    IF lo = len(matrix) * cols
        RETURN false                // every value is smaller than the target
    RETURN matrix[floor(lo / cols)][lo mod cols] = target
```

Each staircase probe discards a row or a column, so there are at most `m + n` of them: `O(m + n)` time and `O(1)` space. The flat search costs `O(log(m n))`. Rows and columns sorted separately call for the staircase; rows that continue one another call for one flat search. The staircase also counts. Count Negative Numbers in a Sorted Matrix walks it from the bottom-left along the border of the negatives, adding a row's whole negative tail at each step up, and Kth Smallest Element in a Sorted Matrix binary searches on the value (#15) with a staircase count of the cells at most `mid` as its check. The classic mistake in the flat search is dividing by the number of rows instead of the length of a row: in the 3 by 4 example position 3 holds the `7`, but dividing by 3 sends the read to row 1, column 0, the `10`, and the `7` is never found.

*Practice:* LC 240 Search a 2D Matrix II · LC 74 Search a 2D Matrix · LC 1351 Count Negative Numbers in a Sorted Matrix · LC 378 Kth Smallest Element in a Sorted Matrix
