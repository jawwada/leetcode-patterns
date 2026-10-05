"""
Heap Sort - Fundamentals
Chapter: fundamentals/sorting
Key operations: heapify into a max-heap, swap the root with the last heap slot, sift the root down

Build a max-heap in place (sift down from the last parent to the root), then repeat: swap the root,
the maximum, with the last slot of the heap region, shrink the region by one, and sift the new root
down. The sorted suffix grows from the right. O(n log n) always, O(1) extra space, not stable.
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""


# --- algorithm ---
def sift_down(a, i, size):
    """Max-heap sift: swap a[i] with its larger child while that child is bigger. O(log n)."""
    while True:
        child = 2 * i + 1
        if child + 1 < size and a[child + 1] > a[child]:
            child += 1                 # pick the larger of the two children
        if child >= size or a[child] <= a[i]:
            return                     # no child, or the heap property already holds here
        a[i], a[child] = a[child], a[i]
        i = child


def heap_sort(nums):
    """Heapify, then move the max to the end n - 1 times. O(n log n), in place."""
    a = list(nums)
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):    # last parent down to the root
        sift_down(a, i, n)
    for end in range(n - 1, 0, -1):        # end goes down to 1 so the last two values get ordered
        a[0], a[end] = a[end], a[0]        # the max leaves the heap and joins the sorted suffix
        sift_down(a, 0, end)               # sift inside the shrunk heap a[:end], not all of a
    return a


# --- try it ---
print(heap_sort([5, 2, 4, 6, 1, 3]))   # -> [1, 2, 3, 4, 5, 6]
print(heap_sort([2, 1]))               # -> [1, 2]
print(heap_sort([1, 1, 1]))            # -> [1, 1, 1]
print(heap_sort([]))                   # -> []
