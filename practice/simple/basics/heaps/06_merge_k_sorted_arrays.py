"""
Merge K Sorted Arrays (basics: heaps)
Merge k sorted arrays into one sorted array.
  [[1, 4, 7], [2, 5], [0, 8, 9]]  ->  [0, 1, 2, 4, 5, 7, 8, 9]

Idea: the next output is always one of the k current heads. Keep one head per array in a
      min-heap as (value, array index, position): pop the smallest, push the next value from
      the same array. Each value enters and leaves the heap once.

Pseudocode:
  heap = [(arr[0], i, 0) for each non-empty array i]
  while heap:
      val, i, j = pop the smallest; output val
      if array i has an element after j: push (arrays[i][j + 1], i, j + 1)

Time O(N log k) for N values in total, space O(k) for the heap.
"""
import heapq


def merge_k_sorted(arrays):
    heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]   # one head per array
    heapq.heapify(heap)
    merged = []
    while heap:
        val, i, j = heapq.heappop(heap)  # smallest head overall
        merged.append(val)
        if j + 1 < len(arrays[i]):       # array i has a next value
            heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))
    return merged


if __name__ == "__main__":
    print(merge_k_sorted([[1, 4, 7], [2, 5], [0, 8, 9]]))  # [0, 1, 2, 4, 5, 7, 8, 9]
    print(merge_k_sorted([[], [3, 3], [1]]))              # [1, 3, 3]
