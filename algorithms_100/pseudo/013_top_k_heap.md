---
rank: 13
slug: top_k_heap
---

Given an unsorted array and an integer `k`, return the kth largest value, where duplicates count as separate values; the same method returns the k largest values themselves. In `[3, 1, 5, 12, 2, 11]` with `k = 3` the three largest are `12`, `11` and `5`, so the answer is `5`.

Sorting answers it in `O(n log n)` but orders all n values when only k of them matter. Keep instead a min-heap of the k largest values seen so far. Push each value; when the heap grows to `k + 1` values, pop its smallest. The popped value can never be among the k largest, because the k values still in the heap are all at least as large. After the last value the heap holds exactly the k largest, and its top, the smallest of them, is the kth largest.

A min-heap for a question about the largest feels backwards, and that is the point. The top of the heap is the weakest member of the current top k, the gatekeeper at the door: a newcomer that cannot beat it is popped right back out, and one that can beat it pushes the gatekeeper out instead. The heap never holds more than `k + 1` values, so each push and pop costs `O(log k)`, not `O(log n)`.

```text
k = 3; heap contents listed smallest first, so the top comes first
  value   after the push   size > 3?   popped   heap kept
    3     3                no                   3
    1     1 3              no                   1 3
    5     1 3 5            no                   1 3 5
   12     1 3 5 12         yes           1      3 5 12
    2     2 3 5 12         yes           2      3 5 12
   11     3 5 11 12        yes           3      5 11 12
heap top 5 is the 3rd largest; the heap holds the top three
```

```pseudo
FUNCTION TopK(nums, k)
    heap ← empty min-heap
    FOR EACH value IN nums
        heap.push(value)
        IF len(heap) > k                   // one too many: drop the smallest
            heap.pop()
    RETURN heap

FUNCTION KthLargest(nums, k)
    heap ← TopK(nums, k)
    RETURN heap.top()                      // the smallest of the k largest
```

Each of the n values costs one push and at most one pop on a heap of at most `k + 1` values, so the time is `O(n log k)` and the space `O(k)`. That beats sorting when k is small, and it works on an endless stream: LC 703 keeps this heap alive and answers after every new value. Signals: k largest, k most frequent, k closest. K Closest Points to Origin is the same loop with a distance key in the opposite direction: keeping the k smallest distances needs a max-heap, which `heapq` gives when you push `(-(x² + y²), x, y)`, so the popped point is the farthest so far. Top K Frequent Elements counts first and runs the loop on `(count, value)` pairs, or uses the buckets of #43. Quickselect (#42) is expected `O(n)` but reorders the array and needs all of it at once. The classic mistake is reaching for a max-heap because the problem says largest: a size-k max-heap evicts the biggest values, exactly the ones to keep.

*Practice:* LC 215 Kth Largest Element in an Array · LC 703 Kth Largest Element in a Stream · LC 347 Top K Frequent Elements · LC 973 K Closest Points to Origin
