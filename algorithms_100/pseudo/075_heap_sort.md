---
rank: 75
slug: heap_sort
---

Sort an array of integers in place, with `O(1)` extra space and an `O(n log n)` bound even in the worst case. `[4, 10, 3, 5, 1]` becomes `[1, 3, 4, 5, 10]`.

Selection sort finds the maximum, moves it to the end and repeats on the rest; each search is a linear scan, so it costs `O(n²)`. Heap sort is selection sort with a max-heap doing the search. First turn the array into a max-heap in place with the bottom-up build of Heapify (#41), mirrored so that every parent is at least its children and the maximum sits at index 0. Then repeat: swap `nums[0]` with `nums[end]`, the last slot of the heap, which drops the maximum into its final place; shrink the heap to `nums[0..end-1]`; and sift the new root down to restore the heap.

Picture a wall inside the array. Left of it is a max-heap that loses one slot per step; right of it is the sorted tail, which gains one. Each swap carries the largest value still in the heap across the wall, so the tail fills from the right in decreasing order. The heap lives in the very array it sorts, which is why no extra space is needed.

```text
build, i = 1 then 0:   4 10 3 5 1  →  10 5 3 4 1     max-heap, max at 0
  end   swap        after the swap     after the sift-down   (│ = wall)
   4    10 and 1    1 5 3 4 │ 10       5 4 3 1 │ 10
   3     5 and 1    1 4 3 │ 5 10       4 1 3 │ 5 10
   2     4 and 3    3 1 │ 4 5 10       3 1 │ 4 5 10
   1     3 and 1    1 │ 3 4 5 10       1 │ 3 4 5 10
```

```pseudo
FUNCTION SiftDown(nums, i, n)              // max-heap on nums[0..n-1]
    WHILE true
        largest ← i
        left ← 2 * i + 1
        right ← 2 * i + 2
        IF left < n AND nums[left] > nums[largest]
            largest ← left
        IF right < n AND nums[right] > nums[largest]
            largest ← right
        IF largest = i                     // no child is larger: done
            RETURN
        swap(nums[i], nums[largest])
        i ← largest

FUNCTION HeapSort(nums)
    n ← len(nums)
    FOR i FROM floor(n / 2) - 1 DOWNTO 0   // build: last parent to root
        SiftDown(nums, i, n)
    FOR end FROM n - 1 DOWNTO 1
        swap(nums[0], nums[end])           // the max joins the sorted tail
        SiftDown(nums, 0, end)             // the heap is nums[0..end-1]
    RETURN nums
```

The build is `O(n)` and each of the n - 1 sift-downs costs `O(log n)`, so heap sort is `O(n log n)` in the worst case, with `O(1)` extra space because sift-down is a loop. It is not stable: the swap from the root to the end carries a value past others equal to it. In practice it loses to quick sort (#12), because sift-down jumps from `i` to `2i + 1` across memory and caches dislike that; its niche is the guarantee, which is why introsort, behind most C++ `std::sort` implementations, switches to heap sort when quick sort recurses too deep. Signals: an in-place sort with a worst-case bound, or only the top of the order, since after k swaps the tail holds the k largest values in sorted order. The classic mistake is sifting with `n` instead of `end` after the swap: the sift sees the maximum just parked at `nums[end]` as a child and pulls it back into the heap, and the example comes back as `[10, 5, 3, 4, 1]`, still a heap and not sorted.

*Practice:* LC 912 Sort an Array · LC 215 Kth Largest Element in an Array
