---
rank: 60
slug: quickselect
---

Find the kth largest value of an unsorted array, where duplicates count as separate values. In `[3, 2, 1, 5, 6, 4]` with `k = 2` the answer is `5`.

Sorting finds it in `O(n log n)`, and the size-k heap of #19 in `O(n log k)`. Quickselect reaches expected `O(n)` with one fact about the partition of Quick Sort (#18): after partitioning, the pivot sits at its final sorted index `p`, with only smaller values to its left. In ascending order the kth largest lives at index `target = n - k`. If `p = target`, the pivot is the answer. If `p < target`, the answer lies to the right of the pivot and everything from `lo` to `p` can be forgotten; if `p > target`, it lies to the left. Quick sort recurses into both sides; quickselect keeps only one, so it needs no recursion at all, just a loop that narrows the window `[lo, hi]`.

Picture the window closing in on index `target`, which never leaves it. With distinct values, a random pivot lands in the middle half of the window half of the time, and such a pivot cuts the window to at most three quarters of its size. So it takes two rounds on average to shrink the window by a quarter, and the expected work is at most twice the geometric series `n + 3n/4 + 9n/16 + …`, that is at most 8n.

```text
k = 2, n = 6, so the answer sits at index target = 6 - 2 = 4
one run; the pivots are random picks
  window   pivot   nums after partitioning the window   p   next
  [0, 5]     2     [1 2 3 5 6 4]                         1   1 < 4: lo ← 2
  [2, 5]     6      1 2 [3 5 4 6]                        5   5 > 4: hi ← 4
  [2, 4]     5      1 2 [3 4 5] 6                        4   4 = 4: return 5
```

```pseudo
FUNCTION Partition(nums, lo, hi)
    pick ← RandomInt(lo, hi)            // lo ≤ pick ≤ hi
    swap(nums[pick], nums[hi])          // park the pivot at the end
    pivot ← nums[hi]
    store ← lo                          // invariant: nums[lo..store-1] < pivot
    FOR i FROM lo TO hi - 1
        IF nums[i] < pivot              // a small value joins the left region
            swap(nums[store], nums[i])
            store ← store + 1
    swap(nums[store], nums[hi])         // pivot between the regions
    RETURN store

FUNCTION KthLargest(nums, k)
    target ← len(nums) - k              // the answer's index in sorted order
    lo ← 0
    hi ← len(nums) - 1
    WHILE true
        p ← Partition(nums, lo, hi)
        IF p = target
            RETURN nums[p]
        ELSE IF p < target
            lo ← p + 1                  // the answer is right of the pivot
        ELSE
            hi ← p - 1                  // the answer is left of the pivot
```

On distinct values the expected time is `O(n)` and the extra space `O(1)`; a run of unlucky pivots still costs `O(n²)`. Against the heap of #19, quickselect is faster on average but reorders the input, needs all of it in memory and keeps that quadratic tail; the heap works on a stream at `O(n log k)` every time. Signals: kth largest or smallest, k closest, top k in any order, since when the loop stops `nums[target..n-1]` holds the k largest values, unsorted, just as aiming at index `k - 1` leaves the k smallest in `nums[0..k-1]`; that is how it answers K Closest Points to Origin on squared distances and Top K Frequent Elements on counts. Many equal values are its weak spot: they all land on one side of the `<` test, so an array of identical values goes quadratic unless k is close to n; the three-way partition of #52 groups them in the middle and stops as soon as the target falls among them. The classic mistake is aiming at index `k - 1`, which finds the kth smallest: on the example it returns 2 instead of 5.

*Practice:* LC 215 Kth Largest Element in an Array · LC 973 K Closest Points to Origin · LC 347 Top K Frequent Elements
