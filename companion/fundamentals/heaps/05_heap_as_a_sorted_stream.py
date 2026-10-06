"""
Heap as a Sorted Stream (Traced) - Fundamentals
Chapter: fundamentals/heaps
Key operations: push at a leaf then sift up, pop the root then sift the last leaf down, pull k or pull all

Push items in any order, then pop: each pop returns the smallest item left, so the pops form a
sorted stream. Every push and pop prints its swaps, so you can watch the heap repair itself along
one path. Pulling all n items is heap sort, O(n log n); pulling only k costs O(n + k log n).
Example: push 5, 3, 8, 1, 9, 2 then pop everything -> 1 2 3 5 8 9
"""


# --- algorithm ---
def push(heap, value):
    """Insert at the next leaf (keeps the tree complete), then swap up while smaller than the parent. O(log n)."""
    heap.append(value)
    i = len(heap) - 1
    steps = []
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:
            break
        steps.append(str(value) + " swaps up past " + str(heap[parent]))
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent
    print("push", value, "->", heap, " ", ", ".join(steps) if steps else "stays at its leaf")


def pop(heap):
    """Take the root, move the last leaf into the root, swap it down toward the smaller child. O(log n)."""
    top = heap[0]
    last = heap.pop()
    steps = []
    if len(heap) > 0:
        heap[0] = last
        i = 0
        n = len(heap)
        while True:
            child = 2 * i + 1
            if child + 1 < n and heap[child + 1] < heap[child]:
                child = child + 1          # the SMALLER child moves up, so its sibling stays below it
            if child >= n or heap[i] <= heap[child]:
                break
            steps.append(str(last) + " sinks past " + str(heap[child]))
            heap[i], heap[child] = heap[child], heap[i]
            i = child
    print("pop ", top, "->", heap, " ", ", ".join(steps) if steps else "nothing to repair")
    return top


def sorted_stream(values, k):
    """Push everything, then pull only the k smallest: the heap never sorts what you do not ask for."""
    heap = []
    for v in values:
        push(heap, v)
    out = []
    while heap and len(out) < k:
        out.append(pop(heap))
    return out


# --- try it ---
print(sorted_stream([5, 3, 8, 1, 9, 2], 6))   # pull all = heap sort -> [1, 2, 3, 5, 8, 9]
print()
print(sorted_stream([7, 4, 6, 1, 2], 2))      # pull only the 2 smallest -> [1, 2]
