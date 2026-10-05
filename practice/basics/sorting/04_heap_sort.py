"""
Heap Sort - Basics
Area: sorting
Key operations: heapify into a max-heap, swap the root with the last unsorted slot, sift the new root down inside the shrunk heap

Build a max-heap in place (sift down from the last parent to the root), then repeat: swap the root, the
maximum, with the last slot of the heap region, shrink the region by one, and sift the new root down.
The sorted suffix grows from the right. O(n log n) in every case, O(1) extra space, not stable.
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


def levels(a):
    """Trace helper: the heap array drawn as tree levels, '6 | 5 4 | 2 1 3'."""
    out, i, w = [], 0, 1
    while i < len(a):
        out.append(" ".join(map(str, a[i:i + w])))
        i, w = i + w, w * 2
    return " | ".join(out)


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """Python's sorted (Timsort), the reference for every sorting exercise. O(n log n)."""
    return sorted(nums)


# --- optimal ---
def sift_down(a: List[int], i: int, n: int) -> None:
    """Max-heap sift: swap a[i] with its larger child while that child is bigger; a[:n] is the heap. O(log n)."""
    while True:
        c = 2 * i + 1
        if c + 1 < n and a[c + 1] > a[c]:
            c += 1
        if c >= n or a[c] <= a[i]:
            return
        a[i], a[c] = a[c], a[i]
        log(f"    sift: a[{i}]={a[c]} < child a[{c}]={a[i]}, swap  {a[:n]}")
        i = c


def solve(nums: List[int]) -> List[int]:
    """Heapify, then move the max to the end n - 1 times. O(n log n), in place."""
    a = list(nums)
    n = len(a)
    log(f"heapify {a} into a max-heap, sifting indices {n // 2 - 1}..0")
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)
    log(f"max-heap {a}  tree: {levels(a)}")
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        log(f"swap root {a[end]} with a[{end}]={a[0]}: heap {a[:end]} | sorted {a[end:]}")
        sift_down(a, 0, end)
        log(f"  heap {a[:end]} tree: {levels(a[:end])} | sorted {a[end:]}")
    return a


# --- demo ---
def demo():
    return solve([5, 2, 4, 6, 1, 3])


# --- tests ---
def tests():
    assert solve([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]
    assert solve([]) == []
    assert solve([1]) == [1]
    assert solve([2, 1]) == [1, 2]
    assert solve([1, 2, 3]) == [1, 2, 3]
    assert solve([3, 2, 1]) == [1, 2, 3]
    assert solve([2, 2, 1, 2]) == [1, 2, 2, 2]
    import random
    rng = random.Random(0)
    for _ in range(200):
        a = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "        sift_down(a, 0, end)",
        "with":    "        sift_down(a, 0, n)",
        "fix": "sift inside the SHRUNK heap a[:end]; the sorted suffix a[end:] must not take part",
        "why": "With n the sift can swap the new root with a value already placed in the sorted suffix, pulling the max back into the heap: [5, 2, 4, 6, 1, 3] ends unsorted.",
        "decoys": [
            {"line": "        a[0], a[end] = a[end], a[0]", "change": "should swap a[0] with a[end - 1]"},
            {"line": "    for i in range(n // 2 - 1, -1, -1):", "change": "should start at n // 2"},
            {"line": "        if c + 1 < n and a[c + 1] > a[c]:", "change": "should be c + 1 <= n"},
        ],
    },
    {
        "replace": "    for end in range(n - 1, 0, -1):",
        "with":    "    for end in range(n - 1, 1, -1):",
        "fix": "run end down to 1: the last swap puts the two remaining heap values in order",
        "why": "Stopping before end = 1 leaves a[0] >= a[1] as a two-element max-heap: [5, 2, 4, 6, 1, 3] ends [2, 1, 3, 4, 5, 6].",
        "decoys": [
            {"line": "        if c >= n or a[c] <= a[i]:", "change": "should be c > n"},
            {"line": "        i = c", "change": "should be i += 1"},
            {"line": "    n = len(a)", "change": "should be len(a) - 1"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
