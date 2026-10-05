"""
Top K Largest with a Size-k Min-Heap - Fundamentals
Chapter: fundamentals/heaps
Key operations: fill to k, compare with the root, heappushpop replaces it, root is the k-th largest

Return the k largest values of a stream (1 <= k), in ascending order, using a min-heap that holds
at most k values: its root is the smallest of the best, so a new value gets in only when it beats
the root, and the root is what leaves. The heap never grows past k, so each step costs O(log k).
Example: nums=[3, 1, 5, 12, 2, 11], k=3 -> [5, 11, 12]
"""
import heapq   # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def top_k_largest(nums, k):
    """Min-heap of the k largest so far; the root is the gatekeeper. O(n log k)."""
    heap = []
    for value in nums:
        if len(heap) < k:   # push freely only while FEWER than k values are in
            heapq.heappush(heap, value)
        elif value > heap[0]:   # bigger than the smallest of the best: it belongs in
            heapq.heappushpop(heap, value)   # push value, then pop the smallest, in one step
    return sorted(heap)


def kth_largest(nums, k):
    """The root of the size-k min-heap is the k-th largest. O(n log k)."""
    heap = top_k_largest(nums, k)
    return heap[0]


# --- try it ---
print(top_k_largest([3, 1, 5, 12, 2, 11], 3))   # -> [5, 11, 12]
print(top_k_largest([3, 1, 5, 12, 2, 11], 1))   # -> [12]
print(top_k_largest([4, 4, 4, 1], 2))           # -> [4, 4]
print(kth_largest([3, 1, 5, 12, 2, 11], 3))     # -> 5
