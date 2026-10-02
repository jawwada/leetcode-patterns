"""
Substring with Concatenation of All Words (LeetCode 30)  — Hard
Pattern: Word-sized sliding window, one pass per offset

Problem
-------
Given a string s and a list words of equal-length strings (duplicates allowed), return the
start indices of every substring of s that is a concatenation of all the words in any order,
each used exactly once.
Example: s = "barfoothefoobarman", words = ["foo","bar"] -> [0, 9] ("barfoo", "foobar").

Brute force
-----------
Let L = len(word), m = len(words). For every start i (n - mL + 1 of them) slice the next m
chunks of length L, count them, and compare with the word multiset. O(n * m * L) time,
O(m) space. The wasted work is that start i and start i + L share m - 1 of their m chunks,
yet both counts are rebuilt from scratch.

From brute force to optimal
---------------------------
Starts that differ by a multiple of L look at the same chunk boundaries, so group the
starts into L residue classes (offsets 0..L-1). Within one offset, the substring is a
sequence of fixed chunks and the problem becomes "find windows of exactly m consecutive
chunks whose multiset equals words" — a classic counting sliding window over the chunk
sequence. Maintain a count map of chunks inside the window. When the right chunk is not a
word, reset the window after it. When it is a word, add it; while it is now over-counted,
drop chunks from the left. When the window holds exactly m chunks, record its start and
shift the left edge by one chunk. Each chunk is added and removed once per offset, and each
offset scans n/L chunks, so the total is O(L * n/L * L) = O(n * L) for slicing/hashing,
independent of m.

Intuition
---------
Fixed-length words mean the only freedom is where the chunk grid is anchored. Once the grid
is fixed, the question "is this run of m chunks a permutation of words?" is the anagram-of-
multiset check, and multiset-equality windows can be slid by removing one chunk and adding
one chunk. A non-word chunk is a hard wall that no valid window can cross.

Geometric view
--------------
Draw s as a ruler with ticks every L characters, once for each of the L possible phases.
On each ruler slide a window of up to m tiles. Tiles in the window are tinted by count;
a tile that would make a word over-counted pushes the left edge right until that word is
back in budget, and a tile that is not a word at all cuts the ruler and the window
restarts after it.

Steps
-----
1. L = len(words[0]), m = len(words), need = Counter(words).
2. For each offset in range(L): left = offset, have = Counter(), count = 0.
3.   For right from offset to n - L step L: w = s[right:right+L].
4.     If w not in need: clear have, count = 0, left = right + L; continue.
5.     have[w] += 1; count += 1; while have[w] > need[w]: remove s[left:left+L], left += L.
6.     If count == m: record left; remove s[left:left+L], left += L, count -= 1.
7. Return the recorded starts.

Complexity: O(n * L) time, O(m * L) space — L offsets, each scanning n/L chunks at O(L) per slice.
Pitfalls: looping over all n starts instead of L offsets (that is the brute force again);
not resetting the window on a non-word chunk; forgetting that words can repeat, so a plain
set is wrong; off-by-one on the last chunk start (right <= n - L).
"""
from collections import Counter
from typing import List


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not words or not s:
            return []
        L, m, n = len(words[0]), len(words), len(s)
        need = Counter(words)
        result = []
        for offset in range(L):
            have = Counter()
            left = offset
            count = 0                         # chunks currently in the window
            for right in range(offset, n - L + 1, L):
                w = s[right:right + L]
                if w not in need:             # wall: no valid window spans it
                    have.clear()
                    count = 0
                    left = right + L
                    continue
                have[w] += 1
                count += 1
                while have[w] > need[w]:      # shrink until w is back in budget
                    have[s[left:left + L]] -= 1
                    count -= 1
                    left += L
                if count == m:
                    result.append(left)
                    have[s[left:left + L]] -= 1
                    count -= 1
                    left += L
        return result


def brute_force(s: str, words: List[str]) -> List[int]:
    if not words:
        return []
    L, m = len(words[0]), len(words)
    need = Counter(words)
    result = []
    for i in range(len(s) - m * L + 1):
        chunks = Counter(s[j:j + L] for j in range(i, i + m * L, L))
        if chunks == need:
            result.append(i)
    return result


if __name__ == "__main__":
    s = Solution()
    assert s.findSubstring("barfoothefoobarman", ["foo", "bar"]) == [0, 9]
    assert s.findSubstring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]) == []
    assert sorted(s.findSubstring("barfoofoobarthefoobarman", ["bar", "foo", "the"])) == [6, 9, 12]
    assert sorted(s.findSubstring("aaaaaa", ["aa", "aa"])) == [0, 1, 2]
    assert s.findSubstring("a", ["aa"]) == []
    import random
    random.seed(30)
    cases = [("barfoothefoobarman", ["foo", "bar"]), ("aaaaaa", ["aa", "aa"]),
             ("barfoofoobarthefoobarman", ["bar", "foo", "the"])]
    for _ in range(200):
        L = random.randint(1, 3)
        vocab = ["".join(random.choice("ab") for _ in range(L)) for _ in range(3)]
        words = [random.choice(vocab) for _ in range(random.randint(1, 3))]
        text = "".join(random.choice("ab") for _ in range(random.randint(1, 15)))
        cases.append((text, words))
    for text, words in cases:
        assert sorted(s.findSubstring(text, words)) == sorted(brute_force(text, words))
    print("ok")
