"""
Valid Palindrome (LeetCode 125)  — Easy
Pattern: Converging two pointers

Problem
-------
A phrase is a palindrome if, after lowercasing and removing every non-alphanumeric
character, it reads the same forwards and backwards. Return True if s is one.
Example: "A man, a plan, a canal: Panama" -> True ("amanaplanacanalpanama").
         "race a car" -> False.

Brute force
-----------
Build a cleaned string of lowercase alphanumerics, then compare it with its reverse
(cleaned == cleaned[::-1]). O(n) time but O(n) extra space for two copies. The
wasted work is materialising the filtered string and its full reversal when all we
need is to compare mirrored characters pairwise — most of the copy is never needed
if a mismatch appears early.

From brute force to optimal
---------------------------
The comparison cleaned == reversed checks position i against position len-1-i for
every i. We can do that directly on the original string with two indices walking
inward from both ends. The only wrinkle is the filter: when a pointer sits on a
non-alphanumeric character, advance it (the filter is applied lazily, on the fly).
Compare lowercase forms; a mismatch returns False immediately. No copies, O(1)
space, and early exit on the first mismatch.

Intuition
---------
A palindrome is symmetric about its centre, so the first character must match the
last, the second must match the second-to-last, and so on. Two pointers converging
from the ends check exactly these mirror pairs. Skipping non-alphanumerics is just
"ignore this cell and keep walking".

Geometric view
--------------
Picture the string as a row of tiles with two fingers on the outermost tiles. Each
step, both fingers slide inward over any punctuation/space tiles until they rest on
letters or digits, then compare. The fingers meet in the middle; every tile is
visited once by exactly one finger.

Steps
-----
1. left = 0, right = len(s) - 1.
2. While left < right:
3.   advance left past non-alphanumerics; retreat right past non-alphanumerics.
4.   if s[left].lower() != s[right].lower(), return False.
5.   left += 1, right -= 1.
6. Return True.

Complexity: O(n) time, O(1) space — each index is touched by one pointer once.
Pitfalls: forgetting the left < right guard inside the skip loops (can run off the
end on strings like ".,"); comparing without lowercasing; treating digits as
non-alphanumeric.
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True


def brute_force(s: str) -> bool:
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    sol = Solution()
    assert sol.isPalindrome("A man, a plan, a canal: Panama") is True
    assert sol.isPalindrome("race a car") is False
    assert sol.isPalindrome(" ") is True
    assert sol.isPalindrome(".,") is True
    assert sol.isPalindrome("0P") is False
    for case in ("A man, a plan, a canal: Panama", "race a car", " ", ".,", "0P", "ab@a"):
        assert sol.isPalindrome(case) == brute_force(case)
    print("ok")
