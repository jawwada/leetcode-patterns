---
rank: 87
slug: longest_palindromic_substring
---

Given a string, return its longest substring that reads the same forwards and backwards, the leftmost one on a tie. For `babad` the answer is `bab`; `aba` is just as long but starts later.

The brute force tests every substring, `O(n²)` of them at `O(n)` each, for cubic time. Turn the test inside out: a palindrome is symmetric about its middle, so grow palindromes outward from every possible middle instead of checking substrings one by one. A middle is either a character (odd length, like `aba`) or the gap between two neighbors (even length, like `abba`), which makes `n + (n - 1) = 2n - 1` centers. Number them so that even centers sit on characters and odd centers on gaps: center `c` starts with `left = floor(c / 2)` and `right = left + c mod 2`.

From each center, two arms swing outward in step while they land on equal characters. The moment they differ, or one runs off the string, the window just inside the arms is the longest palindrome around that center, and nothing wider around it can be one, since a wider window would contain the mismatched pair at mirror positions. Keep the longest window seen; a strict comparison leaves ties with the earlier center.

```text
s          b   a   b   a   d
index      0   1   2   3   4
center     0 1 2 3 4 5 6 7 8     even center: a char, odd center: a gap

center   (left, right)   grows to   stops at      best so far
  0         (0, 0)        "b"        left edge     "b"
  1         (0, 1)        ""         b ≠ a         "b"
  2         (1, 1)        "bab"      left edge     "bab"
  3         (1, 2)        ""         a ≠ b         "bab"
  4         (2, 2)        "aba"      b ≠ d         "bab"  (tie keeps first)
  5         (2, 3)        ""         b ≠ a         "bab"
  6         (3, 3)        "a"        b ≠ d         "bab"
  7         (3, 4)        ""         a ≠ d         "bab"
  8         (4, 4)        "d"        right edge    "bab"
```

```pseudo
FUNCTION LongestPalindrome(s)
    best_start ← 0
    best_len ← 0
    FOR center FROM 0 TO 2 * len(s) - 2
        left ← floor(center / 2)
        right ← left + center mod 2           // even: a char, odd: a gap
        WHILE left ≥ 0 AND right < len(s) AND s[left] = s[right]
            left ← left - 1                   // ends match: grow both ways
            right ← right + 1
        length ← right - left - 1             // one step past each end
        IF length > best_len                  // strict: ties keep the first
            best_start ← left + 1
            best_len ← length
    RETURN s[best_start..best_start + best_len - 1]
```

Each of the `2n - 1` centers expands at most about `n / 2` times, so the scan is `O(n²)` time in the worst case (one letter repeated) and `O(1)` extra space. Reach for it when a problem says palindromic substring: contiguous, with `n` in the low thousands. The same loop counts every palindromic substring if it adds one per successful expansion step, because each step uncovers exactly one new palindrome. Manacher's algorithm gets to `O(n)` by starting each expansion part of the way out, using the mirror image of a palindrome already found; it is rarely expected in an interview. A palindromic subsequence is not contiguous and needs dynamic programming instead. The classic mistake is expanding only around characters, which misses every even-length palindrome and returns `c` for `cbbd` instead of `bb`; the other is an off-by-one when turning the overshot arms back into a window.

*Practice:* LC 5 Longest Palindromic Substring · LC 647 Palindromic Substrings · LC 516 Longest Palindromic Subsequence
