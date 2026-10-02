"""
Implement String Split (custom warm-up)  — Easy
Pattern: Linear scan with state

Problem
-------
Implement split(s, sep) with the exact semantics of Python's str.split(sep) for a NON-EMPTY
separator, without using str.split or re: pieces between consecutive separators are kept
(even when empty), leading/trailing separators yield empty strings at the ends, and matches
are non-overlapping, left to right. Example: split("a,,b,", ",") -> ["a", "", "b", ""];
split("aaa", "aa") -> ["", "a"]; split("", ",") -> [""].

Brute force
-----------
Loop: k = s.find(sep); if none, emit the remainder and stop; else emit s[:k] and set
s = s[k+len(sep):]. Each find scans from the start of the (shrinking) remainder and each
slice copies the remainder, so worst case O(n^2) copying with n/|sep| pieces; the matching
itself is O(n*m). The wasted work: the remainder is copied once per piece, and every piece
boundary is re-derived from a fresh string object.

From brute force to optimal
---------------------------
The redundancy is rebuilding the remainder after every match. Observation: the remainder is
just a suffix identified by a start index, so track `start` instead of slicing. A single
index i walks the string; at each position compare s[i:i+m] with sep: on a match emit
s[start:i], jump i past the separator (non-overlapping) and set start = i; otherwise i += 1.
After the loop emit s[start:] -- this final emit is what produces the trailing empty string
for "a," and the [""] result for an empty input. Time O(n*m) for the comparisons (O(n) for a
single-char separator), space O(n) for the output.

Intuition
---------
A split is "cut at every match, keep whatever lies between cuts, including nothing". Walk the
string once, remembering where the current piece began; each match closes a piece and opens
the next one right after the separator.

Geometric view
--------------
Two markers on the string: `start` (beginning of the piece under construction) and `i` (the
scan head). When the window s[i:i+m] equals sep, the segment [start, i) is snipped off as a
piece, and both markers jump to i+m. At the end the tail [start, n) is the last piece, even if
it has zero length.

Steps
-----
1. Reject an empty separator (Python raises ValueError; say so in the interview).
2. parts = [], start = 0, i = 0, m = len(sep).
3. While i <= len(s) - m: if s[i:i+m] == sep: append s[start:i]; i += m; start = i.
   Else i += 1.
4. Append s[start:] and return parts.

Complexity: O(n*m) time, O(n) space — each position compared against sep at most once; output
holds every input character once plus one slot per separator.

Interview talking points
------------------------
- Edge cases to state up front: empty s -> [""]; s == sep -> ["", ""]; sep at both ends ->
  empty strings at both ends; adjacent separators -> empty pieces between them.
- Empty separator: Python raises ValueError("empty separator"); some languages split into
  characters. Ask which is wanted; never loop forever.
- Multi-character separator: matches are non-overlapping and leftmost ("aaa" split on "aa"
  -> ["", "a"]). Advancing i by m, not 1, after a match is what enforces this.
- Unicode: Python strings are sequences of code points, so the algorithm is unchanged, but
  mention that grapheme clusters (e + combining accent) can be split apart if the separator
  matches a code point inside a cluster; byte-level splitting on UTF-8 would also need care.
- maxsplit and str.split() with no argument (whitespace runs, no empty pieces) are different
  semantics -- good follow-ups.
Pitfalls: Advancing i by 1 after a match (creates overlapping matches); forgetting the final
piece; using `while i < len(s)` and then slicing past the end (works in Python but hides the
boundary logic); treating "no separator found" as an empty result instead of [s].
"""
from typing import List


class Solution:
    def split(self, s: str, sep: str) -> List[str]:
        if not sep:
            raise ValueError("empty separator")
        m = len(sep)
        parts, start, i = [], 0, 0
        while i <= len(s) - m:
            if s[i:i + m] == sep:                   # separator starts at i
                parts.append(s[start:i])            # may be "" between adjacent separators
                i += m                              # non-overlapping: skip the whole separator
                start = i
            else:
                i += 1
        parts.append(s[start:])                     # trailing piece, possibly ""
        return parts


def brute_force(s: str, sep: str) -> List[str]:
    if not sep:
        raise ValueError("empty separator")
    parts = []
    while True:
        k = s.find(sep)                             # rescans from the start of the remainder
        if k == -1:
            parts.append(s)
            return parts
        parts.append(s[:k])
        s = s[k + len(sep):]                        # copies the remainder for every piece


if __name__ == "__main__":
    s = Solution()
    cases = [
        ("a,b,c", ","), ("a,,b,", ","), (",a,", ","), ("", ","), (",", ","), ("abc", ","),
        ("aaa", "aa"), ("a--b----c", "--"), ("héllo→wörld→", "→"), ("x", "xx"), ("abab", "ab"),
    ]
    assert s.split("a,b,c", ",") == ["a", "b", "c"]
    assert s.split("a,,b,", ",") == ["a", "", "b", ""]
    assert s.split("", ",") == [""]
    assert s.split("aaa", "aa") == ["", "a"]
    assert s.split("héllo→wörld→", "→") == ["héllo", "wörld", ""]
    for text, sep in cases:
        assert s.split(text, sep) == text.split(sep) == brute_force(text, sep)
    try:
        s.split("abc", "")
        assert False, "empty separator must raise"
    except ValueError:
        pass
    print("ok")
