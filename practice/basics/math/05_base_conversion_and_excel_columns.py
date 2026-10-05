"""
Base Conversion and Excel Column Titles (LeetCode 168) - Basics
Area: math
Key operations: divmod(n, b) peels the lowest digit, Horner n = n * b + digit, subtract 1 before divmod for 1-based digits

to_base(n, b) writes n in base b (2..36) by repeated divmod, collecting digits lowest first;
from_base reads it back with Horner's rule. Excel columns (LeetCode 168 and 171) are base 26 with
digits A..Z standing for 1..26 and no zero: subtract 1 before each divmod so that 26 -> Z and 27 -> AA.
Example: to_base(2026, 2) -> '11111101010'; from_base('ff', 16) -> 255; column_title(701) -> 'ZY'; column_number('AB') -> 28
"""
import sys
import random
from itertools import product
from string import ascii_uppercase

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(n: int) -> str:
    """Count: list the titles in order (A..Z, AA..ZZ, AAA..) until there are n, take the n-th. O(n) strings built."""
    titles, length = [], 1
    while len(titles) < n:
        titles += ["".join(t) for t in product(ascii_uppercase, repeat=length)]
        length += 1
    return titles[n - 1]


def brute_to_base(n: int, b: int) -> str:
    """Count from 0 to n in base b, one increment with carry at a time. O(n) increments instead of O(log n) divisions."""
    digits = [0]
    for _ in range(n):
        i = len(digits) - 1
        while i >= 0 and digits[i] == b - 1:
            digits[i] = 0
            i -= 1
        if i < 0:
            digits.insert(0, 1)
        else:
            digits[i] += 1
    return "".join(DIGITS[d] for d in digits)


# --- optimal ---
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n: int, b: int) -> str:
    """Repeated divmod by b gives the digits least significant first; reverse at the end. O(log_b n)."""
    if n == 0:
        return "0"
    sign, n, digits = "-" if n < 0 else "", abs(n), []
    log(f"to_base({sign}{n}, {b}):")
    while n:
        n, d = divmod(n, b)
        digits.append(DIGITS[d])
        log(f"  {n * b + d} = {n} * {b} + {d} -> digit '{DIGITS[d]}', collected lowest first: {''.join(digits)}")
    return sign + "".join(reversed(digits))


def from_base(s: str, b: int) -> int:
    """Horner: n = n * b + digit, one character at a time from the left. O(len)."""
    n = 0
    log(f"from_base('{s}', {b}):")
    for ch in s:
        n = n * b + DIGITS.index(ch)
        log(f"  '{ch}' = {DIGITS.index(ch)} -> n = {n}")
    return n


def column_title(n: int) -> str:
    """Bijective base 26: divmod(n - 1, 26) so the digits run 1..26 (A..Z) with no zero. O(log n)."""
    out = []
    log(f"column_title({n}):")
    while n:
        n, r = divmod(n - 1, 26)
        out.append(chr(ord("A") + r))
        log(f"  n - 1 = {n * 26 + r} = {n} * 26 + {r} -> '{chr(ord('A') + r)}', collected lowest first: {''.join(out)}")
    return "".join(reversed(out))


def column_number(s: str) -> int:
    """Horner in base 26 with A = 1 .. Z = 26. O(len)."""
    n = 0
    log(f"column_number('{s}'):")
    for ch in s:
        n = n * 26 + ord(ch) - ord("A") + 1
        log(f"  '{ch}' = {ord(ch) - ord('A') + 1} -> n = {n}")
    return n


# --- demo ---
def demo():
    return to_base(2026, 2), from_base("ff", 16), column_title(701), column_number("AB")


# --- tests ---
def tests():
    global VERBOSE
    VERBOSE = False  # keep the trace to the demo
    assert to_base(2026, 2) == "11111101010" and from_base("11111101010", 2) == 2026
    assert to_base(255, 16) == "ff" and from_base("ff", 16) == 255
    assert to_base(0, 7) == "0" and to_base(-10, 2) == "-1010" and to_base(35, 36) == "z" and to_base(36, 36) == "10"
    assert to_base(100, 10) == "100" and from_base("0", 5) == 0 and from_base("007", 8) == 7
    assert column_title(1) == "A" and column_title(26) == "Z" and column_title(27) == "AA"
    assert column_title(28) == "AB" and column_title(52) == "AZ" and column_title(701) == "ZY" and column_title(702) == "ZZ"
    assert column_title(703) == "AAA" and column_title(18278) == "ZZZ"
    assert column_number("A") == 1 and column_number("Z") == 26 and column_number("AA") == 27
    assert column_number("ZY") == 701 and column_number("ZZZ") == 18278
    rng = random.Random(0)
    for _ in range(200):
        n, b = rng.randint(0, 300), rng.randint(2, 36)
        s = to_base(n, b)
        assert s == brute_to_base(n, b) and from_base(s, b) == n == int(s, b), (n, b)
        c = rng.randint(1, 702)
        assert column_title(c) == brute_force(c) and column_number(column_title(c)) == c, c


# --- bugs ---
BUGS = [
    {
        "replace": "        n, r = divmod(n - 1, 26)",
        "with":    "        n, r = divmod(n, 26)",
        "fix": "subtract 1 before the divmod: the digits are 1..26, not 0..25, so 26 must leave remainder 25 (Z) and quotient 0",
        "why": "Without the -1, 26 splits as 1 * 26 + 0 and prints 'BA' instead of 'Z'; every multiple of 26 is wrong.",
        "decoys": [
            {"line": "        out.append(chr(ord(\"A\") + r))", "change": "should be chr(ord(\"A\") + r - 1)"},
            {"line": "    return \"\".join(reversed(out))", "change": "no reversal needed"},
            {"line": "        n = n * 26 + ord(ch) - ord(\"A\") + 1", "change": "should subtract 1 instead of adding"},
        ],
    },
    {
        "replace": "    return sign + \"\".join(reversed(digits))",
        "with":    "    return sign + \"\".join(digits)",
        "fix": "divmod produces the digits least significant first, so reverse them before joining",
        "why": "The digits come out backwards: to_base(2026, 2) returns '01010111111' instead of '11111101010'.",
        "decoys": [
            {"line": "        n, d = divmod(n, b)", "change": "should be divmod(n - 1, b)"},
            {"line": "        digits.append(DIGITS[d])", "change": "should append str(d)"},
            {"line": "    if n == 0:", "change": "should be if n <= 0"},
        ],
    },
    {
        "replace": "        n = n * 26 + ord(ch) - ord(\"A\") + 1",
        "with":    "        n = n * 26 + ord(ch) - ord(\"A\")",
        "fix": "A is 1, not 0: add 1 to the letter's offset",
        "why": "Every letter is one too small: column_number('A') returns 0 and column_number('AB') returns 27 instead of 28.",
        "decoys": [
            {"line": "        n = n * b + DIGITS.index(ch)", "change": "should be n + b * DIGITS.index(ch)"},
            {"line": "        n, r = divmod(n - 1, 26)", "change": "should be divmod(n, 26) - 1"},
            {"line": "    sign, n, digits = \"-\" if n < 0 else \"\", abs(n), []", "change": "should be n < 1"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    tests()
    print("ok")
