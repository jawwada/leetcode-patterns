---
rank: 73
slug: median_k_sorted_arrays
---

Given `k` sorted arrays of integers holding `N ≥ 1` values in total, return the median of all of them: the middle value when `N` is odd, the average of the two middle values when `N` is even. For `[1, 4, 9]`, `[2, 3, 7, 10]` and `[5, 8]` the nine values in order are `1 2 3 4 5 7 8 9 10`, so the median is `5`.

The brute force merges the arrays with a min-heap of their front elements (#14) and pops until it reaches the middle, `O(N log k)`. The faster idea stops hunting for a position and searches for a value instead. Ask of any integer `v`: how many values are at most `v`? Each array answers with one upper-bound binary search (#9), and the sum over all arrays is a count that never shrinks as `v` grows. So the question "are at least `r` values at most `v`?" reads ✗ ✗ ✗ then ✓ ✓ ✓ along the number line, and the `r`-th smallest value is the first ✓, found by binary search on the answer (#10) between the smallest first element and the largest last element.

That first ✓ is always a real element of some array, because the count changes only at values that appear in the arrays: if `v` were absent, `v - 1` would have the same count and would be an earlier ✓. The median then takes one or two of these order statistics, counted from 1: rank `⌊N / 2⌋ + 1` when `N` is odd, and the average of ranks `⌊N / 2⌋` and `⌊N / 2⌋ + 1` when it is even.

```text
[1, 4, 9]  [2, 3, 7, 10]  [5, 8]: N = 9, so the median is the 5th smallest
value v          1   2   3   4   5   6   7   8   9  10
count(≤ v)       1   2   3   4   5   5   6   7   8   9
count ≥ 5?       ✗   ✗   ✗   ✗   ✓   ✓   ✓   ✓   ✓   ✓
                                 ▲ the first ✓ is 5, a real element

   lo   hi   mid   count(≤ mid), per array   ≥ 5?   move
    1   10     5    2 + 2 + 1 = 5             yes   hi ← 5
    1    5     3    1 + 2 + 0 = 3             no    lo ← 4
    4    5     4    2 + 2 + 0 = 4             no    lo ← 5
    5    5   lo = hi: the 5th smallest value is 5
```

```pseudo
FUNCTION CountAtMost(arr, value)        // upper bound (#9): values ≤ value
    lo ← 0
    hi ← len(arr)
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF arr[mid] ≤ value
            lo ← mid + 1
        ELSE
            hi ← mid
    RETURN lo

FUNCTION KthSmallest(arrays, rank)      // smallest v with count(≤ v) ≥ rank
    lo ← ∞
    hi ← -∞
    FOR EACH arr IN arrays
        IF len(arr) > 0
            lo ← min(lo, arr[0])                // smallest first element
            hi ← max(hi, arr[len(arr) - 1])     // largest last element
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        count ← 0
        FOR EACH arr IN arrays
            count ← count + CountAtMost(arr, mid)
        IF count ≥ rank
            hi ← mid                    // mid already covers rank values
        ELSE
            lo ← mid + 1                // too few values are ≤ mid
    RETURN lo

FUNCTION MedianKSorted(arrays)
    total ← 0
    FOR EACH arr IN arrays
        total ← total + len(arr)
    IF total mod 2 = 1
        RETURN KthSmallest(arrays, floor(total / 2) + 1)
    low ← KthSmallest(arrays, floor(total / 2))
    high ← KthSmallest(arrays, floor(total / 2) + 1)
    RETURN (low + high) / 2
```

Each probe of the value search runs `k` binary searches of `O(log L)`, where `L` is the longest array, and the search halves the value range `R` every time, so the cost is `O(k log L log R)` time and `O(1)` extra space, no matter how many values sit before the middle. With few long arrays it beats the heap merge by far; for exactly two arrays, the partition search of #40 is tighter still. The same count-then-search pattern works on any sorted structure that can count the values at most `v` quickly, such as a sorted matrix, a multiplication table or the pairwise distances of a sorted array. The classic mistake is an off-by-one in the ranks: they count from 1, so the median of an odd `N` is rank `⌊N / 2⌋ + 1`, and rank `⌊N / 2⌋` returns the value just before it.

*Practice:* LC 4 Median of Two Sorted Arrays · LC 378 Kth Smallest Element in a Sorted Matrix · LC 719 Find K-th Smallest Pair Distance · LC 668 Kth Smallest Number in Multiplication Table
