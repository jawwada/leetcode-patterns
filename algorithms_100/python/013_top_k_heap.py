"""
Top-K Elements - Keep a Size-K Min-Heap

Given an unsorted array and k, return the kth largest value (duplicates
count); the same heap also holds the k largest values themselves:
[3, 1, 5, 12, 2, 11], k = 3 -> 5 (the three largest are 12, 11 and 5).
"""
import heapq   # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def top_k(nums, k):
    """Min-heap of the k largest values so far. O(n log k) time, O(k) space."""
    heap = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:               # one too many: drop the smallest
            heapq.heappop(heap)
    return heap


def kth_largest(nums, k):
    """The top of the size-k min-heap is the kth largest. O(n log k)."""
    heap = top_k(nums, k)
    return heap[0]                      # the smallest of the k largest


# --- try it ---
print(kth_largest([3, 1, 5, 12, 2, 11], 3))          # -> 5
print(sorted(top_k([3, 1, 5, 12, 2, 11], 3)))        # -> [5, 11, 12]
print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # -> 4
print(kth_largest([-1, -1], 2))                      # -> -1
