"""
String to Integer (atoi) (LeetCode 8)  — Medium
Pattern: Single-pass state machine with early clamp

Problem
-------
Convert a string to a 32-bit signed integer the way C's atoi does: skip leading spaces, read an
optional '+'/'-', read digits until a non-digit, ignore the rest, and clamp the result to
[-2^31, 2^31 - 1]. Leading zeros are allowed.
Example: "   -042" -> -42; "4193 with words" -> 4193; "words and 987" -> 0;
"-91283472332" -> -2147483648.

Brute force
-----------
Strip leading spaces, slice off the sign, slice out the maximal run of digits, call int() on
that substring (or 0 if empty), apply the sign and clamp. O(n) time, O(n) extra space for the
slices. The wasted work is materialising substrings and converting a potentially huge digit run
into a big integer only to throw almost all of it away when clamping; in a fixed-width language
that conversion would overflow before the clamp even runs.

From brute force to optimal
---------------------------
All the information needed is one character at a time, so use a single index and a small state
machine: SPACE -> SIGN -> DIGITS -> STOP. Accumulate num = num * 10 + digit as digits arrive and
check the bound after every step; as soon as sign * num leaves the 32-bit range, return the
clamp immediately. This is O(1) extra space, never builds a substring, and never holds a
number larger than 10 * INT_MAX, which is how a real atoi in C avoids undefined overflow.

Intuition
---------
Parsing is a left-to-right scan whose behaviour depends only on the current phase. Spaces are
allowed only before the sign, the sign only before the first digit, and anything after the
digits is noise. Clamping during accumulation is safe because once the magnitude exceeds the
limit no later digit can bring it back.

Geometric view
--------------
"   -042abc"
 ^^^          skip spaces        state SPACE
    ^         read '-' sign=-1   state SIGN
     ^^^      0 -> 0 -> 4 -> 42  state DIGITS, bound check after each digit
        ^     'a' stops the scan state STOP -> return -42
Pointer moves strictly right; each phase can only hand off to the next.

Steps
-----
1. i = 0; skip while s[i] == ' '.
2. If s[i] in '+-': set sign, i += 1.
3. While '0' <= s[i] <= '9': num = num*10 + digit; if sign*num >= INT_MAX return INT_MAX;
   if sign*num <= INT_MIN return INT_MIN; i += 1.
4. Return sign * num.

Complexity: O(n) time, O(1) space — one pass, one accumulator.
Pitfalls: str.isdigit() accepts unicode digits; allowing spaces AFTER the sign ("+ 1" is 0);
          clamping only at the end (fine in Python, overflow elsewhere).
"""


class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX, INT_MIN = 2**31 - 1, -2**31
        i, n = 0, len(s)
        while i < n and s[i] == " ":
            i += 1
        sign = 1
        if i < n and s[i] in "+-":
            sign = -1 if s[i] == "-" else 1
            i += 1
        num = 0
        while i < n and "0" <= s[i] <= "9":
            num = num * 10 + (ord(s[i]) - 48)
            if sign * num >= INT_MAX:          # clamp as soon as the bound is crossed
                return INT_MAX
            if sign * num <= INT_MIN:
                return INT_MIN
            i += 1
        return sign * num


def brute_force(s: str) -> int:
    """Slice out sign and digit run, convert with int(), then clamp; O(n) extra space."""
    s = s.lstrip(" ")
    sign = 1
    if s[:1] in ("+", "-"):
        sign = -1 if s[0] == "-" else 1
        s = s[1:]
    digits = ""
    for ch in s:
        if not "0" <= ch <= "9":
            break
        digits += ch
    value = sign * int(digits) if digits else 0
    return max(-2**31, min(2**31 - 1, value))


if __name__ == "__main__":
    sol = Solution()
    assert sol.myAtoi("42") == 42
    assert sol.myAtoi("   -042") == -42
    assert sol.myAtoi("1337c0d3") == 1337
    assert sol.myAtoi("0-1") == 0
    assert sol.myAtoi("words and 987") == 0
    assert sol.myAtoi("-91283472332") == -2147483648
    assert sol.myAtoi("91283472332") == 2147483647
    assert sol.myAtoi("") == 0                     # edge: empty
    assert sol.myAtoi("+-12") == 0                 # edge: double sign
    assert sol.myAtoi("  +  413") == 0             # edge: space after sign
    cases = ["42", "   -042", "1337c0d3", "0-1", "words and 987", "-91283472332",
             "91283472332", "", "+-12", "  +  413", "2147483647", "-2147483648", "00000-42a1234"]
    for c in cases:
        assert sol.myAtoi(c) == brute_force(c), c
    print("ok")
