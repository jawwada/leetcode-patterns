"""
String to Integer (atoi) (LeetCode 8) - Medium
Chapter: strings
Pattern: Single-pass state machine with early clamp

Convert a string to a 32-bit signed integer like C's atoi: skip leading spaces, read an optional
'+' or '-', read digits until a non-digit, ignore the rest, and clamp to [-2^31, 2^31 - 1].
Example: "   -042" -> -42; "4193 with words" -> 4193; "words and 987" -> 0;
"-91283472332" -> -2147483648.
"""


# --- brute force ---
def brute_force(s):
    """Strip spaces, slice off the sign, slice out the digits, int() them, clamp. O(n), O(n)."""
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    s = s.lstrip(" ")
    sign = 1
    if len(s) > 0 and s[0] == "-":
        sign = -1
        s = s[1:]
    elif len(s) > 0 and s[0] == "+":
        s = s[1:]
    digits = ""
    for ch in s:
        if ch < "0" or ch > "9":
            break                         # the first non-digit ends the number
        digits += ch
    if digits == "":
        return 0
    value = sign * int(digits)            # may be a huge number, clamped only afterwards
    return max(INT_MIN, min(INT_MAX, value))


# --- optimal ---
def my_atoi(s):
    """One index walks spaces, then sign, then digits; clamp the moment it overflows. O(n), O(1)."""
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    n = len(s)
    i = 0
    while i < n and s[i] == " ":
        i += 1                            # skip leading spaces
    sign = 1
    if i < n and (s[i] == "+" or s[i] == "-"):
        if s[i] == "-":
            sign = -1
        i += 1                            # the sign is allowed only right before the digits
    num = 0
    while i < n and s[i] >= "0" and s[i] <= "9":
        digit = ord(s[i]) - ord("0")
        num = num * 10 + digit
        if sign * num >= INT_MAX:         # clamp as soon as the bound is crossed
            return INT_MAX
        if sign * num <= INT_MIN:
            return INT_MIN
        i += 1
    return sign * num


# --- try the brute force ---
print(brute_force("   -042"))             # -> -42
print(brute_force("4193 with words"))     # -> 4193
print(brute_force("words and 987"))       # -> 0
print(brute_force("-91283472332"))        # -> -2147483648


# --- try the optimal ---
print(my_atoi("   -042"))                 # -> -42
print(my_atoi("4193 with words"))         # -> 4193
print(my_atoi("words and 987"))           # -> 0
print(my_atoi("-91283472332"))            # -> -2147483648
