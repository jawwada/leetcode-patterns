"""
Palindrome Partitioning (LeetCode 131) - Medium
Area: backtracking
Key operations: choose a palindromic prefix, recurse on the rest, record at the end, undo the choice

Given a string s, return every way to split s into pieces such that each piece is a palindrome.
Any order of partitions is accepted; here they are returned sorted for determinism.
Example: "aab" -> [["a", "a", "b"], ["aa", "b"]]
"""
from typing import List


# --- brute force ---
def brute_force(s: str) -> List[List[str]]:
    """Enumerate all 2^(n-1) ways to place cuts between characters (one bit per gap), build the
    pieces, keep the partitions whose pieces are all palindromes. O(2^n * n): a mask whose first
    piece is not a palindrome is still fully built and checked, and so are its 2^k relatives."""
    n, out = len(s), []
    for mask in range(1 << max(n - 1, 0)):
        pieces, start = [], 0
        for i in range(1, n + 1):
            if i == n or mask >> (i - 1) & 1:
                pieces.append(s[start:i])
                start = i
        if all(p == p[::-1] for p in pieces):
            out.append(pieces)
    return sorted(out)


# --- optimal ---
def is_palindrome(piece: str) -> bool:
    """Two pointers walking inwards from both ends. O(len)."""
    i, j = 0, len(piece) - 1
    while i < j:
        if piece[i] != piece[j]:
            return False
        i, j = i + 1, j - 1
    return True


def solve(s: str) -> List[List[str]]:
    """Backtracking: at position start try every prefix s[start:end]; only a palindromic prefix is
    chosen, then recurse on the rest and undo. A dead prefix prunes all partitions beginning with
    it. O(n * 2^n) worst case (all characters equal), O(n) recursion depth."""
    result, path = [], []

    def backtrack(start):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if is_palindrome(piece):
                path.append(piece)
                backtrack(end)
                path.pop()

    backtrack(0)
    return sorted(result)


# --- demo ---
def demo():
    return solve("aab")


# --- bugs ---
BUGS = [
    {
        "replace": "            result.append(path[:])",
        "with":    "            result.append(path)",
        "fix": "record a copy, path[:]; path is mutated by later pops",
        "why": "Every recorded partition is the same list object, which the backtracking empties again on the way out, so the result is a list of empty lists.",
        "decoys": [
            {"line": "                path.pop()", "change": "should be path.pop(0)"},
            {"line": "        if start == len(s):", "change": "should be start == len(s) - 1"},
            {"line": "    return sorted(result)", "change": "should return result[::-1]"},
        ],
    },
    {
        "replace": "        for end in range(start + 1, len(s) + 1):",
        "with":    "        for end in range(start + 1, len(s)):",
        "fix": "end must reach len(s) inclusive: range(start + 1, len(s) + 1)",
        "why": "Stopping at len(s) - 1 never lets a piece include the last character, so backtrack(len(s)) is never reached and nothing is recorded.",
        "decoys": [
            {"line": "            piece = s[start:end]", "change": "should be s[start:end + 1]"},
            {"line": "                backtrack(end)", "change": "should be backtrack(end + 1)"},
            {"line": "        if start == len(s):", "change": "should be start >= len(s) - 1"},
        ],
    },
    {
        "replace": "    i, j = 0, len(piece) - 1",
        "with":    "    i, j = 0, len(piece)",
        "fix": "the right pointer starts on the last character, len - 1",
        "why": "Starting j at len(piece) reads one past the end: IndexError on the first non-empty piece.",
        "decoys": [
            {"line": "    while i < j:", "change": "should be i <= j"},
            {"line": "        i, j = i + 1, j - 1", "change": "should only move i"},
            {"line": "    return True", "change": "should return i == j"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
