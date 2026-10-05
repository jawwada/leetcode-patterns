"""
Base Conversion and Excel Column Titles - Fundamentals
Chapter: fundamentals/math
Key operations: n % b and n // b peel the lowest digit, Horner n = n * b + digit, n - 1 for A..Z

to_base(n, b) writes n in base b (2..36) by repeated division, collecting digits lowest first;
from_base reads it back with Horner's rule. Excel columns (LeetCode 168 and 171) are base 26 with
digits A..Z standing for 1..26 and no zero: subtract 1 before dividing so 26 -> Z and 27 -> AA.
Example: to_base(2026, 2) -> '11111101010'; from_base('ff', 16) -> 255; column_title(701) -> 'ZY'
"""


# --- algorithm ---
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, base):
    """Repeated division by base gives the digits lowest first; reverse at the end. O(log n)."""
    if n == 0:
        return "0"
    sign = ""
    if n < 0:
        sign = "-"
    n = abs(n)
    digits = []
    while n > 0:
        digit = n % base
        n = n // base
        digits.append(DIGITS[digit])
    digits.reverse()              # the lowest digit came out first
    return sign + "".join(digits)


def from_base(s, base):
    """Horner: n = n * base + digit, one character at a time from the left. O(len)."""
    n = 0
    for ch in s:
        n = n * base + DIGITS.index(ch)
    return n


def column_title(n):
    """Bijective base 26: subtract 1 before dividing so the digits run 1..26 (A..Z). O(log n)."""
    letters = []
    while n > 0:
        n = n - 1                 # 26 must give remainder 25 (Z) and quotient 0, not 'BA'
        letters.append(chr(ord("A") + n % 26))
        n = n // 26
    letters.reverse()
    return "".join(letters)


def column_number(s):
    """Horner in base 26 with A = 1 .. Z = 26. O(len)."""
    n = 0
    for ch in s:
        n = n * 26 + ord(ch) - ord("A") + 1    # A is 1, not 0
    return n


# --- try it ---
print(to_base(2026, 2))          # -> 11111101010
print(to_base(255, 16))          # -> ff
print(from_base("ff", 16))       # -> 255
print(column_title(701))         # -> ZY
print(column_title(26))          # -> Z
print(column_number("AB"))       # -> 28
