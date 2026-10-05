"""
Reverse Integer and Palindrome Number (LeetCode 7) - Basics
Area: math
Key operations: digit = n % 10 and n //= 10 (divmod), rev = rev * 10 + digit, sign and 32-bit range check, reverse only half

LeetCode 7: reverse the digits of a signed 32-bit integer; return 0 if the result leaves
[-2^31, 2^31 - 1]. LeetCode 9: decide whether an integer reads the same backwards without turning it
into a string: reverse just the lower half of the digits and compare it with the upper half.
Example: reverse(-123) -> -321; reverse(1534236469) -> 0 (overflow); is_palindrome(12321) -> True
"""
import sys
import random
from typing import Tuple

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(x: int) -> Tuple[int, bool]:
    """Reverse the decimal string of |x|; compare str(x) with its reverse. O(digits), but it builds strings."""
    rev = int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)
    return (rev if INT_MIN <= rev <= INT_MAX else 0), (x >= 0 and str(x) == str(x)[::-1])


# --- optimal ---
INT_MIN, INT_MAX = -2**31, 2**31 - 1


def reverse(x: int) -> int:
    """Peel digits off |x| with divmod(n, 10), rebuild, restore the sign, reject 32-bit overflow. O(digits)."""
    sign = -1 if x < 0 else 1
    n, rev = abs(x), 0
    log(f"reverse({x}):")
    while n:
        n, d = divmod(n, 10)
        rev = rev * 10 + d
        log(f"  digit {d}: rev = {rev}, left = {n}")
    rev *= sign
    log(f"  sign {sign:+d} -> {rev}; in [{INT_MIN}, {INT_MAX}]? {INT_MIN <= rev <= INT_MAX}")
    return rev if INT_MIN <= rev <= INT_MAX else 0


def is_palindrome(x: int) -> bool:
    """Reverse the lower digits while they are fewer than the upper ones, then compare the halves. O(digits)."""
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    half = 0
    log(f"is_palindrome({x}):")
    while x > half:
        x, d = divmod(x, 10)
        half = 10 * half + d
        log(f"  upper = {x}, reversed lower = {half}")
    return x == half or x == half // 10


# --- demo ---
def demo():
    return reverse(-123), is_palindrome(12321)


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # keep the trace to the demo
    assert reverse(-123) == -321 and reverse(123) == 321 and reverse(120) == 21
    assert reverse(0) == 0 and reverse(7) == 7 and reverse(-7) == -7
    assert reverse(1534236469) == 0                   # 9646324351 > 2^31 - 1
    assert reverse(-2147483648) == 0 and reverse(2147483647) == 0
    assert reverse(1463847412) == 2147483641          # just fits
    assert is_palindrome(12321) and is_palindrome(1221) and is_palindrome(0) and is_palindrome(7)
    assert not is_palindrome(-121) and not is_palindrome(10) and not is_palindrome(123)
    assert is_palindrome(1000021) is False and is_palindrome(100001) is True
    rng = random.Random(0)
    for _ in range(200):
        s = str(rng.randint(0, 999))
        x = rng.choice([rng.randint(-10**4, 10**4), rng.randint(-2**31, 2**31 - 1), int(s + s[::-1]), int(s + s[-2::-1])])
        r, p = brute_force(x)
        assert reverse(x) == r and is_palindrome(x) == p, x


# --- bugs ---
BUGS = [
    {
        "replace": "    while x > half:",
        "with":    "    while x >= half:",
        "fix": "stop as soon as the reversed lower half is at least as long as what is left: while x > half",
        "why": "With >=, an even-length palindrome takes one digit too many: 1221 becomes upper 1, lower 122, and 1 matches neither 122 nor 12.",
        "decoys": [
            {"line": "    return x == half or x == half // 10", "change": "should be x == half only"},
            {"line": "        half = 10 * half + d", "change": "should be half + d * 10"},
            {"line": "    sign = -1 if x < 0 else 1", "change": "should be x <= 0"},
        ],
    },
    {
        "replace": "    if x < 0 or (x % 10 == 0 and x != 0):",
        "with":    "    if x < 0 or x % 10 == 0:",
        "fix": "a trailing zero rules out a palindrome only for x != 0; zero itself is a palindrome",
        "why": "0 % 10 == 0, so is_palindrome(0) returns False instead of True.",
        "decoys": [
            {"line": "        rev = rev * 10 + d", "change": "should be rev + d * 10"},
            {"line": "    return rev if INT_MIN <= rev <= INT_MAX else 0", "change": "should use strict < on both sides"},
            {"line": "    n, rev = abs(x), 0", "change": "should start from x, not abs(x)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
