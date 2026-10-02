# Valid Sudoku

*LeetCode 36 · Medium · Pattern: Hash set per row/column/box · Reading time ~6 min*

## What the problem is really asking

You get a 9x9 board, partly filled with digits `'1'` to `'9'` and `'.'` for blanks. Decide whether the filled cells
break any rule: no digit may repeat in a row, in a column, or in any of the nine 3x3 boxes. You do not have to solve the
puzzle or decide whether it can be solved. Only the digits already on the board matter.

The answer is a yes/no. What makes it a little fiddly is that each cell belongs to three groups at once, and one of those
groups, the box, is not a row or a column of the grid but a block you have to locate with arithmetic.

```text
     c: 0 1 2   3 4 5   6 7 8
r 0     8 3 . | . 7 . | . . .
r 1     6 . . | 1 9 5 | . . .
r 2     . 9 8 | . . . | . 6 .     <- 8 at (2,2) and 8 at
        ------+-------+------        (0,0) share box 0
r 3     8 . . | . 6 . | . . 3     <- and (0,0), (3,0) share
r 4     4 . . | 8 . 3 | . . 1        column 0
r 5     7 . . | . 2 . | . . 6
        ------+-------+------
r 6     . 6 . | . . . | 2 8 .
r 7     . . . | 4 1 9 | . . 5
r 8     . . . | . 8 . | . 7 9     answer: False
```

This is LeetCode's valid example board with the top-left 5 changed to 8. That one edit breaks two rules.

## Do it by hand first

A human checks this in units: read row 0, are the digits distinct? Row 1? Then the columns, then the boxes. Twenty-seven
units, each "are these up to nine digits all different?"

How do you check one unit by hand? You read the digits and keep a mental tick list: "8, 3, 7: haven't seen 7, tick it".
The moment you meet a digit already ticked, the unit is broken. That tick list is a set.

```text
box 0 by hand:  8 3 . 6 . . . 9 8
tick list:  {8} {8,3} {8,3,6} {8,3,6,9}
then 8 -> already ticked!
```

So the structure is a set per unit. Doing the 27 units one after another reads every cell three times. Can one sweep
feed all three of a cell's sets at once? Yes, if we can work out which box a cell belongs to.

## The first honest attempt

For each filled cell `(r, c)` with digit `d`, scan all of row `r`, all of column `c`, and the whole box for another `d`.
That is 81 cells times up to 27 lookups each.

On a fixed 9x9 board, any algorithm is O(1), so the honest framing is the general `n x n` board (with `sqrt(n)` boxes):
each cell scans `O(n)` other cells, for `O(n^3)` total. The waste: row `r` is scanned once by every filled cell in it,
nine times instead of once, and every pair of cells in a unit gets compared twice (once from each side).

```text
row 0: 8 3 . . 7 . . . .
from (0,0): scan 3 . . 7 . . . .
from (0,1): scan 8 . . 7 . . . .   same row again
from (0,4): scan 8 3 . . . . . .   and again
```

## The turning point

Claim: validity is 27 independent "all distinct" checks, and "all distinct" over a stream of items is exactly "insert
into a set; fail if it is already there".

So give every unit its own set: `rows[0..8]`, `cols[0..8]`, `boxes[0..8]`. Sweep the board once in row-major order. For
each filled cell, test its digit against its three sets; if any already holds it, return False; otherwise insert it into
all three. If the sweep finishes, return True. Every unit received each of its digits exactly once, and a repeat is caught
the moment the second copy arrives.

The only non-obvious piece is the box number. Boxes form their own 3x3 grid. Row `r` sits in box-row `r // 3`, column `c`
sits in box-column `c // 3`, and numbering boxes left to right, top to bottom gives:

```text
b = (r // 3) * 3 + c // 3

            c//3: 0     1     2
r//3 = 0       [ b0 ][ b1 ][ b2 ]
r//3 = 1       [ b3 ][ b4 ][ b5 ]
r//3 = 2       [ b6 ][ b7 ][ b8 ]

cell (4, 7): r//3 = 1, c//3 = 2 -> b = 1*3 + 2 = 5
```

This is the same move as turning a 2D index into a 1D one, `row * width + col`, applied to the coarse grid of boxes. It
is the "index as hash" idea from the background: we did not need to hash the box; we computed its slot.

Here is how the sets look in memory: three arrays of nine sets each, and each cell points into one slot of each array.

```text
rows : [ s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8 ]
cols : [ s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8 ]
boxes: [ s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8 ]
cell (2,2) -> rows[2], cols[2], boxes[0]
```

## Watch it work

The board above, sweeping row by row. Only filled cells do anything.

Frame 1

```text
row 0: 8 3 . . 7 . . . .
rows[0] = {8,3,7}
cols[0] = {8}  cols[1] = {3}  cols[4] = {7}
boxes[0] = {8,3}   boxes[1] = {7}
```

Row 0 has three digits; no set contained them, so each goes into its three sets.

Frame 2

```text
row 1: 6 . . 1 9 5 . . .
rows[1] = {6,1,9,5}
cols[0] = {8,6}  cols[3] = {1}  cols[4] = {7,9}
boxes[0] = {8,3,6}   boxes[1] = {7,1,9,5}
```

Still no clash. Box 1 now holds the 7 from row 0 and three digits from row 1.

Frame 3

```text
row 2: . 9 8 . . . . 6 .
          ^ (2,1) d=9  b = 0*3 + 1//3 = 0
rows[2] = {}  cols[1] = {3}  boxes[0] = {8,3,6}
9 in none of them -> insert
boxes[0] = {8,3,6,9}
```

The 9 at `(2,1)` passes all three checks.

Frame 4

```text
row 2: . 9 8 . . . . 6 .
            ^ (2,2) d=8  b = 0*3 + 2//3 = 0
rows[2] = {9}  cols[2] = {}  boxes[0] = {8,3,6,9}
                                         ^ 8 already here
return False
```

The 8 from `(0,0)` is waiting in box 0. We never reach row 3, where column 0 would also have complained.

Invariant across frames: after each processed cell, every set holds exactly the digits of its unit that the sweep has
passed, and no set contains a repeat.

## Why it is correct

Before each cell, each of the 27 sets contains exactly the digits already swept in its unit, each once. When a filled
cell `(r, c)` with digit `d` arrives:

- If `d` is already in `rows[r]`, `cols[c]` or `boxes[b]`, an earlier cell in that same unit holds `d`, so the board is
  genuinely invalid. Returning False is correct.
- Otherwise inserting `d` into the three sets keeps the invariant for the next cell.

If the board is invalid, some unit has two cells with the same digit; when the sweep reaches the later of the two, the
earlier is already in that unit's set and the check fires. If we finish without firing, no unit ever saw a repeat, so
the board is valid.

The box formula is correct because `r // 3` and `c // 3` each take values 0, 1, 2, and `3 * x + y` is a bijection from
those pairs to 0..8, so different boxes never share a set.

## Cost

- Time: O(1) for the fixed 81-cell board; for an `n x n` board, O(n^2): each cell does three average O(1) set operations.
- Space: O(1) for 9x9; O(n^2) in general (27 sets, at most 81 entries total for 9x9).

A tighter variant replaces each set with a 9-bit integer: bit `d` set means digit `d` seen. `mask & (1 << d)` tests and
`mask |= 1 << d` inserts. Same asymptotics, smaller constants.

## Variations you will meet

- **One set of strings.** Insert tokens like `"8 in row 0"`, `"8 in col 0"`, `"8 in box 0 0"` into a single set. Same
  logic; the unit identity moves into the key.
- **Sudoku Solver.** Now you must fill the blanks. The same three-set bookkeeping becomes the legality check inside a
  backtracking search, with an undo (remove from the sets) when you backtrack.
- **Validate an n x n Latin square or a general grid with regions.** Replace the box formula with whatever maps a cell to
  its region, often a precomputed region id per cell.
- **Detect the duplicate's location.** Store value to cell coordinates in each unit (a dict instead of a set) to report
  which two cells conflict.

## What to carry forward

"All distinct" is a set with a collision check, and when items belong to several groups, compute each group's slot by
arithmetic and feed all of them in one sweep. The next problem keeps the dict but changes the key: instead of grouping by
a computed position, we group by a computed fingerprint of the item itself.
