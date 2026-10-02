"""
Minimum Window Substring (LeetCode 76)  — Hard
Pattern: Variable-size sliding window

Problem
-------
Given strings s and t, return the shortest substring of s that contains every character of t
(with multiplicity), or "" if none exists.
Example: s = "ADOBECODEBANC", t = "ABC" -> "BANC".

Brute force
-----------
For each start i, extend j to the right while counting letters until the window covers t,
record it, then move to i+1. O(n^2 * |alphabet|) time, O(|alphabet|) space. The wasted work:
start i+1 recounts letters s[i+1..j] that the previous window already counted, and every
step compares full histograms.

From brute force to optimal
---------------------------
The redundancy is recounting a stretch that is already counted. Observation: once a window
[left, right] covers t, every window with the same left and a larger right also covers t,
so right never needs to back up; and once the window stops covering t after left advances,
only growing right can fix it. Both edges therefore move monotonically. To make "covers t"
an O(1) check, keep need[ch] (positive = still required, negative = surplus) and a single
counter `missing` = total characters still required; the window covers t iff missing == 0.

Intuition
---------
Expand right until the window is a valid cover, then shrink left as far as possible while
it stays valid (the left end is then a required character). Record the length, evict that
left character to break validity, and continue expanding right.

Geometric view
--------------
Two pointers on s. R races ahead until the window holds all of t; L then creeps right,
discarding surplus letters, until it rests on a letter that is needed. Snapshot the
interval, nudge L one more step (breaking coverage), and let R run again. The recorded
intervals are the candidate windows; the shortest wins.

Steps
-----
1. need = Counter(t); missing = len(t); left = 0; best = (start 0, length inf).
2. For each right, ch: if need[ch] > 0, missing -= 1. Then need[ch] -= 1.
3. While missing == 0: shrink left over chars with need < 0 (surplus), restoring their counts.
4. Record the window if shorter. Then evict s[left] (need += 1, missing += 1, left += 1).
5. Return the best window or "".

Complexity: O(|s| + |t|) time, O(|alphabet|) space — each pointer traverses s once.
Pitfalls: Decrementing missing for surplus characters (only when need[ch] > 0); forgetting
that need[] goes negative to encode surplus; returning the window before shrinking.
"""
from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)
        missing = len(t)                     # chars of t still not in the window
        left = 0
        best_start, best_len = 0, float("inf")
        for right, ch in enumerate(s):
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1                    # negative count = surplus copies
            if missing == 0:                 # window covers t: shrink the left edge
                while need[s[left]] < 0:
                    need[s[left]] += 1
                    left += 1
                if right - left + 1 < best_len:
                    best_start, best_len = left, right - left + 1
                need[s[left]] += 1           # evict a required char so right must grow again
                missing += 1
                left += 1
        return "" if best_len == float("inf") else s[best_start:best_start + best_len]


def brute_force(s: str, t: str) -> str:
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have = Counter()                                 # recounted for every start
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= need[c] for c in need):
                if not best or j - i + 1 < len(best):
                    best = s[i:j + 1]
                break
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [("ADOBECODEBANC", "ABC"), ("a", "a"), ("a", "aa"), ("ab", "b"), ("aabbcc", "abc")]
    assert s.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert s.minWindow("a", "a") == "a"
    assert s.minWindow("a", "aa") == ""
    assert s.minWindow("ab", "b") == "b"
    for c in cases:
        assert s.minWindow(*c) == brute_force(*c)
    print("ok")
