"""
Heapify by Hand - Basics
Area: heaps
Key operations: sift down from the last parent to the root, pick the smaller child, swap while child < node

Turn an array into a min-heap in place. Children of index i sit at 2i+1 and 2i+2, so the last parent is
n//2 - 1. Walk i from that parent down to 0 and sift a[i] down: swap it with its smaller child while
that child is smaller. Every subtree below i is already a heap when i's turn comes.
Example: [9, 4, 7, 1, 2, 6, 3] -> [1, 2, 3, 4, 9, 6, 7]
"""
import sys
import heapq
from typing import List

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
def brute_force(nums: List[int]) -> List[int]:
    """The library does the same Floyd build; with distinct values the arrays match exactly. O(n)."""
    a = list(nums)
    heapq.heapify(a)
    return a


def is_min_heap(a: List[int]) -> bool:
    """Every child is >= its parent at (i-1)//2."""
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))


# --- optimal ---
def sift_down(a: List[int], i: int, n: int) -> None:
    """Move a[i] down while a child is smaller; stop at a leaf or when both children are >= it."""
    while True:
        l, r, smallest = 2 * i + 1, 2 * i + 2, i
        if l < n and a[l] < a[smallest]:
            smallest = l
        if r < n and a[r] < a[smallest]:
            smallest = r
        if smallest == i:
            return
        a[i], a[smallest] = a[smallest], a[i]
        log(f"    swap a[{i}]={a[smallest]} with smaller child a[{smallest}]={a[i]} -> {a}")
        i = smallest


def solve(nums: List[int]) -> List[int]:
    """Floyd's build: sift down every internal node, last parent first, root last. O(n) total."""
    a = list(nums)
    n = len(a)
    log(f"start {a}  tree: {levels(a)}  last parent = {n // 2 - 1}")
    for i in range(n // 2 - 1, -1, -1):
        log(f"sift down index {i} (value {a[i]}, children {a[2 * i + 1:2 * i + 3]})")
        sift_down(a, i, n)
        log(f"    now {a}  tree: {levels(a)}")
    return a


# --- demo ---
def demo():
    return solve([9, 4, 7, 1, 2, 6, 3])


# --- tests ---
def tests():
    assert solve([9, 4, 7, 1, 2, 6, 3]) == [1, 2, 3, 4, 9, 6, 7]
    assert solve([]) == []
    assert solve([5]) == [5]
    assert solve([1, 2, 3, 4]) == [1, 2, 3, 4]  # already a heap: no swaps
    assert solve([4, 3, 2, 1]) == [1, 3, 2, 4]
    assert solve([3, 3, 3]) == [3, 3, 3]
    import random
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(0, 12)
        distinct = rng.sample(range(100), n)
        assert solve(distinct) == brute_force(distinct), distinct  # same swaps as heapq when values differ
        dup = [rng.randint(1, 4) for _ in range(n)]
        out = solve(dup)  # ties may land in different slots than heapq's, but it must still be a heap
        assert is_min_heap(out) and sorted(out) == sorted(dup), dup


# --- bugs ---
BUGS = [
    {
        "replace": "    for i in range(n // 2 - 1, -1, -1):",
        "with":    "    for i in range(n // 2 - 1, 0, -1):",
        "fix": "the range must reach index 0: the root is the last node to sift down",
        "why": "range(.., 0, -1) stops at 1, so the root is never sifted: [9, 4, 7, 1, 2, 6, 3] keeps 9 on top.",
        "decoys": [
            {"line": "        if smallest == i:", "change": "should be smallest != i"},
            {"line": "        a[i], a[smallest] = a[smallest], a[i]", "change": "should swap a[i] with a[l]"},
            {"line": "    n = len(a)", "change": "should be len(a) - 1"},
        ],
    },
    {
        "replace": "        if r < n and a[r] < a[smallest]:",
        "with":    "        if r < n and a[r] < a[i]:",
        "fix": "compare the right child with the smaller candidate so far, not with the node",
        "why": "Children 1 and 3 under a 9: both beat 9, so the right child 3 wins and 1 ends up below 3, breaking the heap.",
        "decoys": [
            {"line": "        if l < n and a[l] < a[smallest]:", "change": "should be l <= n"},
            {"line": "        i = smallest", "change": "should be i = 2 * i + 1"},
            {"line": "    a = list(nums)", "change": "should sort nums first"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
