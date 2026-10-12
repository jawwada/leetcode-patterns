"""
Merge k Sorted Lists (LeetCode 23)
Merge k ascending lists into one ascending list.
  [[1, 4, 5], [1, 3, 4], [2, 6]]  ->  [1, 1, 2, 3, 4, 4, 5, 6]
  (plain Python lists stand in for linked lists; j plays the node pointer)

Idea: the next output value is always one of the k current heads.
      Keep the heads in a min-heap; pop the smallest, then push the next element from the same list.

Pseudocode:
  heap = [(list[0], i, 0) for each non-empty list i]
  while heap:
      val, i, j = pop smallest
      output val
      if list i has an element after j: push (lists[i][j+1], i, j+1)

Time O(N log k) for N values in total, space O(k) for the heap.
"""
import heapq


def merge_k_lists(lists):
    heap = [(row[0], i, 0) for i, row in enumerate(lists) if row]  # one head per list
    heapq.heapify(heap)
    merged = []
    while heap:
        val, i, j = heapq.heappop(heap)        # smallest head overall
        merged.append(val)
        if j + 1 < len(lists[i]):              # same list still has more
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return merged


if __name__ == "__main__":
    print(merge_k_lists([[1, 4, 5], [1, 3, 4], [2, 6]]))  # [1, 1, 2, 3, 4, 4, 5, 6]
    print(merge_k_lists([[], [7], [2, 9]]))              # [2, 7, 9]
