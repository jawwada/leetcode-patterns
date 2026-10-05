"""
Minimum Window Substring (LeetCode 76) - Hard
Chapter: sliding_window
Pattern: Variable-size sliding window

Given strings s and t, return the shortest substring of s that contains every character
of t with multiplicity, or "" if none exists.
Example: s = "ADOBECODEBANC", t = "ABC" -> "BANC".
"""
import math                         # math.inf is "longer than any window"


# --- helpers ---
def count_items(items):
    """How many times each item appears, as a dict."""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


# --- brute force ---
def covers(have, need):
    """True when have holds at least need[ch] copies of every ch."""
    for ch in need:
        if have.get(ch, 0) < need[ch]:
            return False
    return True


def brute_force(s, t):
    """From every start, extend right until the window covers t. O(n^2 * alphabet) time."""
    need = count_items(t)
    best = ""
    for start in range(len(s)):
        have = {}                               # recounted from scratch for every start
        for end in range(start, len(s)):
            have[s[end]] = have.get(s[end], 0) + 1
            if covers(have, need):
                if best == "" or end - start + 1 < len(best):
                    best = s[start:end + 1]
                break                           # longer windows from this start cannot win
    return best


# --- optimal ---
def min_window(s, t):
    """Grow right until t is covered, shrink left while it stays covered. O(n + m) time."""
    need = count_items(t)
    missing = len(t)                            # characters of t not yet in the window
    left = 0
    best_start = 0
    best_len = math.inf
    for right in range(len(s)):
        ch = s[right]
        if need.get(ch, 0) > 0:                 # a copy we still needed, not a surplus one
            missing -= 1
        need[ch] = need.get(ch, 0) - 1          # below zero means surplus copies
        if missing == 0:                        # the window covers t: shrink it
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_start = left
                best_len = right - left + 1
            need[s[left]] += 1                  # evict one needed char so right must grow again
            missing += 1
            left += 1
    if best_len == math.inf:
        return ""
    return s[best_start:best_start + best_len]


# --- try the brute force ---
print(brute_force("ADOBECODEBANC", "ABC"))   # -> BANC
print(brute_force("a", "a"))                 # -> a
print(brute_force("a", "aa"))                # -> (empty line)
print(brute_force("aabbcc", "abc"))          # -> abbc


# --- try the optimal ---
print(min_window("ADOBECODEBANC", "ABC"))    # -> BANC
print(min_window("a", "a"))                  # -> a
print(min_window("a", "aa"))                 # -> (empty line)
print(min_window("aabbcc", "abc"))           # -> abbc
