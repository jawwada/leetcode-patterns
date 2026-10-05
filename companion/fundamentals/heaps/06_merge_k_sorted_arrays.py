"""
Merge K Sorted Arrays - Fundamentals
Chapter: fundamentals/heaps
Key operations: seed heap with each head (value, array, index), pop the min, push that array's next

Merge k sorted arrays into one sorted array. A min-heap holds one candidate per array: pop the
smallest, append it, and push the successor from the same array. Each element enters and leaves
the heap once.
Example: [[1, 4, 7], [2, 5], [0, 8, 9]] -> [0, 1, 2, 4, 5, 7, 8, 9]
"""
import heapq   # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def merge_k_sorted(arrays):
    """One candidate per array in a heap keyed (value, which array, position). O(N log k)."""
    heap = []
    for i in range(len(arrays)):
        if len(arrays[i]) > 0:   # an empty array has no head to offer
            heap.append((arrays[i][0], i, 0))
    heapq.heapify(heap)
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(arrays[i]):   # strictly below the length: the successor exists
            heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))
    return out


# --- try it ---
print(merge_k_sorted([[1, 4, 7], [2, 5], [0, 8, 9]]))   # -> [0, 1, 2, 4, 5, 7, 8, 9]
print(merge_k_sorted([[], [1, 2], []]))                 # -> [1, 2]
print(merge_k_sorted([[3, 3], [3]]))                    # -> [3, 3, 3]
print(merge_k_sorted([]))                               # -> []
