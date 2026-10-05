"""
Longest Substring Without Repeating Characters (LeetCode 3) - Medium
Area: sliding window
Key operations: expand right, look up the last index of the new char, jump left past it, record the window length

Given a string s, return the length of the longest substring in which no character repeats.
Example: "abcabcbb" -> 3 ("abc"); "pwwkew" -> 3 ("wke"); "bbbbb" -> 1
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(s: str) -> int:
    """For every start, extend to the right while the characters stay distinct. O(n^2):
    start i+1 rebuilds a set over a stretch that start i already proved distinct."""
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best


# --- optimal ---
def solve(s: str) -> int:
    """Window s[left..right] holds distinct characters. When s[right] was already seen inside the
    window, jump left just past that earlier copy. Each edge only moves right: O(n)."""
    last = {}  # char -> index of its most recent occurrence
    left = 0   # window is s[left..right]
    best = 0
    log(f"    {s}")
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            log(f"r={right} '{ch}' repeats at {last[ch]} (inside window from {left}) -> left = {last[ch] + 1}")
            left = last[ch] + 1
        last[ch] = right
        if right - left + 1 > best:
            best = right - left + 1
        log(f"r={right} '{ch}' window [{left}..{right}] '{s[left:right + 1]}' len {right - left + 1} best {best}  last {last}")
        log(f"    {' ' * left}{'^' * (right - left + 1)}")
    return best


# --- demo ---
def demo():
    return solve("abcabcbb")


# --- tests ---
def tests():
    assert solve("abcabcbb") == 3
    assert solve("pwwkew") == 3
    assert solve("bbbbb") == 1
    assert solve("") == 0
    assert solve("a") == 1
    assert solve(" ") == 1
    assert solve("abba") == 2  # stale 'a' must not pull left backwards
    assert solve("dvdf") == 3
    assert solve("abcdef") == 6
    import random
    random.seed(1)
    for _ in range(200):
        t = "".join(random.choice("abcd") for _ in range(random.randint(0, 12)))
        assert solve(t) == brute_force(t), t


# --- bugs ---
BUGS = [
    {
        "replace": "        if ch in last and last[ch] >= left:",
        "with":    "        if ch in last:",
        "fix": "only react to a copy inside the window: ch in last and last[ch] >= left",
        "why": "A stale copy left of the window pulls left backwards: on \"abba\" the final 'a' moves left from 2 back to 1 and the window \"bba\" is counted as length 3 instead of 2.",
        "decoys": [
            {"line": "        last[ch] = right", "change": "should be set only when ch is not yet in last"},
            {"line": "            left = last[ch] + 1", "change": "should be left = right"},
            {"line": "    left = 0   # window is s[left..right]", "change": "should start at -1"},
        ],
    },
    {
        "replace": "            left = last[ch] + 1",
        "with":    "            left = last[ch]",
        "fix": "jump past the earlier copy: left = last[ch] + 1",
        "why": "Leaving left on the earlier copy keeps both copies in the window, so \"abcabcbb\" counts \"abca\" as 4 instead of 3.",
        "decoys": [
            {"line": "        if ch in last and last[ch] >= left:", "change": "should be last[ch] > left"},
            {"line": "        if right - left + 1 > best:", "change": "should be >= best"},
            {"line": "    return best", "change": "should return best + 1"},
        ],
    },
    {
        "replace": "            best = right - left + 1",
        "with":    "            best = right - left",
        "fix": "the window s[left..right] has right - left + 1 characters",
        "why": "The length is off by one, so \"abc\" reports 2 and \"a\" reports 0 instead of 1.",
        "decoys": [
            {"line": "        last[ch] = right", "change": "should be last[ch] = left"},
            {"line": "    last = {}  # char -> index of its most recent occurrence", "change": "should be a set of chars"},
            {"line": "        if right - left + 1 > best:", "change": "should be right - left > best"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
