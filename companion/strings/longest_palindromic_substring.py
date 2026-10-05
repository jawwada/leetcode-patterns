"""
Longest Palindromic Substring (LeetCode 5) - Medium
Chapter: strings
Pattern: Expand around center

Given a string s, return the longest substring that reads the same forwards and backwards;
if several tie, any one is accepted.
Example: "babad" -> "bab" (or "aba"); "cbbd" -> "bb".
"""


# --- brute force ---
def brute_force(s):
    """Test every substring against its reverse, keep the longest. O(n^3) time, O(1) extra space."""
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i:j + 1]
            if len(sub) > len(best) and sub == sub[::-1]:
                best = sub                # longer and a palindrome: new best
    return best


# --- optimal ---
def expand(s, lo, hi):
    """Grow outward from a center while both ends match; return (start, length). O(n) worst case."""
    while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
        lo -= 1
        hi += 1
    return lo + 1, hi - lo - 1            # the loop overshoots by one on each side


def longest_palindrome(s):
    """Try all 2n - 1 centers and expand around each. O(n^2) time, O(1) extra space."""
    best_start = 0
    best_len = 0
    for i in range(len(s)):
        start, length = expand(s, i, i)           # odd length, centred on s[i]
        if length > best_len:
            best_start = start
            best_len = length
        start, length = expand(s, i, i + 1)       # even length, centred between s[i] and s[i+1]
        if length > best_len:
            best_start = start
            best_len = length
    return s[best_start:best_start + best_len]


# --- try the brute force ---
print(brute_force("babad"))                        # -> bab
print(brute_force("cbbd"))                         # -> bb
print(brute_force("a"))                            # -> a
print(brute_force("forgeeksskeegfor"))             # -> geeksskeeg


# --- try the optimal ---
print(longest_palindrome("babad"))                 # -> bab
print(longest_palindrome("cbbd"))                  # -> bb
print(longest_palindrome("a"))                     # -> a
print(longest_palindrome("forgeeksskeegfor"))      # -> geeksskeeg
