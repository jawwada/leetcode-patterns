"""
Primes: Trial Division and the Sieve of Eratosthenes - Basics
Area: math
Key operations: trial divide while d * d <= n, cross off multiples of p starting at p * p, collect the survivors

is_prime(n): n >= 2 and no d in 2..sqrt(n) divides it (a divisor above sqrt(n) pairs with one below).
sieve(n): mark every number 2..n as prime, then for each surviving p up to sqrt(n) cross off
p*p, p*p + p, p*p + 2p, ... (smaller multiples were crossed off by a smaller prime); the survivors are the primes.
Example: is_prime(91) -> False (91 = 7 * 13); sieve(30) -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
"""
from math import isqrt
from typing import List


# --- helpers ---
def row(is_p: List[bool]) -> str:
    """Draw the sieve: a surviving number prints itself, a crossed-off one prints dots of the same width."""
    return " ".join(str(i) if is_p[i] else "." * len(str(i)) for i in range(2, len(is_p)))


# --- brute force ---
def brute_force(n: int) -> List[int]:
    """Trial-divide every k in 2..n by every d in 2..k-1. O(n^2): tests divisors above sqrt(k) and retests composites."""
    return [k for k in range(2, n + 1) if all(k % d for d in range(2, k))]


# --- optimal ---
def is_prime(n: int) -> bool:
    """Trial division by d = 2, 3, 4, ... while d * d <= n. O(sqrt n)."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def sieve(n: int) -> List[int]:
    """Eratosthenes: for each surviving p up to sqrt(n) cross off p*p, p*p+p, ... O(n log log n)."""
    is_p = [False, False] + [True] * (n - 1)
    for p in range(2, isqrt(n) + 1):
        if is_p[p]:
            for m in range(p * p, n + 1, p):
                is_p[m] = False
    return [i for i in range(n + 1) if is_p[i]]


# --- demo ---
def demo():
    return is_prime(91), sieve(30)


# --- bugs ---
BUGS = [
    {
        "replace": "    while d * d <= n:",
        "with":    "    while d * d < n:",
        "fix": "try d while d * d <= n: a perfect square's only small factor is exactly sqrt(n)",
        "why": "With a strict <, d = 2 is never tried against n = 4 (4 < 4 is false), so 4, 9, 25, 49 ... are reported prime.",
        "decoys": [
            {"line": "        d += 1", "change": "should be d += 2"},
            {"line": "        if n % d == 0:", "change": "should be n // d == 0"},
            {"line": "    for p in range(2, isqrt(n) + 1):", "change": "should run p up to n + 1"},
        ],
    },
    {
        "replace": "            for m in range(p * p, n + 1, p):",
        "with":    "            for m in range(p * p, n, p):",
        "fix": "the range must include n itself: range(p * p, n + 1, p)",
        "why": "range stops before its end, so n is never crossed off when it is composite: sieve(4) returns [2, 3, 4].",
        "decoys": [
            {"line": "    is_p = [False, False] + [True] * (n - 1)", "change": "should be [True] * (n + 1)"},
            {"line": "    return [i for i in range(n + 1) if is_p[i]]", "change": "should be range(2, n)"},
            {"line": "        if is_p[p]:", "change": "should be if not is_p[p]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
