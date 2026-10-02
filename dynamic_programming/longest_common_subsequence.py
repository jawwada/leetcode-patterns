"""
Longest Common Subsequence (LeetCode 1143)  — Medium
Pattern: 2-D DP over two prefixes

Problem
-------
Given strings text1 and text2, return the length of their longest common subsequence: a
sequence of characters appearing in both, in order, not necessarily contiguously.
Example: "abcde", "ace" -> 3 ("ace").  "abc", "def" -> 0.

Brute force
-----------
Recursion on prefix lengths: lcs(i, j) = 1 + lcs(i-1, j-1) if text1[i-1] == text2[j-1],
else max(lcs(i-1, j), lcs(i, j-1)); lcs(0, *) = lcs(*, 0) = 0. On mismatches it
branches twice, so the tree has up to 2^(m+n) nodes: exponential time, O(m+n) stack.
The waste: lcs(i-1, j-1) is reached from both lcs(i-1, j) and lcs(i, j-1), and so on all
the way down.

From brute force to optimal
---------------------------
Overlapping subproblems: lcs(i, j) depends only on the pair of prefix lengths, so there
are only (m+1)(n+1) distinct subproblems (the user's original memo dict cached these).
State: dp[i][j] = LCS length of text1[:i] and text2[:j].
Recurrence: dp[i][j] = dp[i-1][j-1] + 1 if the last chars match,
else max(dp[i-1][j], dp[i][j-1]).
Order: rows i = 1..m top to bottom, columns j = 1..n left to right, so up, left and
up-left are ready. Space reduction: each row reads only the previous row, so keep two
rows (iterate the shorter string as columns). O(m*n) time, O(min(m, n)) space.

Intuition
---------
Look at the last character of each prefix. If they match, that character can safely end
the LCS, so take it and shrink both. If not, at least one of them is unused, so drop one
or the other and keep the better result.

Geometric view
--------------
Draw a grid with text1 down the side and text2 across the top. Each cell looks up, left,
or diagonally up-left. Matches are diagonal steps that add 1; the answer sits in the
bottom-right corner, and the LCS itself is a staircase path of diagonal moves.

Steps
-----
1. If text2 is longer, swap so columns are the shorter string.
2. prev = [0] * (n + 1).
3. For each char a of text1: cur[0] = 0; for j: cur[j] = prev[j-1] + 1 if a == text2[j-1]
   else max(prev[j], cur[j-1]). Then prev = cur.
4. Return prev[n].

Complexity: O(m*n) time, O(min(m, n)) space — every cell once, two rows kept.
Pitfalls: confusing subsequence with substring (substring resets to 0 on mismatch);
overwriting the diagonal value when using a single row; off-by-one between prefix length
and character index.
"""


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if len(text2) > len(text1):
            text1, text2 = text2, text1  # columns = shorter string
        prev = [0] * (len(text2) + 1)
        for a in text1:
            cur = [0] * (len(text2) + 1)
            for j, b in enumerate(text2, 1):
                cur[j] = prev[j - 1] + 1 if a == b else max(prev[j], cur[j - 1])
            prev = cur
        return prev[-1]


def brute_force(text1: str, text2: str) -> int:
    # Match-or-drop-one recursion on the last characters: exponential.
    def lcs(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        if text1[i - 1] == text2[j - 1]:
            return 1 + lcs(i - 1, j - 1)
        return max(lcs(i - 1, j), lcs(i, j - 1))

    return lcs(len(text1), len(text2))


if __name__ == "__main__":
    s = Solution()
    cases = [("abcde", "ace", 3), ("abc", "abc", 3), ("abc", "def", 0),
             ("a", "a", 1), ("bsbininm", "jmjkbkjkv", 1), ("ezupkr", "ubmrapg", 2)]
    for t1, t2, want in cases:
        assert s.longestCommonSubsequence(t1, t2) == want
        assert brute_force(t1, t2) == want
    print("ok")
