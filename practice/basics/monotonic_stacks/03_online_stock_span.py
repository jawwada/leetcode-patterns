"""
Online Stock Span (LeetCode 901) - Basics
Area: monotonic stacks
Key operations: pop while top price <= today, add the popped span to today's, push (price, span)

A StockSpanner receives one price per day; next(price) returns the span: how many consecutive days
ending today (today included) had a price <= today's. A popped day hands its whole span to today,
so the stack only keeps days with strictly decreasing prices bottom to top.
Example: prices [100, 80, 60, 70, 60, 75, 85] -> spans [1, 1, 1, 2, 1, 4, 6]
"""
from typing import List


# --- brute force ---
def brute_force(prices: List[int]) -> List[int]:
    """For every day walk left while the price is <= today's and count. O(n^2)."""
    spans = []
    for i, p in enumerate(prices):
        j = i
        while j >= 0 and prices[j] <= p:
            j -= 1
        spans.append(i - j)
    return spans


# --- optimal ---
class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span) with prices strictly decreasing bottom -> top

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            p, s = self.stack.pop()
            span += s
        self.stack.append((price, span))
        return span


def solve(prices: List[int]) -> List[int]:
    """Feed the prices one by one; each price is pushed once and popped at most once, amortized O(1) per day."""
    spanner, spans = StockSpanner(), []
    for day, p in enumerate(prices):
        spans.append(spanner.next(p))
    return spans


# --- demo ---
def demo():
    return solve([100, 80, 60, 70, 60, 75, 85])


# --- bugs ---
BUGS = [
    {
        "replace": "        while self.stack and self.stack[-1][0] <= price:",
        "with":    "        while self.stack and self.stack[-1][0] < price:",
        "fix": "a day with an EQUAL price belongs to the span, so pop while top <= price",
        "why": "[60, 60] leaves the first 60 on the stack and the second day gets span 1 instead of 2.",
        "decoys": [
            {"line": "        span = 1", "change": "should start at 0"},
            {"line": "        self.stack.append((price, span))", "change": "should push (span, price)"},
            {"line": "        spans.append(spanner.next(p))", "change": "should append spanner.next(p) - 1"},
        ],
    },
    {
        "replace": "            span += s",
        "with":    "            span += 1",
        "fix": "a popped day carries the whole span it already absorbed; add s, not 1",
        "why": "For 75 in the example the popped (70, 2) hides the 60 before it, so the span comes out 3 instead of 4.",
        "decoys": [
            {"line": "            p, s = self.stack.pop()", "change": "should be self.stack.pop(0)"},
            {"line": "        return span", "change": "should return span - 1"},
            {"line": "    spanner, spans = StockSpanner(), []", "change": "spans should start as [1]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
