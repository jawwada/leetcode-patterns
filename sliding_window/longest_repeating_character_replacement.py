"""
Longest Repeating Character Replacement (LeetCode 424)  — Medium
Pattern: Variable-size sliding window

Problem
-------
Given an uppercase string s and an integer k, you may change at most k characters. Return the
length of the longest substring that can be made of a single repeated letter.
Example: s = "AABABBA", k = 1 -> 4 (change the middle A -> "AABBBBA" contains "BBBB").

Brute force
-----------
For each start i, extend j to the right keeping a 26-count of the window; the window is
achievable iff (j - i + 1) - max(count) <= k. O(n^2 * 26) time, O(26) space. The wasted
work: after start i fails, start i+1 recounts letters we just counted, and every step
rescans 26 buckets for the max.

From brute force to optimal
---------------------------
The redundancy is recounting the same stretch for each new start. Observation: a window is
valid iff its length minus the count of its most frequent letter is <= k, and that quantity
only grows when we add a character and only shrinks when we drop one, so a two-pointer window
works: expand right, and when invalid advance left once. A second observation makes it
cleaner: max_freq need never decrease. A smaller max_freq could only yield a shorter window,
and we are after the maximum, so a stale (too large) max_freq never produces a wrong answer.
That lets the window keep its size and merely slide, with no inner shrinking loop.

Intuition
---------
The best window is one whose "minority" characters (everything except the dominant letter)
number at most k. Grow the window while that holds; when it breaks, slide instead of
shrinking, because a shorter window can never beat a length we already achieved.

Geometric view
--------------
A window [L, R] moves right. Inside it a bar chart of 26 counts; the tallest bar is the
letter we keep, the rest are the replacements. The window inflates until replacements exceed
k, then both edges move together like a rigid bar, growing again only when a new dominant
letter appears.

Steps
-----
1. count = [0]*26, left = 0, max_freq = 0, best = 0.
2. For each right: count[s[right]] += 1, max_freq = max(max_freq, that count).
3. If (right - left + 1) - max_freq > k: count[s[left]] -= 1, left += 1.
4. best = max(best, right - left + 1). Return best.

Complexity: O(n) time, O(26) space — each index enters and leaves the window at most once.
Pitfalls: Shrinking with a while loop AND recomputing max over 26 letters (correct but
slower); believing max_freq must be recomputed when left moves (it need not); using the
wrong validity test (window length - max_freq <= k).
"""


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = [0] * 26
        left = max_freq = best = 0
        for right, ch in enumerate(s):
            idx = ord(ch) - 65
            count[idx] += 1
            max_freq = max(max_freq, count[idx])   # never decreases: a stale max can't hurt
            if right - left + 1 - max_freq > k:    # more than k minority chars: slide
                count[ord(s[left]) - 65] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best


def brute_force(s: str, k: int) -> int:
    best = 0
    for i in range(len(s)):
        count = [0] * 26                           # recounted for every start
        for j in range(i, len(s)):
            count[ord(s[j]) - 65] += 1
            if (j - i + 1) - max(count) <= k:
                best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [("ABAB", 2), ("AABABBA", 1), ("AAAA", 0), ("ABCDE", 1), ("", 3)]
    assert s.characterReplacement("ABAB", 2) == 4
    assert s.characterReplacement("AABABBA", 1) == 4
    assert s.characterReplacement("AAAA", 0) == 4
    assert s.characterReplacement("ABCDE", 1) == 2
    for c in cases:
        assert s.characterReplacement(*c) == brute_force(*c)
    print("ok")
