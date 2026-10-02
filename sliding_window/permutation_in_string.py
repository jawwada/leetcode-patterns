"""
Permutation in String (LeetCode 567)  — Medium
Pattern: Fixed-size sliding window with counts

Problem
-------
Return True if some permutation of s1 appears as a contiguous substring of s2.
Example: s1 = "ab", s2 = "eidbaooo" -> True ("ba"); s1 = "ab", s2 = "eidboaoo" -> False.

Brute force
-----------
For every start i in s2, take the substring of length len(s1) and compare sorted copies
(or letter counts built from scratch). O(n * k log k) time with k = len(s1), O(k) space.
The wasted work: consecutive windows share k-1 characters, yet we re-sort / re-count all k.

From brute force to optimal
---------------------------
The redundancy is rebuilding a histogram that differs from its predecessor in exactly two
cells. Observation: a permutation match is just equality of letter histograms, and sliding
the window one step means +1 for the entering letter and -1 for the leaving letter. So keep
one 26-bucket histogram for the current window and compare it to s1's histogram after each
slide. Comparing 26 ints is O(1), so the whole scan is O(n).

Intuition
---------
"Permutation of s1" means "same multiset of letters as s1". A fixed-width window over s2
has a multiset that changes by one letter in, one letter out, so track it incrementally and
check for equality.

Geometric view
--------------
A rigid window of width k slides along s2. Beside it sit two 26-bar histograms: need (s1) and
have (window). Each step one bar in `have` rises and one falls; a hit is when the two
histograms are identical.

Steps
-----
1. If len(s1) > len(s2) return False. Build need[26] from s1.
2. For i, ch in s2: have[ch] += 1; if i >= k, have[s2[i-k]] -= 1 (drop the letter leaving).
3. If have == need return True.
4. Return False after the loop.

Complexity: O(n + 26n) = O(n) time, O(26) space — one pass, constant-size histograms.
Pitfalls: Dropping the leaving character at the wrong index (i-k, not i-k+1); comparing
only when i >= k-1 but still decrementing when i >= k; not handling len(s1) > len(s2).
"""


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        k = len(s1)
        if k > len(s2):
            return False
        need = [0] * 26
        have = [0] * 26
        for ch in s1:
            need[ord(ch) - 97] += 1
        for i, ch in enumerate(s2):
            have[ord(ch) - 97] += 1
            if i >= k:                            # window too wide: drop s2[i-k]
                have[ord(s2[i - k]) - 97] -= 1
            if have == need:                      # same letter multiset = a permutation
                return True
        return False


def brute_force(s1: str, s2: str) -> bool:
    k = len(s1)
    target = sorted(s1)
    for i in range(len(s2) - k + 1):
        if sorted(s2[i:i + k]) == target:       # re-sorts k chars for every start
            return True
    return False


if __name__ == "__main__":
    s = Solution()
    cases = [("ab", "eidbaooo"), ("ab", "eidboaoo"), ("adc", "dcda"), ("abc", "ab"), ("a", "a")]
    assert s.checkInclusion("ab", "eidbaooo") is True
    assert s.checkInclusion("ab", "eidboaoo") is False
    assert s.checkInclusion("adc", "dcda") is True
    assert s.checkInclusion("abc", "ab") is False
    for c in cases:
        assert s.checkInclusion(*c) == brute_force(*c)
    print("ok")
