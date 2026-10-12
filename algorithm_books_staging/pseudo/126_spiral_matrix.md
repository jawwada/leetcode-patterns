---
rank: 126
slug: spiral_matrix
---

Given an `m × n` matrix, return all of its elements in clockwise spiral order: along the top row, down the right column, back along the bottom row, up the left column, and then the same again one ring further in. The 3 by 4 matrix with rows `1 2 3 4`, `5 6 7 8` and `9 10 11 12` reads `1 2 3 4 8 12 11 10 9 5 6 7`.

The direct simulation walks cell by cell with a direction vector and a grid of visited marks, turning right whenever the next cell is off the matrix or already read, and spends `O(m × n)` extra memory on the marks. The marks are wasted, because after every side the unread cells form a rectangle, and four numbers describe that rectangle completely: rows `top` to `bottom`, columns `left` to `right`. Each side of the walk reads one edge of the rectangle and shrinks it by one: after the top row `top` moves down, after the right column `right` moves left, after the bottom row `bottom` moves up, and after the left column `left` moves right. The loop runs while the rectangle is non-empty, peeling the matrix ring by ring from the outside in.

The first two sides of a ring need no check: the loop condition promises an unread top row, and when that row was the last one, the right column's range is empty and reads nothing. By the third side the rectangle may have collapsed. If the top row was the last unread row, `top` has just passed `bottom`, and a bottom row would read that same row again backwards; if the right column was the last unread column, the left column would repeat it upwards. The guards `top ≤ bottom` and `left ≤ right` before the last two sides matter only when the last ring is a strip: a single row, a single column, or the strip left in the middle of a wide or tall matrix. In the example the second ring is the strip `6 7`, and the guard stops the `6` from being read twice.

```text
  1 →  2 →  3 →  4
                 ↓
  5 →  6 →  7    8
  ↑              ↓
  9 ← 10 ← 11 ← 12

side           cells read   top  bottom  left  right   (after the side)
top row →      1 2 3 4       1     2      0     3
right col ↓    8 12          1     2      0     2
bottom row ←   11 10 9       1     1      0     2
left col ↑     5             1     1      1     2
top row →      6 7           2     1      1     2
right col ↓    none          2     1      1     1
bottom row     skipped: top 2 > bottom 1, row 1 would repeat the 6
left col ↑     none          2     1      2     1
top > bottom: the loop stops with all 12 cells read exactly once
```

```pseudo
FUNCTION SpiralOrder(matrix)
    result ← empty list
    IF len(matrix) = 0
        RETURN result
    top ← 0
    bottom ← len(matrix) - 1
    left ← 0
    right ← len(matrix[0]) - 1
    WHILE top ≤ bottom AND left ≤ right
        FOR col FROM left TO right               // top row, left to right
            result.append(matrix[top][col])
        top ← top + 1
        FOR row FROM top TO bottom               // right column, downward
            result.append(matrix[row][right])
        right ← right - 1
        IF top ≤ bottom                          // a bottom row is unread
            FOR col FROM right DOWNTO left       // bottom row, leftward
                result.append(matrix[bottom][col])
            bottom ← bottom - 1
        IF left ≤ right                          // a left column is unread
            FOR row FROM bottom DOWNTO top       // left column, upward
                result.append(matrix[row][left])
            left ← left + 1
    RETURN result
```

Every cell is read once, so the walk costs `O(m × n)` time and `O(1)` extra space beyond the output. Reach for the four shrinking bounds whenever a matrix is processed ring by ring: reading or filling in spiral order, or rotating layer by layer as in the four-way swap of #127. Spiral Matrix II runs the same walk and writes `1, 2, 3, …` instead of reading, and Spiral Matrix III walks an outward spiral from a starting cell with side lengths `1, 1, 2, 2, 3, 3, …`, keeping only the cells inside the grid. The classic mistake is dropping the two guards. Every square matrix still comes out right, which is why the bug survives casual testing, but the single row `[1, 2, 3]` comes back as `[1, 2, 3, 2, 1]`, and the 3 by 4 example gains a second `6` at the end.

*Practice:* LC 54 Spiral Matrix · LC 59 Spiral Matrix II · LC 885 Spiral Matrix III
