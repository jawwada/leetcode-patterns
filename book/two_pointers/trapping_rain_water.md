# Trapping Rain Water
*LeetCode 42 · Hard · Pattern: Converging two pointers with running maxima · Reading time ~11 min*

## What the problem is really asking

You get an elevation map: bar `i` has height `height[i]` and width 1. Rain falls and settles. How many unit squares of water are trapped between the bars?

The answer is one number, a sum over cells. Each cell holds water up to some level, and the whole difficulty is that the level at a cell depends on bars that can be far away on **both** sides.

```text
height = [3, 0, 2, 0, 4, 1, 2]     # bar   ~ water

4 |              #
3 |  #  ~  ~  ~  #
2 |  #  ~  #  ~  #  ~  #
1 |  #  ~  #  ~  #  #  #
  +----------------------
     0  1  2  3  4  5  6

water per cell:  0  3  1  3  0  1  0   total 8
```

## Do it by hand first

Point at cell 1 (height 0). Look left: the tallest bar is 3. Look right: the tallest bar is 4. Water would spill over the lower of those two walls, so the level is 3, and the cell holds `3 - 0 = 3`. Cell 5 (height 1): tallest left is 4, tallest right is 2, level 2, holds 1. Cell 4 (height 4) is itself the tallest on its left, so it holds nothing.

```text
cell  h   tallest left  tallest right  level  water
 0    3        3             4           3      0
 1    0        3             4           3      3
 2    2        3             4           3      1
 3    0        3             4           3      3
 4    4        4             4           4      0
 5    1        4             2           2      1
 6    2        4             2           2      0
                                       total   8
```

(The "tallest" columns include the cell itself, which is why the water is never negative.)

So the rule is: **water at i = min(maxLeft(i), maxRight(i)) - height[i]**. Your hand tracked two running maxima, one from each side. That is the seed.

## The first honest attempt

Apply the rule literally. For every cell, scan left for the tallest bar and scan right for the tallest bar. O(n) work per cell, O(n^2) total, O(1) space.

The repeated work is obvious once drawn. The scan for cell 3 re-reads cells 0 to 2, which the scan for cell 2 just read. `maxLeft(i + 1)` is `max(maxLeft(i), height[i + 1])`, a one-step update, yet the brute force recomputes it from scratch.

```text
cell 2 scans left:  [3  0  2]          max 3
cell 3 scans left:  [3  0  2  0]       max 3
                     ^^^^^^^
                     same cells re-read
cell 4 scans left:  [3  0  2  0  4]    max 4
```

## The turning point

There are two optimisation levels, and the second is the real insight.

**Level 1: precompute the maxima.** One pass left to right fills `maxLeft`; one pass right to left fills `maxRight`; a third pass sums `min(maxLeft[i], maxRight[i]) - height[i]`. O(n) time, O(n) space.

```text
index:      0  1  2  3  4  5  6
height:     3  0  2  0  4  1  2
maxLeft:    3  3  3  3  4  4  4   (-> fill)
maxRight:   4  4  4  4  4  2  2   (<- fill)
min - h:    0  3  1  3  0  1  0   = 8
```

Level 1 is a perfectly good answer. But look at what the formula actually uses. For each cell, only the **smaller** of the two maxima matters. If you somehow knew "the left side is the limiting one here", you would not need the right maximum's exact value at all. That suggests the question: can we find cells where we are sure which side limits, without knowing both maxima?

**Level 2. Claim: put pointers at both ends. If `height[L] < height[R]`, the water at `L` is exactly `leftMax - height[L]`, where `leftMax` is the tallest bar in `[0..L]`; the right side's exact maximum is irrelevant.**

Why? The water at `L` is `min(leftMax, trueRightMax) - height[L]`. We do not know `trueRightMax`, the tallest bar anywhere right of `L`. But we know one bar over there: `height[R]`. So `trueRightMax >= height[R]`. If we can show `leftMax <= height[R]`, then `leftMax <= trueRightMax`, the minimum is `leftMax`, and the cell is settled.

Is `leftMax <= height[R]`? This is where the "shorter side can never do better" idea from Container With Most Water returns. The pointers always move the side standing on the **shorter** bar. So a pointer standing on a tall bar stays put until the other side finds something at least as tall. That gives an invariant:

**Every bar either pointer has already passed is no taller than `max(height[L], height[R])`.**

It holds at the start (nothing passed). If we move `L` because `height[L] < height[R]`, the bar we pass is shorter than `height[R]`, and the new pair still contains `R`, so the maximum of the pair is still at least `height[R]`. Symmetric for `R`. So when `height[L] < height[R]`, every bar on the left that we passed is at most `height[R]`, and `height[L]` itself is less than `height[R]`. Hence `leftMax <= height[R] <= trueRightMax`. Settled.

Symmetrically, if `height[L] >= height[R]`, the water at `R` is `rightMax - height[R]`.

So the algorithm: keep `leftMax`, `rightMax`, and the two pointers. Each step, look at the shorter of the two current bars, update that side's running max to include it, add `max - height` (never negative, because the max includes the bar), and move that pointer inward. Each step settles one cell forever.

```text
why the left cell is settled when h[L] < h[R]:

   leftMax           h[R]   unknown
     |                |     (anything)
  [ ... L ........... R ............ ]
     ^passed bars: all <= h[R]
  level at L = min(leftMax, >= h[R])
             = leftMax
```

## Watch it work

`height = [3, 0, 2, 0, 4, 1, 2]`. `lM` and `rM` are the running maxima; `w` is the water per settled cell.

Frame 1. `h[0] = 3`, `h[6] = 2`. Not `3 < 2`, so settle the right: `rM = 2`, water `2 - 2 = 0`. `R = 5`.

```text
  h: [ 3 | 0 | 2 | 0 | 4 | 1 | 2 ]
       L                       R
  w:                           0
  lM=0  rM=2  total=0
```

Frame 2. `h[0] = 3`, `h[5] = 1`. Settle right: `rM` stays 2, water `2 - 1 = 1`. `R = 4`.

```text
  h: [ 3 | 0 | 2 | 0 | 4 | 1 | 2 ]
       L                   R
  w:                       1   0
  lM=0  rM=2  total=1
```

Frame 3. `h[0] = 3`, `h[4] = 4`. Now `3 < 4`, settle the left: `lM = 3`, water `3 - 3 = 0`. `L = 1`.

```text
  h: [ 3 | 0 | 2 | 0 | 4 | 1 | 2 ]
       L               R
  w:   0                   1   0
  lM=3  rM=2  total=1
```

Frame 4. `h[1] = 0 < h[4] = 4`. Water `3 - 0 = 3`. `L = 2`. Note `lM = 3 > rM = 2`, yet the left is settled correctly: the bound comes from the bar `R` stands on (4), not from `rM`.

```text
  h: [ 3 | 0 | 2 | 0 | 4 | 1 | 2 ]
           L           R
  w:   0   3               1   0
  lM=3  rM=2  total=4
```

Frame 5. `h[2] = 2 < 4`. Water `3 - 2 = 1`. `L = 3`.

```text
  h: [ 3 | 0 | 2 | 0 | 4 | 1 | 2 ]
               L       R
  w:   0   3   1           1   0
  lM=3  rM=2  total=5
```

Frame 6. `h[3] = 0 < 4`. Water `3 - 0 = 3`. `L = 4 = R`: stop. The tallest bar (index 4) is never settled; it holds no water anyway.

```text
  h: [ 3 | 0 | 2 | 0 | 4 | 1 | 2 ]
                       LR
  w:   0   3   1   3       1   0
  lM=3  rM=2  total=8
```

Across all frames, the pointer standing on the taller bar did not move, every settled cell was settled exactly once, and the running maxima only increased.

## Why it is correct

Two facts carry the proof.

1. **Invariant:** every bar already passed by either pointer has height at most `max(height[L], height[R])`. Shown above: we only ever pass the shorter of the two current bars, and the taller one stays in the pair.

2. **Settling is exact:** when `height[L] < height[R]`, the updated `leftMax` (the tallest bar in `[0..L]`) is at most `height[R]` by fact 1, and `height[R]` is at most the true tallest bar to the right of `L`. So `min(maxLeft(L), maxRight(L)) = leftMax`, and the water added is exactly the true water at `L`. The case `height[L] >= height[R]` is symmetric, with `rightMax <= height[L]`.

Each step settles a different cell with its exact water, and the loop runs until the pointers meet. The one unsettled cell is where they meet; it holds a bar that is at least as tall as every passed bar (fact 1), so it is the global maximum and holds no water. The total is therefore the sum of the true water over all cells.

## Cost

- Brute force: O(n^2) time, O(1) space.
- Level 1, two prefix-max arrays: O(n) time, O(n) space.
- Level 2, two pointers: O(n) time, O(1) space. Each iteration settles one cell.

## Variations you will meet

- **Compare running maxima instead of current bars.** Many solutions branch on `leftMax < rightMax` (after updating both with the current bars). It is equally correct: the smaller running max is the binding wall because the other side already has a bar at least that tall. Pick one form and be able to justify it.
- **Monotonic stack version.** Process left to right with a stack of decreasing bars; when a taller bar arrives, pop and fill water in horizontal layers. Also O(n) time, O(n) space, and it generalises to "water between bars" questions that the two-pointer form does not.
- **Trapping Rain Water II (LeetCode 407), a 2D height map.** Two pointers have no 2D analogue. The idea that survives is "settle from the lowest boundary inward": a min-heap holds the boundary, and you always pop the lowest wall, which is the 2D version of "always move the shorter side".
- **Container With Most Water (LeetCode 11).** The sibling: choose one pair of walls for one container. Same shorter-side argument, but there it discards a wall, here it settles a cell.

## What to carry forward

Water at a cell is the lower of the two side maxima minus the bar; when the bar under one pointer is shorter than the bar under the other, that side's running max is guaranteed to be the lower one, so that cell can be settled immediately. The next and final problem keeps two pointers moving forward, now on two different strings, and replaces "settled" with a single bookmark that only moves right.
