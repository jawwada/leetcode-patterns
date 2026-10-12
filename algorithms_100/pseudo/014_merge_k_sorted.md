---
rank: 14
slug: merge_k_sorted
---

Given k arrays, each sorted in ascending order, merge them into one sorted array. `[[1, 4, 7], [2, 5], [0, 3, 6]]` becomes `[0, 1, 2, 3, 4, 5, 6, 7]`.

Concatenating and sorting costs `O(N log N)` for N values in total and throws away the order the arrays already have. Merging the arrays one at a time into a growing result recopies that result k times, `O(Nk)`. The insight is that the next value of the output is always the smallest of the k fronts, one front per array, and a min-heap is the structure that hands back the smallest of a changing set. Put each array's first value in the heap; then pop the smallest front, append it to the output, and push the next value of the same array in its place.

Picture the arrays as k rows with a finger on the front of each. The heap holds what the fingers point at, never more than k values. Each pop moves exactly one finger one step to the right, and a row whose finger falls off the end simply stops taking part. A heap entry is the tuple `(value, row, col)`: the value orders the heap, and `row` and `col` say where the successor lives, at `arrays[row][col + 1]`.

```text
rows: 0 → [1 4 7]   1 → [2 5]   2 → [0 3 6]; the heap starts with 0 1 2
  pop (value, row, col)   then push      heap after   merged
  (0, 2, 0)               (3, 2, 1)      1 2 3        0
  (1, 0, 0)               (4, 0, 1)      2 3 4        0 1
  (2, 1, 0)               (5, 1, 1)      3 4 5        0 1 2
  (3, 2, 1)               (6, 2, 2)      4 5 6        0 1 2 3
  (4, 0, 1)               (7, 0, 2)      5 6 7        0 1 2 3 4
  (5, 1, 1)               row 1 done     6 7          0 1 2 3 4 5
  (6, 2, 2)               row 2 done     7            0 1 2 3 4 5 6
  (7, 0, 2)               row 0 done     empty        0 1 2 3 4 5 6 7
```

```pseudo
FUNCTION MergeKSorted(arrays)
    heap ← empty min-heap                  // of (value, row, col)
    FOR row FROM 0 TO len(arrays) - 1
        IF len(arrays[row]) > 0            // an empty array has no front
            heap.push((arrays[row][0], row, 0))
    merged ← empty list
    WHILE len(heap) > 0
        (value, row, col) ← heap.pop()     // the smallest front of all
        merged.append(value)
        IF col + 1 < len(arrays[row])      // that row has a next value
            heap.push((arrays[row][col + 1], row, col + 1))
    RETURN merged
```

Every value enters and leaves the heap once, and the heap never holds more than k entries, so the time is `O(N log k)` and the extra space `O(k)` beyond the output. Merging the arrays in pairs, level by level as in merge sort (#11), reaches the same `O(N log k)` without a heap. Signals: several sorted sources, k sorted lists, the kth smallest across sorted rows, or a range that must touch every list. LC 23 is this loop on linked lists: push `(node.val, i, node)` for the head of list `i`, and after a pop push `node.next` if it exists. A sorted matrix (LC 378) is a stack of sorted rows: seed the heap with every row's first value, pop k times, and the kth pop is the kth smallest. The classic mistake in Python is pushing `(node.val, node)`: when two values tie, the heap compares the nodes themselves and raises a `TypeError`, so put the list index in the middle as a tie-breaker.

*Practice:* LC 23 Merge k Sorted Lists · LC 378 Kth Smallest Element in a Sorted Matrix · LC 632 Smallest Range Covering Elements from K Lists · LC 373 Find K Pairs with Smallest Sums
