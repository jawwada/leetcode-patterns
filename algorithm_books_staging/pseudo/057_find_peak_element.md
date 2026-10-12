---
rank: 57
slug: find_peak_element
---

Given an array in which no two neighbors are equal, return the index of a peak, a value larger than both of its neighbors, where the positions just outside the array count as `-∞`. Any peak is accepted. In `[1, 2, 1, 3, 5, 6, 4]` both index 1 (value `2`) and index 5 (value `6`) are peaks, and the search below returns `5`.

A linear scan for the first value whose right neighbor is smaller costs `O(n)`. Binary search beats it even though nothing is sorted, because all it needs is a reason to throw half of the range away, and the slope at `mid` supplies one. Stand at `mid` and look at `mid + 1`. If the ground rises, walk right for as long as it keeps rising. The walk cannot climb forever, because the right end drops to `-∞`; it stops at the first index whose right neighbor is lower, and since it arrived there by climbing, that index is higher than both neighbors: a peak, to the right of `mid`. So `lo ← mid + 1` gives up only ground the walk never needed. If the ground falls, the same walk run leftward from `mid` stops at a peak at `mid` or to its left, so `hi ← mid`.

The window keeps the promise that the `-∞` ends make for the whole array: the ground climbs into `lo` from the left and falls away from `hi` to the right. Every move preserves it, since `lo ← mid + 1` happens only when `nums[mid] < nums[mid + 1]` and `hi ← mid` only when `nums[mid] > nums[mid + 1]`. A window entered uphill and left downhill has its highest point at a peak of the whole array, so when it shrinks to the single index `lo = hi`, that index is a peak. The window is closed, `hi = len(nums) - 1`, because `mid < hi` keeps the read of `nums[mid + 1]` inside the array.

```text
value
  6                 ●         two peaks: index 1 and index 5;
  5              ●            the ends count as -∞, so the
  4                    ●      ground falls away at both edges
  3           ●
  2     ●
  1  ●     ●
     0  1  2  3  4  5  6   index

  lo  hi  mid   nums[mid] vs nums[mid + 1]   move
   0   6    3        3 < 5   rising          lo ← 4
   4   6    5        6 > 4   falling         hi ← 5
   4   5    4        5 < 6   rising          lo ← 5
   5   5   lo = hi: index 5 (value 6) is a peak
```

```pseudo
FUNCTION FindPeakElement(nums)
    lo ← 0
    hi ← len(nums) - 1                  // closed window [lo, hi] holds a peak
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)      // mid < hi, so nums[mid + 1] exists
        IF nums[mid] < nums[mid + 1]
            lo ← mid + 1                // rising: a peak lies right of mid
        ELSE
            hi ← mid                    // falling: a peak at mid or left of it
    RETURN lo
```

Each probe halves the window, so the search costs `O(log n)` time and `O(1)` space. Reach for it when a problem asks for any local maximum or minimum, or for the top of a mountain array: Peak Index in a Mountain Array is this loop unchanged, and Find in Mountain Array finds the peak first and then binary searches each slope. On a grid, Find a Peak Element II binary searches the columns: the largest value in the middle column beats its neighbors above and below, and the search steps toward a left or right neighbor that beats it, stopping when neither does, for `O(m log n)`. The classic mistake is borrowing the half-open window of #14: with `hi ← len(nums)`, the first probe on `[1, 2]` is `mid = 1`, and `nums[mid + 1]` reads past the end of the array.

*Practice:* LC 162 Find Peak Element · LC 852 Peak Index in a Mountain Array · LC 1901 Find a Peak Element II · LC 1095 Find in Mountain Array
