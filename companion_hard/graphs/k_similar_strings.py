"""
K-Similar Strings (LeetCode 854) - Hard
Chapter: graphs
Pattern: BFS over states with pruned branching (fix the first mismatch)

s1 and s2 are anagrams of each other (letters a-f, length <= 20). One move swaps two letters of
s1. Return the minimum number of swaps that turns s1 into s2.
Example: s1 = "abac", s2 = "baca" -> 2 (abac -> baac -> baca).
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
def swap(text, i, j):
    """Return text with the characters at i and j exchanged."""
    chars = list(text)
    chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


# --- brute force ---
def brute_force(s1, s2):
    """BFS over strings trying every one of the n(n-1)/2 swaps at each state. Exponential."""
    n = len(s1)
    queue = deque([(s1, 0)])
    seen = {s1}
    while queue:
        current, swaps = queue.popleft()
        if current == s2:
            return swaps
        for i in range(n):
            for j in range(i + 1, n):            # every pair, even positions already correct
                next_string = swap(current, i, j)
                if next_string not in seen:
                    seen.add(next_string)
                    queue.append((next_string, swaps + 1))
    return -1


# --- optimal ---
def k_similar_strings(s1, s2):
    """BFS in layers, but only swap to fix the first mismatch without breaking another. Small."""
    queue = deque([s1])
    seen = {s1}
    swaps = 0
    while queue:
        for _ in range(len(queue)):              # one layer = one swap
            current = queue.popleft()
            if current == s2:
                return swaps
            i = 0
            while current[i] == s2[i]:           # the first mismatch must be fixed eventually
                i += 1
            for j in range(i + 1, len(current)):
                if current[j] == s2[i] and current[j] != s2[j]:   # fixes i, does not break j
                    next_string = swap(current, i, j)
                    if next_string not in seen:
                        seen.add(next_string)
                        queue.append(next_string)
        swaps += 1
    return -1


# --- try the brute force ---
print(brute_force("ab", "ba"))             # -> 1
print(brute_force("abc", "bca"))           # -> 2
print(brute_force("abac", "baca"))         # -> 2
print(brute_force("aabc", "abca"))         # -> 2
print(brute_force("abcdef", "abcdef"))     # -> 0


# --- try the optimal ---
print(k_similar_strings("ab", "ba"))             # -> 1
print(k_similar_strings("abc", "bca"))           # -> 2
print(k_similar_strings("abac", "baca"))         # -> 2
print(k_similar_strings("aabc", "abca"))         # -> 2
print(k_similar_strings("abcdef", "abcdef"))     # -> 0
