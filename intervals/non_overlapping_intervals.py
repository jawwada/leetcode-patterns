"""
Non-overlapping Intervals (LeetCode 435)  — Medium
Pattern: Greedy by earliest end (interval scheduling)

Problem
-------
Given intervals [start, end], return the minimum number to remove so that the rest are
pairwise non-overlapping. Touching intervals ([1,2],[2,3]) do NOT overlap.
Example: [[1,2],[2,3],[3,4],[1,3]] -> 1.  [[1,2],[1,2],[1,2]] -> 2.

Brute force
-----------
Try every subset of intervals, keep the largest subset that is pairwise non-overlapping,
and return n - its size. O(2^n * n^2) time (check all pairs in each subset), O(n) space.
The waste is enormous: subsets that share a bad pair are re-tested from scratch, and most
subsets are obviously dominated by one that swaps an interval for a shorter-ending one.

From brute force to optimal
---------------------------
"Minimum removals" = n - "maximum non-overlapping set", the classic interval scheduling
problem. Observation (exchange argument): among the intervals still available, the one
with the EARLIEST END can always be kept -- any optimal solution that keeps a different
first interval can swap it for the earliest-ending one without creating overlaps, since
that one leaves at least as much room to the right. So sort by end, sweep, and greedily
keep every interval that starts at or after the last kept end; count the rest as removed.
O(n log n), no subsets.

Intuition
---------
To fit the most intervals, always finish as early as possible: pick the interval that
ends first, then the next one that starts after it and ends first, and so on. Every
interval you skip because it starts before the current end is a removal.

Geometric view
--------------
Bars above a number line, sorted by right edge. A vertical "fence" sits at the right
edge of the last kept bar. Walk the bars in end order: a bar whose left edge is at or
past the fence is kept and the fence jumps to its right edge; a bar whose left edge is
before the fence crosses it and is removed. Jumping the fence as little as possible is
what the earliest-end rule achieves.

Steps
-----
1. Sort intervals by end.
2. last_end = -inf, removed = 0.
3. For [s, e]: if s >= last_end: last_end = e else removed += 1.
4. Return removed.

Complexity: O(n log n) time, O(1) extra space — sorting; one pass with two scalars.
Pitfalls: sorting by start instead of end (greedy by start is wrong: [1,100] would block
everything); using > instead of >= so touching intervals are counted as overlapping.
"""
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda iv: iv[1])  # earliest end first
        removed, last_end = 0, float("-inf")
        for start, end in intervals:
            if start >= last_end:
                last_end = end  # keep: it starts after the last kept one finishes
            else:
                removed += 1  # overlaps the kept one, which ends no later: drop this
        return removed


def brute_force(intervals: List[List[int]]) -> int:
    # Enumerate every subset; keep the largest that is pairwise non-overlapping.
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        chosen = [intervals[i] for i in range(n) if mask >> i & 1]
        ok = all(a[1] <= b[0] or b[1] <= a[0]
                 for i, a in enumerate(chosen) for b in chosen[i + 1:])
        if ok:
            best = max(best, len(chosen))
    return n - best


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 2], [2, 3], [3, 4], [1, 3]], 1),
        ([[1, 2], [1, 2], [1, 2]], 2),
        ([[1, 2], [2, 3]], 0),
        ([[1, 100], [11, 22], [1, 11], [2, 12]], 2),
        ([[0, 5]], 0),
    )
    for iv, want in cases:
        assert brute_force([x[:] for x in iv]) == want
        assert s.eraseOverlapIntervals([x[:] for x in iv]) == want
    print("ok")
