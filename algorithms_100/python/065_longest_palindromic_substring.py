"""
Longest Palindromic Substring - Expand Around Every Center

Return the longest contiguous substring that reads the same forwards and
backwards (the leftmost one on a tie): "babad" -> "bab".
"""


# --- algorithm ---
def longest_palindrome(s):
    """Expand around all 2n - 1 centers (n chars, n - 1 gaps); keep the
    longest. O(n^2) time, O(1) space."""
    best_start = 0
    best_len = 0
    for center in range(2 * len(s) - 1):
        left = center // 2
        right = left + center % 2       # even center: a char; odd: a gap
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1                   # ends match: grow one step each way
            right += 1
        length = right - left - 1       # the loop stepped one past each end
        if length > best_len:           # strictly longer: ties keep the first
            best_start = left + 1
            best_len = length
    return s[best_start:best_start + best_len]


# --- try it ---
print(longest_palindrome("babad"))          # -> bab
print(longest_palindrome("cbbd"))           # -> bb
print(longest_palindrome("abacdfgdcaba"))   # -> aba
print(longest_palindrome("a"))              # -> a
