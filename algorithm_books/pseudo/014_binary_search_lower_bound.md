---
rank: 14
slug: binary_search_lower_bound
---

Given an array sorted in non-decreasing order and a target, return the first index whose value is at least the target, or `len(nums)` if every value is smaller. In `[1, 3, 3, 5, 8, 9]` the answer for target `3` is `1`, the first of the two 3s; for target `4` it is `3`, the slot where 4 would be inserted; for target `10` it is `6`, one past the end.

A linear scan finds the answer in `O(n)` and ignores the order. Sorted order turns the question "is `nums[i] ≥ target`?" into a row of answers that reads ✗ ✗ ✗ then ✓ ✓ ✓, because once a value is big enough, every value to its right is too. The lower bound is the boundary between the two runs, and binary search finds a boundary by halving the unknown part. Keep a half-open window `[lo, hi)` with one invariant: every index left of `lo` is a ✗ and every index from `hi` on is a ✓, with the position `len(nums)` counting as a ✓. Probe the middle. A ✗ at `mid` condemns `mid` and everything left of it, so `lo ← mid + 1`. A ✓ at `mid` might be the first ✓, so it becomes the new right edge: `hi ← mid`. When `lo = hi` the window is empty and `lo` sits exactly on the boundary.

Every other search falls out of this template. Exact search checks whether the lower bound actually holds the target. The insert position is the lower bound itself. The upper bound, the first index whose value is greater than the target, is the same loop with `<` replaced by `≤`, so that equal values count as too small. The last occurrence sits just before the upper bound, so first and last position take two searches, and upper bound minus lower bound is the number of copies. First Bad Version is the template with the comparison replaced by a call to `isBadVersion(mid)`.

```text
index            0    1    2    3    4    5    6
nums             1    3    3    5    8    9
nums[i] ≥ 3?     ✗    ✓    ✓    ✓    ✓    ✓    (end counts as ✓)
                      ▲ lower bound = 1

   lo   hi   mid   nums[mid]   < 3?   move
    0    6     3       5        no    hi ← 3     mid is a ✓: keep it
    0    3     1       3        no    hi ← 1     mid is a ✓: keep it
    0    1     0       1        yes   lo ← 1     mid is a ✗: drop it
    1    1   window empty: return lo = 1
```

```pseudo
FUNCTION LowerBound(nums, target)        // first i with nums[i] ≥ target
    lo ← 0
    hi ← len(nums)                       // half-open [lo, hi)
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF nums[mid] < target
            lo ← mid + 1                 // mid and its left are too small
        ELSE
            hi ← mid                     // mid qualifies: keep it in play
    RETURN lo

FUNCTION UpperBound(nums, target)        // first i with nums[i] > target
    lo ← 0
    hi ← len(nums)
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF nums[mid] ≤ target            // equal values count as too small
            lo ← mid + 1
        ELSE
            hi ← mid
    RETURN lo

FUNCTION Search(nums, target)
    i ← LowerBound(nums, target)
    IF i < len(nums) AND nums[i] = target
        RETURN i
    RETURN -1

FUNCTION SearchRange(nums, target)
    first ← LowerBound(nums, target)
    IF first = len(nums) OR nums[first] ≠ target
        RETURN [-1, -1]
    RETURN [first, UpperBound(nums, target) - 1]
```

Each probe halves the window, so a search costs `O(log n)` time and `O(1)` space. Reach for it when the input is sorted and the question is "first", "last", "how many" or "where would it go", and more generally whenever a yes/no question about an index flips exactly once from no to yes, which is binary search on the answer (#15). Python's `bisect_left` and `bisect_right` compute exactly `lower_bound` and `upper_bound`; mention them, but write the loop by hand in an interview. The classic mistake is mixing conventions: `hi ← mid - 1` in this half-open template can jump past the answer, and `WHILE lo ≤ hi` with `hi ← mid` either spins forever once `lo = hi` or reads `nums[len(nums)]`.

*Practice:* LC 704 Binary Search · LC 35 Search Insert Position · LC 34 Find First and Last Position of Element in Sorted Array · LC 278 First Bad Version
