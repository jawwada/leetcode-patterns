"""
Merge K Sorted Arrays - Basics
Area: heaps
Key operations: seed the heap with every array's head as (value, array index, element index), pop the min, push that array's next element

Merge k sorted arrays into one sorted array. A min-heap holds one candidate per array: pop the smallest,
append it, and push the successor from the same array. Each element enters and leaves the heap once.
Example: [[1, 4, 7], [2, 5], [0, 8, 9]] -> [0, 1, 2, 4, 5, 7, 8, 9]
"""
import sys
import heapq
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(arrays: List[List[int]]) -> List[int]:
    """Concatenate and sort. O(N log N); ignores that every array is already sorted."""
    return sorted(x for arr in arrays for x in arr)


# --- optimal ---
def solve(arrays: List[List[int]]) -> List[int]:
    """One candidate per array in a heap keyed (value, which array, position). O(N log k)."""
    heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]
    heapq.heapify(heap)
    log(f"heads {heap}")
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        log(f"pop {val} (array {i} pos {j}) -> out {out}")
        if j + 1 < len(arrays[i]):
            heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))
            log(f"    push next of array {i}: {arrays[i][j + 1]}   heap {heap}")
    return out


# --- demo ---
def demo():
    return solve([[1, 4, 7], [2, 5], [0, 8, 9]])


# --- tests ---
def tests():
    assert solve([[1, 4, 7], [2, 5], [0, 8, 9]]) == [0, 1, 2, 4, 5, 7, 8, 9]
    assert solve([]) == []
    assert solve([[], [], []]) == []
    assert solve([[3]]) == [3]
    assert solve([[], [1, 2], []]) == [1, 2]
    assert solve([[1, 1], [1], [0, 1]]) == [0, 1, 1, 1, 1]
    import random
    rng = random.Random(0)
    for _ in range(200):
        arrays = [sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(0, 4))]
        assert solve(arrays) == brute_force(arrays), arrays


# --- bugs ---
BUGS = [
    {
        "replace": "        if j + 1 < len(arrays[i]):",
        "with":    "        if j + 1 <= len(arrays[i]):",
        "fix": "the successor exists only while j + 1 is STRICTLY below the array's length",
        "why": "After the last element of an array, j + 1 == len, and arrays[i][j + 1] raises IndexError.",
        "decoys": [
            {"line": "        val, i, j = heapq.heappop(heap)", "change": "should be heap.pop(0)"},
            {"line": "    heapq.heapify(heap)", "change": "should be heap.sort(reverse=True)"},
            {"line": "        out.append(val)", "change": "should append arrays[i][j]"},
        ],
    },
    {
        "replace": "    heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]",
        "with":    "    heap = [(arr[0], i, 0) for i, arr in enumerate(arrays)]",
        "fix": "skip empty arrays when seeding: they have no head to offer",
        "why": "An empty input array has no arr[0]: [[], [1, 2], []] raises IndexError before the merge starts.",
        "decoys": [
            {"line": "            heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))", "change": "should push (i, j + 1, value)"},
            {"line": "    while heap:", "change": "should be while len(heap) > 1"},
            {"line": "    return out", "change": "should return sorted(out)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
