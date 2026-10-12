"""
Reverse Integer and Palindrome Number (LeetCode 7) - Basics
Area: math
Key operations: digit = n % 10 and n //= 10 (divmod), rev = rev * 10 + digit, sign and 32-bit range check, reverse only half

LeetCode 7: reverse the digits of a signed 32-bit integer; return 0 if the result leaves
[-2^31, 2^31 - 1]. LeetCode 9: decide whether an integer reads the same backwards without turning it
into a string: reverse just the lower half of the digits and compare it with the upper half.
Example: reverse(-123) -> -321; reverse(1534236469) -> 0 (overflow); is_palindrome(12321) -> True
"""
from typing import Tuple


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
    while n:
        n, d = divmod(n, 10)
        rev = rev * 10 + d
    rev *= sign
    return rev if INT_MIN <= rev <= INT_MAX else 0


def is_palindrome(x: int) -> bool:
    """Reverse the lower digits while they are fewer than the upper ones, then compare the halves. O(digits)."""
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    half = 0
    while x > half:
        x, d = divmod(x, 10)
        half = 10 * half + d
    return x == half or x == half // 10


# --- demo ---
def demo():
    return reverse(-123), is_palindrome(12321)


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
    print("result:", demo())
