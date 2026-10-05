# Maximal Rectangle

*LeetCode 85 · Hard · Pattern: Monotonic stack · Reading time ~11 min*

## The problem

Given an m x n binary matrix of '0'/'1' characters, return the area of the largest rectangle containing only '1's.

```text
Example:
  [["1","0","1","0","0"],
   ["1","0","1","1","1"],
   ["1","1","1","1","1"],
   ["1","0","0","1","0"]]
  -> 6, the 2 x 3 block of 1s in rows 1-2, columns 2-4.
```

## What the problem is really asking

You get an `m x n` grid of `'0'` and `'1'` characters. Find the largest axis-aligned rectangle made only of `'1'` cells, and return its area.

The answer is one number, but the search space is enormous: a rectangle is any choice of top row, bottom row, left column and right column, so there are O(m^2 n^2) of them. What makes it hard is that "all ones" is a condition over a 2-D block, and checking blocks one by one is hopeless. The way out is to notice that you already know how to solve the 1-D version.

```text
board:                 stored as:
     c0 c1 c2 c3 c4    matrix[r][c] is "0"/"1"
r0:   1  0  1  0  0    (strings, not ints)
r1:   1  0 [1  1  1]
r2:   1  1 [1  1  1]
r3:   1  0  0  1  0

[ ] = best rectangle: rows 1-2, cols 2-4, area 6
```

## Do it by hand first

Look for the answer on paper and notice how you do it. You find a promising bottom edge, a row with a long run of ones, and then you look *up* from each cell of that run to see how many ones stand above it. The rectangle can only go as high as the shortest of those columns.

```text
bottom edge = row 2:
     c0 c1 c2 c3 c4
r0:   1  .  1  .  .
r1:   1  .  1  1  1
r2:   1  1  1  1  1
      |  |  |  |  |
up:   3  1  3  2  2     <- ones stacked above
                           (and including) row 2
```

Those counts are a histogram standing on row 2. "The largest all-ones rectangle whose bottom edge is on row 2" is precisely "the largest rectangle in this histogram". Bars 2..4 with heights 3, 2, 2 give `min = 2`, width 3, area 6. What your hand tracked was, per column, the height of the tower of ones ending at the current row. That array is the seed; the previous problem's stack does the rest.

## The first honest attempt

Enumerate every top-left corner `(r1, c1)` and every bottom-right corner `(r2, c2)`, then check that every cell inside is `'1'`. That is O(m^2 n^2) rectangles times O(mn) per check: O(m^3 n^3) time, O(1) space.

```text
rect (r1,c1)-(r2,c2)      rect (r1,c1)-(r2,c2+1)
   [1 1 1]                   [1 1 1 1]
   [1 1 1]                   [1 1 1 1]
    ~~~~~                     ~~~~~
two checks share every cell but the new
column; both rescan them from scratch
```

The obvious waste is that neighbouring rectangles share almost all their cells. A smarter brute force fixes a bottom row and keeps a running column-minimum, which is O(m n^2), but it still re-scans each row's histogram pairwise. The deeper waste is that we have not yet recognised the histogram problem hiding inside.

## The turning point

**Claim: every all-ones rectangle has a bottom row, and among rectangles with bottom row `r`, the largest is the largest rectangle in the histogram `height[c] = number of consecutive ones ending at (r, c)`.**

Why? A rectangle with bottom row `r` spanning columns `c1..c2` and `k` rows tall is all ones exactly when every column in `c1..c2` has at least `k` consecutive ones ending at row `r`, that is, `k <= min(height[c1..c2])`. The tallest such rectangle has height equal to that minimum. That is the histogram definition word for word.

Two structural facts make this cheap.

1. **Heights update in O(n) per row.** Going from row `r-1` to row `r`, a `'1'` extends its tower by one, and a `'0'` knocks it to the ground: `height[c] = height[c] + 1` if the cell is `'1'`, else `0`. No rescanning upward.
2. **Each histogram is solved in O(n)** with the previous problem's rising stack: when a shorter bar arrives, pop taller bars; each popped bar's rectangle spans from the bar beneath it on the stack to the current index.

```text
height = height+1 if cell=='1' else 0
for each row: largest_rectangle(height)
answer = max over rows
```

The solution keeps a permanent 0 at `height[n]` as the sentinel, so every row's stack is flushed at the end. The 2-D problem has become `m` runs of a 1-D problem we have already proved correct.

## Watch it work

The grid above. Each frame shows the histogram for the current bottom row (`#` = on the stack, `:` = popped, `.` = not read yet) with the stack staircase on the right. Index 5 is the sentinel (height 0). All frames match a run of the solution, which returns 6.

Frame 1 — row 0: heights `[1, 0, 1, 0, 0]`.

```text
1 | #   #         |
   -----------    |
 i: 0 1 2 3 4     |
i=1 pop 0 (h=1): left -1, width 1, area 1
i=3 pop 2 (h=1): left 1,  width 1, area 1
staircase at row end: 1 3 4 5   (all h=0:
  a flat floor; zeros never pop zeros)
best = 1
```

Frame 2 — row 1: heights `[2, 0, 2, 1, 1]`.

```text
2 | #   #         |
1 | #   # # #     |
   -----------    |
 i: 0 1 2 3 4     |
i=1 pop 0 (h=2): width 1, area 2
i=3 pop 2 (h=2): left 1, width 1, area 2
i=5 pop 4 (h=1): left 3, width 1, area 1
i=5 pop 3 (h=1): left 1, width 3, area 3
staircase at row end: 1 5   (h=0, 0)
best = 3
```

The towers grew where row 1 had ones and reset to 0 at column 1.

Frame 3 — row 2: heights `[3, 1, 3, 2, 2]`; `i = 1` pops bar 0.

```text
3 | :   .         |
2 | :   . . .     |
1 | : # . . .     | #
   -----------    | --
 i: 0 1 2 3 4     | 1
      ^           | stack
pop 0 (h=3): left -1, width 1, area 3.  best = 3
```

Frame 4 — row 2, `i = 3`: bar 3 (h=2) cuts bar 2 (h=3).

```text
3 | :   :         |
2 | :   : # .     |   #
1 | : # : # .     | # #
   -----------    | ----
 i: 0 1 2 3 4     | 1 3
          ^       | stack
pop 2 (h=3): left 1, width 1, area 3
```

Frame 5 — row 2, `i = 4`: equal height 2 does not pop; push.

```text
3 | :   :         |
2 | :   : # #     |   # #
1 | : # : # #     | # # #
   -----------    | ------
 i: 0 1 2 3 4     | 1 3 4
            ^     | stack
```

The staircase is non-decreasing: 1, 2, 2. Ties are allowed to sit side by side.

Frame 6 — row 2, sentinel `i = 5` flushes.

```text
3 | :   :         |
2 | :   : : :     |
1 | : : : : :     |
   -----------    | --
 i: 0 1 2 3 4 5   | 5  (h=0)
              ^   | stack
pop 4 (h=2): left 3,  width 1, area 2
pop 3 (h=2): left 1,  width 3, area 6
pop 1 (h=1): left -1, width 5, area 5
best = 6
```

Bar 4 undercounts because its tie neighbour, bar 3, sits under it; bar 3 then reports the full width 3, cols 2..4, area 6.

Frame 7 — row 3: heights `[4, 0, 0, 3, 0]`.

```text
4 | #             |
3 | #     #       |
2 | #     #       |
1 | #     #       |
   -----------    |
 i: 0 1 2 3 4     |
i=1 pop 0 (h=4): width 1, area 4
i=4 pop 3 (h=3): left 2, width 1, area 3
staircase at row end: 1 2 4 5   (all h=0)
best stays 6
```

Column 0 is a tower of four ones, but alone it only makes area 4. Across rows, the heights array carried the vertical information forward, and within each row the stack carried the horizontal information. Every row's stack was a non-decreasing staircase, and every bar's area was settled exactly once, when it was popped.

## Why it is correct

Two layers, each with its own invariant.

**Row layer.** After processing row `r`, `height[c]` equals the number of consecutive `'1'` cells ending at `(r, c)` going upward. True for row 0 (one or zero). If true for row `r-1`, a `'1'` at `(r, c)` extends that run by one; a `'0'` ends every run through it, giving 0. By the turning-point claim, the best rectangle with bottom row `r` equals the largest rectangle in this histogram. Every rectangle has some bottom row, so the maximum over rows is the answer.

**Histogram layer.** This is the previous problem's argument, reused verbatim. The stack holds column indices with non-decreasing heights. When bar `t` is popped by `i`, every bar between `t` and `i` is at least `h[t]` (they sat on top of `t` without popping it) and `h[i] < h[t]`, so `i` is the right wall. Every bar between the new top `l` and `t` is taller than `h[t]` (each was popped by a shorter bar chaining to `t`), and `h[l] <= h[t]`, so `l` is the left wall. **The popped bar's answer is fixed at pop time:** no later column can move either wall, so `h[t] * (i - l - 1)` is that bar's final area. With ties, the leftmost bar of a run of equal heights reports the full width (Frame 6), so nothing is lost. The sentinel ensures every bar is popped.

Because both layers are exact, the maximum we record is the true largest rectangle.

## Cost

Time O(mn): each row costs O(n) to update heights and O(n) for the stack pass (each column pushed and popped once).

Space O(n): the heights array and one stack of at most `n + 1` indices.

Levels: the corner-pair brute force is O(m^3 n^3); fixing the bottom row with a running minimum is O(m n^2); the histogram stack brings it to O(mn). If `n` is much larger than `m`, transpose so the stack runs over the shorter side and space is O(min(m, n)).

## Variations you will meet

- **Largest square of ones** (LeetCode 221). Squares do not need the histogram: `dp[r][c] = 1 + min(up, left, up-left)` is enough, O(mn), because a square is determined by one side length.
- **Left/right/height DP.** Keep three arrays per row: `left[c]`, `right[c]` (the walls of the tower at `c`, narrowed row by row) and `height[c]`. Area is `height * (right - left)`. Same O(mn), no stack; the walls play the role of the stack's pops.
- **Count all-ones submatrices** (LeetCode 1504). Same row-by-row heights, but instead of maximising you sum, per row, the number of rectangles ending at each column, which a monotonic stack also accumulates in O(n).
- **Largest rectangle avoiding obstacles in a big sparse grid.** Store only obstacle coordinates and sweep rows; the heights update becomes event-driven, but the per-row histogram step is unchanged.

## What to carry forward

A 2-D rectangle is a 1-D histogram standing on its bottom row: carry tower heights down the rows, and run the rising stack across each one. Reducing to a solved problem is often the whole trick.

The last problem in the chapter uses the stack the other way round, not to measure what a pop closes, but to *choose* what to keep: popping smaller digits so a bigger one moves left.
