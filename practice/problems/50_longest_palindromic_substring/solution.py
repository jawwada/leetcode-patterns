"""
Longest Palindromic Substring (LeetCode 5) - Medium
Area: strings
Key operations: pick a center (odd and even), expand l and r while the ends match, record the best span

Given a string s, return the longest substring that reads the same forwards and backwards.
If several have the maximum length, return the leftmost one.
Example: "babad" -> "bab"
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(s: str) -> str:
    """Check every substring against its reverse, keeping the first longest. O(n^3): O(n^2)
    substrings, O(n) each; the waste is re-checking the inside of a substring whose inner part
    was already tested."""
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i:j + 1]
            if len(sub) > len(best) and sub == sub[::-1]:
                best = sub
    return best


# --- optimal ---
def solve(s: str) -> str:
    """Expand around each of the 2n - 1 centers (a character, or the gap between two) while the
    characters at both ends match. O(n^2) time, O(1) extra space, no table."""
    n = len(s)
    best_lo, best_len = 0, 0
    for center in range(n):
        for l, r in ((center, center), (center, center + 1)):
            log(f"center {center} ({'odd' if l == r else 'even'}): l={l} r={r}")
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
                log(f"    s[{l + 1}] == s[{r - 1}] -> expand to l={l} r={r}, palindrome {s[l + 1:r]!r}")
            if r - l - 1 > best_len:
                best_lo, best_len = l + 1, r - l - 1
                log(f"    new best {s[best_lo:best_lo + best_len]!r} (len {best_len})")
    return s[best_lo:best_lo + best_len]


# --- demo ---
def demo():
    return solve("babad")


# --- tests ---
def tests():
    assert solve("babad") == "bab"  # leftmost of bab / aba
    assert solve("cbbd") == "bb"  # even length
    assert solve("a") == "a"
    assert solve("") == ""
    assert solve("ac") == "a"
    assert solve("aaaa") == "aaaa"
    assert solve("abba") == "abba"  # palindrome reaching index 0
    assert solve("abacdfgdcaba") == "aba"
    assert solve("forgeeksskeegfor") == "geeksskeeg"
    import random
    random.seed(1)
    for _ in range(200):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 10)))
        assert solve(s) == brute_force(s), s


# --- bugs ---
BUGS = [
    {
        "replace": "            if r - l - 1 > best_len:",
        "with":    "            if r - l - 1 >= best_len:",
        "fix": "replace the best only when strictly longer, so the leftmost one is kept",
        "why": "An equal-length palindrome found later overwrites the earlier one, so \"babad\" returns \"aba\" instead of \"bab\" (and \"ac\" returns \"c\").",
        "decoys": [
            {"line": "        for l, r in ((center, center), (center, center + 1)):", "change": "should be (center - 1, center) for the even case"},
            {"line": "    best_lo, best_len = 0, 0", "change": "should start best_len at 1"},
            {"line": "    return s[best_lo:best_lo + best_len]", "change": "should be s[best_lo:best_len]"},
        ],
    },
    {
        "replace": "                best_lo, best_len = l + 1, r - l - 1",
        "with":    "                best_lo, best_len = l, r - l - 1",
        "fix": "the loop stopped one step too far: the palindrome is s[l + 1 : r]",
        "why": "l points to the first mismatching character (or -1), so the recorded span starts one character early: \"cbbd\" returns \"cb\" instead of \"bb\".",
        "decoys": [
            {"line": "                r += 1", "change": "should be r += 2"},
            {"line": "            if r - l - 1 > best_len:", "change": "should be r - l + 1"},
            {"line": "    n = len(s)", "change": "should be n = len(s) - 1"},
        ],
    },
    {
        "replace": "            while l >= 0 and r < n and s[l] == s[r]:",
        "with":    "            while l > 0 and r < n and s[l] == s[r]:",
        "fix": "index 0 is a valid left end: l >= 0",
        "why": "The expansion can never include s[0], so \"abba\" returns \"bb\" instead of \"abba\" and \"a\" returns \"\".",
        "decoys": [
            {"line": "                l -= 1", "change": "should be l -= 2"},
            {"line": "    for center in range(n):", "change": "should be range(1, n)"},
            {"line": "                best_lo, best_len = l + 1, r - l - 1", "change": "should be l + 1, r - l"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
