"""
Merge K Sorted Arrays - Basics
Area: heaps
Key operations: seed the heap with every array's head as (value, array index, element index), pop the min, push that array's next element

Merge k sorted arrays into one sorted array. A min-heap holds one candidate per array: pop the smallest,
append it, and push the successor from the same array. Each element enters and leaves the heap once.
Example: [[1, 4, 7], [2, 5], [0, 8, 9]] -> [0, 1, 2, 4, 5, 7, 8, 9]
"""
import heapq
from typing import List


# --- brute force ---
def brute_force(arrays: List[List[int]]) -> List[int]:
    """Concatenate and sort. O(N log N); ignores that every array is already sorted."""
    return sorted(x for arr in arrays for x in arr)


# --- optimal ---
def solve(arrays: List[List[int]]) -> List[int]:
    """One candidate per array in a heap keyed (value, which array, position). O(N log k)."""
    heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]
    heapq.heapify(heap)
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(arrays[i]):
            heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))
    return out


# --- demo ---
def demo():
    return solve([[1, 4, 7], [2, 5], [0, 8, 9]])


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
    print("result:", demo())
