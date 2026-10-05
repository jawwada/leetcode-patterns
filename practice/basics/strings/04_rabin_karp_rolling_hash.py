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
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
    log(f"pattern {pattern!r} hash {target}; high = {BASE}^{m - 1} mod {MOD} = {high}")
    hits = []
    for i in range(n - m + 1):
        log(f"window [{i}..{i + m - 1}] {text[i:i + m]!r} hash {h}" + (f"  == target -> verify: {'match' if text[i:i + m] == pattern else 'COLLISION, ignored'}" if h == target else ""))
        if h == target and text[i:i + m] == pattern:
            hits.append(i)
            log(f"    hit at {i}")
        if i + m < n:
            h = ((h - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
            log(f"    roll: drop {text[i]!r}, add {text[i + m]!r} -> hash {h}")
    return hits


# --- demo ---
def demo():
    return solve("abracadabra", "abra")


# --- tests ---
def tests():
    assert solve("abracadabra", "abra") == [0, 7]
    assert solve("abccabra", "abra") == [4]  # 'abcc' has the same hash as 'abra': collision, verified away
    assert solve("aaaa", "aa") == [0, 1, 2]
    assert solve("abc", "abcd") == []
    assert solve("", "a") == []
    assert solve("x", "x") == [0]
    import random
    rng = random.Random(0)
    for _ in range(200):
        text = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
        pattern = "".join(rng.choice("abc") for _ in range(rng.randint(1, 3)))
        assert solve(text, pattern) == brute_force(text, pattern), (text, pattern)


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
