"""
Online Stock Span (LeetCode 901) - Fundamentals
Chapter: fundamentals/monotonic_stacks
Key operations: pop while top price <= today, add the popped span to today's, push (price, span)

A StockSpanner receives one price per day; next(price) returns the span: how many consecutive days
ending today (today included) had a price <= today's. A popped day hands its whole span to today,
so the stack only keeps days with strictly decreasing prices bottom to top.
Example: prices [100, 80, 60, 70, 60, 75, 85] -> spans [1, 1, 1, 2, 1, 4, 6]
"""


# --- algorithm ---
class StockSpanner:
    def __init__(self):
        self.stack = []                     # (price, span); prices decreasing bottom -> top

    def next(self, price):
        """Pop every day with price <= today's and absorb its span; amortized O(1) per day."""
        span = 1                            # today counts
        while len(self.stack) > 0 and self.stack[-1][0] <= price:
            top_price, top_span = self.stack.pop()
            span += top_span                # the popped day already covered its own run of days
        self.stack.append((price, span))
        return span


# --- try it ---
spanner = StockSpanner()
print(spanner.next(100))    # -> 1
print(spanner.next(80))     # -> 1
print(spanner.next(60))     # -> 1
print(spanner.next(70))     # -> 2
print(spanner.next(60))     # -> 1
print(spanner.next(75))     # -> 4
print(spanner.next(85))     # -> 6
spanner = StockSpanner()
print(spanner.next(5))      # -> 1
print(spanner.next(5))      # -> 2
print(spanner.next(9))      # -> 3
