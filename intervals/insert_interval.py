"""
Insert Interval (LeetCode 57)  — Medium
Pattern: Sort by start, sweep and merge

Problem
-------
intervals is sorted by start and non-overlapping. Insert newInterval, merging as needed,
and return the result still sorted and non-overlapping.
Example: [[1,3],[6,9]], new=[2,5] -> [[1,5],[6,9]].
         [[1,2],[3,5],[6,7],[8,10],[12,16]], new=[4,8] -> [[1,2],[3,10],[12,16]].

Brute force
-----------
Append newInterval to the list and run the generic Merge Intervals algorithm: sort
(O(n log n)) then sweep. Correct, but it throws away the fact that the input is ALREADY
sorted and pairwise disjoint; the sort is the wasted step, and the sweep re-examines
pairs of original intervals that are guaranteed not to overlap each other.

From brute force to optimal
---------------------------
The redundancy is sorting an already-sorted list and testing already-disjoint pairs.
Observation: only intervals that touch newInterval can change. Those form a contiguous
run in the sorted list, so the output is: (1) everything that ends before new.start,
untouched; (2) one fused interval = union of new with every interval that overlaps it;
(3) everything that starts after new.end, untouched. A single left-to-right pass with
three phases produces exactly this in O(n), no sort, no re-checking disjoint originals.

Intuition
---------
Walk the intervals. While they finish before the new one begins, copy them. While they
overlap the new one, grow the new one to swallow them. Once an interval starts after the
new one ends, emit the (grown) new interval and copy the rest verbatim.

Geometric view
--------------
Bars on a number line, already sorted and separated. The new bar drops in somewhere.
Bars entirely to its left are untouched, bars entirely to its right are untouched, and
the bars it collides with get fused into it, so its left edge becomes the leftmost
collided start and its right edge the rightmost collided end.

Steps
-----
1. i = 0; while intervals[i].end < new.start: append intervals[i]; i += 1.
2. While i < n and intervals[i].start <= new.end: new = [min starts, max ends]; i += 1.
3. Append new; append all remaining intervals.

Complexity: O(n) time, O(n) space — one pass; output list of size up to n + 1.
Pitfalls: using < instead of <= for touching intervals; forgetting to append newInterval
when it goes at the very end; mutating newInterval in place when the caller reuses it.
"""
from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        start, end = newInterval
        out, i, n = [], 0, len(intervals)
        while i < n and intervals[i][1] < start:  # entirely left of the new interval
            out.append(intervals[i])
            i += 1
        while i < n and intervals[i][0] <= end:  # overlaps: absorb into [start, end]
            start = min(start, intervals[i][0])
            end = max(end, intervals[i][1])
            i += 1
        out.append([start, end])
        out.extend(intervals[i:])  # entirely right of the new interval
        return out


def brute_force(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    # Ignore the sorted/disjoint guarantee: add the interval, sort, and merge generically.
    ivs = sorted([iv[:] for iv in intervals] + [newInterval[:]])
    merged = [ivs[0]]
    for s, e in ivs[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 3], [6, 9]], [2, 5], [[1, 5], [6, 9]]),
        ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8], [[1, 2], [3, 10], [12, 16]]),
        ([], [5, 7], [[5, 7]]),
        ([[1, 5]], [6, 8], [[1, 5], [6, 8]]),
        ([[3, 5], [12, 15]], [6, 6], [[3, 5], [6, 6], [12, 15]]),
    )
    for iv, new, want in cases:
        assert brute_force(iv, new) == want
        assert s.insert(iv, new) == want
    print("ok")
