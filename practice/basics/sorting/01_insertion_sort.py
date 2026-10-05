"""
Insertion Sort - Basics
Area: sorting
Key operations: take the next element, shift larger prefix elements one slot right, drop it into the gap

Grow a sorted prefix one element at a time: take a[i], shift every element of the sorted prefix a[:i]
that is bigger than it one slot to the right, and place a[i] in the gap that opens. O(n^2) in general,
O(n) when the input is nearly sorted, in place and stable (equal keys are never shifted past).
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""
from typing import List


def mark(a, k):
    """Trace helper: the array with the sorted prefix a[:k] marked, '[1 2 5 | 4 6 3]'."""
    return "[" + " ".join(map(str, a[:k])) + " | " + " ".join(map(str, a[k:])) + "]"


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """Python's sorted (Timsort), the reference for every sorting exercise. O(n log n)."""
    return sorted(nums)


# --- optimal ---
def solve(nums: List[int]) -> List[int]:
    """Sorted prefix grows by one each round; the new element walks left to its slot. O(n^2), stable."""
    a = list(nums)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# --- demo ---
def demo():
    return solve([5, 2, 4, 6, 1, 3])


# --- bugs ---
BUGS = [
    {
        "replace": "        while j >= 0 and a[j] > key:",
        "with":    "        while j > 0 and a[j] > key:",
        "fix": "let j reach 0: the first element of the prefix must also be able to shift right",
        "why": "With j > 0 the element at index 0 is never shifted, so a new minimum lands at index 1: [2, 1] stays [2, 1].",
        "decoys": [
            {"line": "        key = a[i]", "change": "should be a[i - 1]"},
            {"line": "            j -= 1", "change": "should be j += 1"},
            {"line": "    for i in range(1, len(a)):", "change": "should start at 0"},
        ],
    },
    {
        "replace": "        a[j + 1] = key",
        "with":    "        a[j] = key",
        "fix": "the gap is at j + 1: the loop stops with a[j] <= key, so key goes just to its right",
        "why": "Writing to a[j] overwrites the element that stopped the scan and leaves a duplicate in the gap: [5, 2] becomes [2, 5] only by luck, [5, 2, 4] becomes [2, 4, 4].",
        "decoys": [
            {"line": "            a[j + 1] = a[j]", "change": "should be a[j] = a[j + 1]"},
            {"line": "        j = i - 1", "change": "should be j = i"},
            {"line": "    a = list(nums)", "change": "should sort in place without copying"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
