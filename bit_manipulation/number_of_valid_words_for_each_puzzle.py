"""
Number of Valid Words for Each Puzzle (LeetCode 1178)  — Hard
Pattern: Bitmask counting + submask enumeration

Problem
-------
A word is valid for a puzzle if it contains the puzzle's first letter and every letter of the
word appears in the puzzle. Puzzles have exactly 7 distinct letters; there are up to 10^5 words
and 10^4 puzzles. Return, for each puzzle, how many words are valid for it.
Example: words = ["aaaa","asas","able","ability","actt","actor","access"],
         puzzles = ["aboveyz","abrodyz","abslute","absoryz","actresz","gaswxyz"] -> [1,1,3,2,4,0]
         ("aboveyz": only "aaaa"; "actresz": "aaaa", "asas", "actt", "access").

Brute force
-----------
For each puzzle and each word, check set(word) <= set(puzzle) and puzzle[0] in word.
O(P * W * L) time with L = word length — 10^9 * L character operations. The waste: words are
compared by their letter SET only, and many words share the same set, yet every word is
re-examined for every puzzle; and each check scans all letters although a puzzle has just 7.

From brute force to optimal
---------------------------
Step 1 (collapse words to masks): a word's validity depends only on which letters it has, so
map each word to a 26-bit mask and count how many words share each mask — the 10^5 words
collapse into at most ~10^5 (usually far fewer) distinct masks and are never looked at again.
Step 2 (enumerate the puzzle side, not the word side): word mask w is valid for puzzle mask p
iff w is a SUBSET of p (w & ~p == 0) and w contains the first letter's bit. A 7-letter puzzle
has only 2^7 = 128 submasks, so instead of testing every word mask against p, enumerate the
submasks of p that include the first bit (64 of them) and sum their counts from the hash map.
The standard trick sub = (sub - 1) & p walks all submasks in decreasing order. Total
O(W * L + P * 128).

Intuition
---------
The condition "every letter of the word is in the puzzle" is a subset relation, and subset
relations on small sets are cheap to enumerate from the superset side. Flip the loop: a puzzle
asks "how many words have one of my 64 allowed letter-sets?" and a counter answers each in O(1).

Geometric view
--------------
Write letters as 26 binary columns. A puzzle is a row with seven 1s; its valid words are rows
whose 1s all sit under the puzzle's 1s, with the first-letter column forced to 1. Fixing that
column leaves six free columns = 64 patterns, so the puzzle's answer is the sum of the counter
over 64 specific rows — a hypercube of dimension 6 whose vertices you visit via (sub-1) & p.

Steps
-----
1. cnt = Counter(mask(word) for word in words), mask = OR of 1 << (ord(c) - 97).
2. For each puzzle: p = mask(puzzle), first = 1 << (puzzle[0] - 'a').
3. sub = p; loop: if sub & first: total += cnt[sub]; if sub == 0 break; sub = (sub - 1) & p.
4. Append total.

Complexity: O(W * L + P * 2^7) time, O(W) space for the mask counter.
Pitfalls: enumerating submasks of the WORD side (26 bits, too many); forgetting the first-letter
requirement; off-by-one in the submask loop (must process sub = p and stop after sub = 0).
"""
from collections import Counter
from typing import List


class Solution:
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
        def mask(s: str) -> int:
            m = 0
            for c in s:
                m |= 1 << (ord(c) - 97)
            return m

        cnt = Counter(mask(w) for w in words)        # words collapse to letter-set masks
        ans = []
        for puzzle in puzzles:
            p, first = mask(puzzle), 1 << (ord(puzzle[0]) - 97)
            total, sub = 0, p
            while True:                              # all 2^7 submasks of p, descending
                if sub & first:                      # must contain the first letter
                    total += cnt[sub]
                if sub == 0:
                    break
                sub = (sub - 1) & p                  # next smaller submask
            ans.append(total)
        return ans


def brute_force(words: List[str], puzzles: List[str]) -> List[int]:
    ans = []
    for puzzle in puzzles:
        allowed = set(puzzle)
        ans.append(sum(1 for w in words                # rescan every word per puzzle
                       if puzzle[0] in w and set(w) <= allowed))
    return ans


if __name__ == "__main__":
    s = Solution()
    words = ["aaaa", "asas", "able", "ability", "actt", "actor", "access"]
    puzzles = ["aboveyz", "abrodyz", "abslute", "absoryz", "actresz", "gaswxyz"]
    assert s.findNumOfValidWords(words, puzzles) == [1, 1, 3, 2, 4, 0]
    assert s.findNumOfValidWords(words, puzzles) == brute_force(words, puzzles)
    assert s.findNumOfValidWords(["apple", "pleas", "please"],
                                 ["aelwxyz", "aelpxyz", "aelpsxy", "saelpxy", "xaelpsy"]) \
        == [0, 1, 3, 2, 0]
    assert s.findNumOfValidWords(["a"], ["abcdefg"]) == [1]              # one-letter word
    assert s.findNumOfValidWords(["b"], ["abcdefg"]) == [0]              # lacks first letter
    print("ok")
