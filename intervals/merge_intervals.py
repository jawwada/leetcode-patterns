"""
Merge Intervals (LeetCode 56)  — Medium
Pattern: Sort by start, sweep and merge

Problem
-------
Given intervals [start, end], merge all overlapping ones and return the non-overlapping
intervals that cover the same points. Touching intervals ([1,4],[4,5]) count as overlapping.
Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]].

Brute force
-----------
Repeat until no change: for every pair (i, j), if they overlap replace them with their
union and restart. Each pass is O(n^2) pair checks and up to n merges happen -> O(n^3)
time, O(n) space. The waste: the overlap test is repeated for pairs that were already
found disjoint, and every merge triggers a fresh full-pairs scan.

From brute force to optimal
---------------------------
The redundancy is checking pairs that are far apart on the number line. Observation: if
intervals are sorted by start, an interval can only overlap the one currently being built
(the last merged interval) -- anything that starts later than the current end can never
reach back. So sort once (O(n log n)) and sweep left to right, keeping a single "current"
interval: extend its end when the next start fits inside, otherwise close it and start a
new one. Each interval is compared exactly once -> O(n log n) total.

Intuition
---------
Sort by start so the sweep never has to look backwards. Keep a running interval; the next
interval either begins inside it (extend the end to the max of both ends) or after it
(the running interval is finished -- emit it and start a new one).

Geometric view
--------------
Picture the intervals as horizontal bars stacked above a number line, sorted by left
edge. A vertical sweep line moves right; the "current" bar's right edge is a frontier.
Any bar whose left edge is at or before the frontier is fused into the current bar and
may push the frontier further right; the first bar starting past the frontier closes the
block.

Steps
-----
1. Sort intervals by start.
2. merged = [first]; for each [s, e]: if s <= merged[-1][1]: merged[-1][1] = max(end, e)
   else append [s, e].
3. Return merged.

Complexity: O(n log n) time, O(n) space — sorting; one linear sweep; output list.
Pitfalls: using < instead of <= for touching intervals; setting end = e instead of
max(end, e) when a short interval is nested inside a long one; forgetting to sort.
"""
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda iv: iv[0])
        merged = [intervals[0][:]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)  # nested interval: keep the longer end
            else:
                merged.append([start, end])
        return merged


def brute_force(intervals: List[List[int]]) -> List[List[int]]:
    # Repeatedly scan every pair; merge the first overlapping pair found and restart.
    ivs = [iv[:] for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(ivs)):
            for j in range(i + 1, len(ivs)):
                a, b = ivs[i], ivs[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    ivs[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    ivs.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(ivs)


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[1, 4], [2, 3]], [[1, 4]]),
        ([[5, 6]], [[5, 6]]),
        ([[4, 7], [1, 4], [8, 9], [2, 5]], [[1, 7], [8, 9]]),
    )
    for iv, want in cases:
        assert brute_force([x[:] for x in iv]) == want
        assert s.merge([x[:] for x in iv]) == want
    print("ok")
