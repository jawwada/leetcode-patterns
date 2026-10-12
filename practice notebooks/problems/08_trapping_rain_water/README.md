# Trapping Rain Water (LeetCode 42)

**Area:** two pointers · **Difficulty:** Medium-Hard · **Key operations:** compare the two ends, settle the lower side, update that side's running max, add max - height

## Problem

Given an elevation map `height[i]` (bars of width 1), return how much water it traps after raining. The water standing above bar `i` is `min(tallest bar to its left, tallest bar to its right) - height[i]`, and never negative.

## Example

```
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
water  = 6

             #
     #       # #   #
 #   # #   # # # # # #
 0 1 0 2 1 0 1 3 2 1 2 1
```

One unit above index 2, one above index 4, two above index 5, one above index 6, one above index 9.

## Brute force

For every bar `i`, scan left for the tallest bar (including `i`), scan right for the tallest bar (including `i`), and add `min(left, right) - height[i]`.

O(n²) time, O(1) extra space. The wasted work: the tallest-to-the-left of bar `i+1` is just `max(tallest-to-the-left of i, height[i])`, yet the scan restarts from zero for every bar, and the same on the right.

## From brute force to optimal

The first fix is two prefix arrays, `left_max[i]` and `right_max[i]`, each built in one pass: O(n) time, O(n) space. The second fix removes the arrays. The water above a bar is decided by the *lower* of its two walls, so you only need to be certain which wall is lower, not the exact height of the taller one.

Walk two pointers inward, each carrying the tallest bar it has passed. If `height[left] < height[right]`, the right side already contains a bar taller than `height[left]`, and (by the way the pointers moved) taller than anything the left pointer has passed. So the water above `left` is `left_max - height[left]`, no matter what lies in between. Settle it and move `left`. Otherwise settle `right` the same way. Each bar is settled exactly once with O(1) state.

## Intuition

Picture two walls closing in from the ends, each remembering the tallest bar it has walked past. Water on the side of the lower wall is already decided: the other side is guaranteed to hold something taller, so the water level there is the lower wall's height. Pour that water in, step the lower wall inward, and repeat. The two remembered maxima only grow, and whichever is lower is the one you can trust completely.

## Walkthrough

`L` and `R` are the pointers; `lm`/`rm` are `left_max`/`right_max`. The lower end is settled each step.

```
bars   0  1  0  2  1  0  1  3  2  1  2  1
       L                                R   lm 0 rm 0 water 0   h[L]=0 < h[R]=1 -> settle L=0: lm 0, add 0
          L                             R   lm 0 rm 0 water 0   h[L]=1 >= h[R]=1 -> settle R=11: rm 1, add 0
          L                          R      lm 0 rm 1 water 0   h[L]=1 < h[R]=2 -> settle L=1: lm 1, add 0
             L                       R      lm 1 rm 1 water 0   h[L]=0 < h[R]=2 -> settle L=2: lm 1, add 1-0=1
                L                    R      lm 1 rm 1 water 1   h[L]=2 >= h[R]=2 -> settle R=10: rm 2, add 0
                L                 R         lm 1 rm 2 water 1   h[L]=2 >= h[R]=1 -> settle R=9: rm 2, add 2-1=1
                L              R            lm 1 rm 2 water 2   h[L]=2 >= h[R]=2 -> settle R=8: rm 2, add 0
                L           R               lm 1 rm 2 water 2   h[L]=2 < h[R]=3 -> settle L=3: lm 2, add 0
                   L        R               lm 2 rm 2 water 2   h[L]=1 < h[R]=3 -> settle L=4: lm 2, add 2-1=1
                      L     R               lm 2 rm 2 water 3   h[L]=0 < h[R]=3 -> settle L=5: lm 2, add 2-0=2
                         L  R               lm 2 rm 2 water 5   h[L]=1 < h[R]=3 -> settle L=6: lm 2, add 2-1=1
                            LR              L == R: stop, water 6
```

Notice that index 5 (height 0) gets 2 units from `left_max = 2` alone: the pointer never needed to know that the right side's true maximum is 3, only that it is at least 3 > 2.

## Steps

1. `left = 0`, `right = n - 1`, `left_max = right_max = 0`, `water = 0`.
2. While `left < right`:
3. If `height[left] < height[right]`: `left_max = max(left_max, height[left])`, add `left_max - height[left]`, `left += 1`.
4. Else: `right_max = max(right_max, height[right])`, add `right_max - height[right]`, `right -= 1`.
5. Return `water`.

## Complexity

O(n) time: each iteration settles one bar. O(1) extra space: two pointers and two running maxima.

## Pitfalls

- **Overwriting the running max.** `left_max = height[left]` forgets the wall behind the pointer; on `[1, 0, 2, 0, 3]` the dips get 0 water. Always `max(left_max, height[left])`.
- **Copy-paste across the symmetric branches.** `right_max = max(left_max, height[right])` feeds the left wall into the right side; on `[3, 0, 1]` the 0 gets no water. Each side keeps its own maximum.
- **Stopping one bar early.** `while left < right - 1` leaves one bar unsettled; `[2, 0, 2]` returns 0. Loop while `left < right`.
- **Adding before updating the max.** If the water is added before the running max is updated, a bar taller than the max contributes negative water. Update first, then add, and the difference is never negative.
- **Comparing stale maxima.** Deciding the side with `left_max < right_max` before the current bars are folded in loses the last bar; the example drops from 6 to 5. Compare `height[left]` with `height[right]`, or fold the bar in first.
