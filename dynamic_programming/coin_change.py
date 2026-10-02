"""
Coin Change (LeetCode 322)  — Medium
Pattern: Unbounded knapsack (min coins per amount)

Problem
-------
Given coin denominations (unlimited supply of each) and an amount, return the fewest
coins that sum to the amount, or -1 if it cannot be made. Example: coins=[1,2,5],
amount=11 -> 3 (5+5+1).  coins=[2], amount=3 -> -1.  amount=0 -> 0.

Brute force
-----------
Recursion: f(a) = 1 + min(f(a - c) for each coin c <= a), f(0) = 0, unreachable = inf.
The tree branches k ways (k coins) at every level and can be amount levels deep:
O(k^amount) time in the worst case, O(amount) stack. The waste: f(6) is reached via
5+1, 1+5, 2+2+2, 1+1+... and every path re-solves it from scratch.

From brute force to optimal
---------------------------
Overlapping subproblems: f(a) depends only on the remaining amount a, so there are just
amount + 1 distinct subproblems (the user's original memo dict cached exactly these).
State: dp[a] = fewest coins summing to exactly a (inf if impossible), dp[0] = 0.
Recurrence: dp[a] = 1 + min(dp[a - c] for c in coins if c <= a).
Evaluation order: a = 1..amount ascending, so every dp[a - c] is already final. That
turns the top-down memo into a bottom-up loop with no recursion depth limit.
O(amount * k) time, O(amount) space.

Intuition
---------
Whatever the optimal multiset of coins is, it has some LAST coin c. Remove it and the
rest must be an optimal answer for a - c. So try every possible last coin and take the
best, building answers for small amounts first.

Geometric view
--------------
Picture a number line 0..amount. From each point you can jump forward by any coin value.
dp[a] is the fewest jumps from 0 to a: a shortest-path problem on a line (BFS would also
work), filled left to right because every jump goes rightward.

Steps
-----
1. dp = [0] + [inf] * amount.
2. For a in 1..amount: for c in coins with c <= a: dp[a] = min(dp[a], dp[a - c] + 1).
3. Return dp[amount] if finite else -1.

Complexity: O(amount * k) time, O(amount) space — k transitions per amount.
Pitfalls: greedy largest-coin-first fails (coins [1,3,4], amount 6 -> 3+3, not 4+1+1);
returning inf instead of -1; amount == 0 must return 0.
"""
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        inf = amount + 1  # more coins than could ever be needed
        dp = [0] + [inf] * amount
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1  # c is the last coin used
        return dp[amount] if dp[amount] < inf else -1


def brute_force(coins: List[int], amount: int) -> int:
    # Try every coin as the next coin, recursively: exponential.
    def f(a: int) -> float:
        if a == 0:
            return 0
        return min((1 + f(a - c) for c in coins if c <= a), default=float("inf"))

    best = f(amount)
    return -1 if best == float("inf") else best


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 2, 5], 11, 3), ([2], 3, -1), ([1], 0, 0),
             ([1, 3, 4], 6, 2), ([2, 5, 10, 1], 27, 4), ([186, 419, 83, 408], 50, -1)]
    for coins, amount, want in cases:
        assert s.coinChange(coins, amount) == want
        assert brute_force(coins, amount) == want
    print("ok")
