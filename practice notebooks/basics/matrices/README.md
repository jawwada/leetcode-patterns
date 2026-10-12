# Matrices

A matrix is a list of rows, `matrix[r][c]`, with m rows and n columns. Matrix problems are rarely about a clever data structure; they are about **index arithmetic** (which cell lands where), **bounds** (which cells are still unvisited), and **doing it in place** (storing two states in one cell, or reusing a border row as scratch space). The skill is to name the transformation in one sentence before writing a loop: "transpose then reverse rows", "shrink four bounds", "bit 0 is now, bit 1 is next".

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| read / write a cell | O(1) | `matrix[r][c]`; always `0 <= r < m and 0 <= c < n` first |
| full pass | O(m*n) | every traversal pattern below |
| swap two cells | O(1) | `a[i][j], a[j][i] = a[j][i], a[i][j]`, both sides at once |
| reverse a row | O(n) | `row.reverse()` in place |
| transpose n x n in place | O(n^2) | swap each pair above the diagonal exactly once (`j > i`) |
| staircase search in a sorted matrix | O(m + n) | each step discards a whole row or column |
| 4 / 8 neighbors | O(1) | direction vectors plus a bounds check |

## Index arithmetic to recognise

| Move | Formula |
|---|---|
| transpose | (r, c) -> (c, r) |
| rotate 90 clockwise | (r, c) -> (c, n-1-r), equal to transpose then reverse each row |
| rotate 90 counter-clockwise | (r, c) -> (n-1-c, r), equal to transpose then reverse each column |
| row-major position | r * n + c |
| anti-diagonal index | r + c (m + n - 1 of them) |
| main-diagonal index | r - c |
| 4 neighbors | (-1,0) (1,0) (0,-1) (0,1) |
| 8 neighbors | the 4 above plus (-1,-1) (-1,1) (1,-1) (1,1) |

## Drawn example: rotate [[1,2,3],[4,5,6],[7,8,9]] clockwise

```
input          transpose (swap across the diagonal)   reverse each row
1 2 3          1 4 7                                  7 4 1
4 5 6    ->    2 5 8                            ->    8 5 2
7 8 9          3 6 9                                  9 6 3

swaps made: (0,1)<->(1,0)  (0,2)<->(2,0)  (1,2)<->(2,1)   -- only j > i, each pair once
check: cell (0,0)=1 must land at (c, n-1-r) = (0, 2)       -- top-right, yes
```

The spiral walk of the same matrix peels rings with four bounds:

```
rows 0..2 cols 0..2   top row ->  [1 2 3]   right col v [6 9]   bottom row <- [8 7]   left col ^ [4]
rows 1..1 cols 1..1   top row ->  [5]       right col   []      (top > bottom: stop)
result 1 2 3 6 9 8 7 4 5
```

## The invariants to say out loud

- Rotate: "Transpose then reverse rows. Transpose swaps across the diagonal once per pair, j > i."
- Spiral: "Four bounds, one side per step, re-check `top <= bottom` and `left <= right` before the bottom and left sides."
- Set zeroes: "Record the flags for row 0 and column 0 BEFORE marking; the inside is finished before the borders."
- Staircase search: "From the top-right, bigger means move left, smaller means move down; every step kills a row or a column."
- Game of life: "Bit 0 is now, bit 1 is next. Read neighbors with `& 1`, write with `|= 2`, finish with `>>= 1`."
- Traversals: "Same r + c means same anti-diagonal. Check bounds before touching a neighbor."

## Exercises

| File | Drills |
|---|---|
| `01_rotate_image.py` (LeetCode 48) | in-place transpose with a one-sided double loop, then reverse rows |
| `02_spiral_matrix.py` (LeetCode 54) | four shrinking bounds, the two extra bounds checks that stop double-emitting |
| `03_set_matrix_zeroes.py` (LeetCode 73) | O(1) extra space: flags first, borders as markers, inside before borders |
| `04_search_2d_matrix_staircase.py` (LeetCode 240) | top-right start, move left or down, O(m + n) |
| `05_game_of_life_in_place.py` (LeetCode 289) | two states in one int: `& 1` to read, `|= 2` to write, `>>= 1` to commit |
| `06_matrix_traversal_patterns.py` | row-major, column-major, anti-diagonals by r + c, 4/8 direction vectors with bounds checks |
