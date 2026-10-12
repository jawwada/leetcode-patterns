# Spiral Matrix

*LeetCode 54 · Medium · Pattern: Shrinking boundary traversal · Reading time ~6 min*

## The problem

Given an m x n matrix, return all its elements in clockwise spiral order starting at the top-left and moving right.

```text
Example: [[1,2,3],[4,5,6],[7,8,9]] -> [1, 2, 3, 6, 9, 8, 7, 4,
  5].
```

## What the problem is really asking

You get an `m x n` grid, not necessarily square. Read every cell exactly once in clockwise spiral order: across the top row, down the right edge, back along the bottom, up the left edge, then repeat on the smaller rectangle inside, until nothing is left.

The answer is a flat list of all `m * n` values in that order. Nothing about it is computationally heavy; every cell is visited once, so `O(mn)` is unavoidable and easy. What makes it hard is *correctness at the edges*: the innermost layer can be a single row, a single column or a single cell, and a naive walk emits some of those cells twice.

```text
 3 x 4 grid                 spiral order
  1  2  3  4      ->  1 2 3 4 8 12 11 10 9 5 6 7
  5  6  7  8
  9 10 11 12          path:  -> -> -> v
                             ^  -> ->  v   (inner row 6 7)
                             <- <- <- v
```

## Do it by hand first

Put your finger on `1` and trace. Right to `4`. You hit the wall, turn down: `8`, `12`. Wall, turn left: `11`, `10`, `9`. Turn up: `5`. Now the next cell up is `1`, which you already read, so that counts as a wall too. Turn right: `6`, `7`. Turn down: nothing new. Done.

```text
 hand trace, cells numbered by visit order
    1  2  3  4          visit:  1  2  3  4
    5  6  7  8                 10 11 12  5
    9 10 11 12                  9  8  7  6
```

What did your hand keep track of? Two things: which way you are going, and where the "walls" are. At first the walls are the grid edges. After one lap, the walls are the edges of the part you have not read yet. That unread part is always a rectangle. That is the seed.

## The first honest attempt

Simulate the finger literally. Keep a `visited` grid of booleans, a position `(r, c)` and a direction from the list right, down, left, up. At each step emit the cell, mark it, and look one step ahead; if the next cell is out of bounds or already visited, rotate the direction clockwise. Stop after `m * n` emissions.

This is correct and `O(mn)` time. The cost is `O(mn)` extra space for `visited`, plus a bounds-and-visited check on every single step.

Where is the waste? The visited grid records, cell by cell, information that is fully described by four numbers. Look at the visited cells after one lap:

```text
 visited after the first lap (X = visited)
   X X X X
   X . . X     the unvisited part is the rectangle
   X X X X     rows 1..1, columns 1..2
 the grid stores 12 booleans to say "top=1, bottom=1,
 left=1, right=2"
```

## The turning point

**Claim: the unvisited cells always form one rectangle, `top..bottom x left..right`, and each side of the walk consumes exactly one edge of it.**

Why is that true? Start with the whole grid: one rectangle. Walk its top row completely, left to right. What is unvisited now is the same rectangle minus its top row, which is again a rectangle with `top` one larger. Walk its right column completely, top to bottom: remove that column, `right` one smaller. The bottom row, right to left: `bottom` one smaller. The left column, bottom to top: `left` one larger. Each move shrinks one bound by one and keeps the rectangle shape. So the four integers `top, bottom, left, right` carry all the state the walker needs, and a `visited` grid is unnecessary.

This turns the simulation into a loop over *layers*:

```text
 one layer, bounds before the lap: top=T, bottom=B,
 left=L, right=R
        L           R
   T    a  a  a  a  a      a: top row  L..R   then T += 1
        d  .  .  .  b      b: right col T..B  then R -= 1
        d  .  .  .  b      c: bottom row R..L then B -= 1
   B    c  c  c  c  b      d: left col B..T   then L += 1
```

The edge cases come from the shrinking. After the top row and right column are consumed, the remaining rectangle may already be empty in one dimension. If only one row was left, the "bottom row" *is* the top row you just read; walking it again duplicates it. If only one column was left, the left column is the right column you just read. So before the bottom row, re-check `top <= bottom`; before the left column, re-check `left <= right`. Those two guards are the entire difficulty of the problem.

```text
 the trap: a 1 x 3 remainder (top == bottom)
   [ 6  7  8 ]   top row reads 6 7 8, top becomes > bottom
                 right column is empty, right moves to 7
   without the guard, bottom row reads 7 6 again
```

The loop condition `top <= bottom and left <= right` says "the rectangle is non-empty", and it is checked once per layer.

## Watch it work

Example: the 3x4 grid `1..12`. Notation: `T B L R` are the bounds; `#` marks emitted cells.

Frame 1 — layer 0 begins: `T=0 B=2 L=0 R=3`; the rectangle is the whole grid.

```text
        L           R
   T    1   2   3   4       out: []
        5   6   7   8
   B    9  10  11  12
```

Frame 2 — top row `L..R` emitted, then `T=1`.

```text
        #   #   #   #       out: 1 2 3 4
   T    5   6   7   8       T=1 B=2 L=0 R=3
   B    9  10  11  12
```

Frame 3 — right column rows `T..B` emitted (`8`, `12`), then `R=2`. Guard `T<=B` (1<=2) holds.

```text
        #   #   #   #       out: 1 2 3 4 8 12
   T    5   6   7   #       T=1 B=2 L=0 R=2
   B    9  10  11   #
        L       R
```

Frame 4 — bottom row `R..L` emitted (`11 10 9`), then `B=1`. Guard `L<=R` (0<=2) holds.

```text
        #   #   #   #       out: ... 8 12 11 10 9
   TB   5   6   7   #       T=1 B=1 L=0 R=2
        #   #   #   #
```

Frame 5 — left column rows `B..T` emitted (just `5`), then `L=1`. Layer 0 done.

```text
        #   #   #   #       out: ... 11 10 9 5
   TB   #   6   7   #       T=1 B=1 L=1 R=2
        #   #   #   #            remaining: 1 x 2
            L   R
```

Frame 6 — layer 1: top row emits `6 7`, `T=2`. Right column `T..B` is empty (2>1), `R=1`. Guard `T<=B` fails: bottom row skipped. Guard `L<=R` (1<=1) holds but rows `B..T` (1 down to 2) is empty. `L=2`; loop ends.

```text
        #   #   #   #       out: 1 2 3 4 8 12 11 10 9 5 6 7
        #   #   #   #       T=2 B=1 L=2 R=1 -> empty
        #   #   #   #       12 cells, each once
```

Across every frame the unemitted cells were exactly the rectangle `T..B x L..R`, and each emission removed one full edge of it. When `T > B` or `L > R` the rectangle is empty, which is why the loop stops with every cell emitted once.

## Why it is correct

Invariant: *at the start of each side, the cells not yet emitted are exactly the rectangle `top..bottom x left..right`, and the output so far is the spiral order of everything outside it.*

Initially the rectangle is the whole grid and the output is empty. Walking the top row emits row `top` from `left` to `right`, which is precisely the next stretch of the spiral; incrementing `top` restores the invariant. The same holds for the right column (rows `top..bottom` of column `right`, then `right -= 1`), and so on.

The guards keep the invariant honest. After the first two sides, if `top > bottom` the rectangle has no rows, so there is no bottom row to walk; walking anyway would re-emit cells outside the rectangle. Likewise for `left > right` and the left column. Python's empty `range` covers the remaining degenerate cases, as frame 6 showed. Since each emission removes a cell from the rectangle and the loop runs until the rectangle is empty, every cell is emitted exactly once, in spiral order.

## Cost

- **Time:** `O(mn)` — each cell is appended once; each layer's bookkeeping is `O(1)`.
- **Space:** `O(1)` extra beyond the output — four integers replace the `O(mn)` visited grid of the simulation.

## Variations you will meet

- **Spiral Matrix II (LeetCode 59).** Fill an `n x n` grid with `1..n^2` in spiral order. Identical bounds loop; write `counter` instead of reading. Being square, the guards matter only at the center.
- **Spiral Matrix III (LeetCode 885).** Start in the middle and spiral *outward*, possibly leaving the grid. Bounds no longer shrink; instead the run lengths follow `1, 1, 2, 2, 3, 3, ...`, and you only record steps that land inside.
- **Spiral Matrix IV (LeetCode 2326).** Fill from a linked list, `-1` where the list runs out. Same loop, consuming list nodes.
- **Rotate a layer, or rotate the grid ring by ring.** Rotate Image's four-cycle variant iterates layers exactly like this; the bound variables are the same `top/bottom/left/right`.

## What to carry forward

When a walk's turning points are predictable, replace the visited set with the bounds of the unvisited region; re-check the bounds whenever one moves mid-loop.

The next problem, Set Matrix Zeroes, stays on the board but uses its edges differently: the first row and column become *storage* for flags, and the order of writes decides whether those flags survive.
