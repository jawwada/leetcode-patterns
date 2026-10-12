"""
Longest Palindromic Substring (LeetCode 5)
Return the longest substring that reads the same forwards and backwards.
  s = "babad"  ->  "bab"   ("aba" is also valid)

Idea: every palindrome has a center: a character (odd length) or a gap (even length).
      Try all 2n - 1 centers and expand outwards while both ends match.

Pseudocode:
  for each center i:
      for (l, r) in [(i, i), (i, i + 1)]:
          while in bounds and s[l] == s[r]: l -= 1; r += 1
          palindrome is s[l+1 : r]; keep it if longest

Time O(n^2), space O(1).
"""


def longest_palindrome(s):
    best_start, best_len = 0, 0
    for i in range(len(s)):
        for l, r in ((i, i), (i, i + 1)):        # odd center, even center
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1                           # expand outwards
                r += 1
            if r - l - 1 > best_len:             # palindrome is s[l+1:r]
                best_start, best_len = l + 1, r - l - 1
    return s[best_start:best_start + best_len]


if __name__ == "__main__":
    print(longest_palindrome("babad"))  # bab
    print(longest_palindrome("cbbd"))   # bb
    print(longest_palindrome("a"))      # a
