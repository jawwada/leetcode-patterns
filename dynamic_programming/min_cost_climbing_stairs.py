"""
Min Cost Climbing Stairs (LeetCode 746)  — Easy
Pattern: 1-D DP over prefixes (Fibonacci-style)

Problem
-------
cost[i] is the price of stepping on stair i. After paying you may climb one or two
stairs. You may start on stair 0 or stair 1. Return the minimum cost to reach the top,
which is one past the last stair. Example: [10,15,20] -> 15 (start at 1, jump to top).
[1,100,1,1,1,100,1,1,100,1] -> 6.

Brute force
-----------
Recursion: f(i) = cost[i] + min(f(i+1), f(i+2)) is the cheapest way from stair i to the
top, f(i) = 0 for i >= n; answer min(f(0), f(1)). Every call branches twice, giving a
Fibonacci-shaped call tree: O(1.6^n) time, O(n) stack. The waste: f(i+2) is solved once
directly and again inside f(i+1).

From brute force to optimal
---------------------------
Overlapping subproblems: there are only n + 1 distinct stairs, but the recursion solves
each one Fibonacci-many times.
State: dp[i] = minimum cost to STAND on position i without having paid cost[i] yet
(dp[0] = dp[1] = 0 because you may start there for free).
Recurrence: dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]).
Order: i = 2..n left to right (the user's original table); answer dp[n]. Space
reduction: each cell reads only the two before it, so keep two rolling values. O(n) time,
O(1) space.

Intuition
---------
To arrive at step i you came from i-1 (and paid for it) or from i-2 (and paid for it).
Take the cheaper of those two arrivals; repeat up to the top.

Geometric view
--------------
Picture a staircase with a price tag on each step. Two running totals ride up the stairs
side by side: "cheapest to reach the step below me" and "cheapest to reach two below".
Each new step looks back at just those two.

Steps
-----
1. a, b = 0, 0  (dp[i-2], dp[i-1] at i = 2).
2. For i in 2..n: a, b = b, min(b + cost[i-1], a + cost[i-2]).
3. Return b.

Complexity: O(n) time, O(1) space — one pass, two rolling values.
Pitfalls: the top is index n, not n - 1; starting cost is 0 for both stair 0 and 1;
adding cost[i] when landing instead of when leaving.
"""
from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        a = b = 0  # dp[i-2], dp[i-1]: cheapest cost to stand on those positions
        for i in range(2, len(cost) + 1):
            a, b = b, min(b + cost[i - 1], a + cost[i - 2])
        return b


def brute_force(cost: List[int]) -> int:
    # f(i) = cost from stair i to the top, trying both jumps: exponential.
    def f(i: int) -> int:
        if i >= len(cost):
            return 0
        return cost[i] + min(f(i + 1), f(i + 2))

    return min(f(0), f(1))


if __name__ == "__main__":
    s = Solution()
    cases = [([10, 15, 20], 15), ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], 6),
             ([0, 0], 0), ([5, 3], 3), ([0, 1, 2, 2], 2)]
    for cost, want in cases:
        assert s.minCostClimbingStairs(cost) == want
        assert brute_force(cost) == want
    print("ok")
