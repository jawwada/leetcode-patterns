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
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
    log(f"counting sort {nums}: counts {counts}   (counts[v] = how many v)")
    out = []
    for v, c in enumerate(counts):
        out += [v] * c
        log(f"    value {v} x{c} -> {out}")
    return out


def bucket_sort(xs: List[float]) -> List[float]:
    """n buckets over [0, 1); int(x * n) grows with x, so bucket order is value order. O(n) expected."""
    n = len(xs)
    buckets = [[] for _ in range(n)]
    log(f"bucket sort {xs}: {n} buckets, x goes to int(x * {n})")
    for x in xs:
        buckets[int(x * n)].append(x)
        log(f"    {x} -> bucket {int(x * n)}")
    log(f"buckets {buckets}")
    out = []
    for b in buckets:
        out += sorted(b)
    log(f"sort each bucket and concatenate -> {out}")
    return out


def solve(values: list) -> list:
    """Counting sort for ints, bucket sort for floats in [0, 1)."""
    if all(isinstance(v, int) for v in values):
        return counting_sort(values)
    return bucket_sort(values)


# --- demo ---
def demo():
    return solve([2, 5, 3, 0, 2, 3, 0, 3]), solve([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68])


# --- tests ---
def tests():
    assert solve([2, 5, 3, 0, 2, 3, 0, 3]) == [0, 0, 2, 2, 3, 3, 3, 5]
    assert solve([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]) == [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]
    assert solve([]) == []
    assert solve([7]) == [7]
    assert solve([0.5]) == [0.5]
    assert solve([0, 0, 0]) == [0, 0, 0]
    assert solve([9, 0]) == [0, 9]
    assert solve([0.99, 0.98, 0.0, 0.97]) == [0.0, 0.97, 0.98, 0.99]  # three values in the top bucket
    import random
    rng = random.Random(0)
    for _ in range(200):
        ints = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
        assert solve(ints) == brute_force(ints), ints
        floats = [rng.randrange(100) / 100 for _ in range(rng.randint(1, 10))]  # in [0, 1)
        assert solve(floats) == brute_force(floats), floats


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
