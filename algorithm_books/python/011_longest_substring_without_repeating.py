"""
Longest Substring Without Repeating Characters - Variable Window with \
Last-Seen Index

Given a string, return the length of its longest substring in which no
character appears twice: "abcbad" -> 4 (the window "cbad").
"""


# --- algorithm ---
def length_of_longest_substring(s):
    """Window s[left..right] has no repeats; on a repeat inside it, jump left
    past the earlier copy. O(n) time, O(alphabet) space."""
    last_seen = {}                  # char -> index of its latest occurrence
    left = 0
    best = 0
    for right in range(len(s)):
        ch = s[right]
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1    # jump past the copy in the window
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


# --- try it ---
print(length_of_longest_substring("abcbad"))      # -> 4
print(length_of_longest_substring("abcabcbb"))    # -> 3
print(length_of_longest_substring("abba"))        # -> 2
print(length_of_longest_substring("bbbbb"))       # -> 1
print(length_of_longest_substring(""))            # -> 0
