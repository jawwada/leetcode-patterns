"""
Maximum Subarray (LeetCode 53)  — Medium
Pattern: Greedy running sum (Kadane)

Problem
-------
Given an integer array `nums`, return the largest sum of any contiguous non-empty subarray.
Example: nums = [-2,1,-3,4,-1,2,1,-5,4] -> 6 (subarray [4,-1,2,1]).

Brute force
-----------
For every start i, extend an end j to the right accumulating the running sum and track the best.
O(n^2) time, O(1) space (O(n^3) if you re-sum each (i, j) from scratch). The wasted work: for a
fixed end j, we recompute "best sum ending at j" from every possible start, although the starts
are not independent — a negative prefix hurts every j that includes it.

From brute force to optimal
---------------------------
The redundancy is reconsidering all starts for every end. Observation: the best subarray ending
at j either extends the best subarray ending at j-1 or starts fresh at j; extending only pays off
if the carried sum is positive. So one running sum `cur` suffices: cur = max(nums[j], cur + nums[j]).
Equivalently, in greedy terms: whenever the running sum drops below zero, drop it and restart —
a negative prefix can never help a later subarray. One pass, two variables.

Intuition
---------
Walk left to right adding each number to a running total. A negative running total is dead
weight: any subarray that keeps it would be better off without it, so reset to the current
element. Record the maximum total seen at any moment.

Geometric view
--------------
Plot the running sum as a path. Each time the path dips below zero, you cut it and start a new
path from the x-axis. The answer is the highest point reached by any path segment.

    nums:  -2   1  -3   4  -1   2   1  -5   4
    cur:   -2   1  -2   4   3   5   6   1   5
            ^reset  ^reset        ^best = 6

Steps
-----
1. cur = best = nums[0].
2. For x in nums[1:]: cur = max(x, cur + x); best = max(best, cur).
3. Return best.

Complexity: O(n) time, O(1) space — a single pass with two scalars.
Pitfalls: initialising best to 0 (fails for all-negative arrays); resetting cur to 0 instead of
to x (same bug); forgetting the subarray must be non-empty.
"""
from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        cur = best = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)            # a negative running sum is dead weight: restart at x
            best = max(best, cur)
        return best


def brute_force(nums: List[int]) -> int:
    best = nums[0]
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            best = max(best, total)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-3, -1, -2], -1),
        ([2, -1, 2, -1, 2], 4),
    ]
    for nums, want in cases:
        assert s.maxSubArray(nums) == want
        assert brute_force(nums) == want
    print("ok")
