"""
Best Time to Buy and Sell Stock (LeetCode 121)  — Easy
Pattern: Running minimum sweep

Problem
-------
prices[i] is the price of a stock on day i. Choose one day to buy and a later day to sell
so that profit is maximised; return 0 if no profitable trade exists.
Example: prices = [7,1,5,3,6,4] -> 5 (buy at 1 on day 1, sell at 6 on day 4).

Brute force
-----------
Try every pair (buy day i, sell day j > i) and keep the best prices[j] - prices[i].
O(n^2) time, O(1) space. The wasted work: for every sell day j we rescan all earlier days
to find the cheapest buy, although that minimum changes at most once between j-1 and j.

From brute force to optimal
---------------------------
The redundancy is recomputing "cheapest price before j" from scratch for every j.
Observation: the best buy for sell day j is exactly min(prices[0..j-1]), and that running
minimum is maintained in O(1) as j sweeps right. So the inner loop collapses into two
scalars: lowest price seen so far and best profit so far. Seen as a window, the left edge
is the cheapest day so far and the right edge is today; the left edge only ever jumps
forward to a new low, so every day is examined once.

Intuition
---------
Each day ask "if I sold today, what is the best I could have done?" The answer depends only
on the lowest price before today, so carry that single number along instead of rescanning.

Geometric view
--------------
Picture the price curve. Pointer L sits on the lowest valley seen so far and R walks right.
When R dips below L's price the valley moves to R; otherwise the vertical gap R - L is a
candidate profit. The best gap over the whole sweep is the answer.

Steps
-----
1. min_price = +inf, best = 0.
2. For each price p: best = max(best, p - min_price), then min_price = min(min_price, p).
3. Return best.

Complexity: O(n) time, O(1) space — one pass with two scalars.
Pitfalls: Updating min_price before computing the profit for the same day; forgetting that
the answer is 0 when prices only fall; trying to track the buy day index when only the
price is needed.
"""
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float("inf")
        best = 0
        for p in prices:
            best = max(best, p - min_price)   # sell today, bought at the cheapest day so far
            min_price = min(min_price, p)
        return best


def brute_force(prices: List[int]) -> int:
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):   # rescans all earlier buys for each sell day
            best = max(best, prices[j] - prices[i])
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [[7, 1, 5, 3, 6, 4], [7, 6, 4, 3, 1], [5], [2, 4, 1, 7]]
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
    assert s.maxProfit([5]) == 0
    assert s.maxProfit([2, 4, 1, 7]) == 6
    for c in cases:
        assert s.maxProfit(c) == brute_force(c)
    print("ok")
