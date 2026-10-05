# Container With Most Water
*LeetCode 11 · Medium · Pattern: Converging two pointers, move the limiting side · Reading time ~8 min*

## The problem

Given heights of n vertical lines at x = 0..n-1, choose two lines that together with the x-axis form the container
holding the most water; the area is min(h[i], h[j]) * (j - i). Return the maximum area.

```text
Example: height = [1, 8, 6, 2, 5, 4, 8, 3, 7] -> 49 (indices 1
  and 8).
```

## What the problem is really asking

You have n vertical lines standing on the x-axis at positions 0 to n-1, with heights `height[i]`. Pick two of them; together with the axis they form a container. Water fills it up to the shorter line, so it holds `min(height[i], height[j]) * (j - i)`. Return the largest amount any pair can hold.

The answer is a single number. The difficulty: there are n(n-1)/2 pairs, the array is **not** sorted, and there is no target to compare against. The pruning trick from Two Sum II seems to have nothing to grip.

```text
height = [2, 3, 10, 5, 7, 8, 9]

 10 |       #
  9 |       #~~~~~~~~~~~#
  8 |       #~~~~~~~~#~~#
  7 |       #~~~~~#~~#~~#
  6 |       #~~~~~#~~#~~#
  5 |       #~~#~~#~~#~~#
  4 |       #~~#~~#~~#~~#
  3 |    #  #~~#~~#~~#~~#
  2 | #  #  #~~#~~#~~#~~#
  1 | #  #  #~~#~~#~~#~~#
    +---------------------
      0  1  2  3  4  5  6

best: lines 2 and 6, min(10, 9) * 4 = 36
```

## Do it by hand first

Start with the widest container, the two outermost lines: heights 2 and 9, width 6, area 12. The water is capped at 2 by the left line. Now think about what to try next. If you keep the left line (height 2) and pick any other right line, the width shrinks and the height is still at most 2. Every such container is worse than 12. The left line is finished; cross it out.

```text
  [ 2 | 3 | 10 | 5 | 7 | 8 | 9 ]
    L                        R
  area = min(2,9) * 6 = 12
  any partner for 2 that is closer than 6
  holds at most 2 * (less than 6) < 12
  -> line 0 can never do better: drop it
```

Your hand tracked two lines and the best area so far, and each time it dropped the shorter line.

## The first honest attempt

Evaluate every pair, keep the maximum. O(n^2) time, O(1) space.

The repeated work: once you know a line is the shorter wall of a container, every narrower container that keeps that wall is doomed, yet the brute force evaluates all of them.

```text
with line 0 (height 2) as the short wall:
  (0,6) = 12   (0,5) <= 10  (0,4) <= 8
  (0,3) <= 6   (0,2) <= 4   (0,1) <= 2
  five pairs evaluated for nothing
```

## The turning point

**Claim: in the current pair `(L, R)`, the shorter line cannot be part of any better container that lies inside `[L, R]`, so discard it and move its pointer inward.**

Justify it. Say `height[L] <= height[R]`. Any other container that uses line `L` and some `R' < R` has:

- width `R' - L`, strictly less than `R - L`;
- height `min(height[L], height[R'])`, which is at most `height[L]`.

So its area is strictly less than `height[L] * (R - L)`, which is exactly the area we just recorded. No container using line `L` inside the current range can beat what we already have. Line `L` is done.

What about moving the taller side instead? If you drop `R` and keep `L`, the new container is narrower and its height is still capped by `height[L]`. It can only get worse. Moving the taller side throws away possibilities without any chance of gain; moving the shorter side is the only move that might raise the cap.

This is the same shape as Two Sum II: one comparison, one whole row or column of the pair grid deleted. The monotone property is different. There it was sorted order. Here it is: **the shorter side can never do better** by keeping itself and shrinking the width.

Ties: if `height[L] == height[R]`, both lines are the cap; either can be dropped by the argument above. The solution moves `R` in that case, which is fine.

## Watch it work

`height = [2, 3, 10, 5, 7, 8, 9]`. Each frame records an area, then drops the shorter line.

Frame 1. `L = 0`, `R = 6`: `min(2, 9) * 6 = 12`. Best 12. Left is shorter; `L = 1`.

```text
  [ 2 | 3 | 10 | 5 | 7 | 8 | 9 ]
    L                        R
  area 12   best 12   drop L (2 < 9)
```

Frame 2. `L = 1`, `R = 6`: `min(3, 9) * 5 = 15`. Best 15. `L = 2`.

```text
  [ 2 | 3 | 10 | 5 | 7 | 8 | 9 ]
    x   L                    R
  area 15   best 15   drop L (3 < 9)
```

Frame 3. `L = 2`, `R = 6`: `min(10, 9) * 4 = 36`. Best 36. Now the right line is shorter; `R = 5`.

```text
  [ 2 | 3 | 10 | 5 | 7 | 8 | 9 ]
    x   x   L                R
  area 36   best 36   drop R (9 < 10)
```

Frame 4. `L = 2`, `R = 5`: `min(10, 8) * 3 = 24`. Best stays 36. `R = 4`.

```text
  [ 2 | 3 | 10 | 5 | 7 | 8 | 9 ]
    x   x   L            R   x
  area 24   best 36   drop R (8 < 10)
```

Frame 5. `L = 2`, `R = 4`: `min(10, 7) * 2 = 14`. `R = 3`.

```text
  [ 2 | 3 | 10 | 5 | 7 | 8 | 9 ]
    x   x   L        R   x   x
  area 14   best 36   drop R (7 < 10)
```

Frame 6. `L = 2`, `R = 3`: `min(10, 5) * 1 = 5`. `R = 2` meets `L`; stop. Answer 36.

```text
  [ 2 | 3 | 10 | 5 | 7 | 8 | 9 ]
    x   x   L    R   x   x   x
  area 5    best 36   pointers meet
```

Across the frames, the tall line 10 never moved once it became `L`: it was never the shorter side. Every dropped line was the short wall of the container recorded just before it was dropped.

## Why it is correct

Invariant: the best container overall is either already recorded in `best`, or both its lines lie in `[L, R]`.

At the start `[L, R]` is everything. At each step we record the area of `(L, R)` and then drop the shorter line, say `L`. If the optimal container uses line `L` with a partner outside `[L, R]`, it already lacked both lines in range, so by the invariant it was recorded earlier. Any container using `L` with a partner inside the range has area at most the one we just recorded, by the turning-point argument. So nothing better than `best` is lost by dropping `L`.

When the range is empty, every container has been accounted for, and `best` is the maximum.

## Cost

- Time: O(n). Each step moves one pointer inward; n - 1 steps.
- Space: O(1). Two indices and the best so far.

Brute force: O(n^2) time, O(1) space.

## Variations you will meet

- **Trapping Rain Water (LeetCode 42)**: instead of choosing one pair, every cell holds water up to the lower of the tallest walls on its two sides. The same "shorter side is settled" argument applies, with running maxima. That is the next problem.
- **Largest Rectangle in Histogram (LeetCode 84)**: the rectangle's height is the minimum over a contiguous range of bars, not just the two ends. Two pointers do not work; a monotonic stack does.
- **Skip lines no taller than the one you dropped**: after moving `L` past a short line, any next line that is not taller than it cannot improve the cap and is narrower, so you can skip it without computing an area. Same O(n), fewer multiplications.
- **Return the indices**: record `(L, R)` whenever `best` improves.

## What to carry forward

When no sorted order exists, look for a quantity that caps the objective (here the shorter wall): keeping the cap while shrinking the width can never help, so the capped side is the one to discard. The next problem applies the same "shorter side is settled" logic to every cell of the skyline at once, carrying a running maximum on each side.
