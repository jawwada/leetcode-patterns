"""
Rabin-Karp Rolling Hash - Basics
Area: strings
Key operations: polynomial hash of a window, roll it in O(1) by dropping the left char and adding the right one, verify on a hash hit

Hash the pattern and the first window of the text with a base-BASE polynomial modulo MOD. Sliding
the window one step costs O(1): subtract the leftmost character times BASE^(m-1), multiply by BASE,
add the new character. Equal hashes may be collisions, so a hit is confirmed by a direct compare.
Return every start index. The small modulus here makes collisions visible in the trace.
Example: text "abracadabra", pattern "abra" -> [0, 7]
"""
from typing import List


# --- helpers ---
BASE, MOD = 256, 101  # tiny modulus on purpose: collisions show up in the trace


# --- brute force ---
def brute_force(text: str, pattern: str) -> List[int]:
    """Compare the pattern at every start index. O(n * m); every window is compared character by character."""
    m = len(pattern)
    return [i for i in range(len(text) - m + 1) if text[i:i + m] == pattern]


# --- optimal ---
def solve(text: str, pattern: str) -> List[int]:
    """Roll one hash across the text; compare characters only when the hashes agree. O(n + m) expected."""
    n, m = len(text), len(pattern)
    high = pow(BASE, m - 1, MOD)  # weight of the window's leftmost character
    target, h = 0, 0
    for k in range(m):
        target = (target * BASE + ord(pattern[k])) % MOD
    for k in range(min(m, n)):
        h = (h * BASE + ord(text[k])) % MOD
    hits = []
    for i in range(n - m + 1):
        if h == target and text[i:i + m] == pattern:
            hits.append(i)
        if i + m < n:
            h = ((h - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
    return hits


# --- demo ---
def demo():
    return solve("abracadabra", "abra")


# --- bugs ---
BUGS = [
    {
        "replace": "        if h == target and text[i:i + m] == pattern:",
        "with":    "        if h == target:",
        "fix": "a hash hit is a candidate, not a proof: confirm with a direct character compare",
        "why": "Different windows can share a hash; 'abcc' hashes like 'abra' and is reported as a hit at index 0 of 'abccabra'.",
        "decoys": [
            {"line": "    high = pow(BASE, m - 1, MOD)  # weight of the window's leftmost character", "change": "should be pow(BASE, m, MOD)"},
            {"line": "        if i + m < n:", "change": "should be i + m <= n"},
            {"line": "            hits.append(i)", "change": "should append i + m"},
        ],
    },
    {
        "replace": "            h = ((h - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD",
        "with":    "            h = ((h - ord(text[i])) * BASE + ord(text[i + m])) % MOD",
        "fix": "the leftmost character carries weight BASE^(m-1): subtract ord(text[i]) * high",
        "why": "Removing the dropped character with weight 1 leaves garbage in the hash, so later windows never match: 'abracadabra' finds [0] only.",
        "decoys": [
            {"line": "    for i in range(n - m + 1):", "change": "should be range(n - m)"},
            {"line": "        target = (target * BASE + ord(pattern[k])) % MOD", "change": "should add k instead of ord(pattern[k])"},
            {"line": "    return hits", "change": "should return hits[::-1]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
