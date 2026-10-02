"""
Longest Palindromic Substring (LeetCode 5)  — Medium
Pattern: Expand around center

Problem
-------
Given a string s, return the longest substring that reads the same forwards and backwards. If
there are several, any one is accepted.
Example: "babad" -> "bab" (or "aba"); "cbbd" -> "bb".

Brute force
-----------
Enumerate every substring s[i:j+1] (O(n^2) of them) and check each for being a palindrome by
comparing it to its reverse (O(n)). O(n^3) time, O(1) extra space. The wasted work is in the
palindrome check: when s[i:j+1] is tested we have already tested s[i+1:j], whose answer decides
the outer one except for one extra comparison, yet we recompute it from scratch.

From brute force to optimal
---------------------------
Instead of fixing endpoints and testing inward, fix the MIDDLE and grow outward: a palindrome is
determined by its center, and extending it one step each side costs one comparison. There are
only 2n - 1 centers (n single characters for odd lengths, n - 1 gaps for even lengths). From
each center expand while s[lo] == s[hi]; the moment the characters differ, no wider palindrome
with that center exists, so stop. Every comparison either grows a palindrome or ends a center,
giving O(n^2) worst case with O(1) space and typically far less, with no table to fill.

Intuition
---------
A palindrome is symmetric around its center, so it is "mirror-grown": the longest palindrome
centered at c is the biggest radius r with s[c-r] == s[c+r]. Checking radii in increasing order
and stopping at the first mismatch is correct because a mismatch at radius r kills every
radius > r too.

Geometric view
--------------
s = b a b a d
center 1 ('a'): lo=1 hi=1 -> lo=0 hi=2 'b'=='b' -> lo=-1 stop   palindrome s[0:3] = "bab"
center between 1 and 2: s[1]='a' != s[2]='b' -> nothing
Two pointers start together (or adjacent) and walk apart symmetrically until they disagree.

Steps
-----
1. best_lo, best_len = 0, 0.
2. For each i: expand(i, i) for odd length and expand(i, i+1) for even length.
3. expand: while in bounds and s[lo] == s[hi]: lo -= 1, hi += 1. Palindrome is s[lo+1:hi].
4. If its length hi - lo - 1 beats best_len, record lo + 1 and the length.
5. Return s[best_lo : best_lo + best_len].

Complexity: O(n^2) time worst case (all-same string), O(1) extra space — 2n-1 centers, each
            expanding at most n/2 steps.
Pitfalls: forgetting even-length centers; off-by-one when the loop exits (palindrome is
          s[lo+1:hi], not s[lo:hi+1]); empty-string input.
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        best_lo, best_len = 0, 0

        def expand(lo: int, hi: int) -> None:
            nonlocal best_lo, best_len
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1
                hi += 1
            if hi - lo - 1 > best_len:             # palindrome is s[lo+1:hi]
                best_lo, best_len = lo + 1, hi - lo - 1

        for i in range(len(s)):
            expand(i, i)          # odd length, centred on s[i]
            expand(i, i + 1)      # even length, centred between s[i] and s[i+1]
        return s[best_lo:best_lo + best_len]


def brute_force(s: str) -> str:
    """Test every substring against its reverse, O(n^3)."""
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i:j + 1]
            if len(sub) > len(best) and sub == sub[::-1]:
                best = sub
    return best


if __name__ == "__main__":
    sol = Solution()
    assert sol.longestPalindrome("babad") in ("bab", "aba")
    assert sol.longestPalindrome("cbbd") == "bb"
    assert sol.longestPalindrome("a") == "a"
    assert sol.longestPalindrome("") == ""               # edge: empty
    assert sol.longestPalindrome("forgeeksskeegfor") == "geeksskeeg"
    for s in ["babad", "cbbd", "a", "ac", "aaaa", "abacdfgdcaba", "forgeeksskeegfor"]:
        assert len(sol.longestPalindrome(s)) == len(brute_force(s))
    print("ok")
