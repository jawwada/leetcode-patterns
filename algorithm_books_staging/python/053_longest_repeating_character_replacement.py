"""
Longest Repeating Character Replacement - Window Length Minus Top Count at \
Most k

Given a string of uppercase letters and an integer k, return the length of
the longest substring that becomes one repeated letter after replacing at
most k of its characters: "AABABBA", k 1 -> 4 ("AABA" becomes "AAAA").
"""


# --- algorithm ---
def character_replacement(s, k):
    """Grow the window s[left..right]; slide left while length - max_count > k.
    max_count, the top count so far, never drops. O(n) time, O(26) space."""
    count = [0] * 26                # letter counts inside the window
    max_count = 0                   # top single-letter count seen so far
    left = 0
    best = 0
    for right in range(len(s)):
        slot = ord(s[right]) - ord('A')
        count[slot] += 1
        max_count = max(max_count, count[slot])
        while right - left + 1 - max_count > k:     # too many to replace
            drop = ord(s[left]) - ord('A')
            count[drop] -= 1
            left += 1               # runs at most once per step
        best = max(best, right - left + 1)
    return best


# --- try it ---
print(character_replacement("AABABBA", 1))   # -> 4
print(character_replacement("ABAB", 2))      # -> 4
print(character_replacement("ABCDE", 1))     # -> 2
print(character_replacement("AAAA", 0))      # -> 4
print(character_replacement("", 2))          # -> 0
