"""
Heap Push and Pop by Hand - Fundamentals
Chapter: fundamentals/heaps
Key operations: push: append, float up via (i-1)//2; pop: last to root, sink to the smaller child

Implement a min-heap on a plain list. Push appends the value and floats it up while it is smaller
than its parent at (i-1)//2. Pop takes the root, moves the LAST element to the root, and sinks it
by swapping with the smaller child while that child is smaller.
Example: push 5, 3, 8, pop, push 1, pop, pop -> popped values 3, 1, 5
"""


# --- algorithm ---
def heap_push(heap, value):
    """Append at the end, then swap up while the parent is bigger. O(log n)."""
    heap.append(value)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:   # float up only while the PARENT is bigger
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def heap_pop(heap):
    """Take the root, move the last element there, sink it toward the smaller child. O(log n)."""
    top = heap[0]
    last = heap.pop()
    if len(heap) == 0:
        return top
    heap[0] = last
    i = 0
    n = len(heap)
    while True:
        child = 2 * i + 1
        if child + 1 < n and heap[child + 1] < heap[child]:   # sink toward the SMALLER child
            child = child + 1
        if child >= n or heap[i] <= heap[child]:
            break
        heap[i], heap[child] = heap[child], heap[i]
        i = child
    return top


# --- try it ---
heap = []
heap_push(heap, 5)
heap_push(heap, 3)
heap_push(heap, 8)
print(heap)             # -> [3, 5, 8]
print(heap_pop(heap))   # -> 3
heap_push(heap, 1)
print(heap)             # -> [1, 8, 5]
print(heap_pop(heap))   # -> 1
print(heap_pop(heap))   # -> 5
print(heap)             # -> [8]
