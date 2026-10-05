"""
Longest Happy Prefix (LeetCode 1392) - Hard
Chapter: strings
Pattern: KMP failure function (longest border)

A happy prefix is a non-empty proper prefix of s that is also a suffix of s. Return the
longest one, or "" if there is none.
Example: "level" -> "l"; "ababab" -> "abab"; "leetcodeleet" -> "leet"; "a" -> "".
"""


# --- brute force ---
def brute_force(s):
    """Try every length from longest to shortest, comparing prefix and suffix. O(n^2) time."""
    n = len(s)
    for length in range(n - 1, 0, -1):             # longest candidate first
        if s[:length] == s[n - length:]:           # a fresh O(length) comparison each time
            return s[:length]
    return ""


# --- optimal ---
def longest_happy_prefix(s):
    """KMP failure array: fail[i] = longest border of s[:i+1], built from fail[i-1]. O(n)."""
    n = len(s)
    fail = [0] * n
    for i in range(1, n):
        k = fail[i - 1]                            # border length so far; try to extend it by s[i]
        while k > 0 and s[i] != s[k]:
            k = fail[k - 1]                        # mismatch: shrink to the border of the border
        if s[i] == s[k]:
            k += 1
        fail[i] = k
    return s[:fail[n - 1]]                         # the border of the whole string


# --- try the brute force ---
print(brute_force("level"))                        # -> l
print(brute_force("ababab"))                       # -> abab
print(brute_force("leetcodeleet"))                 # -> leet
print(brute_force("aaaa"))                         # -> aaa


# --- try the optimal ---
print(longest_happy_prefix("level"))               # -> l
print(longest_happy_prefix("ababab"))              # -> abab
print(longest_happy_prefix("leetcodeleet"))        # -> leet
print(longest_happy_prefix("aaaa"))                # -> aaa
