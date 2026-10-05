"""
Quick Sort - Basics
Area: sorting
Key operations: Lomuto partition around the last element, swap the pivot into its final slot, recurse on both sides

Pick the last element as the pivot. Walk j across the range keeping a[lo..i] as the elements <= pivot:
every time a[j] <= pivot grow that region by swapping a[j] in. Finally swap the pivot to i + 1, its
final position, and recurse on the two sides. The pivot choice is deterministic so the trace is
reproducible. O(n log n) on average, O(n^2) on sorted input with this pivot, in place, not stable.
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """Python's sorted (Timsort), the reference for every sorting exercise. O(n log n)."""
    return sorted(nums)


# --- optimal ---
def partition(a: List[int], lo: int, hi: int) -> int:
    """Lomuto: pivot a[hi]; a[lo..i] holds the values <= pivot; return the pivot's final index. O(hi - lo)."""
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def quick_sort(a: List[int], lo: int, hi: int) -> None:
    """Partition, then sort the two sides; a range of 0 or 1 elements is already sorted."""
    if lo < hi:
        p = partition(a, lo, hi)
        quick_sort(a, lo, p - 1)
        quick_sort(a, p + 1, hi)


def solve(nums: List[int]) -> List[int]:
    a = list(nums)
    quick_sort(a, 0, len(a) - 1)
    return a


# --- demo ---
def demo():
    return solve([5, 2, 4, 6, 1, 3])


# --- bugs ---
BUGS = [
    {
        "replace": "    a[i + 1], a[hi] = a[hi], a[i + 1]",
        "with":    "    a[i], a[hi] = a[hi], a[i]",
        "fix": "the pivot belongs at i + 1, the first slot AFTER the small side a[lo..i]",
        "why": "Swapping with a[i] throws the last small element to the far right: [3, 1, 2] partitions into [2, 3, 1] and sorts wrong.",
        "decoys": [
            {"line": "    i = lo - 1", "change": "should be i = lo"},
            {"line": "        if a[j] <= pivot:", "change": "should be < to keep duplicates right"},
            {"line": "    pivot = a[hi]", "change": "should be a[lo]"},
        ],
    },
    {
        "replace": "    for j in range(lo, hi):",
        "with":    "    for j in range(lo, hi + 1):",
        "fix": "scan up to hi - 1 only: the pivot sits at hi and must not be swapped into the small side",
        "why": "The pivot satisfies a[j] <= pivot, so it gets swapped away from hi and the final swap places garbage: [2, 1] loops into RecursionError.",
        "decoys": [
            {"line": "        quick_sort(a, lo, p - 1)", "change": "should be quick_sort(a, lo, p)"},
            {"line": "        quick_sort(a, p + 1, hi)", "change": "should be quick_sort(a, p, hi)"},
            {"line": "    if lo < hi:", "change": "should be lo <= hi"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
