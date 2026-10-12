"""
Heapify - Build a Heap in O(n) with Sift-Down

Rearrange an array in place into a min-heap, a tree stored level by level in
which every parent is at most its children, then push and pop on it by hand:
[9, 5, 6, 2, 3, 7, 1] -> [1, 2, 6, 5, 3, 7, 9].
"""
import heapq   # the library min-heap, used here only to compare


# --- algorithm ---
def sift_down(heap, i, n):
    """Swap heap[i] with its smaller child until no child is smaller; only
    heap[0..n-1] is the heap. O(log n)."""
    while True:
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right
        if smallest == i:               # no child is smaller: done
            return
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest


def heapify(heap):
    """Sift down every parent, the last parent first. O(n) in total."""
    n = len(heap)
    for i in range(n // 2 - 1, -1, -1):  # last parent, back to the root
        sift_down(heap, i, n)


def sift_up(heap, i):
    """Swap heap[i] with its parent while it is smaller. O(log n)."""
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:     # the parent is no larger: done
            return
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def heap_push(heap, value):
    """Add the value as the last leaf, then sift it up. O(log n)."""
    heap.append(value)
    sift_up(heap, len(heap) - 1)


def heap_pop(heap):
    """Swap the root with the last leaf, cut it off, sift down. O(log n)."""
    last = len(heap) - 1
    heap[0], heap[last] = heap[last], heap[0]
    top = heap.pop()                    # remove the last slot: the old root
    sift_down(heap, 0, len(heap))
    return top


# --- try it ---
nums = [9, 5, 6, 2, 3, 7, 1]
heapify(nums)
print(nums)                             # -> [1, 2, 6, 5, 3, 7, 9]
heap_push(nums, 4)
print(nums)                             # -> [1, 2, 6, 4, 3, 7, 9, 5]
print(heap_pop(nums))                   # -> 1
print(nums)                             # -> [2, 3, 6, 4, 5, 7, 9]
same = [9, 5, 6, 2, 3, 7, 1]
heapq.heapify(same)                     # the library: same array this time
print(same)                             # -> [1, 2, 6, 5, 3, 7, 9]
