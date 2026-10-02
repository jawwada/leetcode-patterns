"""
Palindrome Pairs (LeetCode 336)  — Hard
Pattern: Hash map of reversed words + prefix/suffix palindrome split

Problem
-------
Given distinct words, return all index pairs (i, j), i != j, such that words[i] + words[j] is a
palindrome. Example: ["abcd","dcba","lls","s","sssll"] -> [[0,1],[1,0],[3,2],[2,4]]
("abcddcba", "dcbaabcd", "slls", "llssssll"). ["a",""] -> [[0,1],[1,0]].

Brute force
-----------
Try every ordered pair (i, j), build words[i] + words[j], and test it against its reverse.
O(n^2 * L) time where L is the word length, O(L) space. The wasted work: for a fixed words[i]
the test against each of the n-1 partners re-reads words[i] from scratch, and almost all
partners fail at the very first character comparison; nothing learned about words[i] is reused.

From brute force to optimal
---------------------------
The redundancy is scanning n partners per word. Observation: if w + x is a palindrome and
|w| >= |x|, then x read backwards must equal a PREFIX of w, and the leftover middle of w must
itself be a palindrome; symmetrically if |w| < |x|, rev(w) is a suffix of x. So the partner is
determined by w alone: split w = pre + suf at each of the |w|+1 cut points; if suf is a
palindrome the partner is rev(pre) (placed after w); if pre is a palindrome the partner is
rev(suf) (placed before w). The structure that answers "does rev(pre) exist and where?" in O(1)
is a hash map from reversed word -> index. Total work drops from O(n^2 L) to O(n L^2):
n words, L+1 cuts, O(L) palindrome test each.

Intuition
---------
A palindrome concatenation has the shorter word mirrored at the far end of the longer one. So
walk the cut point along the longer word: one side must be a palindrome (the middle), and the
other side's reverse must be a whole word in the list. The map tells you instantly whether that
reverse exists. Skipping the "suf is empty" case for the second rule prevents reporting the
equal-length pair twice (it is already found from the other word with an empty prefix).

Geometric view
--------------
   w = [ pre | suf ]      partner before w: rev(suf) + pre + suf  needs pre palindrome
                          partner after  w: pre + suf + rev(pre)  needs suf palindrome
Slide a cut bar across w; at each stop one half is the mirror seam and the other half must
reflect exactly onto some word in the dictionary.

Steps
-----
1. where = {rev(word): index for every word}.
2. For each word w at i and each cut j in 0..len(w): pre, suf = w[:j], w[j:].
3. If pre is a palindrome and suf in where (and not i): add [where[suf], i].
4. If j < len(w) and suf is a palindrome and pre in where (and not i): add [i, where[pre]].
5. Return the collected pairs.

Complexity: O(n * L^2) time, O(n * L) space — L+1 cuts per word, O(L) palindrome test, one
map entry per word.
Pitfalls: duplicate pairs when both words are full reverses of each other (guard j < len(w)
for the suffix rule); pairing a word with itself (where[...] == i); the empty string must pair
with every palindromic word in both orders.
"""
from typing import List


class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        where = {w[::-1]: i for i, w in enumerate(words)}   # reversed word -> its index
        res = []
        for i, w in enumerate(words):
            for j in range(len(w) + 1):                      # w = pre + suf
                pre, suf = w[:j], w[j:]
                # pre is a palindrome: rev(suf) + pre + suf reads the same both ways
                if pre == pre[::-1] and suf in where and where[suf] != i:
                    res.append([where[suf], i])
                # suf is a palindrome: pre + suf + rev(pre); j < len(w) skips the duplicate
                if j < len(w) and suf == suf[::-1] and pre in where and where[pre] != i:
                    res.append([i, where[pre]])
        return res


def brute_force(words: List[str]) -> List[List[int]]:
    res = []
    for i, a in enumerate(words):
        for j, b in enumerate(words):                        # every ordered pair
            if i != j and (a + b) == (a + b)[::-1]:
                res.append([i, j])
    return res


if __name__ == "__main__":
    s = Solution()
    same = lambda a, b: sorted(map(tuple, a)) == sorted(map(tuple, b))
    assert same(s.palindromePairs(["abcd", "dcba", "lls", "s", "sssll"]),
                [[0, 1], [1, 0], [3, 2], [2, 4]])
    assert same(s.palindromePairs(["bat", "tab", "cat"]), [[0, 1], [1, 0]])
    assert same(s.palindromePairs(["a", ""]), [[0, 1], [1, 0]])
    assert s.palindromePairs(["abc"]) == []
    import random
    random.seed(2)
    for _ in range(200):
        pool = {"".join(random.choice("ab") for _ in range(random.randint(0, 4)))
                for _ in range(random.randint(1, 7))}
        ws = list(pool)
        assert same(s.palindromePairs(ws), brute_force(ws)), ws
    print("ok")
