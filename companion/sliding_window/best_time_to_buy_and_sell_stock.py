"""
Best Time to Buy and Sell Stock (LeetCode 121) - Easy
Chapter: sliding_window
Pattern: Running minimum sweep

prices[i] is the price of a stock on day i. Choose one day to buy and a later day to sell
so that the profit is as large as possible; return 0 if no profitable trade exists.
Example: prices = [7, 1, 5, 3, 6, 4] -> 5 (buy at 1 on day 1, sell at 6 on day 4).
"""
import math                     # math.inf is "bigger than any price"


# --- brute force ---
def brute_force(prices):
    """Try every buy day with every later sell day. O(n^2) time, O(1) space."""
    best = 0
    for buy in range(len(prices)):
        for sell in range(buy + 1, len(prices)):    # rescans every earlier buy for each sell
            profit = prices[sell] - prices[buy]
            if profit > best:
                best = profit
    return best


# --- optimal ---
def max_profit(prices):
    """Carry the cheapest price so far and sell today against it. O(n) time, O(1) space."""
    min_price = math.inf
    best = 0
    for price in prices:
        profit = price - min_price                  # sell today, bought on the cheapest day so far
        if profit > best:
            best = profit
        if price < min_price:                       # update the minimum AFTER using it
            min_price = price
    return best


# --- try the brute force ---
print(brute_force([7, 1, 5, 3, 6, 4]))   # -> 5
print(brute_force([7, 6, 4, 3, 1]))      # -> 0
print(brute_force([2, 4, 1, 7]))         # -> 6


# --- try the optimal ---
print(max_profit([7, 1, 5, 3, 6, 4]))    # -> 5
print(max_profit([7, 6, 4, 3, 1]))       # -> 0
print(max_profit([2, 4, 1, 7]))          # -> 6
