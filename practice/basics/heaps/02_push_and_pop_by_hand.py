"""
Heap Push and Pop by Hand - Basics
Area: heaps
Key operations: append then float up via parent (i-1)//2, move the last element to the root, sink toward the smaller child

Implement a min-heap on a plain list. Push appends the value and floats it up while it is smaller than
its parent at (i-1)//2. Pop takes the root, moves the LAST element to the root, and sinks it by swapping
with the smaller child while that child is smaller. solve(ops) runs the operations (an int pushes it,
None pops) and returns the popped values in order.
Example: [5, 3, 8, None, 1, None, None] -> [3, 1, 5]
"""
import sys
import heapq
from typing import List, Optional

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


def levels(a):
    """Trace helper: the heap array drawn as tree levels, '1 | 3 5 | 9 7 2'."""
    out, i, w = [], 0, 1
    while i < len(a):
        out.append(" ".join(map(str, a[i:i + w])))
        i, w = i + w, w * 2
    return " | ".join(out)


# --- brute force ---
def brute_force(ops: List[Optional[int]]) -> List[int]:
    """Same operations on the library heap. O(log n) each."""
    heap, popped = [], []
    for op in ops:
        if op is None:
            popped.append(heapq.heappop(heap))
        else:
            heapq.heappush(heap, op)
    return popped


# --- optimal ---
def push(heap: List[int], x: int) -> None:
    """Append at the end, then swap up while the parent is bigger. O(log n)."""
    heap.append(x)
    i = len(heap) - 1
    while i > 0 and heap[(i - 1) // 2] > heap[i]:
        p = (i - 1) // 2
        heap[i], heap[p] = heap[p], heap[i]
        log(f"    float {x}: index {i} -> parent {p}  {heap}")
        i = p


def pop(heap: List[int]) -> int:
    """Take the root, put the last element there, then sink it toward the smaller child. O(log n)."""
    top, last = heap[0], heap.pop()
    if heap:
        heap[0] = last
    i, n = 0, len(heap)
    while True:
        c = 2 * i + 1
        if c + 1 < n and heap[c + 1] < heap[c]:
            c += 1
        if c >= n or heap[i] <= heap[c]:
            break
        heap[i], heap[c] = heap[c], heap[i]
        log(f"    sink {last}: index {i} -> smaller child {c}  {heap}")
        i = c
    return top


def solve(ops: List[Optional[int]]) -> List[int]:
    """Drive the hand-rolled heap; returns the popped values in order."""
    heap, popped = [], []
    for op in ops:
        if op is None:
            log(f"pop: root {heap[0]} leaves, last {heap[-1]} moves to the root")
            popped.append(pop(heap))
            log(f"    -> popped {popped[-1]}   heap {heap}  tree: {levels(heap)}")
        else:
            log(f"push {op}: append at index {len(heap)}")
            push(heap, op)
            log(f"    -> heap {heap}  tree: {levels(heap)}")
    return popped


# --- demo ---
def demo():
    return solve([5, 3, 8, None, 1, None, None])


# --- tests ---
def tests():
    assert solve([5, 3, 8, None, 1, None, None]) == [3, 1, 5]
    assert solve([]) == []
    assert solve([7, None]) == [7]
    assert solve([2, 2, 2, None, None, None]) == [2, 2, 2]
    assert solve([5, 4, 3, 2, 1, None, None, None, None, None]) == [1, 2, 3, 4, 5]
    assert solve([1, 2, 3, 4, 5, None, None, None, None, None]) == [1, 2, 3, 4, 5]
    import random
    rng = random.Random(0)
    for _ in range(200):
        ops, size = [], 0
        for _ in range(rng.randint(0, 16)):
            if size and rng.random() < 0.4:
                ops.append(None)
                size -= 1
            else:
                ops.append(rng.randint(1, 9))
                size += 1
        ops += [None] * size  # drain, so every pushed value is popped once
        assert solve(ops) == brute_force(ops), ops


# --- bugs ---
BUGS = [
    {
        "replace": "    while i > 0 and heap[(i - 1) // 2] > heap[i]:",
        "with":    "    while i > 0 and heap[(i - 1) // 2] < heap[i]:",
        "fix": "float up while the PARENT is bigger; a min-heap keeps the small value on top",
        "why": "Reversed, big values float up: push 5, 3, 8 gives [8, 3, 5] and the first pop returns 8 instead of 3.",
        "decoys": [
            {"line": "        p = (i - 1) // 2", "change": "should be i // 2"},
            {"line": "    heap.append(x)", "change": "should insert at index 0"},
            {"line": "        i = p", "change": "should be i -= 1"},
        ],
    },
    {
        "replace": "        if c + 1 < n and heap[c + 1] < heap[c]:",
        "with":    "        if c + 1 < n and heap[c + 1] > heap[c]:",
        "fix": "sink toward the SMALLER child; the larger one would become a parent bigger than its sibling",
        "why": "Popping from [1, 2, 3, 4, 5] moves 5 to the root and swaps it with 3 instead of 2, so the next pop returns 3.",
        "decoys": [
            {"line": "        if c >= n or heap[i] <= heap[c]:", "change": "should be c > n"},
            {"line": "    top, last = heap[0], heap.pop()", "change": "should pop index 0"},
            {"line": "    return top", "change": "should return heap[0]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
