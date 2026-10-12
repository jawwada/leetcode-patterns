---
rank: 18
slug: quick_sort
---

Sort an array of integers in place, rearranging it without a second array. `[6, 3, 7, 4, 1, 5, 2]` becomes `[1, 2, 3, 4, 5, 6, 7]`.

Merge sort (#17) does its work after the recursive calls, merging sorted halves into a new list. Quick sort does its work before them, in place. Partition the range around one value, the pivot: every smaller value moves to its left and every other value to its right. The pivot now sits in its final position, and the two sides are independent problems that never need to be combined. Sort each side the same way and the whole range is sorted.

The Lomuto partition is a single pass. Pick a random index, swap that value to the end and call it `pivot`. Then `i` scans the range from left to right while `store` marks where the next small value goes, under the invariant that `nums[lo..store-1]` holds only values less than the pivot. When `nums[i]` is smaller, swap it into `nums[store]` and advance `store`. At the end one swap moves the pivot to `store`, right between the two regions. Picture a wall that slides to the right: everything left of the wall is smaller than the pivot, everything between the wall and `i` is not.

```text
random pick: index 3, pivot 4, parked at the end: 6 3 7 2 1 5 4
  i   nums[i]   < 4?   nums after the step (│ = store)   store
  0      6       no    │6 3 7 2 1 5 4                      0
  1      3       yes    3│6 7 2 1 5 4                      1
  2      7       no     3│6 7 2 1 5 4                      1
  3      2       yes    3 2│7 6 1 5 4                      2
  4      1       yes    3 2 1│6 7 5 4                      3
  5      5       no     3 2 1│6 7 5 4                      3
pivot swapped to store: 3 2 1 4 7 5 6, so p = 3
then sort 3 2 1 and 7 5 6; the 4 never moves again
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

FUNCTION SortRange(nums, lo, hi)
    IF lo ≥ hi                          // 0 or 1 values: sorted already
        RETURN
    p ← Partition(nums, lo, hi)
    SortRange(nums, lo, p - 1)          // the pivot at p is final: skip it
    SortRange(nums, p + 1, hi)

FUNCTION QuickSort(nums)
    SortRange(nums, 0, len(nums) - 1)
    RETURN nums
```

A balanced split gives `log2 n` levels of `O(n)` partitioning, so `O(n log n)` time. A pivot that is always the smallest or largest value peels off one element per level and costs `O(n²)`; with a fixed last-element pivot, an already sorted array does exactly that. A random pivot makes no input order bad: on distinct values the expected time is `O(n log n)` and the expected stack depth `O(log n)`. Quick sort is not stable, because a long swap can carry a value past an equal one. Hoare's original partition moves two indices inward from both ends and swaps each misplaced pair; it makes fewer swaps and splits a run of equal values down the middle. Reach for quick sort when the sort must be in place and fast on average, and for its partition alone in kth largest (#60). The classic mistake is ignoring duplicates, and this two-way partition makes it: with the `<` test, an array of equal values leaves the left side empty at every level, so even a random pivot goes quadratic and the recursion runs n levels deep; the three-way partition of #52 fixes it.

*Practice:* LC 912 Sort an Array · LC 215 Kth Largest Element in an Array · LC 75 Sort Colors
