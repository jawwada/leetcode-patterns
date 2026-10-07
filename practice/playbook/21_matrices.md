## Matrices

> A grid is a list of rows, and every matrix trick is index arithmetic on `(r, c)`: the row first, counting down; the column second, counting right.

**Reach for it when** the input is a grid, board or image and the problem says *in place* or *O(1) extra space*, *rotate*, *spiral* or *clockwise*, *diagonal*, *set its entire row and column*, *every row and every column is sorted*, or *all cells update at the same time*. (Searching a grid for regions or shortest paths is BFS/DFS: see [Graphs I](#s17). This section is about moving indices around.)

**In this repo:** `math_geometry/` (Rotate Image, Spiral Matrix, Set Matrix Zeroes) · basics: `practice/simple/basics/matrices/01_rotate_image.py`, `02_spiral_matrix.py`, `03_set_matrix_zeroes.py`, `04_search_2d_matrix_staircase.py`, `05_game_of_life_in_place.py`, `06_matrix_traversal_patterns.py` · grid walks with bounds checks in the bank: `practice/simple/39_word_search.py`, `practice/simple/41_number_of_islands.py`, `practice/simple/44_rotting_oranges.py` · diagonals as `r - c` and `r + c`: `practice/simple/40_n_queens.py`

### The picture

```text
grid = [[1,  2,  3,  4],          R = len(grid)    = 3 rows
        [5,  6,  7,  8],          C = len(grid[0]) = 4 columns
        [9, 10, 11, 12]]

          c=0  c=1  c=2  c=3
   r=0  [  1    2    3    4 ]     grid[1][2] == 7: the row first (down), then the column (right)
   r=1  [  5    6   (7)   8 ]     its 4 neighbours: up (0, 2), down (2, 2), left (1, 1), right (1, 3)
   r=2  [  9   10   11   12 ]     a step is (r + dr, c + dc); it is inside iff 0 <= r < R and 0 <= c < C

   "\" diagonals: r - c is constant          "/" anti-diagonals: r + c is constant
          0  -1  -2  -3                             0   1   2   3
          1   0  -1  -2                             1   2   3   4
          2   1   0  -1                             2   3   4   5
```

The main walk of this section, the spiral, peels the grid like an onion: the outer ring first, then the ring inside it.

```text
            left                  right
             v                      v
   top  ->   1 -->  2 -->  3 -->    4       lap 1: top row ->, right column down, bottom row <-,
                                    |              left column up. Each wall steps inward right
             5 -->  6 -->  7        8              after its side is walked, so the next side starts
             ^                      |              one cell later and no corner is read twice.
 bottom ->   9 <-- 10 <-- 11 <--   12       lap 2: only row 1, columns 1..2 is left: 6, 7
```

**Why it is cheap:** reading every cell is already O(R·C), so most matrix problems are not about time. Their brute forces waste memory, and each optimal version trades that memory for one observation:

| Problem | What the brute force wastes | The observation that removes it |
|---|---|---|
| Rotate Image | a second matrix | a quarter-turn is two mirror flips, and a flip is only swaps |
| Spiral Matrix | a `visited` grid | the unvisited cells always form a rectangle, so four numbers describe them |
| Set Matrix Zeroes | a copy, or two sets | a row that holds a zero is doomed anyway, so its first cell can carry the flag |
| Game of Life | a copy of the board | a 0/1 cell has spare bits to hold tomorrow's value |
| Search a sorted matrix | time: an O(R·C) scan | from a corner, one comparison drops a whole row or column: O(R + C) |

### From idea to code

Every tool in this section is index arithmetic, so first the vocabulary: directions, the bounds check, and making a grid without the classic aliasing bug.

```python
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]             # up, down, left, right


def neighbors(grid, r, c):
    R, C = len(grid), len(grid[0])
    out = []
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C:                # check BEFORE reading grid[nr][nc]
            out.append((nr, nc))
    return out


grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(neighbors(grid, 0, 0), neighbors(grid, 1, 2))   # [(1, 0), (0, 1)] [(0, 2), (2, 2), (1, 1), (1, 3)]

shared = [[0] * 3] * 2                 # WRONG: a list holding the SAME row twice
fresh = [[0] * 3 for _ in range(2)]    # right: a new row each time round the loop
shared[0][0] = fresh[0][0] = 7
print(shared, fresh)                   # [[7, 0, 0], [7, 0, 0]] [[7, 0, 0], [0, 0, 0]]
clone = [row[:] for row in grid]       # copy a grid row by row
clone[0][0] = 99
print(grid[0][0])                      # 1: the original is untouched
```

**Try it**
- Delete the bounds check in `neighbors` and print `[grid[nr][nc] for nr, nc in neighbors(grid, 0, 0)]`: no error, you get `[9, 5, 4, 2]`. Python reads `grid[-1][0]` as the *last* row, so a missing check silently wraps around. Only the far side crashes, and only when you read the cells: `[grid[nr][nc] for nr, nc in neighbors(grid, 2, 3)]` raises `IndexError` at `(3, 3)`.
- Replace the copy with `clone = grid[:]` and rerun: `grid[0][0]` prints 99. `grid[:]` copies the outer list only; both lists still point at the same rows.
- Make an 8-direction list `DIRS8 = DIRS + [(-1, -1), (-1, 1), (1, -1), (1, 1)]` and loop over it instead: the corner `(0, 0)` has 3 neighbours, the inner cell `(1, 1)` has 8.

Now the walk with the most index decisions in it: the spiral.

**The idea in one sentence:** *the cells you have not visited yet always form a rectangle, so walk its four sides in order and move each wall inward right after you walk it.*

| Decision | Spiral (four walls) answer |
|---|---|
| **State**: what must I remember? | four walls `top, bottom, left, right`, and the output list |
| **Definition**: what exactly does each variable mean? | the unvisited cells are exactly rows `top..bottom` × columns `left..right`, **all four inclusive** |
| **Invariant**: what is true at the end of every step? | the unvisited cells form a rectangle, possibly empty: it is empty exactly when `top > bottom` or `left > right`. Every cell outside it has been output once, in spiral order |
| **Step**: how does one side change the state? | walk one side, then move that wall in by one. A side is a row or a column, and its line must still exist: a row needs `top <= bottom`, a column needs `left <= right`. The `while` test guarantees both for the first two sides. But `top += 1` can use up the last row and `right -= 1` the last column, so re-check `top <= bottom` before the bottom row and `left <= right` before the left column |
| **Record**: when is the answer updated? | append each cell as you walk past it, *before* that side's wall moves |
| **Init**: starting values | `top, bottom, left, right = 0, R - 1, 0, C - 1`: the whole grid is unvisited |
| **Return**: what comes back? | the output once the walls cross; `[]` for an empty grid |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "how many rows, how many columns" | `R, C = len(grid), len(grid[0])` (after checking the grid is not empty) |
| "the cell in row r, column c" | `grid[r][c]`: row first, always |
| "one step in every direction, if it stays inside" | `for dr, dc in DIRS:` then `if 0 <= nr < R and 0 <= nc < C:` |
| "walk the top wall, left to right" | `for c in range(left, right + 1): out.append(grid[top][c])` |
| "that wall is used up" | `top += 1` |
| "walk the right column, top to bottom" | `for r in range(top, bottom + 1): out.append(grid[r][right])`, after `top += 1` |
| "walk the bottom wall, right to left" | `for c in range(right, left - 1, -1):` (the stop `left - 1` is excluded) |
| "walk the left column, bottom to top" | `for r in range(bottom, top - 1, -1):` |
| "is there still a row between the walls?" | `if top <= bottom:` |
| "is there still a column between the walls?" | `if left <= right:` |
| "the walls have crossed" | `while top <= bottom and left <= right:` is false |

On every side the order is RECORD, then STEP: read the side while its wall still marks it, then move the wall. Moving it first skips that row; moving it one side too late reads the corner twice.

```python
def spiral_order(grid):
    if not grid or not grid[0]:
        return []
    out = []                                         # STATE: the cells so far, in spiral order
    top, bottom = 0, len(grid) - 1                   # STATE + INIT: unvisited = rows top..bottom,
    left, right = 0, len(grid[0]) - 1                #   columns left..right (all inclusive)
    while top <= bottom and left <= right:           # the rectangle is not empty
        for c in range(left, right + 1):             # top row, left -> right
            out.append(grid[top][c])                 # RECORD as we walk past
        top += 1                                     # STEP: the top wall moves in
        for r in range(top, bottom + 1):             # right column, going down
            out.append(grid[r][right])               # RECORD
        right -= 1                                   # STEP: the right wall moves in
        if top <= bottom:                            # a row is still left
            for c in range(right, left - 1, -1):     # bottom row, right -> left
                out.append(grid[bottom][c])          # RECORD
            bottom -= 1                              # STEP: the bottom wall moves in
        if left <= right:                            # a column is still left
            for r in range(bottom, top - 1, -1):     # left column, going up
                out.append(grid[r][left])            # RECORD
            left += 1                                # STEP: the left wall moves in
    return out                                       # RETURN: the walls have crossed


print(spiral_order(grid))                            # [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
print(spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))   # [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

**Try it**
- Delete the line `if top <= bottom:` (keep the loop under it, dedented) and run `spiral_order([[1, 2, 3]])`: `[1, 2, 3, 2, 1]`. With one row left, the "bottom row" is the top row you already walked, walked back.
- Do the same with `if left <= right:` and run `spiral_order([[1], [2], [3]])`: `[1, 2, 3, 2]`. The single column is walked down and then partly back up.
- Change `range(right, left - 1, -1)` to `range(right, left, -1)`: on `grid` the 9 goes missing. A `range` never includes its stop, so walking *down to* `left` needs `left - 1`.
- Print `(top, bottom, left, right)` at the top of the `while` for a 4 x 4 grid: `(0, 3, 0, 3)` then `(1, 2, 1, 2)`, one lap per ring.

### Watch it work

Each block is one lap; each line is one side of the current rectangle. Watch the guards skip the sides that no longer exist.

```python
def trace_spiral(grid):
    top, bottom, left, right = 0, len(grid) - 1, 0, len(grid[0]) - 1
    while top <= bottom and left <= right:
        print(f"walls: rows {top}..{bottom}, columns {left}..{right}")
        print("   top row    ->", [grid[top][c] for c in range(left, right + 1)])
        top += 1
        print("   right col  v ", [grid[r][right] for r in range(top, bottom + 1)])
        right -= 1
        if top <= bottom:
            print("   bottom row <-", [grid[bottom][c] for c in range(right, left - 1, -1)])
            bottom -= 1
        else:
            print("   bottom row    skipped: no row left")
        if left <= right:
            print("   left col   ^ ", [grid[r][left] for r in range(bottom, top - 1, -1)])
            left += 1
        else:
            print("   left col      skipped: no column left")


trace_spiral(grid)
```

**Try it**
- Predict, then run `trace_spiral([[1, 2], [3, 4], [5, 6], [7, 8]])`: a single lap, `1 2 | 4 6 8 | 7 | 5 3`. After it `left = 1 > right = 0`, so the walls have crossed.
- Run `trace_spiral([[5]])`: the top row takes the only cell, and both guards skip their side.
- Move `top += 1` below the right-column `print` (the wall moves one side too late): the right column becomes `[4, 8, 12]`, so the corner 4 is read twice. The same edit in `spiral_order` gives `[1, 2, 3, 4, 4, 8, 12, 11, 10, 9, 5, 6, 7, 7]`.
- Run it on a 5 x 5 grid, `[[5 * r + c for c in range(5)] for r in range(5)]`: three laps, and the last one is just the centre cell 12.

### The rest of the toolbox

**Derive any index map in 30 seconds.** Say where `(0, 0)` and `(0, 1)` must land, then read the formula off. Clockwise: the top-left corner goes to the top-right corner of the new grid, `(0, R-1)`, and one step right becomes one step down, so `(r, c) -> (c, R-1-r)`. Always check a map on a non-square grid, where a wrong `R` or `C` shows up at once.

| Move | `(r, c)` goes to | New shape | A new grid in one line |
|---|---|---|---|
| transpose | `(c, r)` | C x R | `[list(t) for t in zip(*g)]` |
| rotate clockwise | `(c, R-1-r)` | C x R | `[list(t) for t in zip(*g[::-1])]` |
| rotate counter-clockwise | `(C-1-c, r)` | C x R | `[list(t) for t in zip(*g)][::-1]` |
| rotate 180° | `(R-1-r, C-1-c)` | R x C | `[row[::-1] for row in g[::-1]]` |
| mirror left-right | `(r, C-1-c)` | R x C | `[row[::-1] for row in g]` |

| Name for a cell | Key | All cells with one key |
|---|---|---|
| flat index | `i = r * C + c` | back: `r, c = divmod(i, C)` |
| `\` diagonal | `k = r - c` | `for r in range(max(0, k), min(R, C + k)):` with `c = r - k` |
| `/` anti-diagonal | `d = r + c` | `for r in range(max(0, d - C + 1), min(R, d + 1)):` with `c = d - r` (keeps `0 <= c < C`) |
| ring (layer) | `min(r, c, R-1-r, C-1-c)` | its distance to the nearest edge |
| 3 x 3 box (sudoku) | `(r // 3) * 3 + c // 3` | boxes numbered 0..8, row by row |

#### Rotate an n x n matrix in place

**Idea:** a clockwise quarter-turn sends `(r, c)` to `(c, n-1-r)`. That move is two mirror flips in a row, and a flip is only swaps: mirror across the main diagonal (the transpose, `(r, c) -> (c, r)`), then mirror left-right (reverse each row, `(c, r) -> (c, n-1-r)`).

```text
  1 2 3                      1 4 7                        7 4 1
  4 5 6   -- transpose -->   2 5 8   -- reverse rows -->  8 5 2
  7 8 9    swap across "\"   3 6 9     flip left-right    9 6 3
```

The other classic way turns four cells at once, ring by ring. Call them `a, b, d, e` (the name `c` is taken: it is the column). Each one is the previous one with the same map applied: `b` is where `a` goes, `d` is where `b` goes, `e` is where `d` goes, and `e` goes back to `a`:

```text
   n = 4, ring 0, c = 1:      . a . .        a = (0, 1) -> b = (1, 3)
                              . . . b        b = (1, 3) -> d = (3, 2)
                              e . . .        d = (3, 2) -> e = (2, 0)
                              . . d .        e = (2, 0) -> a
```

In the code, every cell on the left receives the value of the cell that turns into it, so the right side is the left side shifted one place, last first: `a, b, d, e` receive `e, a, b, d`.

```python
def rotate_clockwise(m):                       # n x n, in place
    n = len(m)
    for r in range(n):
        for c in range(r + 1, n):              # above the diagonal only: each pair swapped once
            m[r][c], m[c][r] = m[c][r], m[r][c]
    for row in m:
        row.reverse()                          # then mirror left <-> right


def rotate_by_rings(m):                        # the same turn, four cells per move
    n = len(m)
    for r in range(n // 2):                    # ring r (the centre of an odd n stays put)
        for c in range(r, n - 1 - r):          # the ring's top edge, minus its last cell
            m[r][c], m[c][n - 1 - r], m[n - 1 - r][n - 1 - c], m[n - 1 - c][r] = \
                m[n - 1 - c][r], m[r][c], m[c][n - 1 - r], m[n - 1 - r][n - 1 - c]


a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = [row[:] for row in a]
rotate_clockwise(a)
rotate_by_rings(b)
print(a)         # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
print(a == b)    # True
```

**Try it**
- Change `range(r + 1, n)` to `range(n)` in the transpose: you get `[[3, 2, 1], [6, 5, 4], [9, 8, 7]]`, only the mirror image. Every pair was swapped twice, which undid the transpose.
- Replace `for row in m: row.reverse()` with `m.reverse()` (reverse the *order* of the rows): `[[3, 6, 9], [2, 5, 8], [1, 4, 7]]`, the counter-clockwise turn.
- Call `rotate_clockwise` four times on the same matrix and compare it with a saved copy: four quarter-turns change nothing.
- In `rotate_by_rings`, print `(r, c)` for each move on a 4 x 4: `(0, 0) (0, 1) (0, 2) (1, 1)`. Four moves of four cells cover all 16.

#### Set Matrix Zeroes with O(1) extra space

**Idea:** the answer needs only R + C facts ("row r has a zero", "column c has a zero"), and the matrix's own first column and first row can hold them. We write `m[r][0] = 0` only when row r contains a zero, and then that whole row ends up zero anyway, so nothing is lost (the same goes for `m[0][c]` and column c). The markers do overwrite two facts, whether row 0 and column 0 had a zero *themselves*: save those in two booleans first, and fix row 0 and column 0 last.

```text
   row flags live in column 0, column flags live in row 0

     1  1  1  1                  1  0  1  1      m[0][1] = 0: "zero column 1"
     1  0  1  1   -- mark -->    0  0  1  1      m[1][0] = 0: "zero row 1"
     1  1  1  1                  1  1  1  1
```

```python
def set_zeroes(m):
    R, C = len(m), len(m[0])
    row0 = any(x == 0 for x in m[0])                  # STATE: the two facts the markers overwrite
    col0 = any(m[r][0] == 0 for r in range(R))
    for r in range(1, R):                             # mark: row flags in column 0,
        for c in range(1, C):                         #       column flags in row 0
            if m[r][c] == 0:
                m[r][0] = m[0][c] = 0                 # STEP: flag row r and column c
    for r in range(1, R):                             # apply the flags to the inner cells
        for c in range(1, C):
            if m[r][0] == 0 or m[0][c] == 0:
                m[r][c] = 0                           # RECORD: apply the flags
    if row0:                                          # the marker row and column go LAST
        for c in range(C):
            m[0][c] = 0                               # RECORD: row 0
    if col0:
        for r in range(R):
            m[r][0] = 0                               # RECORD: column 0


z = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
set_zeroes(z)
print(z)    # [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
```

**Try it**
- Print `m` right after the marking loop for `[[1, 1, 1], [1, 0, 1], [1, 1, 1]]`: `[[1, 0, 1], [0, 0, 1], [1, 1, 1]]`. The flags sit in row 0 and column 0, exactly as in the picture.
- Start the two apply loops at 0 (`range(R)` and `range(C)`) and rerun the example: every cell becomes 0. Row 0 is applied first, and its new zeros then look like flags for every column.
- Try the shortcut that drops the booleans: mark from every cell (`range(R)` and `range(C)` in the marking loops), then let `if m[0][0] == 0:` zero both row 0 and column 0. `[[1, 0], [1, 1]]` gives `[[0, 0], [0, 0]]` instead of `[[0, 0], [1, 0]]`: one cell cannot say "row 0" and "column 0" separately.
- Delete `col0` and its block, then run `[[1, 1], [0, 1]]`: you get `[[1, 1], [0, 0]]` instead of `[[0, 1], [0, 0]]`. The original 0 still works as row 1's flag, but nothing ever zeroes column 0.

#### Search a matrix sorted by rows and by columns: the staircase

**Idea:** stand on the top-right corner. It is the largest value in its row and the smallest in its column, so one comparison throws away a whole column (too big: everything below it is even bigger) or a whole row (too small: everything to its left is even smaller). After each step the cells still in play are rows `r..` and columns `..c`, and `(r, c)` is again their top-right corner, so the same argument repeats.

```text
  target = 5                    15 > 5: the column below is all bigger   -> step left
   1   4   7  11  15            11 > 5, then 7 > 5: same                  -> left, left
   2   5   8  12  19             4 < 5: the row to its left is smaller   -> step down
   3   6   9  16  22             5 == 5: found after 5 looks (never more than R + C - 1)
  10  13  14  17  24
  18  21  23  26  30
```

```python
def search_sorted_matrix(m, target):
    if not m or not m[0]:
        return False
    r, c = 0, len(m[0]) - 1                    # top-right corner
    while r < len(m) and c >= 0:               # still inside
        if m[r][c] == target:
            return True
        if m[r][c] > target:
            c -= 1                             # everything below is bigger: drop the column
        else:
            r += 1                             # everything to the left is smaller: drop the row
    return False


sm = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
print(search_sorted_matrix(sm, 5), search_sorted_matrix(sm, 20))   # True False
```

**Try it**
- Count the looks for target 20, which is absent: 9 = R + C − 1. The walk goes 15, 19, 22, 16, 17, 26, 23, 21, 18 and steps off the bottom.
- Start at the bottom-left corner instead (`r, c = len(m) - 1, 0`, move up when too big and right when too small): same answers. That corner is also the biggest of one line and the smallest of the other. The top-left is not: both of its moves go to bigger values.
- Search for 0 and for 31: the walk leaves the grid on the left side and on the bottom side, and both return `False`.

#### Game of Life in place: two states in one cell

**Idea:** every cell must be computed from the *old* board, so writing a new value straight away corrupts neighbours that are read later. A cell needs one bit but an int has plenty: keep today in bit 0, write tomorrow into bit 1, and let neighbours read `cell & 1`. A last pass shifts tomorrow into place. (For values wider than one bit, pack two numbers in base K: `cell = old + K * new`, read the old value with `% K`, and finish with `// K`.)

```text
  value   bit 1 (tomorrow)   bit 0 (today)
    0           0                 0          dead, stays dead
    1           0                 1          alive, dies
    2           1                 0          dead, is born
    3           1                 1          alive, survives
```

```python
def game_of_life(board):
    R, C = len(board), len(board[0])
    for r in range(R):
        for c in range(C):
            live = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if (dr or dc) and 0 <= nr < R and 0 <= nc < C:   # 8 neighbours, inside
                        live += board[nr][nc] & 1          # bit 0 = today, even if bit 1 is set
            if live == 3 or (live == 2 and board[r][c] & 1):
                board[r][c] |= 2                           # tomorrow goes into bit 1
    for r in range(R):
        for c in range(C):
            board[r][c] >>= 1                              # tomorrow becomes today


blinker = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
game_of_life(blinker)
print(blinker)    # [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
```

**Try it**
- Print the board just before the final `>>= 1` pass: `[[0, 2, 0], [1, 3, 1], [0, 2, 0]]`. You can read births (2), deaths (1) and survivors (3) straight off it.
- Replace `board[nr][nc] & 1` with `board[nr][nc]` and rerun the blinker: you get `[[0, 1, 0], [1, 0, 1], [0, 0, 0]]`. Cells already marked 2 or 3 count as two or three neighbours, so the centre "sees" 6 and dies.
- Run `game_of_life` twice on the blinker: it flips back to the horizontal line (it has period 2).
- A 2 x 2 block `[[1, 1], [1, 1]]` never changes: every cell has exactly 3 live neighbours.

#### Traversal patterns: name a line by what stays constant

**Idea:** along a "\" diagonal `r - c` stays the same; along a "/" anti-diagonal `r + c` stays the same; the ring (layer) of a cell is its distance to the nearest edge. So "walk the cells line by line" becomes "group the cells by a key" (the keys are in the table above). A transpose swaps the roles of `r` and `c`; for a non-square grid it must build a new C x R grid.

```python
def group_by(grid, key):                       # key(r, c) -> which line the cell is on
    lines = defaultdict(list)
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            lines[key(r, c)].append(x)         # row-major order inside each line
    return [lines[k] for k in sorted(lines)]


grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
R, C = len(grid), len(grid[0])
print(group_by(grid, lambda r, c: r - c))      # [[4], [3, 8], [2, 7, 12], [1, 6, 11], [5, 10], [9]]
print(group_by(grid, lambda r, c: r + c))      # [[1], [2, 5], [3, 6, 9], [4, 7, 10], [8, 11], [12]]
print(group_by(grid, lambda r, c: min(r, c, R - 1 - r, C - 1 - c)))   # [[1, 2, 3, 4, 5, 8, 9, 10, 11, 12], [6, 7]]
print([list(col) for col in zip(*grid)])       # [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
```

**Try it**
- Reverse every *even-numbered* anti-diagonal and flatten: `[x for k, d in enumerate(group_by(grid, lambda r, c: r + c)) for x in (d[::-1] if k % 2 == 0 else d)]` gives `[1, 2, 5, 9, 6, 3, 4, 7, 10, 11, 8, 12]`, the zigzag order of Diagonal Traverse (498).
- Toeplitz check (766), "every '\' diagonal holds one value": `all(len(set(d)) == 1 for d in group_by(t, lambda r, c: r - c))` is `True` for `t = [[1, 2, 3], [4, 1, 2], [5, 4, 1]]`. Change one cell and watch it turn `False`.
- Walk anti-diagonal `d = 3` straight from the table, without grouping: `[grid[r][d - r] for r in range(max(0, d - C + 1), min(R, d + 1))]` is `[4, 7, 10]`, the same as `group_by(grid, lambda r, c: r + c)[3]`.

### Where it goes wrong

1. **Aliased rows.** `[[0] * C] * R` is R references to one row, so writing one cell writes the whole column. Fix: `[[0] * C for _ in range(R)]`, and copy with `[row[:] for row in grid]` (not `grid[:]`).
2. **Negative indexes do not crash.** `grid[-1][c]` quietly reads the last row, so a missing `0 <= nr` check gives wrong answers instead of an error: the neighbours of `(0, 0)` would include `grid[-1][0] = 9`. Check bounds *before* indexing.
3. **Rows and columns mixed up.** `grid[r][c]`, row first; `R = len(grid)`, `C = len(grid[0])`. Swap `R` and `C` in `neighbors` and, on the 3 x 4 grid, `(2, 0)` gets the neighbour `(3, 0)` (reading it raises `IndexError`) while `(1, 2)` loses `(1, 3)`. A square test grid hides this: always test one non-square grid.
4. **Transposing twice.** `for c in range(n)` swaps every pair twice, so after the row reversal `[[1, 2], [3, 4]]` becomes `[[2, 1], [4, 3]]`, a mirror. Use `range(r + 1, n)`, and after the transpose reverse each *row* (clockwise), not the row order (counter-clockwise).
5. **Spiral without the two re-checks.** A last single row or column is walked twice: `[[1, 2, 3]]` gives `[1, 2, 3, 2, 1]`.
6. **Destroying markers before using them.** In Set Matrix Zeroes, record whether row 0 and column 0 have zeros *first*, and zero them *last*. Without `col0`, `[[1, 1], [0, 1]]` gives `[[1, 1], [0, 0]]`.
7. **Overwriting a value others still need.** In Game of Life, write tomorrow into a spare bit and read `cell & 1`. Without the `& 1`, the blinker gives `[[0, 1, 0], [1, 0, 1], [0, 0, 0]]`.
8. **Staircase from the wrong corner.** From the top-left of `[[1, 4], [2, 5]]` with target 2: 1 is too small, but both moves (to 4 and to 2) go to bigger values, so there is no direction. Start top-right (or bottom-left).
9. **Negative slice stops.** `grid[bottom][right:left - 1:-1]` breaks when `left == 0`: the stop becomes −1, which means "the last item", so `[1, 2, 3, 4][3:-1:-1] == []`. Use `range(right, left - 1, -1)` or `row[left:right + 1][::-1]`.
10. **Rebinding instead of mutating.** Inside `rotate(matrix)`, `matrix = [list(t) for t in zip(*matrix[::-1])]` only rebinds the local name: the caller's `[[1, 2], [3, 4]]` is unchanged. `matrix[:] = ...` mutates it (correct, but it uses O(n²) extra memory).
11. **`zip` gives tuples.** `list(zip(*[[1, 2], [3, 4]]))[0][0] = 9` raises `TypeError`: convert each one with `list(t)`.
12. **`len(grid[0])` on an empty grid** raises `IndexError`: handle `[]` and `[[]]` before anything else.

### Edge cases to say out loud

Empty grid (`[]`, `[[]]`) · 1 x 1 · a single row · a single column · non-square R ≠ C (in-place rotation needs a square) · zeros inside the marker row or column · a target smaller or bigger than everything · a board with nothing alive.

```python
def after(fn, m):                              # run an in-place function on a copy, return the copy
    m = [row[:] for row in m]
    fn(m)
    return m


assert spiral_order([]) == [] and spiral_order([[]]) == []
assert spiral_order([[7]]) == [7]
assert spiral_order([[1, 2, 3]]) == [1, 2, 3]                  # one row: the guards stop the way back
assert spiral_order([[1], [2], [3]]) == [1, 2, 3]              # one column
assert spiral_order([[1, 2], [3, 4], [5, 6]]) == [1, 2, 4, 6, 5, 3]
assert after(rotate_clockwise, [[5]]) == [[5]]
assert after(rotate_clockwise, [[1, 2], [3, 4]]) == [[3, 1], [4, 2]]
assert after(set_zeroes, [[0, 1], [1, 1]]) == [[0, 0], [0, 1]]   # the zero is in the marker corner
assert after(set_zeroes, [[1], [0], [3]]) == [[0], [0], [0]]     # a single column
assert not search_sorted_matrix([[]], 1)
assert not search_sorted_matrix(sm, 0) and search_sorted_matrix(sm, 30) and search_sorted_matrix(sm, 18)
assert after(game_of_life, [[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
print("edge cases pass")
```

**Try it**
- Add `assert after(rotate_by_rings, [[1, 2], [3, 4]]) == [[3, 1], [4, 2]]` and run: the ring version agrees on the smallest ring.
- Predict `after(game_of_life, [[1]])` before running (`[[0]]`: a lonely cell dies), then write it as an assert.
- Feed `after(rotate_clockwise, [[1, 2, 3], [4, 5, 6]])`: no error, but `[[3, 4, 1], [6, 5, 2]]` is not a rotation (a rotated 2 x 3 grid is 3 x 2). In-place rotation only makes sense for a square.

Asserts check the cases you thought of. Simple versions that are hard to get wrong check the ones you didn't: a walker that turns right whenever it is blocked (it needs a `visited` set, which is fine whenever O(R·C) extra space is allowed, and it has no guards to forget), two sets for the zeroes, and the one-line rotation from the map table. Run them side by side on random grids of every shape, 1 x N and N x 1 included. The walker is also the brute force to say first in the interview.

```python
def spiral_brute(grid):                        # the walker: turn right when blocked
    if not grid or not grid[0]:
        return []
    R, C = len(grid), len(grid[0])
    seen, out, r, c, d = set(), [], 0, 0, 0
    TURNS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up: clockwise order
    for _ in range(R * C):                      # one step per cell
        out.append(grid[r][c])
        seen.add((r, c))
        nr, nc = r + TURNS[d][0], c + TURNS[d][1]
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in seen:
            d = (d + 1) % 4                     # blocked: turn clockwise
            nr, nc = r + TURNS[d][0], c + TURNS[d][1]
        r, c = nr, nc
    return out


def zeroes_brute(m):                           # two sets instead of markers
    rows = {r for r, row in enumerate(m) for x in row if x == 0}
    cols = {c for row in m for c, x in enumerate(row) if x == 0}
    return [[0 if r in rows or c in cols else x for c, x in enumerate(row)] for r, row in enumerate(m)]


random.seed(0)
for _ in range(300):
    R, C = random.randint(1, 5), random.randint(1, 5)        # 1 x N and N x 1 included
    m = [[random.randint(0, 3) for _ in range(C)] for _ in range(R)]
    assert spiral_order(m) == spiral_brute(m), m
    assert after(set_zeroes, m) == zeroes_brute(m), m
    sq = [row[:min(R, C)] for row in m[:min(R, C)]]          # the largest square in the corner
    assert after(rotate_clockwise, sq) == [list(t) for t in zip(*sq[::-1])], sq
print("walls, markers and in-place rotation agree with the simple versions on 300 random grids")
```

**Try it**
- Delete the `if top <= bottom:` guard in `spiral_order` (rerun its cell), then rerun this one: the assert stops on the one-row grid `[[3, 0, 2]]` and prints it.
- Do the same with the `if left <= right:` guard: now the one-column grid `[[1], [1], [1]]` is the first to fail. Its three cells come out four times.
- Replace `zip(*sq[::-1])` with `zip(*sq)` (the transpose, not the turn): the rotation check fails on the very first grid.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Rotate counter-clockwise** | transpose, then reverse the row *order* (`m.reverse()`) | 48 (other way) |
| **Rotate 180°** | reverse the row order and reverse every row | 1886 (try all four turns) |
| **Spiral fill** | the same four walls, writing `1, 2, 3, ...` instead of reading | 59 |
| **Spiral outward from a cell** | step lengths 1, 1, 2, 2, 3, 3, ...; record only the steps that land inside | 885 |
| **Zigzag diagonals** | group by `r + c`, reverse every other group | 498 |
| **Toeplitz check** | every cell equals its up-left neighbour (`r - c` is constant) | 766 |
| **Transpose a non-square** | a new C x R grid: `[list(col) for col in zip(*grid)]` | 867 |
| **Shift the grid k steps** | flat index: the cell at `i` moves to `(i + k) % (R * C)` | 1260 |
| **Fully sorted (row-major) matrix** | one sorted array of R·C items: binary search on the flat index (see [Binary Search](#s09)) | 74 |
| **k-th smallest in a sorted matrix** | binary search on the value; a staircase counts the cells ≤ mid | 378 |
| **Sparse matrix multiplication** | multiply only the non-zero entries | 311 |
| **Tic-tac-toe on n x n** | +1/−1 counters per row, column, diagonal (`r == c`) and anti-diagonal (`r + c == n - 1`); a counter reaching ±n wins; O(1) per move | 348 |
| **Queens and diagonals** | `r - c` and `r + c` as set keys | 51, 52 |
| **Candy Crush** | mark the crushed cells by negating them, then compact each column bottom-up with a write pointer | 723 |
| **Rotating the Box** | slide the stones to the right end of each row (stopping at obstacles), then rotate clockwise | 1861 |
| **Game of Life on an unbounded board** | a set of live cells; count neighbours with a `Counter` | 289 follow-up |

**k-th smallest in a sorted matrix** (378). The cells ≤ v can be *counted* with a staircase in O(R + C): from the bottom-left, a cell ≤ v counts together with everything above it. That count only grows with v, so binary-search the smallest v whose count reaches k (binary search on the answer, as in [Binary Search](#s09)). That v is always a matrix value: if it weren't, `count(v - 1)` would be the same, and v would not be the smallest.

```python
def count_at_most(m, v):                       # staircase from the bottom-left: cells <= v
    r, c, count = len(m) - 1, 0, 0
    while r >= 0 and c < len(m[0]):
        if m[r][c] <= v:
            count += r + 1                     # this cell and everything above it
            c += 1
        else:
            r -= 1                             # too big, and so is the rest of this row
    return count


def kth_smallest(m, k):
    lo, hi = m[0][0], m[-1][-1]                # the answer is a value in [lo, hi]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_at_most(m, mid) >= k:
            hi = mid                           # mid is enough: the answer is <= mid
        else:
            lo = mid + 1                       # too few cells <= mid: the answer is bigger
    return lo


sorted_m = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
print(kth_smallest(sorted_m, 8), [count_at_most(sorted_m, v) for v in (11, 12, 13)])   # 13 [5, 6, 8]
```

**Try it**
- `count_at_most(sorted_m, 14)` is also 8, but 14 is not in the matrix. It can never be the answer: 13 already reaches the same count, and the search looks for the *smallest* such v.
- Change `hi = mid` to `hi = mid - 1`: `kth_smallest(sorted_m, 6)` returns 11 instead of 12. `mid = 12` was itself the answer, and it got thrown away.
- `kth_smallest(sorted_m, 7)` and `kth_smallest(sorted_m, 8)` are both 13: duplicates take one rank each.

**Two Google favourites.** Sparse Matrix Multiplication (311): a zero adds nothing to `out[i][j] = sum(A[i][k] * B[k][j])`, so keep only the non-zero entries of each row of B and skip the zeros of A. Game of Life on an unbounded board: the board no longer fits in a grid, so keep the *set* of live cells and let each one vote for its 8 neighbours; a `Counter` of the votes is the neighbour count.

```python
def multiply_sparse(A, B):                     # A is R x K, B is K x C
    nz_B = [[(j, v) for j, v in enumerate(row) if v] for row in B]   # non-zeros of each row of B
    out = [[0] * len(B[0]) for _ in A]
    for i, row in enumerate(A):
        for k, a in enumerate(row):
            if a:                              # a zero in A meets nothing
                for j, b in nz_B[k]:
                    out[i][j] += a * b
    return out


def life_step(live):                           # live = a set of (r, c): no borders at all
    votes = Counter((r + dr, c + dc) for r, c in live
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc)
    return {cell for cell, k in votes.items() if k == 3 or (k == 2 and cell in live)}


print(multiply_sparse([[1, 0, 0], [-1, 0, 3]], [[7, 0, 0], [0, 0, 0], [0, 0, 1]]))   # [[7, 0, 0], [-7, 0, 3]]
print(sorted(life_step({(1, 0), (1, 1), (1, 2)})))   # [(0, 1), (1, 1), (2, 1)]
```

**Try it**
- Count the multiplications with a counter in the innermost loop: 3 for this example, against 2 · 3 · 3 = 18 for the plain triple loop.
- Run `life_step` twice on the blinker: you are back at `{(1, 0), (1, 1), (1, 2)}`.
- A glider walks: run `life_step` four times on `{(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)}` and every cell has moved one step down and one step right.

### Say it in the interview

> "First the brute force: a walker with a visited set that turns right whenever it's blocked. That's O(R·C) time and O(R·C) extra space. The visited set is the waste: the unvisited cells always form a rectangle, so four walls describe them. I walk the top row, the right column, the bottom row and the left column, moving each wall in right after I walk it, and I re-check before the last two sides because the rectangle can shrink to a single row or column. O(R·C) time, O(1) extra space."

Then point at the two re-checks, and test a 1 x 3, a 3 x 1 and one non-square grid out loud. For the other tools, the line to point at is the one that makes in-place safe: `range(r + 1, n)` in the transpose, "flags first, borders last" in Set Matrix Zeroes, `& 1` in Game of Life.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Game of Life | `practice/simple/basics/matrices/05_game_of_life_in_place.py` | today in bit 0, tomorrow in bit 1; neighbours read `cell & 1`; shift everything at the end |
| Rotate Image | `math_geometry/rotate_image.py` · `practice/simple/basics/matrices/01_rotate_image.py` | clockwise = transpose (swap only above the diagonal) + reverse each row |
| Search a 2D Matrix II | `practice/simple/basics/matrices/04_search_2d_matrix_staircase.py` | start top-right: too big drops a column, too small drops a row; O(R + C) |
| Set Matrix Zeroes | `math_geometry/set_matrix_zeroes.py` · `practice/simple/basics/matrices/03_set_matrix_zeroes.py` | row 0 and column 0 hold the flags; remember their own zeros first, zero them last |
| Spiral Matrix | `math_geometry/spiral_matrix.py` · `practice/simple/basics/matrices/02_spiral_matrix.py` | four inclusive walls; walk a side, move its wall in; re-check before the bottom and left sides |

### Self-check

1. Why does the spiral need `if top <= bottom` before the bottom row, but no check before the right column?
<details><summary>Answer</summary>After <code>top += 1</code> there may be no rows left. The right-column loop is then simply empty (its <code>range(top, bottom + 1)</code> has nothing in it), but the bottom-row loop would walk the row we just walked, backwards. The <code>if</code> stops that. The same reasoning puts <code>if left &lt;= right</code> before the left column.</details>

2. In Set Matrix Zeroes, why is it safe to overwrite `m[r][0]` with a flag?
<details><summary>Answer</summary>We only write it when row r contains a zero, and then the whole row, including <code>m[r][0]</code>, ends up zero anyway. The one fact that writing destroys is whether column 0 itself held a zero, and that was saved in <code>col0</code> before marking began.</details>

3. Which corners can the staircase search start from, and why not the top-left?
<details><summary>Answer</summary>Top-right or bottom-left: each is the largest value of one line and the smallest of the other, so every comparison rules out a whole row or column. From the top-left both moves go to bigger values, so when the value is too small you don't know which way to go.</details>

4. Where does `(r, c)` go in a clockwise turn of an R x C grid, and how do you check it?
<details><summary>Answer</summary>To <code>(c, R-1-r)</code>, in a new C x R grid. Check two cells: <code>(0, 0)</code> must land in the top-right corner, <code>(0, R-1)</code>, and <code>(0, 1)</code> must land one row below it, <code>(1, R-1)</code>. Then try the map on a non-square grid.</details>
