"""
House Robber (LeetCode 198)  — Medium
Pattern: 1-D DP over prefixes (Fibonacci-style)

Problem
-------
Houses in a row hold nums[i] money. You cannot rob two adjacent houses. Return the most
money you can rob. Example: [1,2,3,1] -> 4 (houses 0 and 2).  [2,7,9,3,1] -> 12
(houses 0, 2, 4).

Brute force
-----------
Recursion: rob(i) = max(rob(i + 1), nums[i] + rob(i + 2)), rob(i >= n) = 0. Two branches
per house gives a Fibonacci-shaped tree: O(1.6^n) time, O(n) stack. The waste: rob(i + 2)
is computed once on the "take" branch and again inside the "skip" branch's rob(i + 1).

From brute force to optimal
---------------------------
Overlapping subproblems: rob(i) depends only on i (the user's original memo keyed on
(i, canRob), which is the same information), so there are only n distinct subproblems.
State: dp[i] = best loot from the first i houses.
Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]) — skip house i-1, or rob it and
fall back to the best from two houses earlier. dp[0] = 0, dp[1] = nums[0].
Order: left to right. Space reduction: only dp[i-1] and dp[i-2] are read, so keep two
rolling values. O(n) time, O(1) space.

Intuition
---------
At each house the only decision is rob or skip. Robbing forces you to skip the neighbour,
so its value pairs with the best total from two houses back; skipping inherits the best
total from one house back. Keep the better of the two as you sweep.

Geometric view
--------------
Picture two running totals walking down the street: "best up to the previous house" and
"best up to the house before that". At each new house the new best is either the first
total, or the second total plus this house's money.

Steps
-----
1. prev2, prev1 = 0, 0.
2. For x in nums: prev2, prev1 = prev1, max(prev1, prev2 + x).
3. Return prev1.

Complexity: O(n) time, O(1) space — one pass, two rolling values.
Pitfalls: greedy "rob every other house" (odd vs even indices) fails on [2,1,1,2];
single-house input; updating prev1 before saving it into prev2.
"""
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        prev2 = prev1 = 0  # best loot up to house i-2, i-1
        for x in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1


def brute_force(nums: List[int]) -> int:
    # Rob-or-skip recursion at every house: exponential.
    def best(i: int) -> int:
        if i >= len(nums):
            return 0
        return max(best(i + 1), nums[i] + best(i + 2))

    return best(0)


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 2, 3, 1], 4), ([2, 7, 9, 3, 1], 12), ([5], 5),
             ([2, 1, 1, 2], 4), ([0, 0, 0], 0)]
    for nums, want in cases:
        assert s.rob(nums) == want
        assert brute_force(nums) == want
    print("ok")
