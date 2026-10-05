"""
GCD and LCM with Euclid's Algorithm - Fundamentals
Chapter: fundamentals/math
Key operations: (a, b) -> (b, a % b) until b == 0, lcm = |a| // gcd * |b|

gcd(a, b) is the largest integer dividing both, lcm(a, b) the smallest positive one both divide.
Euclid replaces (a, b) by (b, a % b) until b is 0: every common divisor of (a, b) also divides
(b, a % b), so the gcd survives while the pair shrinks fast.
Example: (252, 105) -> (105, 42) -> (42, 21) -> (21, 0): gcd 21, lcm 252 // 21 * 105 = 1260
"""


# --- algorithm ---
def gcd(a, b):
    """Euclid: (a, b) -> (b, a % b) until b == 0; the common divisors never change. O(log min)."""
    a = abs(a)
    b = abs(b)
    while b != 0:                 # stop only when the remainder is exactly 0, not at 1
        remainder = a % b
        a = b
        b = remainder
    return a


def lcm(a, b):
    """lcm * gcd = |a * b|; divide by the gcd first so the product stays small. O(log min)."""
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)


# --- try it ---
print(gcd(252, 105))     # -> 21
print(lcm(252, 105))     # -> 1260
print(gcd(7, 13))        # -> 1
print(lcm(4, 6))         # -> 12
print(gcd(0, 5))         # -> 5
