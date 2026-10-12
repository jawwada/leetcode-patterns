"""
Best Time to Buy and Sell Stock - Track the Running Minimum

Given a stock's price on each day, buy on one day and sell on a later day to
make the largest profit, or return 0 if no trade makes money:
[7, 1, 5, 3, 6, 4] -> 5 (buy at 1, sell at 6).
"""
import math                         # math.inf is higher than any price


# --- algorithm ---
def max_profit(prices):
    """Sell each day against the running minimum. O(n) time, O(1) space."""
    min_price = math.inf            # cheapest price so far
    best = 0                        # no trade at all earns 0
    for price in prices:
        if price < min_price:       # a cheaper day to have bought on
            min_price = price
        profit = price - min_price  # sell today, bought at the running minimum
        if profit > best:
            best = profit
    return best


# --- try it ---
print(max_profit([7, 1, 5, 3, 6, 4]))   # -> 5
print(max_profit([7, 6, 4, 3, 1]))      # -> 0
print(max_profit([2, 4, 1, 7]))         # -> 6
print(max_profit([]))                   # -> 0
