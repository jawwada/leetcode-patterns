"""
Longest Duplicate Substring (LeetCode 1044) - Hard
Chapter: strings
Pattern: Binary search on the answer + rolling hash

Given a string of lowercase letters, return any longest substring that occurs two or more
times (occurrences may overlap), or "" if every substring is unique.
Example: "banana" -> "ana" (at indices 1 and 3); "abcd" -> "".
"""


# --- brute force ---
def brute_force(s):
    """For each length, longest first, put every window in a set until one repeats. O(n^3)."""
    n = len(s)
    for length in range(n - 1, 0, -1):
        seen = set()
        for i in range(n - length + 1):
            window = s[i:i + length]
            if window in seen:
                return window                      # the first repeat at the longest length wins
            seen.add(window)
    return ""


# --- optimal ---
MOD = (1 << 61) - 1                                # a large prime keeps hash collisions rare
BASE = 257                                         # the "digit" weight of the rolling hash


def find_repeat(s, codes, length):
    """Start of some window of this length that also appears earlier, or -1. O(n) expected."""
    n = len(s)
    h = 0
    for i in range(length):
        h = (h * BASE + codes[i]) % MOD            # the first window as a base-BASE number
    seen = {h: [0]}                                # hash -> starts of the windows with that hash
    power = pow(BASE, length, MOD)                 # weight of the character leaving the window
    for i in range(1, n - length + 1):
        h = (h * BASE - codes[i - 1] * power + codes[i + length - 1]) % MOD   # slide by one
        if h in seen:
            for j in seen[h]:
                if s[j:j + length] == s[i:i + length]:
                    return i                       # a real repeat, not just a hash collision
            seen[h].append(i)
        else:
            seen[h] = [i]
    return -1


def longest_duplicate_substring(s):
    """Binary search the length; check each length with a rolling hash. O(n log n) expected."""
    n = len(s)
    codes = []
    for ch in s:
        codes.append(ord(ch) - ord("a") + 1)       # letters as numbers 1..26
    lo = 1
    hi = n - 1
    start = -1
    best = 0
    while lo <= hi:                                # a repeat of length L implies every shorter L
        mid = (lo + hi) // 2
        i = find_repeat(s, codes, mid)
        if i >= 0:
            start = i                              # feasible: remember it and try longer
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    if start < 0:
        return ""
    return s[start:start + best]


# --- try the brute force ---
print(brute_force("banana"))                       # -> ana
print(brute_force("abcd"))                         # -> (empty line)
print(brute_force("aaaaa"))                        # -> aaaa
print(brute_force("abcabcabc"))                    # -> abcabc


# --- try the optimal ---
print(longest_duplicate_substring("banana"))       # -> ana
print(longest_duplicate_substring("abcd"))         # -> (empty line)
print(longest_duplicate_substring("aaaaa"))        # -> aaaa
print(longest_duplicate_substring("abcabcabc"))    # -> abcabc
