"""
Minimum Window Substring - Expand Right, Shrink Left

Given strings s and t, return the shortest substring of s that contains every
character of t, repeats included ("" if there is none):
s "ADOBECODEBANC", t "ABC" -> "BANC".
"""


# --- algorithm ---
def char_counts(text):
    """How many copies of each character text holds. O(len(text))."""
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def min_window(s, t):
    """Grow right to cover t, shrink left while covered. O(len(s) + len(t))."""
    if len(t) == 0:
        return ""                   # nothing to cover
    need = char_counts(t)           # char -> copies the window lacks
    missing = len(t)                # chars of t not yet covered, with repeats
    left = 0
    best_start = 0
    best_len = len(s) + 1           # longer than any real window
    for right in range(len(s)):
        ch = s[right]
        if need.get(ch, 0) > 0:
            missing -= 1            # this copy fills a real gap
        need[ch] = need.get(ch, 0) - 1  # below zero: a spare copy
        while missing == 0:         # covers t: record, then shrink
            if right - left + 1 < best_len:
                best_start = left
                best_len = right - left + 1
            drop = s[left]
            need[drop] += 1
            if need[drop] > 0:
                missing += 1        # dropped a copy the window needed
            left += 1
    if best_len > len(s):
        return ""                   # no window ever covered t
    return s[best_start:best_start + best_len]


# --- try it ---
print(min_window("ADOBECODEBANC", "ABC"))       # -> BANC
print(min_window("AAB", "AA"))                  # -> AA
print(min_window("a", "a"))                     # -> a
print(min_window("a", "aa") == "")              # -> True
