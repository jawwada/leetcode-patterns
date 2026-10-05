"""
Generate Parentheses (LeetCode 22) - Basics
Area: backtracking
Key operations: choose an open bracket while opened < n, choose a close bracket while closed < opened, unchoose

Return every well-formed string of n pairs of parentheses. Two counters replace the used[] flags:
an open bracket is allowed while fewer than n are placed, a close bracket while it has an unmatched
open bracket to its left. Results sorted.
Example: n = 3 -> ["((()))", "(()())", "(())()", "()(())", "()()()"]
"""
import sys
from itertools import product
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def balanced(s: str) -> bool:
    depth = 0
    for ch in s:
        depth += 1 if ch == "(" else -1
        if depth < 0:
            return False
    return depth == 0


def brute_force(n: int) -> List[str]:
    """Enumerate all 2^(2n) bracket strings and keep the balanced ones. O(n * 4^n); the valid ones are a vanishing fraction."""
    return sorted("".join(p) for p in product("()", repeat=2 * n) if balanced(p))


# --- optimal ---
def solve(n: int) -> List[str]:
    """Two counters guard the two choices, so every leaf of the tree is valid. O(n * number of results)."""
    res, path = [], []

    def backtrack(opened: int, closed: int) -> None:
        if len(path) == 2 * n:
            res.append("".join(path))
            log("  " * len(path) + f"record {''.join(path)}")
            return
        if opened < n:
            path.append("(")
            log("  " * len(path) + f"choose open  -> {''.join(path)}  opened={opened + 1} closed={closed}")
            backtrack(opened + 1, closed)
            path.pop()
            log("  " * (len(path) + 1) + f"unchoose open  -> {''.join(path)}")
        if closed < opened:
            path.append(")")
            log("  " * len(path) + f"choose close -> {''.join(path)}  opened={opened} closed={closed + 1}")
            backtrack(opened, closed + 1)
            path.pop()
            log("  " * (len(path) + 1) + f"unchoose close -> {''.join(path)}")

    backtrack(0, 0)
    return sorted(res)


# --- demo ---
def demo():
    return solve(3)


# --- tests ---
def tests():
    assert solve(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert solve(1) == ["()"]
    assert solve(2) == ["(())", "()()"]
    assert solve(0) == [""]
    import random
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(0, 5)
        assert solve(n) == brute_force(n), n


# --- bugs ---
BUGS = [
    {
        "replace": "        if closed < opened:",
        "with":    "        if closed < n:",
        "fix": "a close bracket needs an unmatched open bracket before it: closed < opened",
        "why": "Any string with n of each bracket is accepted, including ')(' for n = 1 and '))((' for n = 2.",
        "decoys": [
            {"line": "        if opened < n:", "change": "should be opened < n - 1"},
            {"line": "        if len(path) == 2 * n:", "change": "should be == n"},
            {"line": "    backtrack(0, 0)", "change": "should be backtrack(1, 0)"},
        ],
    },
    {
        "replace": "        if opened < n:",
        "with":    "        if opened <= n:",
        "fix": "at most n open brackets: place one only while opened < n",
        "why": "One extra open bracket is allowed, so strings like '((' for n = 1 reach length 2n and are recorded unclosed.",
        "decoys": [
            {"line": "        if closed < opened:", "change": "should be closed <= opened"},
            {"line": "            backtrack(opened + 1, closed)", "change": "should be backtrack(opened, closed + 1)"},
            {"line": "    return sorted(res)", "change": "should return res unsorted"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
