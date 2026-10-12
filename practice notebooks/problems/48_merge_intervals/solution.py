"""
Merge Intervals (LeetCode 56) - Medium
Area: intervals
Key operations: sort by start, compare start with the last merged end, extend end with max, open a new interval

Given a list of intervals [start, end], merge all overlapping intervals and return the
non-overlapping intervals that cover exactly the same points. Touching intervals such as
[1,4] and [4,5] count as overlapping.
Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
"""
from typing import List


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
    merged = [list(intervals[0])]
    for start, end in intervals[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return merged


# --- demo ---
def demo():
    return solve([[1, 3], [2, 6], [8, 10], [15, 18]])


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
    print("result:", demo())
