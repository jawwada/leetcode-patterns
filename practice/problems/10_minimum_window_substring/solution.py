"""
Minimum Window Substring (LeetCode 76) - Medium-Hard
Area: sliding window
Key operations: count what is needed, expand right and bump formed, shrink left while every count is met, record the shortest

Given strings s and t, return the shortest substring of s that contains every character of t
(with multiplicity), or "" if there is none.
Example: s = "ADOBECODEBANC", t = "ABC" -> "BANC"
"""
import sys
from collections import Counter

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(s: str, t: str) -> str:
    """For every start, extend to the right counting letters until the window covers t, record it.
    O(n^2 * |t|): start i+1 recounts the stretch start i already counted and rechecks all of t."""
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have = Counter()
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= need[c] for c in need):
                if not best or j - i + 1 < len(best):
                    best = s[i:j + 1]
                break
    return best


# --- optimal ---
def solve(s: str, t: str) -> str:
    """Window s[left..right] with a count of its letters; formed = how many distinct letters of t
    have their count met. Expand right; while all are met shrink left and record. O(|s| + |t|)."""
    need = Counter(t)
    have = Counter()
    formed, required = 0, len(need)  # formed == required <=> the window covers t
    left = 0
    best_start, best_len = 0, float("inf")
    log(f"need {dict(need)}  required {required}")
    for right, ch in enumerate(s):
        have[ch] += 1
        if ch in need and have[ch] == need[ch]:
            formed += 1
        log(f"r={right} in '{ch}': have {{{', '.join(f'{c}:{have[c]}' for c in need)}}} formed {formed}/{required}  window [{left}..{right}] '{s[left:right + 1]}'")
        while formed == required:
            if right - left + 1 < best_len:
                best_start, best_len = left, right - left + 1
            log(f"    covers t: [{left}..{right}] '{s[left:right + 1]}' len {right - left + 1}, best '{s[best_start:best_start + best_len]}'")
            out = s[left]
            have[out] -= 1
            if out in need and have[out] < need[out]:
                formed -= 1
            left += 1
            log(f"    out '{out}': have[{out}] {have[out]}, formed {formed}/{required}  window [{left}..{right}] '{s[left:right + 1]}'")
        log(f"    {s}")
        log(f"    {' ' * left}{'^' * (right - left + 1)}")
    return "" if best_len == float("inf") else s[best_start:best_start + best_len]


# --- demo ---
def demo():
    return solve("ADOBECODEBANC", "ABC")


# --- tests ---
def tests():
    assert solve("ADOBECODEBANC", "ABC") == "BANC"
    assert solve("a", "a") == "a"
    assert solve("a", "aa") == ""  # multiplicity matters
    assert solve("aa", "aa") == "aa"
    assert solve("ab", "b") == "b"
    assert solve("abc", "d") == ""
    assert solve("", "a") == ""
    assert solve("aabbcc", "abc") == "abbc"
    assert solve("aab", "ab") == "ab"
    import random
    random.seed(1)
    for _ in range(200):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 10)))
        t = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
        got, want = solve(s, t), brute_force(s, t)
        assert len(got) == len(want) and got in s and not (Counter(t) - Counter(got) if got else want), (s, t, got, want)


# --- bugs ---
BUGS = [
    {
        "replace": "        if ch in need and have[ch] == need[ch]:",
        "with":    "        if ch in need and have[ch] >= need[ch]:",
        "fix": "bump formed only at the moment the count is met: have[ch] == need[ch]",
        "why": "Every surplus copy bumps formed again, so after formed overshoots the shrink loop keeps going past a needed letter: s = \"aab\", t = \"ab\" returns \"a\".",
        "decoys": [
            {"line": "        have[ch] += 1", "change": "should run only when ch in need"},
            {"line": "            left += 1", "change": "should run before have[out] is decremented"},
            {"line": "    formed, required = 0, len(need)  # formed == required <=> the window covers t", "change": "required should be len(t)"},
        ],
    },
    {
        "replace": "            if out in need and have[out] < need[out]:",
        "with":    "            if out in need and have[out] <= need[out]:",
        "fix": "formed drops only when the count falls below what is needed: have[out] < need[out]",
        "why": "Dropping a surplus copy already breaks the window, so the shrink stops too early and the surplus is never trimmed: s = \"aab\", t = \"ab\" returns \"aab\" instead of \"ab\".",
        "decoys": [
            {"line": "            formed += 1", "change": "should be formed = required"},
            {"line": "            have[out] -= 1", "change": "should run after left += 1"},
            {"line": "        while formed == required:", "change": "should be formed >= required"},
        ],
    },
    {
        "replace": "        while formed == required:",
        "with":    "        if formed == required:",
        "fix": "shrink with a while loop: keep dropping from the left as long as the window still covers t",
        "why": "A single shrink step per expansion never trims the surplus, so the window stays wide: \"ADOBECODEBANC\" / \"ABC\" returns \"ADOBEC\" instead of \"BANC\".",
        "decoys": [
            {"line": "            if right - left + 1 < best_len:", "change": "should be <= best_len"},
            {"line": "            out = s[left]", "change": "should be s[left + 1]"},
            {"line": "    return \"\" if best_len == float(\"inf\") else s[best_start:best_start + best_len]", "change": "should slice to best_start + best_len - 1"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
