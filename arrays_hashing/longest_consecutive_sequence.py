"""
Longest Consecutive Sequence (LeetCode 128)  — Medium
Pattern: Hash set with sequence-start detection

Problem
-------
Given an unsorted integer array, return the length of the longest run of consecutive
integers (values, not positions) in O(n) time.
Example: nums = [100, 4, 200, 1, 3, 2] -> 4, from the run 1, 2, 3, 4.

Brute force
-----------
For every element x, count upward: is x+1 in the array? x+2? ... each check a linear
scan. O(n^3) worst case (n starts, up to n steps, each an O(n) scan), O(1) space.
Sorting first and scanning gives O(n log n), but the problem demands O(n). The
repeated work is twofold: linear membership scans, and counting the same run again
from every one of its members (the run 1-2-3-4 is walked from 1, from 2, from 3 and
from 4).

From brute force to optimal
---------------------------
First redundancy: membership scans. Put everything in a hash set so "is x+1 present?"
is O(1). Second redundancy: re-walking a run from each of its members. Observe that
a run has exactly one natural starting point — the element x such that x-1 is NOT in
the set. Only begin counting from those. Every element then belongs to exactly one
walk (the one started at its run's minimum), so the total number of x+1 probes across
all walks is at most n. That amortisation is the whole trick.

Intuition
---------
A run of consecutive values is fully determined by its smallest element. Identify
the smallest elements (no left neighbour in the set) and measure each run once, from
its bottom. The set gives O(1) neighbour checks, so measuring all runs costs O(n)
total despite the nested loop.

Geometric view
--------------
Lay the distinct values on an integer number line as dots. Runs are maximal
unbroken stretches of dots. The algorithm looks at each dot, keeps only those whose
left neighbour is empty (the left end of a stretch), and from each such left end
walks right until a gap, recording the stretch length.

Steps
-----
1. Build a set from nums (also deduplicates).
2. For each x in the set, skip it if x - 1 is in the set (not a run start).
3. Otherwise walk y = x, x+1, x+2, ... while y in the set, counting length.
4. Keep the maximum length seen; return it (0 for an empty array).

Complexity: O(n) time, O(n) space — each element is the start of at most one walk
and is visited inside at most one walk.
Pitfalls: iterating over the list instead of the set (duplicates re-walk runs);
forgetting the x-1 check makes it O(n^2); sorting first violates the stated bound.
"""
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        values = set(nums)
        best = 0
        for x in values:
            if x - 1 in values:        # not the start of a run; its run is counted elsewhere
                continue
            length = 1
            while x + length in values:
                length += 1
            best = max(best, length)
        return best


def brute_force(nums: List[int]) -> int:
    best = 0
    for x in nums:
        length = 1
        while x + length in nums:      # list membership is a linear scan
            length += 1
        best = max(best, length)
    return best


if __name__ == "__main__":
    s = Solution()
    assert s.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert s.longestConsecutive([]) == 0
    assert s.longestConsecutive([1, 1, 1]) == 1
    for case in ([100, 4, 200, 1, 3, 2], [0, 3, 7, 2, 5, 8, 4, 6, 0, 1], [], [1, 1, 1]):
        assert s.longestConsecutive(case) == brute_force(case)
    print("ok")
