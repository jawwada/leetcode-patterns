---
rank: 37
slug: trapping_rain_water
---

Given the heights of bars of width 1 standing side by side, return how many units of rain water they trap between them. `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` traps `6`.

Look at one column at a time. The water above bar `i` rises to the lower of the two walls around it, the tallest bar on its left and the tallest bar on its right, bar `i` itself included, so the column holds `min(max left, max right) - height[i]` units. The brute force rescans both sides for every column, `O(n²)`. Two arrays, prefix maxima from the left and suffix maxima from the right, precompute both walls in `O(n)` time at the price of `O(n)` extra space.

The two-pointer version needs neither array, because a column only needs its lower wall exactly. Walk `left` and `right` inward, with `left_max` the tallest bar seen from the left end and `right_max` the tallest seen from the right end. If `left_max < right_max`, the true right wall of column `left` is at least `right_max` and so already taller; the lower wall is `left_max`, and the column is settled. Add its water and move `left`. Otherwise the mirror argument settles column `right`. The pointer behind the lower wall always moves, so the two meet on a tallest bar, which holds no water.

```text
3                      #                  # bar   ~ water
2              # ~ ~ ~ # # ~ #
1          # ~ # # ~ # # # # # #
height   0 1 0 2 1 0 1 3 2 1 2 1
water    0 0 1 0 1 2 1 0 0 1 0 0   total 6
by       L L L L L L L · R R R R   (· where the pointers meet)
left right  left_max right_max   settles    water  total
  0   11       0        1        left  0     +0      0
  1   11       1        1        right 11    +0      0
  1   10       1        2        left  1     +0      0
  2   10       1        2        left  2     +1      1
  3   10       2        2        right 10    +0      1
  3    9       2        2        right 9     +1      2
  3    8       2        2        right 8     +0      2
  3    7       2        3        left  3     +0      2
  4    7       2        3        left  4     +1      3
  5    7       2        3        left  5     +2      5
  6    7       2        3        left  6     +1      6
```

```pseudo
FUNCTION Trap(height)
    left ← 0
    right ← len(height) - 1
    left_max ← 0                           // tallest bar in height[0..left]
    right_max ← 0                          // tallest bar in height[right..n-1]
    water ← 0
    WHILE left < right
        left_max ← max(left_max, height[left])
        right_max ← max(right_max, height[right])
        IF left_max < right_max            // right wall taller: settle left
            water ← water + left_max - height[left]
            left ← left + 1
        ELSE                               // left wall as tall: settle right
            water ← water + right_max - height[right]
            right ← right - 1
    RETURN water
```

Each step settles one column, so the scan is `O(n)` time with `O(1)` extra space. Reach for this whenever the answer at a position depends on the extremes on both sides of it: the lower side decides, so the lower side moves. Container With Most Water is the cousin, where the area between two lines is capped by the shorter line and the pointer at the shorter line moves. Trapping Rain Water II lifts the problem onto a grid, where a min-heap of boundary cells plays the lower wall. The classic mistake is adding `left_max - height[left]` before raising `left_max` to include the current bar, which goes negative whenever that bar is a new tallest.

*Practice:* LC 42 Trapping Rain Water · LC 11 Container With Most Water · LC 407 Trapping Rain Water II
