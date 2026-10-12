"""
GCD and LCM with Euclid's Algorithm - Basics
Area: math
Key operations: (a, b) -> (b, a % b) until b == 0, lcm = |a| // gcd * |b|

gcd(a, b) is the largest integer dividing both, lcm(a, b) the smallest positive integer both divide.
Euclid: replace (a, b) by (b, a % b) until b is 0; the surviving a is the gcd, because every common
divisor of (a, b) is also a common divisor of (b, a % b) and the pair shrinks fast.
Example: (252, 105) -> (105, 42) -> (42, 21) -> (21, 0): gcd 21, lcm 252 // 21 * 105 = 1260
"""
from typing import Tuple


# --- brute force ---
def brute_force(a: int, b: int) -> Tuple[int, int]:
    """Try every divisor from 1 to min(|a|, |b|), then every multiple of max(|a|, |b|). O(min(a, b) + a*b/max(a, b))."""
    a, b = abs(a), abs(b)
    if a == 0 or b == 0:
        return max(a, b), 0
    g = max(d for d in range(1, min(a, b) + 1) if a % d == 0 and b % d == 0)
    m = next(m for m in range(max(a, b), a * b + 1, max(a, b)) if m % a == 0 and m % b == 0)
    return g, m


# --- optimal ---
def gcd(a: int, b: int) -> int:
    """Euclid: (a, b) -> (b, a % b) until b == 0; the set of common divisors never changes. O(log min(a, b))."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def solve(a: int, b: int) -> Tuple[int, int]:
    """Return (gcd, lcm); divide by the gcd before multiplying so the product stays small. O(log min(a, b))."""
    g = gcd(a, b)
    m = 0 if a == 0 or b == 0 else abs(a) // g * abs(b)
    return g, m


# --- demo ---
def demo():
    return solve(252, 105)


# --- bugs ---
BUGS = [
    {
        "replace": "    while b:",
        "with":    "    while b > 1:",
        "fix": "loop until b is exactly 0; the gcd is the a that remains when the remainder hits 0",
        "why": "Stopping one step early returns the second-to-last remainder: gcd(7, 13) walks (13, 7) (7, 6) (6, 1) and answers 6 instead of 1.",
        "decoys": [
            {"line": "        a, b = b, a % b", "change": "should be a, b = a % b, b"},
            {"line": "    a, b = abs(a), abs(b)", "change": "should not drop the signs"},
            {"line": "    g = gcd(a, b)", "change": "should be gcd(b, a)"},
        ],
    },
    {
        "replace": "    m = 0 if a == 0 or b == 0 else abs(a) // g * abs(b)",
        "with":    "    m = 0 if a == 0 or b == 0 else abs(a) // g * abs(b) // g",
        "fix": "divide by the gcd exactly once: lcm * gcd = |a * b|",
        "why": "Dividing by the gcd twice shrinks the answer whenever gcd > 1: lcm(252, 105) comes out 60 instead of 1260.",
        "decoys": [
            {"line": "    return a", "change": "should return b"},
            {"line": "        a, b = b, a % b", "change": "should be b, a // b"},
            {"line": "    return g, m", "change": "should return m, g"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
