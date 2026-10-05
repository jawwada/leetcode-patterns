"""
Longest Repeating Character Replacement (LeetCode 424) - Medium
Chapter: sliding_window
Pattern: Variable-size sliding window

Given an uppercase string s and an integer k, you may change at most k characters. Return
the length of the longest substring that can be turned into one repeated letter.
Example: s = "AABABBA", k = 1 -> 4 (change one letter to get "AAAA" or "BBBB").
"""


# --- brute force ---
def brute_force(s, k):
    """For every start, extend right with 26 counts; valid if minority <= k. O(26 n^2), O(26)."""
    best = 0
    for start in range(len(s)):
        count = [0] * 26                            # recounted from scratch for every start
        for end in range(start, len(s)):
            count[ord(s[end]) - ord("A")] += 1
            length = end - start + 1
            if length - max(count) <= k:            # keep the top letter, change all the others
                if length > best:
                    best = length
    return best


# --- optimal ---
def character_replacement(s, k):
    """Window keeps the top letter and changes the rest; slide when > k. O(n) time, O(26) space."""
    count = [0] * 26
    left = 0
    max_freq = 0                # count of the most frequent letter ever seen in a window
    best = 0
    for right in range(len(s)):
        idx = ord(s[right]) - ord("A")
        count[idx] += 1
        if count[idx] > max_freq:
            max_freq = count[idx]                   # never lowered: a smaller window can't win
        if (right - left + 1) - max_freq > k:       # more than k letters to change: slide
            count[ord(s[left]) - ord("A")] -= 1
            left += 1
        length = right - left + 1
        if length > best:
            best = length
    return best


# --- try the brute force ---
print(brute_force("ABAB", 2))      # -> 4
print(brute_force("AABABBA", 1))   # -> 4
print(brute_force("AAAA", 0))      # -> 4
print(brute_force("ABCDE", 1))     # -> 2


# --- try the optimal ---
print(character_replacement("ABAB", 2))      # -> 4
print(character_replacement("AABABBA", 1))   # -> 4
print(character_replacement("AAAA", 0))      # -> 4
print(character_replacement("ABCDE", 1))     # -> 2
