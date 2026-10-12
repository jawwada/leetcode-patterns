# Container With Most Water (LeetCode 11)

**Area:** two pointers · **Difficulty:** Medium · **Key operations:** pointers at both ends, area = shorter wall * width, move the shorter side inward

## Problem

Given the heights of n vertical lines at x = 0 .. n-1, choose two lines that together with the x-axis form the container holding the most water. The area between lines `i` and `j` is `min(h[i], h[j]) * (j - i)`. Return the maximum area.

## Example

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
answer = 49         walls at index 1 and 8: min(8, 7) * (8 - 1)
```

## Brute force

Evaluate `min(h[i], h[j]) * (j - i)` for every pair `i < j` and keep the maximum.

O(n²) time, O(1) space. The wasted work: once we know which of the two walls is shorter, every pair that *keeps* that shorter wall and brings the other wall closer is provably worse (narrower, and the height is still capped by the short wall), yet the brute force evaluates all of them.

## From brute force to optimal

Start with the widest container, `lo = 0` and `hi = n - 1`. Its height is capped by the shorter wall. Every other container that still uses that shorter wall is narrower and no taller, so it cannot beat the one we just measured. That means the shorter wall can be **discarded entirely**: no pair involving it will ever be better. Move the pointer on the shorter side inward and repeat. Each step throws away one wall for good, so after n - 1 steps every pair that could possibly win has been considered. Ties can move either side.

## Intuition

Area is width times the smaller height. As the two pointers walk toward each other you keep trading width for the *chance* of a taller pair. Moving the short wall is the only move that can ever raise the water level; moving the tall wall only loses width while the level stays stuck at the short wall. Picture the skyline with two walls at the extremes: each step, demolish the shorter wall, slide that pointer inward, and remember the best rectangle seen so far.

## Walkthrough

`L` and `R` are the two pointers, `~` the span of water between them.

```
height      1   8   6   2   5   4   8   3   7
index       0   1   2   3   4   5   6   7   8

L   ~   ~   ~   ~   ~   ~   ~   R      min(1, 7) * 8 =  8   best  8   left shorter  -> L = 1
    L   ~   ~   ~   ~   ~   ~   R      min(8, 7) * 7 = 49   best 49   right shorter -> R = 7
    L   ~   ~   ~   ~   ~   R          min(8, 3) * 6 = 18   best 49   right shorter -> R = 6
    L   ~   ~   ~   ~   R              min(8, 8) * 5 = 40   best 49   equal, move R -> R = 5
    L   ~   ~   ~   R                  min(8, 4) * 4 = 16   best 49   right shorter -> R = 4
    L   ~   ~   R                      min(8, 5) * 3 = 15   best 49   right shorter -> R = 3
    L   ~   R                          min(8, 2) * 2 =  4   best 49   right shorter -> R = 2
    L   R                              min(8, 6) * 1 =  6   best 49   right shorter -> R = 1

L meets R: return 49
```

The wall of height 1 at index 0 is discarded after one measurement: nothing paired with it could beat 8.

## Steps

1. `lo = 0`, `hi = n - 1`, `best = 0`.
2. While `lo < hi`: `area = min(h[lo], h[hi]) * (hi - lo)`, `best = max(best, area)`.
3. If `h[lo] < h[hi]`, `lo += 1`; otherwise `hi -= 1`.
4. Return `best`.

## Complexity

O(n) time: each iteration moves one pointer inward, so there are at most n - 1 iterations. O(1) space.

## Pitfalls

- **Moving the taller side.** `if h[lo] > h[hi]: lo += 1` keeps the short wall, so the height stays capped while the width shrinks; on the example the wall of height 1 is kept until the end.
- **`max` instead of `min`.** Water spills over the shorter wall. With `max` the first step on the example reports 64.
- **Width off by one.** `hi - lo + 1` counts columns instead of distance: `[1, 1]` gives 2 instead of 1.
- **Stopping on equal heights.** When the walls are equal, move either side; stopping or moving both at once can skip the answer. The `else` branch handles it.
