"""
Counting Sort and Bucket Sort - Basics
Area: sorting
Key operations: count occurrences by value, emit each value count times, drop floats into n buckets by int(x * n), sort each bucket and concatenate

Two non-comparison sorts. Counting sort for small non-negative ints: counts[v] is how often v occurs,
then walk the counts in order. O(n + k) where k is the max value. Bucket sort for floats in [0, 1):
bucket index int(x * n) is monotone in x, so sorting each bucket and concatenating sorts everything;
O(n) expected when values are spread evenly. solve picks counting sort for ints and bucket sort otherwise.
Example: [2, 5, 3, 0, 2, 3, 0, 3] -> [0, 0, 2, 2, 3, 3, 3, 5]
         [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68] -> [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]
"""
from typing import List


# --- brute force ---
def brute_force(values: list) -> list:
    """Python's sorted (Timsort), the reference for every sorting exercise. O(n log n)."""
    return sorted(values)


# --- optimal ---
def counting_sort(nums: List[int]) -> List[int]:
    """Index by value: counts[v] copies of v, emitted in index order. O(n + max)."""
    if not nums:
        return []
    counts = [0] * (max(nums) + 1)
    for x in nums:
        counts[x] += 1
    out = []
    for v, c in enumerate(counts):
        out += [v] * c
    return out


def bucket_sort(xs: List[float]) -> List[float]:
    """n buckets over [0, 1); int(x * n) grows with x, so bucket order is value order. O(n) expected."""
    n = len(xs)
    buckets = [[] for _ in range(n)]
    for x in xs:
        buckets[int(x * n)].append(x)
    out = []
    for b in buckets:
        out += sorted(b)
    return out


def solve(values: list) -> list:
    """Counting sort for ints, bucket sort for floats in [0, 1)."""
    if all(isinstance(v, int) for v in values):
        return counting_sort(values)
    return bucket_sort(values)


# --- demo ---
def demo():
    return solve([2, 5, 3, 0, 2, 3, 0, 3]), solve([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68])


# --- bugs ---
BUGS = [
    {
        "replace": "    counts = [0] * (max(nums) + 1)",
        "with":    "    counts = [0] * max(nums)",
        "fix": "values run from 0 to max inclusive, so the counts array needs max + 1 slots",
        "why": "The largest value has no slot: counting [2, 5, 3] raises IndexError at counts[5].",
        "decoys": [
            {"line": "        counts[x] += 1", "change": "should be counts[x] = 1"},
            {"line": "        out += [v] * c", "change": "should be out += [c] * v"},
            {"line": "    for v, c in enumerate(counts):", "change": "should iterate reversed(counts)"},
        ],
    },
    {
        "replace": "        out += sorted(b)",
        "with":    "        out += b",
        "fix": "sort each bucket before concatenating; a bucket only groups nearby values, it does not order them",
        "why": "Values that share a bucket keep arrival order: 0.78 and 0.72 both go to bucket 7 and come out as 0.78, 0.72.",
        "decoys": [
            {"line": "        buckets[int(x * n)].append(x)", "change": "should be int(x * (n - 1))"},
            {"line": "    buckets = [[] for _ in range(n)]", "change": "should be [[]] * n"},
            {"line": "    n = len(xs)", "change": "should be len(xs) + 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
