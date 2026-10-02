"""
Partition Labels (LeetCode 763)  — Medium
Pattern: Greedy interval merging by last occurrence

Problem
-------
Partition the string `s` into as many parts as possible so that each letter appears in at most
one part; return the part sizes in order.
Example: s = "ababcbacadefegdehijhklij" -> [9,7,8] ("ababcbaca", "defegde", "hijhklij").

Brute force
-----------
Grow the current part one character at a time; after each extension, scan the remainder of the
string to check whether any letter in the current part appears later. If none does, cut.
O(n^2) time, O(26) space. The wasted work: rescanning the suffix for each letter at every
position, when "where does this letter last appear?" is a fixed fact we could precompute once.

From brute force to optimal
---------------------------
The redundancy is repeated suffix scans. Observation: a part that starts at i cannot end before
last[c] for every letter c inside it, where last[c] is the final index of c in s. So each letter
defines an interval [first, last]; parts are exactly the merged unions of overlapping intervals.
Precompute last[] in one pass; then sweep with `end = max(end, last[s[i]])` and cut whenever
i == end. Two linear passes, constant extra memory.

Intuition
---------
Every letter owns a span from its first to its last occurrence. A part must swallow the entire
span of every letter it touches. Sweep left to right, keep pushing the required end rightwards;
when the sweep catches up with the required end, nothing inside points further — cut.

Geometric view
--------------
Draw each letter's span as a horizontal bar. Overlapping bars chain into one block; a cut goes
where no bar crosses.

    s:    a b a b c b a c a | d e f e g d e | h i j h k l i j
    a:    [---------------]
    b:      [-------]
    c:          [-----]
    d:                      [---------]
    e:                        [-------]
    i reaches end=8 -> cut 9; end=15 -> cut 7; end=23 -> cut 8

Steps
-----
1. last = {c: i for i, c in enumerate(s)}.
2. start = end = 0; for i, c: end = max(end, last[c]).
3. If i == end: append end - start + 1; start = i + 1.
4. Return the sizes.

Complexity: O(n) time, O(1) space — two passes; the map has at most 26 keys.
Pitfalls: cutting when i >= end before updating end with the current letter; forgetting to reset
start; producing indices instead of sizes.
"""
from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last = {c: i for i, c in enumerate(s)}   # final index of every letter
        sizes = []
        start = end = 0
        for i, c in enumerate(s):
            end = max(end, last[c])          # the part must stretch to cover c's last occurrence
            if i == end:                     # nothing inside points further right: cut here
                sizes.append(end - start + 1)
                start = i + 1
        return sizes


def brute_force(s: str) -> List[int]:
    sizes, start = [], 0
    for i in range(len(s)):
        part = set(s[start:i + 1])
        if not any(ch in part for ch in s[i + 1:]):   # rescan the suffix every step
            sizes.append(i - start + 1)
            start = i + 1
    return sizes


if __name__ == "__main__":
    s = Solution()
    cases = [
        ("ababcbacadefegdehijhklij", [9, 7, 8]),
        ("eccbbbbdec", [10]),
        ("abc", [1, 1, 1]),
        ("a", [1]),
        ("abca", [4]),
    ]
    for string, want in cases:
        assert s.partitionLabels(string) == want
        assert brute_force(string) == want
    print("ok")
