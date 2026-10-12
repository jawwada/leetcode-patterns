# Rotate Image

*LeetCode 48 · Medium · Pattern: Transpose + reverse rows (in-place matrix rotation) · Reading time ~6 min*

## The problem

Rotate an n x n matrix by 90 degrees clockwise in place, without allocating a second matrix.

```text
Example: [[1,2,3],[4,5,6],[7,8,9]] -> [[7,4,1],[8,5,2],[9,6,3]].
```

## What the problem is really asking

You get an `n x n` grid of numbers. Turn it a quarter turn clockwise, like rotating a photo on your phone, and do it *in place*: the same list of lists must hold the rotated picture afterwards, and you are not allowed a second grid.

The answer is not a value but a rearrangement. Every cell has to end up somewhere specific, and the difficulty is purely logistical: when you write a value into its destination, you overwrite whatever was sitting there, and that value still needs to get to *its* destination.

```text
 before (n = 3)          after (clockwise)
 1 2 3                   7 4 1
 4 5 6        ->         8 5 2
 7 8 9                   9 6 3
 top row 1 2 3 became the right column, read top to bottom
```

## Do it by hand first

With a pencil you would not think about overwriting at all. You would read the old picture and draw a new one. Look at where things go:

- The top row `1 2 3` becomes the right column.
- The left column `1 4 7`, read bottom to top (`7 4 1`), becomes the top row.
- The center `5` stays.

Write it as coordinates. Cell `(r, c)` lands at `(c, n-1-r)`. Check: `1` is at `(0,0)` and goes to `(0,2)`; `3` at `(0,2)` goes to `(2,2)`; `7` at `(2,0)` goes to `(0,0)`. Yes.

```text
 (r, c) -> (c, n-1-r)
   1 at (0,0) -> (0,2)      3 at (0,2) -> (2,2)
   9 at (2,2) -> (2,0)      7 at (2,0) -> (0,0)
 the four corners chase each other in a 4-cycle
   (0,0) -> (0,2) -> (2,2) -> (2,0) -> (0,0)
```

What did your hand keep track of? The *formula* `(r, c) -> (c, n-1-r)`, and a second sheet of paper to draw on. The formula is the seed. The second sheet is what we must get rid of.

## The first honest attempt

The direct translation of "draw a new picture": allocate `rotated = [[0]*n for _ in range(n)]`, set `rotated[c][n-1-r] = matrix[r][c]` for every cell, then copy `rotated` back row by row.

It is correct and it is `O(n^2)` time, which is optimal, since every cell has to move. The problem is space: `O(n^2)` extra. Where is the waste? Every value is written twice, once into the copy and once back, and the copy exists only because we did not know an order of writes that avoids clobbering values we still need.

```text
 the clobbering problem, writing in place naively
 step: put 1 (from (0,0)) into (0,2)
   1 2 1   <- 3 is gone, and it still had to go to (2,2)
   4 5 6
   7 8 9
```

You could fix that by saving the overwritten value and following the 4-cycle `(0,0) -> (0,2) -> (2,2) -> (2,0)` around the ring, one temp variable at a time. That works, and it is the classic "rotate four cells at once" answer, but the index arithmetic for every ring and every offset is a reliable source of off-by-one bugs at a whiteboard.

## The turning point

**Claim: a 90-degree rotation is a reflection across the main diagonal followed by a left-right mirror, and each reflection is trivially in place.**

Why is a reflection easy? A reflection pairs cells up: cell A goes to B and B goes to A. So you swap them. Nothing is ever overwritten before it is read, because a swap reads both cells first. No temp grid, no cycle-chasing.

Now check the composition with the formulas.

- Transpose: `(r, c) -> (c, r)`.
- Mirror each row: `(r, c) -> (r, n-1-c)`.
- Apply transpose first, then mirror: `(r, c) -> (c, r) -> (c, n-1-r)`.

That is exactly the rotation formula from the hand solution. The algebra is the proof.

```text
 the card picture
   original         flip on diagonal     turn the page
   1 2 3            1 4 7                7 4 1
   4 5 6     ->     2 5 8        ->      8 5 2
   7 8 9            3 6 9                9 6 3
           (r,c)->(c,r)         (r,c)->(r,n-1-c)
```

The only care needed is in the transpose loop. If you loop over *all* `(r, c)` and swap, every off-diagonal pair is swapped twice (once when you visit `(r, c)`, once when you visit `(c, r)`) and the matrix comes back unchanged. So visit only cells strictly above the diagonal: `c` runs from `r + 1` to `n - 1`. The diagonal itself is the mirror line and never moves.

The mirror step is just `row.reverse()` on each row, which Python does in place.

The other rotations fall out of the same toolkit, which is the real payoff of thinking in reflections:

```text
 clockwise          transpose, then mirror rows (left<->right)
 counter-clockwise  transpose, then mirror columns (top<->bot)
 180 degrees        mirror rows, then mirror columns
```

## Watch it work

Example: the 3x3 grid `1..9`. Above-diagonal cells are `(0,1)`, `(0,2)`, `(1,2)`.

Frame 1 — start. Transpose will visit `(r, c)` with `c > r`.

```text
      c=0 c=1 c=2
 r=0   1   2   3      above diagonal: (0,1) (0,2) (1,2)
 r=1   4   5   6      diagonal 1 5 9 stays put
 r=2   7   8   9
```

Frame 2 — swap `(0,1)` with `(1,0)`: `2` and `4` trade places.

```text
 r=0   1  [4]  3
 r=1  [2]  5   6
 r=2   7   8   9
```

Frame 3 — swap `(0,2)` with `(2,0)`: `3` and `7` trade places.

```text
 r=0   1   4  [7]
 r=1   2   5   6
 r=2  [3]  8   9
```

Frame 4 — swap `(1,2)` with `(2,1)`: `6` and `8` trade. Transpose done; rows are now the old columns.

```text
 r=0   1   4   7
 r=1   2   5  [8]
 r=2   3  [6]  9
```

Frame 5 — reverse each row in place. This is the clockwise rotation.

```text
 r=0   7   4   1      row0 reversed
 r=1   8   5   2      row1 reversed
 r=2   9   6   3      row2 reversed
```

Invariant across frames 2 to 4: every mirror pair already visited holds its two values exchanged (final for the transpose), and every pair not yet visited still holds its original two values, untouched. Each swap finalises two cells and touches nothing else. During frame 5, each row is independent, so reversing one never disturbs another.

## Why it is correct

Two facts.

First, the transpose loop visits each unordered pair `{(r, c), (c, r)}` with `r != c` exactly once, because it only ever visits the member with `c > r`. A swap exchanges the pair. So after the loop, `matrix[r][c]` holds what was at `(c, r)`: the grid is the transpose. Diagonal cells are their own partners and are correctly left alone.

Second, reversing row `r` sends column `c` to column `n-1-c` within that row, for every row. Composing: the value originally at `(r, c)` sat at `(c, r)` after the transpose and at `(c, n-1-r)` after the mirror. That is the definition of a clockwise quarter turn, so every value lands where it should, and since both steps are bijections on positions, no value is lost or duplicated.

## Cost

- **Time:** `O(n^2)` — the transpose does `n(n-1)/2` swaps and the mirror does `n * floor(n/2)` swaps; each cell moves at most twice.
- **Space:** `O(1)` extra — swaps use Python's tuple assignment, no scratch grid.

The brute force was `O(n^2)` time too; the improvement is entirely in space, from `O(n^2)` to `O(1)`.

## Variations you will meet

- **Counter-clockwise rotation.** Transpose, then reverse the *order of rows* (`matrix.reverse()`), or equivalently reverse each row first and then transpose. Check with a corner: `(0,0)` must end at `(n-1, 0)`.
- **Rotate a non-square `m x n` matrix.** In place is impossible, since the shape changes to `n x m`. You must build a new matrix: `[list(row) for row in zip(*matrix[::-1])]` is clockwise in one line.
- **Determine Whether Matrix Can Be Obtained by Rotation (LeetCode 1886).** Apply the in-place rotation up to four times and compare after each. Same tool, used as a subroutine.
- **The four-cell cycle version.** For each ring `layer` and offset `i`, rotate the four cells `(layer, layer+i)`, `(layer+i, last)`, `(last, last-i)`, `(last-i, layer)` with one temp. Same complexity, fewer total writes (each cell written once), more indices to get right.

## What to carry forward

A grid move is a formula on `(r, c)`; when a move is hard to do in place, factor it into reflections, because reflections are just swaps.

The next problem, Spiral Matrix, keeps the board and the coordinate thinking, but instead of moving cells it walks them in layers, replacing a visited grid with four moving bounds.
