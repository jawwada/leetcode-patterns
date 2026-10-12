"""
Merge K Sorted Arrays - A Heap of the Front Elements

Merge k sorted arrays of integers into one sorted array:
[[1, 4, 7], [2, 5], [0, 3, 6]] -> [0, 1, 2, 3, 4, 5, 6, 7].
"""
import heapq   # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def merge_k_sorted(arrays):
    """Heap of each array's front as (value, row, col); pop the smallest and
    push its successor. O(N log k) time for N values in k arrays."""
    heap = []                                   # of (value, row, col)
    for row in range(len(arrays)):
        if len(arrays[row]) > 0:                # an empty array has no front
            heapq.heappush(heap, (arrays[row][0], row, 0))
    merged = []
    while len(heap) > 0:
        value, row, col = heapq.heappop(heap)   # the smallest front of all
        merged.append(value)
        if col + 1 < len(arrays[row]):          # that row has a next value
            heapq.heappush(heap, (arrays[row][col + 1], row, col + 1))
    return merged


# --- try it ---
arrays = [[1, 4, 7], [2, 5], [0, 3, 6]]
print(merge_k_sorted(arrays))                  # -> [0, 1, 2, 3, 4, 5, 6, 7]
print(merge_k_sorted([[2, 2], [], [-1, 2]]))   # -> [-1, 2, 2, 2]
print(merge_k_sorted([[5]]))                   # -> [5]
print(merge_k_sorted([]))                      # -> []
