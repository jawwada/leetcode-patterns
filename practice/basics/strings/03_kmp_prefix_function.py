"""
KMP Prefix Function - Basics
Area: strings
Key operations: build the failure table, fall back with fail[k - 1] on a mismatch, extend on a match, record a hit and keep going

fail[i] is the length of the longest proper prefix of pattern[:i + 1] that is also its suffix. When
text[i] does not match pattern[j], the first j characters already match, so instead of restarting at
i - j + 1 the pattern slides to its longest border: j = fail[j - 1]. Return every start index.
Example: text "aabaaabaab", pattern "aab" -> [0, 4, 7]   (failure table of "aab": [0, 1, 0])
"""
from typing import List


# --- brute force ---
def brute_force(text: str, pattern: str) -> List[int]:
    """Compare the pattern at every start index. O(n * m); after a mismatch it forgets everything that matched."""
    m = len(pattern)
    return [i for i in range(len(text) - m + 1) if text[i:i + m] == pattern]


# --- optimal ---
def build_failure(pattern: str) -> List[int]:
    """fail[i] = longest border of pattern[:i + 1]; k tracks the border being extended. O(m)."""
    fail = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = fail[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    return fail


def solve(text: str, pattern: str) -> List[int]:
    """One pass over text; j = matched prefix length, never moves i backwards. O(n + m)."""
    fail = build_failure(pattern)
    hits, j = [], 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = fail[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            hits.append(i - j + 1)
            j = fail[-1]
    return hits


# --- demo ---
def demo():
    return solve("aabaaabaab", "aab")


# --- bugs ---
BUGS = [
    {
        "replace": "            j = fail[-1]",
        "with":    "            j = 0",
        "fix": "after a hit keep the longest border of the whole pattern (fail[-1]) so overlapping hits are found",
        "why": "Resetting to 0 restarts after each hit and misses overlaps: 'aaaa' with 'aa' returns [0, 2] instead of [0, 1, 2].",
        "decoys": [
            {"line": "            hits.append(i - j + 1)", "change": "should append i"},
            {"line": "        if ch == pattern[j]:", "change": "should be if j < len(pattern) and ch == pattern[j]"},
            {"line": "    fail = [0] * len(pattern)", "change": "should be [-1] * len(pattern)"},
        ],
    },
    {
        "replace": "        while j > 0 and ch != pattern[j]:",
        "with":    "        if j > 0 and ch != pattern[j]:",
        "fix": "fall back repeatedly (while, not if) until the character matches or j reaches 0",
        "why": "One fall-back may land on another mismatch; j then stays too large, and 'aaxaab' reports a false hit of 'aaab' at index 2.",
        "decoys": [
            {"line": "            j = fail[j - 1]", "change": "should be j = fail[j]"},
            {"line": "            j += 1", "change": "should be j = i + 1"},
            {"line": "    for i in range(1, len(pattern)):", "change": "should start at 0"},
        ],
    },
    {
        "replace": "    for i in range(1, len(pattern)):",
        "with":    "    for i in range(len(pattern)):",
        "fix": "start at i = 1: a border must be a PROPER prefix, so fail[0] is always 0",
        "why": "At i = 0 the character matches itself, fail[0] becomes 1 and every later entry is one too big: 'aab' gets [1, 2, 3] instead of [0, 1, 0].",
        "decoys": [
            {"line": "            k = fail[k - 1]", "change": "should be k = fail[k]"},
            {"line": "        fail[i] = k", "change": "should be fail[i] = k - 1"},
            {"line": "    return fail", "change": "should return fail[1:]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
