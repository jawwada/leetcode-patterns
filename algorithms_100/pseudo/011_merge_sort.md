---
rank: 11
slug: merge_sort
---

Sort an array of integers into ascending order and return the result as a new list. `[5, 2, 4, 7, 1, 3, 2, 6]` becomes `[1, 2, 2, 3, 4, 5, 6, 7]`.

Insertion sort, the brute force, slides each value left past every larger one and costs `O(n²)` on reversed input. Merge sort starts from a cheaper fact: two lists that are already sorted combine into one sorted list in a single pass, because the smallest value not yet taken always sits at the front of one of them. So cut the array in half, sort each half by the same method, and merge the two sorted halves. The recursion bottoms out at lists of zero or one value, which are sorted by definition, and all the real work happens on the way back up, in the merges.

The merge is two fingers, one on the front of each half: compare the two fronts, take the smaller, advance that finger, and when one half runs out, copy the rest of the other. Taking the left front on a tie, `≤` rather than `<`, keeps equal values in their original order, which is what makes merge sort stable. Picture the recursion as a tree of cuts. Every row of the tree holds all n values, cut into more and more pieces, and after about `log2 n` rounds of cutting the pieces are single values. On the way back up each row is merged with `O(n)` work in total, because every value is copied once per row.

```text
split  [5 2 4 7 1 3 2 6]                          one list of 8
       [5 2 4 7]           [1 3 2 6]              2 lists of 4
       [5 2]     [4 7]     [1 3]     [2 6]        4 lists of 2
       [5] [2]   [4] [7]   [1] [3]   [2] [6]      8 lists of 1: sorted
merge  [2 5]     [4 7]     [1 3]     [2 6]        8 values copied
       [2 4 5 7]           [1 2 3 6]              8 values copied
       [1 2 2 3 4 5 6 7]                          8 values copied
```

```pseudo
FUNCTION Merge(left, right)
    merged ← empty list
    i ← 0                                  // front of left
    j ← 0                                  // front of right
    WHILE i < len(left) AND j < len(right)
        IF left[i] ≤ right[j]              // a tie takes the left one: stable
            merged.append(left[i])
            i ← i + 1
        ELSE
            merged.append(right[j])
            j ← j + 1
    WHILE i < len(left)                    // one side is used up: copy the rest
        merged.append(left[i])
        i ← i + 1
    WHILE j < len(right)
        merged.append(right[j])
        j ← j + 1
    RETURN merged

FUNCTION MergeSort(nums)
    IF len(nums) ≤ 1
        RETURN copy of nums                // 0 or 1 values: sorted already
    mid ← floor(len(nums) / 2)
    left ← MergeSort(nums[0..mid - 1])
    right ← MergeSort(nums[mid..len(nums) - 1])
    RETURN Merge(left, right)
```

There are `log2 n` levels of merging, rounded up, each costing `O(n)`, so the time is `O(n log n)` in every case, plus `O(n)` extra space for the merged lists. Reach for merge sort when the sort must be stable, when the data is a linked list (LC 148 splits at the middle with slow and fast pointers and needs no random access), and when a problem counts pairs `i < j` with `nums[i] > nums[j]`. That inversion count is the classic extension: when the merge takes `right[j]` while `len(left) - i` left values still wait, all of them are larger and came earlier in the array, so adding `len(left) - i` at that step counts every inversion; LC 315 and LC 493 are this count with a twist. The classic mistake is stopping when the main loop ends: `Merge([1, 4], [2, 3])` runs out of right values at `[1, 2, 3]` and loses the `4`.

*Practice:* LC 912 Sort an Array · LC 148 Sort List · LC 315 Count of Smaller Numbers After Self · LC 493 Reverse Pairs
