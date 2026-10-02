"""
Valid Number (LeetCode 65)  — Hard
Pattern: Single-pass state machine with flags

Problem
-------
Return True if the string is a valid number: an optional sign, then an integer ("12") or a
decimal ("3.", ".5", "3.14"), optionally followed by 'e'/'E', an optional sign and an integer.
No spaces, no "inf"/"nan". Example: "2e10" -> True, "-.9" -> True, "4." -> True;
"e3" -> False (no mantissa), "99e2.5" -> False (exponent must be an integer), "." -> False.

Brute force
-----------
Split-and-check: scan for an 'e'; the left half must be a decimal/integer and the right half a
signed integer. "Decimal" is checked by scanning for a '.', splitting again and testing each
side with .isdigit(). Each piece is sliced and re-scanned by a different helper, so the string is
walked three or four times, and the grammar is spread across several functions whose edge cases
("+" alone, "." alone, "1e") must each be remembered separately. O(n) time but O(n) extra space
for slices; the wasted work is the repeated re-scanning of the same characters.

From brute force to optimal
---------------------------
The redundancy is re-scanning: every helper looks at the same characters again to answer a
yes/no question that depends only on WHAT HAS ALREADY BEEN SEEN. Observation: the grammar has
only three pieces of memory: "have I seen a digit (in the current part)?", "have I seen a dot?",
"have I seen an exponent?". Each character's legality is decided by those flags plus the
previous character (a sign is legal only at index 0 or right after 'e'). So a single
left-to-right pass carrying three booleans is a complete state machine; the string is valid iff
no character is rejected and the final state has a digit in the last part.

Intuition
---------
Think of the number as "mantissa [e exponent]". A dot is allowed once and never after 'e'. An
'e' is allowed once and only if a digit precedes it, and it resets the digit flag because the
exponent needs its own digits. A sign is allowed only at the very start or immediately after
'e'. Anything else is a reject. At the end, seen_digit tells you the last part was non-empty.

Geometric view
--------------
Picture a cursor moving along the string with three light bulbs above it: DIGIT, DOT, EXP.
Each character either flips a bulb on (digit, dot, e), is tolerated (a sign in position), or
trips the fuse (reject). 'e' switches DIGIT off, so the bulbs must light up again on the right.

Steps
-----
1. seen_digit = seen_dot = seen_exp = False.
2. For each char c at index i: digit -> seen_digit = True.
3. '+'/'-': legal only if i == 0 or s[i-1] in "eE"; otherwise reject.
4. '.': reject if seen_dot or seen_exp; else seen_dot = True.
5. 'e'/'E': reject if seen_exp or not seen_digit; else seen_exp = True, seen_digit = False.
6. Any other char: reject. Return seen_digit at the end.

Complexity: O(n) time, O(1) space — one pass, three booleans.
Pitfalls: a sign after 'e' is legal ("3e+7"); '.' after 'e' is not ("99e2.5"); forgetting to
reset seen_digit after 'e' accepts "1e"; "." and "+" alone must be rejected (no digit seen).
"""


class Solution:
    def isNumber(self, s: str) -> bool:
        seen_digit = seen_dot = seen_exp = False
        for i, c in enumerate(s):
            if "0" <= c <= "9":
                seen_digit = True
            elif c in "+-":
                if i > 0 and s[i - 1] not in "eE":        # sign only at start or right after e
                    return False
            elif c == ".":
                if seen_dot or seen_exp:                  # one dot, and never in the exponent
                    return False
                seen_dot = True
            elif c in "eE":
                if seen_exp or not seen_digit:            # one e, and it needs a mantissa
                    return False
                seen_exp = True
                seen_digit = False                        # the exponent needs its own digits
            else:
                return False
        return seen_digit


def brute_force(s: str) -> bool:
    def digits(t: str) -> bool:
        return t != "" and all("0" <= c <= "9" for c in t)

    def is_int(t: str) -> bool:
        return digits(t[1:] if t[:1] in ("+", "-") else t)

    def is_dec(t: str) -> bool:                           # signed integer or signed a.b
        if t[:1] in ("+", "-"):
            t = t[1:]
        if "." not in t:
            return digits(t)
        a, b = t.split(".", 1)                            # re-scans both halves
        return (a == "" or digits(a)) and (b == "" or digits(b)) and (a + b) != ""

    for k, c in enumerate(s):                             # split at the exponent, if any
        if c in "eE":
            return is_dec(s[:k]) and is_int(s[k + 1:])
    return is_dec(s)


if __name__ == "__main__":
    s = Solution()
    valid = ["2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3", "3e+7", "+6e-1",
             "53.5e93", "-123.456e789", "0", "46.e3"]
    invalid = ["abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53", ".", "+", "e",
               ".e1", "1e+", "+.", "", " 1", "1 ", "4e+.5", "3.e", "+-1"]
    for v in valid:
        assert s.isNumber(v), v
    for v in invalid:
        assert not s.isNumber(v), v
    for v in valid + invalid:
        assert s.isNumber(v) == brute_force(v), v
    print("ok")
