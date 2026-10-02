"""
Valid Anagram (LeetCode 242)  — Easy
Pattern: Fixed-alphabet frequency count

Problem
-------
Given two lowercase strings s and t, return True if t is an anagram of s: the same letters with
the same multiplicities in any order.
Example: s = "anagram", t = "nagaram" -> True; s = "rat", t = "car" -> False.

Brute force
-----------
Sort both strings and compare: sorted(s) == sorted(t). O(n log n) time, O(n) space for the
sorted copies. The wasted work is the sort itself: we impose a total ORDER on the letters when
the question only cares about how many of each letter there are. Ordering 26 symbols is far
more information than a multiset comparison needs.

From brute force to optimal
---------------------------
Two strings are anagrams iff every letter appears the same number of times in both. The
alphabet is fixed (26 lowercase letters), so a frequency table is a 26-cell array, not a
hash map, and filling it is one linear pass. Walk both strings together: +1 for the letter from
s, -1 for the letter from t; they are anagrams iff every cell ends at zero. A length check up
front rejects the trivial mismatch before counting.

Intuition
---------
Anagram = same histogram. Build one histogram as a difference (s adds, t subtracts) so the
answer is "is everything zero", and no second table or second pass is needed.

Geometric view
--------------
26 buckets as columns. Each letter of s pushes its column up by one, each letter of t pulls it
down by one. If at the end the skyline is flat at zero, the two strings are anagrams; any
column above or below zero is a letter one string has more of.

Steps
-----
1. If len(s) != len(t): return False.
2. count = [0] * 26.
3. For a, b in zip(s, t): count[a] += 1; count[b] -= 1.
4. Return not any(count).

Complexity: O(n) time, O(1) space — a single pass over a fixed 26-cell array.
Pitfalls: skipping the length check (zip truncates silently); using sorted() and calling it
          O(n); unicode input (switch to a dict of counts).
"""


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        count = [0] * 26
        for a, b in zip(s, t):
            count[ord(a) - 97] += 1      # s adds to the histogram
            count[ord(b) - 97] -= 1      # t subtracts from it
        return not any(count)


def brute_force(s: str, t: str) -> bool:
    """Sort both strings and compare, O(n log n)."""
    return sorted(s) == sorted(t)


if __name__ == "__main__":
    sol = Solution()
    assert sol.isAnagram("anagram", "nagaram") is True
    assert sol.isAnagram("rat", "car") is False
    assert sol.isAnagram("a", "ab") is False         # edge: different lengths
    assert sol.isAnagram("", "") is True             # edge: empty strings
    for s, t in [("anagram", "nagaram"), ("rat", "car"), ("aabb", "abab"), ("aabb", "aabc"), ("a", "ab")]:
        assert sol.isAnagram(s, t) == brute_force(s, t)
    print("ok")
