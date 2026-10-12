---
rank: 39
slug: search_rotated_sorted_array
---

A sorted array of distinct values was rotated at an unknown pivot, so `[0, 1, 2, 4, 5, 6, 7]` may now read `[6, 7, 0, 1, 2, 4, 5]`. Return the index of a target, or `-1` if it is absent, in `O(log n)` time. In `[6, 7, 0, 1, 2, 4, 5]` the target `0` sits at index `2`.

A linear scan costs `O(n)`. Finding the rotation point first and then binary searching the correct side reaches `O(log n)` in two passes, but one pass is enough. Picture the array as two ascending ramps with a cliff between them. Cut the window at any `mid` and the cliff falls into at most one of the two halves, so the other half is a single ramp, fully sorted. One comparison tells which: if `nums[lo] ≤ nums[mid]`, the left half climbs without a break, because a cliff inside it would leave `nums[mid]` below `nums[lo]`; otherwise the cliff is on the left and the right half is sorted. A sorted half answers "could the target be in here?" with two comparisons against its ends. If the target lies inside its range, search there; if not, it can only be in the other half. Either way half the window disappears, exactly as in plain binary search. The window is the closed `[lo, hi]` of an exact search, since the loop reads `nums[hi]` as a real element.

Two relatives use the same picture. To find the minimum (LC 153), compare `nums[mid]` with `nums[hi]`: if `nums[mid] > nums[hi]`, the cliff and the minimum just after it lie to the right of `mid`, so `lo ← mid + 1`; otherwise `hi ← mid`. With duplicates (LC 81), `nums[lo] = nums[mid] = nums[hi]` hides which half is sorted: `[1, 1, 1, 0, 1]` and `[1, 0, 1, 1, 1]` look identical at those three probes. The safe move is to drop one copy from each end, which makes the worst case `O(n)`.

```text
value
  7        ●                         a cliff after index 1 splits the
  6     ●                            array into two ascending ramps
  5                       ●
  4                    ●
  2                 ●
  1              ●
  0           ●
        0  1  2  3  4  5  6   index

  lo  hi  mid  nums[mid]  sorted half      target 0 in it?   move
   0   6    3       1     right: 1 .. 5    no                hi ← 2
   0   2    1       7     left:  6 .. 7    no                lo ← 2
   2   2    2       0     nums[mid] = target: return 2
```

```pseudo
FUNCTION SearchRotated(nums, target)
    lo ← 0
    hi ← len(nums) - 1                      // closed window [lo, hi]
    WHILE lo ≤ hi
        mid ← floor((lo + hi) / 2)
        IF nums[mid] = target
            RETURN mid
        IF nums[lo] ≤ nums[mid]             // left half is sorted
            IF nums[lo] ≤ target AND target < nums[mid]
                hi ← mid - 1                // target inside the left half
            ELSE
                lo ← mid + 1                // so it must be on the right
        ELSE                                // right half is sorted
            IF nums[mid] < target AND target ≤ nums[hi]
                lo ← mid + 1                // target inside the right half
            ELSE
                hi ← mid - 1                // so it must be on the left
    RETURN -1
```

Each step discards half of the window, so the search takes `O(log n)` time and `O(1)` space. The signals are words like "rotated" or "shifted" next to "sorted", together with a demand for `O(log n)`. The classic mistake is writing `nums[lo] < nums[mid]` instead of `≤`: when the window shrinks to two elements, `lo = mid` and the left half is the single element `nums[mid]`, which is sorted, but the strict test calls the right half sorted instead; on `[3, 1]` with target `1` it discards the `1` and returns `-1`.

*Practice:* LC 33 Search in Rotated Sorted Array · LC 153 Find Minimum in Rotated Sorted Array · LC 81 Search in Rotated Sorted Array II · LC 154 Find Minimum in Rotated Sorted Array II
