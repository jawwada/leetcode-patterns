"""
Word Squares (LeetCode 425)  — Hard
Pattern: Prefix trie + row-by-row backtracking

Problem
-------
Given distinct words of equal length n, return every word square: a list
of n words such that the k-th row and the k-th column read the same word
(the square is symmetric). Words may be reused.
Example: ["area","lead","wall","lady","ball"] ->
[["ball","area","lead","lady"], ["wall","area","lead","lady"]].

Brute force
-----------
Try every ordered sequence of n words (with repetition) and keep those
whose matrix is symmetric. O(W^n * n^2) time (exponential), O(n) space.
The wasted work: most sequences die at the second row, because row 2 must
start with the second letter of row 1, yet the brute force still fills
all n rows and only checks symmetry at the end; and it re-filters the
whole word list for every candidate row instead of asking directly
"which words start with this prefix?".

From brute force to optimal
---------------------------
Symmetry gives a strong incremental constraint: after placing rows
0..k-1, row k must begin with the prefix formed by column k of those
rows (square[0][k] + square[1][k] + ... + square[k-1][k]). So backtrack
row by row and only try words with that prefix. The remaining cost is the
prefix query; scanning all W words per step is O(W * n). A trie answers
it: walk the prefix in O(n), and the node reached holds the indices of
every word passing through it (stored at build time), so the candidates
are read off directly. Invariant at depth k: the first k rows and first k
columns already agree, so the square can never need repair later.

Intuition
---------
Build the square one row at a time, and let the columns you have already
written dictate the next row's beginning. The trie turns "all words with
this prefix" into a pointer walk, and pruning happens as early as
possible because an impossible prefix has no trie node at all.

Geometric view
--------------
Picture the n x n grid filled from the top. After k rows, the first k
columns are fixed too (symmetry mirrors rows into columns), which fixes
the top k letters of column k, i.e. the required prefix of row k. The
trie is a branching diagram; the prefix is a path down it, and the leaves
reachable below that path are precisely the legal next rows.

Steps
-----
1. Build the trie; at every node keep a list of indices of words passing
   through it (so prefix -> candidates in O(n)).
2. backtrack(square): if len(square) == n, record a copy.
3. k = len(square); prefix = "".join(row[k] for row in square).
4. Walk the trie along prefix; if a letter is missing, return.
5. For each word index at the final node: push the word, recurse, pop.
6. Start the backtracking once with every word as row 0.

Complexity: O(W * n * 26^(n-1)) time worst case, O(W * n) space — n-1
rows each pick from at most all words sharing a prefix; the trie stores
W*n characters with an index list per node.
Pitfalls: computing the prefix from the wrong column (row index k of
each previous row); storing words only at terminal nodes (then every
prefix query needs a subtree walk); not allowing a word to be reused.
"""
from itertools import product
from typing import Dict, List


class Solution:
    def wordSquares(self, words: List[str]) -> List[List[str]]:
        n = len(words[0])
        trie: Dict = {"$": list(range(len(words)))}   # the empty prefix (row 0) matches every word
        for i, w in enumerate(words):
            node = trie
            for ch in w:
                node = node.setdefault(ch, {})
                node.setdefault("$", []).append(i)   # every word passing through this prefix

        def candidates(prefix: str) -> List[int]:
            node = trie
            for ch in prefix:
                if ch not in node:
                    return []
                node = node[ch]
            return node.get("$", [])

        squares: List[List[str]] = []
        square: List[str] = []

        def backtrack() -> None:
            k = len(square)
            if k == n:
                squares.append(square[:])
                return
            prefix = "".join(row[k] for row in square)   # column k of the rows so far
            for i in candidates(prefix):
                square.append(words[i])
                backtrack()
                square.pop()

        backtrack()
        return squares


def brute_force(words: List[str]) -> List[List[str]]:
    # Every ordered n-tuple of words (repetition allowed), symmetry checked only at the end: O(W^n * n^2).
    n = len(words[0])
    out = []
    for rows in product(words, repeat=n):
        if all(rows[r][c] == rows[c][r] for r in range(n) for c in range(n)):
            out.append(list(rows))
    return out


if __name__ == "__main__":
    s = Solution()
    cases = [(["area", "lead", "wall", "lady", "ball"],
              [["ball", "area", "lead", "lady"], ["wall", "area", "lead", "lady"]]),
             (["abat", "baba", "atan", "atal"],
              [["baba", "abat", "baba", "atal"], ["baba", "abat", "baba", "atan"]]),   # reuse of "baba"
             (["a"], [["a"]]),                                                       # 1x1 square
             (["ab", "ba", "aa"],
              [["aa", "aa"], ["aa", "ab"], ["ab", "ba"], ["ba", "aa"], ["ba", "ab"]]),
             (["abc", "def"], [])]                                                   # no square at all
    for words, want in cases:
        assert sorted(s.wordSquares(words)) == sorted(want), words
        assert sorted(brute_force(words)) == sorted(want), words
    print("ok")
