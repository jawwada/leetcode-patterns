"""
Find Longest Awesome Substring (LeetCode 1542) - Hard
Chapter: bit_manipulation
Pattern: Prefix parity mask + first-seen positions

A string of digits is awesome if some rearrangement of it is a palindrome, that is, at most
one digit appears an odd number of times. Given a digit string s, return the length of its
longest awesome substring (a single character always counts).
Example: "3242415" -> 5 ("24241" rearranges to "24142").   "12345678" -> 1.
"""


# --- brute force ---
def brute_force(s):
    """Grow every substring from every start and count the odd digits. O(n^2) time."""
    best = 0
    for i in range(len(s)):
        counts = [0] * 10
        for j in range(i, len(s)):  # the substring s[i..j]
            counts[int(s[j])] += 1
            odd = 0
            for digit in range(10):
                if counts[digit] % 2 == 1:
                    odd += 1
            if odd <= 1:
                best = max(best, j - i + 1)
    return best


# --- optimal ---
def longest_awesome(s):
    """Prefix parity masks; a substring is awesome when two masks differ in <= 1 bit. O(10 n)."""
    first_seen = {0: -1}  # parity mask -> earliest prefix index that produced it
    mask = 0
    best = 0
    for j in range(len(s)):
        mask ^= 1 << int(s[j])  # flip this digit's parity bit
        if mask in first_seen:  # same parities: every digit count in between is even
            best = max(best, j - first_seen[mask])
        for digit in range(10):  # exactly one digit odd in between
            partner = mask ^ (1 << digit)
            if partner in first_seen:
                best = max(best, j - first_seen[partner])
        if mask not in first_seen:
            first_seen[mask] = j  # keep only the earliest, it gives the longest substring
    return best


# --- try the brute force ---
print(brute_force("3242415"))    # -> 5
print(brute_force("12345678"))   # -> 1
print(brute_force("213123"))     # -> 6
print(brute_force("00"))         # -> 2


# --- try the optimal ---
print(longest_awesome("3242415"))    # -> 5
print(longest_awesome("12345678"))   # -> 1
print(longest_awesome("213123"))     # -> 6
print(longest_awesome("00"))         # -> 2
