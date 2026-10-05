"""
Merge Intervals (LeetCode 56) - Medium
Area: intervals
Key operations: sort by start, compare start with the last merged end, extend end with max, open a new interval

Given a list of intervals [start, end], merge all overlapping intervals and return the
non-overlapping intervals that cover exactly the same points. Touching intervals such as
[1,4] and [4,5] count as overlapping.
Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(intervals: List[List[int]]) -> List[List[int]]:
    """Paint every covered point of a number line (in half units, so [1,2] and [3,4] stay apart),
    then read off the maximal painted runs. O(n * C) for coordinate range C; the waste is touching
    every point inside every interval when only the endpoints matter."""
    painted = set()
    for s, e in intervals:
        painted.update(range(2 * s, 2 * e + 1))
    runs = []
    for p in sorted(painted):
        if runs and p - 1 == runs[-1][1]:
            runs[-1][1] = p
        else:
            runs.append([p, p])
    return [[a // 2, b // 2] for a, b in runs]


# --- optimal ---
def solve(intervals: List[List[int]]) -> List[List[int]]:
    """Sort by start; sweep once keeping the last merged interval. A new interval either starts
    inside it (extend its end) or after it (open a new one). O(n log n) for the sort."""
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda iv: iv[0])
    log(f"sorted by start: {intervals}")
    merged = [list(intervals[0])]
    log(f"open {merged[0]} | merged {merged}")
    for start, end in intervals[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
            log(f"[{start},{end}] starts inside the open interval: extend its end to {last[1]} -> merged {merged}")
        else:
            merged.append([start, end])
            log(f"[{start},{end}] starts after end {last[1]}: open new -> merged {merged}")
    return merged


# --- demo ---
def demo():
    return solve([[1, 3], [2, 6], [8, 10], [15, 18]])


# --- tests ---
def tests():
    assert solve([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert solve([[1, 4], [4, 5]]) == [[1, 5]]  # touching counts as overlapping
    assert solve([[1, 4], [2, 3]]) == [[1, 4]]  # nested: keep the longer end
    assert solve([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]
    assert solve([[5, 6]]) == [[5, 6]]
    assert solve([]) == []
    assert solve([[4, 7], [1, 4], [8, 9], [2, 5]]) == [[1, 7], [8, 9]]  # unsorted input
    assert solve([[2, 2], [1, 1], [2, 3]]) == [[1, 1], [2, 3]]  # zero-length intervals
    original = [[1, 3], [2, 6]]
    assert solve(original) == [[1, 6]] and original == [[1, 3], [2, 6]]  # input untouched
    import random
    random.seed(1)
    for _ in range(200):
        ivs = []
        for _ in range(random.randint(0, 8)):
            s = random.randint(0, 15)
            ivs.append([s, s + random.randint(0, 5)])
        assert solve(ivs) == brute_force(ivs), ivs


# --- bugs ---
BUGS = [
    {
        "replace": "        if start <= last[1]:",
        "with":    "        if start < last[1]:",
        "fix": "touching intervals overlap: compare with <=",
        "why": "An interval that starts exactly where the last one ends is kept separate, so [[1,4],[4,5]] returns [[1,4],[4,5]] instead of [[1,5]].",
        "decoys": [
            {"line": "    merged = [list(intervals[0])]", "change": "should start empty: merged = []"},
            {"line": "        last = merged[-1]", "change": "should be last = merged[0]"},
            {"line": "    return merged", "change": "should return sorted(merged)"},
        ],
    },
    {
        "replace": "            last[1] = max(last[1], end)",
        "with":    "            last[1] = end",
        "fix": "keep the longer end: last[1] = max(last[1], end)",
        "why": "A short interval nested inside the current one shrinks it: [[1,4],[2,3]] returns [[1,3]] instead of [[1,4]].",
        "decoys": [
            {"line": "    for start, end in intervals[1:]:", "change": "should iterate over all of intervals"},
            {"line": "            merged.append([start, end])", "change": "should append [last[1], end]"},
            {"line": "        if start <= last[1]:", "change": "should be if end <= last[1]"},
        ],
    },
    {
        "replace": "    intervals = sorted(intervals, key=lambda iv: iv[0])",
        "with":    "    intervals = sorted(intervals, key=lambda iv: iv[1])",
        "fix": "sort by START so an interval can only overlap the one currently being built",
        "why": "Sorted by end, a long interval arrives last and overlaps earlier closed ones, which the sweep never revisits: [[1,10],[2,3],[4,5]] returns [[2,3],[4,10]] instead of [[1,10]].",
        "decoys": [
            {"line": "    if not intervals:", "change": "should be if len(intervals) < 2"},
            {"line": "            last[1] = max(last[1], end)", "change": "should be max(last[0], end)"},
            {"line": "        return []", "change": "should return intervals"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
