"""
Online Stock Span (basics: monotonic_stacks)
next(price) returns how many consecutive days, ending today, had a price <= today's.
  prices 100, 80, 60, 70, 60, 75, 85  ->  spans 1, 1, 1, 2, 1, 4, 6

Idea: a day with price <= today's is inside today's span, and so is every day it covered.
      So pop it and add its span to today's. The stack keeps (price, span) pairs with
      prices strictly decreasing bottom to top.

Pseudocode:
  next(price):
      span = 1                                  # today itself
      while stack is not empty and top price <= price:
          span += span of the popped day        # absorb the days it covered
      push (price, span)
      return span

Time amortized O(1) per call (each day is pushed once, popped at most once), space O(n).
"""


class StockSpanner:
    def __init__(self):
        self.stack = []                  # (price, span), prices decreasing

    def next(self, price):
        span = 1                         # today counts
        while self.stack and self.stack[-1][0] <= price:
            old_price, old_span = self.stack.pop()
            span += old_span             # absorb the days it covered
        self.stack.append((price, span))
        return span


if __name__ == "__main__":
    spanner = StockSpanner()
    print([spanner.next(p) for p in [100, 80, 60, 70, 60, 75, 85]])  # [1, 1, 1, 2, 1, 4, 6]
    spanner = StockSpanner()
    print([spanner.next(p) for p in [60, 60, 60]])                   # [1, 2, 3]
