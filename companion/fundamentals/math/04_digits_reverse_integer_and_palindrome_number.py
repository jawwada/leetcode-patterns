"""
Reverse Integer and Palindrome Number - Fundamentals
Chapter: fundamentals/math
Key operations: digit = n % 10 and n //= 10, rev = rev * 10 + digit, 32-bit check, reverse half

LeetCode 7: reverse the digits of a signed 32-bit integer; return 0 if the result leaves
[-2^31, 2^31 - 1]. LeetCode 9: decide whether an integer reads the same backwards without making it
into a string: reverse just the lower half of the digits and compare it with the upper half.
Example: reverse(-123) -> -321; reverse(1534236469) -> 0 (overflow); is_palindrome(12321) -> True
"""


# --- algorithm ---
INT_MIN = -2 ** 31
INT_MAX = 2 ** 31 - 1


def reverse_integer(x):
    """Peel digits off |x| with % 10 and // 10, rebuild, restore the sign, reject overflow."""
    sign = 1
    if x < 0:
        sign = -1
    n = abs(x)
    rev = 0
    while n > 0:
        digit = n % 10            # lowest digit comes off first ...
        n = n // 10
        rev = rev * 10 + digit    # ... and becomes the highest digit of the answer
    rev = rev * sign
    if rev < INT_MIN or rev > INT_MAX:
        return 0
    return rev


def is_palindrome_number(x):
    """Reverse only the lower half of the digits, then compare it with the upper half."""
    if x < 0:
        return False
    if x % 10 == 0 and x != 0:    # a trailing zero has no leading zero to match; 0 itself is fine
        return False
    half = 0
    while x > half:               # stop once the reversed part is at least as long as the rest
        digit = x % 10
        x = x // 10
        half = half * 10 + digit
    return x == half or x == half // 10    # odd length: the middle digit is the last one in half


# --- try it ---
print(reverse_integer(-123))            # -> -321
print(reverse_integer(1534236469))      # -> 0
print(reverse_integer(120))             # -> 21
print(is_palindrome_number(12321))      # -> True
print(is_palindrome_number(1221))       # -> True
print(is_palindrome_number(10))         # -> False
