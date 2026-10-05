"""
Longest Substring Without Repeating Characters (LeetCode 3) - Medium
Chapter: sliding_window
Pattern: Variable-size sliding window

Given a string s, return the length of the longest substring whose characters are all
different from each other.
Example: s = "abcabcbb" -> 3 ("abc"); s = "pwwkew" -> 3 ("wke"); s = "bbbbb" -> 1.
"""


# --- brute force ---
def brute_force(s):
    """For every start, extend right while characters stay distinct. O(n^2) time, O(n) space."""
    best = 0
    for start in range(len(s)):
        seen = set()                                # rebuilt from scratch for every start
        for end in range(start, len(s)):
            if s[end] in seen:
                break
            seen.add(s[end])
        if len(seen) > best:
            best = len(seen)
    return best


# --- optimal ---
def length_of_longest_substring(s):
    """Window [left, right]; on a repeat jump left past the earlier copy. O(n) time, O(n) space."""
    last = {}                   # char -> index where it was most recently seen
    left = 0
    best = 0
    for right in range(len(s)):
        ch = s[right]
        if ch in last and last[ch] >= left:         # the earlier copy is inside the window
            left = last[ch] + 1                     # jump just past it, never backwards
        last[ch] = right
        length = right - left + 1
        if length > best:
            best = length
    return best


# --- try the brute force ---
print(brute_force("abcabcbb"))   # -> 3
print(brute_force("bbbbb"))      # -> 1
print(brute_force("pwwkew"))     # -> 3
print(brute_force("abba"))       # -> 2


# --- try the optimal ---
print(length_of_longest_substring("abcabcbb"))   # -> 3
print(length_of_longest_substring("bbbbb"))      # -> 1
print(length_of_longest_substring("pwwkew"))     # -> 3
print(length_of_longest_substring("abba"))       # -> 2
