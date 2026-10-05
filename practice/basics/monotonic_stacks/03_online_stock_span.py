"""
Online Stock Span (LeetCode 901) - Basics
Area: monotonic stacks
Key operations: pop while top price <= today, add the popped span to today's, push (price, span)

A StockSpanner receives one price per day; next(price) returns the span: how many consecutive days
ending today (today included) had a price <= today's. A popped day hands its whole span to today,
so the stack only keeps days with strictly decreasing prices bottom to top.
Example: prices [100, 80, 60, 70, 60, 75, 85] -> spans [1, 1, 1, 2, 1, 4, 6]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
            log(f"    pop ({p}, span {s}) <= {price}: span so far {span}")
        self.stack.append((price, span))
        log(f"    push ({price}, {span}); stack top->bottom {self.stack[::-1]}")
        return span


def solve(prices: List[int]) -> List[int]:
    """Feed the prices one by one; each price is pushed once and popped at most once, amortized O(1) per day."""
    spanner, spans = StockSpanner(), []
    for day, p in enumerate(prices):
        log(f"day {day} price {p}")
        spans.append(spanner.next(p))
    return spans


# --- demo ---
def demo():
    return solve([100, 80, 60, 70, 60, 75, 85])


# --- tests ---
def tests():
    assert solve([100, 80, 60, 70, 60, 75, 85]) == [1, 1, 1, 2, 1, 4, 6]
    assert solve([31, 41, 48, 59, 79]) == [1, 2, 3, 4, 5]
    assert solve([5, 4, 3, 2, 1]) == [1, 1, 1, 1, 1]
    assert solve([60, 60, 60]) == [1, 2, 3]        # equal prices count
    assert solve([]) == []
    assert solve([9]) == [1]
    import random
    rng = random.Random(0)
    for _ in range(200):
        a = [rng.randint(1, 9) for _ in range(rng.randint(0, 10))]
        assert solve(a) == brute_force(a), a


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
