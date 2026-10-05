"""
Heapify by Hand - Fundamentals
Chapter: fundamentals/heaps
Key operations: sift down from last parent to root, pick the smaller child, swap while child < node

Turn an array into a min-heap in place. Children of index i sit at 2i+1 and 2i+2, so the last
parent is n//2 - 1. Walk i from that parent down to 0 and sift heap[i] down: swap it with its
smaller child while that child is smaller. Every subtree below i is already a heap by then.
Example: [9, 4, 7, 1, 2, 6, 3] -> [1, 2, 3, 4, 9, 6, 7]
"""


# --- algorithm ---
def sift_down(heap, i, n):
    """Move heap[i] down while a child is smaller; stop at a leaf or when no child is smaller."""
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:   # compare with the smaller candidate
            smallest = right
        if smallest == i:
            return
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest


def heapify(nums):
    """Floyd's build: sift down every internal node, last parent first, root last. O(n) total."""
    heap = list(nums)
    n = len(heap)
    for i in range(n // 2 - 1, -1, -1):   # the range must reach 0: the root is sifted last
        sift_down(heap, i, n)
    return heap


# --- try it ---
print(heapify([9, 4, 7, 1, 2, 6, 3]))   # -> [1, 2, 3, 4, 9, 6, 7]
print(heapify([5, 4, 3, 2, 1]))         # -> [1, 2, 3, 5, 4]
print(heapify([2, 1]))                  # -> [1, 2]
print(heapify([]))                      # -> []
