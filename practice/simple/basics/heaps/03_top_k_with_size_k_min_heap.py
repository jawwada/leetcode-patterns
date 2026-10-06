"""
Top K Largest with a Size-k Min-Heap (basics: heaps)
Return the k largest values of a list in ascending order, holding at most k values at a time.
  nums = [3, 1, 5, 12, 2, 11], k = 3  ->  [5, 11, 12]

Idea: a min-heap of the k best so far keeps the WEAKEST of them at the root: the gatekeeper.
      A new value gets in only if it beats the root, and then the root is what leaves.
      The heap never grows past k, so each step costs O(log k).

Pseudocode:
  heap = []
  for x in nums:
      if len(heap) < k: push x                     # still filling up
      elif x > heap[0]: push x, pop the root       # heappushpop
  return sorted(heap)

Time O(n log k), space O(k).
"""
import heapq


def top_k_largest(nums, k):
    heap = []                            # min-heap of the k largest so far
    for x in nums:
        if len(heap) < k:                # not full yet: just add
            heapq.heappush(heap, x)
        elif x > heap[0]:                # beats the weakest of the best
            heapq.heappushpop(heap, x)   # x goes in, the old root comes out
    return sorted(heap)


if __name__ == "__main__":
    print(top_k_largest([3, 1, 5, 12, 2, 11], 3))  # [5, 11, 12]
    print(top_k_largest([4, 1, 4, 4], 2))          # [4, 4]
    print(top_k_largest([7, 2], 5))                # [2, 7]
