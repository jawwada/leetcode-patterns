"""
Valid Anagram (LeetCode 242) - Easy
Chapter: strings
Pattern: Fixed-alphabet frequency count

Given two lowercase strings s and t, return True if t is an anagram of s: the same letters
with the same multiplicities, in any order.
Example: s = "anagram", t = "nagaram" -> True; s = "rat", t = "car" -> False.
"""


# --- brute force ---
def brute_force(s, t):
    """Sort both strings and compare the sorted letters. O(n log n) time, O(n) space."""
    sorted_s = sorted(s)
    sorted_t = sorted(t)
    if sorted_s == sorted_t:              # anagrams sort to the identical sequence
        return True
    return False


# --- optimal ---
def is_anagram(s, t):
    """One 26-cell histogram: s adds, t subtracts, every cell must end at 0. O(n), O(1) space."""
    if len(s) != len(t):
        return False
    count = [0] * 26
    for i in range(len(s)):
        letter_s = ord(s[i]) - ord("a")   # 'a' -> cell 0, 'b' -> cell 1, ...
        letter_t = ord(t[i]) - ord("a")
        count[letter_s] += 1              # s pushes its column up
        count[letter_t] -= 1              # t pulls it back down
    for c in count:
        if c != 0:
            return False                  # one string has more of this letter
    return True


# --- try the brute force ---
print(brute_force("anagram", "nagaram"))   # -> True
print(brute_force("rat", "car"))           # -> False
print(brute_force("a", "ab"))              # -> False
print(brute_force("aabb", "abab"))         # -> True


# --- try the optimal ---
print(is_anagram("anagram", "nagaram"))    # -> True
print(is_anagram("rat", "car"))            # -> False
print(is_anagram("a", "ab"))               # -> False
print(is_anagram("aabb", "abab"))          # -> True
