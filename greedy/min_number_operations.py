"""
Minimum Number of Increments on Subarrays to Form a Target Array (LeetCode 1526)  — Hard
Pattern: Count only the rises (adjacent-difference greedy)

Problem
-------
Start from an all-zero array. One operation picks any contiguous subarray and adds 1 to every
element in it. Return the minimum operations to reach `target`.
Example: target = [3,1,5,4,2,3,4,2] -> 9.

Brute force
-----------
Simulate: while any element is below target, find the longest run of positions still below
target, and increment that run by one. Each pass costs O(n) and there are up to max(target)
passes, so O(n * max) time. The waste: every pass re-scans the whole array just to find where
the runs are, even though the run boundaries are fully determined by the target's shape.

From brute force to optimal
---------------------------
Think of the target as a skyline. Each operation paints one horizontal brush stroke of height 1
across a contiguous range. A stroke can only START at a position where the skyline goes UP
relative to its left neighbor (or at index 0). Walking left to right, position i needs exactly
max(0, target[i] - target[i-1]) new strokes to begin there; where the skyline falls or stays
flat, the existing strokes simply end or continue for free. Summing the rises counts every
stroke exactly once at its left edge.

Intuition
---------
Every operation has exactly one left edge, and left edges only pay for increases. So the answer
is target[0] plus the sum of all positive adjacent differences.

Geometric view
--------------
Draw the target as bars. Each operation is a 1-high horizontal brick laid across some columns.
Bricks must be supported, so a column that is taller than its left neighbor needs that many
bricks to begin at it. Flat or falling steps need no new bricks.

Steps
-----
1. ops = target[0] (that many strokes must start at index 0).
2. For each i >= 1, if target[i] > target[i-1], add the difference.
3. Return ops.

Complexity: O(n) time, O(1) space — one pass, two variables.
Pitfalls: counting falls as well as rises; forgetting the first element starts target[0] strokes.
"""
from typing import List


class Solution:
    def minNumberOperations(self, target: List[int]) -> int:
        ops = target[0]
        for i in range(1, len(target)):
            if target[i] > target[i - 1]:
                ops += target[i] - target[i - 1]
        return ops


def brute_force(target: List[int]) -> int:
    cur = [0] * len(target)
    ops = 0
    while True:
        i, n = 0, len(target)
        # find the first position still below target
        while i < n and cur[i] >= target[i]:
            i += 1
        if i == n:
            return ops
        # extend the stroke across the longest run of still-short positions
        while i < n and cur[i] < target[i]:
            cur[i] += 1
            i += 1
        ops += 1


if __name__ == "__main__":
    s = Solution()
    for t in ([3, 1, 5, 4, 2, 3, 4, 2], [1, 2, 3, 2, 1], [3, 1, 1, 2], [5]):
        assert s.minNumberOperations(t) == brute_force(t)
    assert s.minNumberOperations([3, 1, 5, 4, 2, 3, 4, 2]) == 9
    assert s.minNumberOperations([1, 2, 3, 2, 1]) == 3
    assert s.minNumberOperations([3, 1, 1, 2]) == 4
    print("ok")
