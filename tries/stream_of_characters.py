"""
Stream of Characters (LeetCode 1032)  — Hard
Pattern: Reversed trie walked backwards over a bounded recent-history buffer

Problem
-------
StreamChecker(words) is fed one character at a time via query(letter),
which must return True when some word in the list is a suffix of
everything queried so far.
Example: words=["cd","f","kl"]; stream a b c d e f g h i j k l ->
query returns False False False True False True False False False
False False True (at d "cd" ends, at f "f" ends, at l "kl" ends).

Brute force
-----------
Append the letter to a growing string and test stream.endswith(w) for
every word. O(W * L) per query where L is the longest word, O(stream)
space. The wasted work is twofold: every query re-examines all W words
independently even though most cannot match the latest letter at all,
and the stream is kept forever although only the last L characters can
ever be part of a match.

From brute force to optimal
---------------------------
Bound the memory first: a word of length <= L can only match the last L
letters, so keep a deque of at most L recent characters and the space
becomes O(L). Then collapse the W independent endswith checks: a word is
a suffix of the stream iff the stream read BACKWARDS from its last letter
spells the word reversed. Insert every word reversed into a trie; a query
walks the trie from the root while reading the deque newest-to-oldest.
All W words are checked simultaneously because the walk follows exactly
the characters present, and it stops as soon as a trie node has no
matching child, or as soon as a terminal marker is found. Worst case per
query is O(L) steps instead of O(W * L). Invariant: after k backward
steps, the trie node reached corresponds to the last k stream letters,
reversed.

Intuition
---------
Suffix matching is prefix matching on the reversed string. Reverse the
dictionary once, and the newest character is always the first letter of
the thing being matched, so a trie rooted at "most recent letter" lets
one backward walk test every word at the same time.

Geometric view
--------------
Draw the reversed trie branching from a root and a tape of the last L
stream letters with its head at the newest letter. Each query lays the
tape against the trie: step one letter older, one edge deeper. The walk
either falls off the trie (no word ends here) or lands on a marked node
(a word ends here); it never needs to look further back than the deepest
leaf.

Steps
-----
1. Build the trie from each word reversed; mark the end node with "$".
   Record L = max word length.
2. query(letter): append to the deque; drop the oldest if len > L.
3. node = root; for ch in reversed(deque): if ch not in node return False;
   node = node[ch]; if "$" in node return True.
4. Return False when the deque is exhausted.

Complexity: O(L) per query, O(sum of word lengths + L) space — one
backward walk bounded by the longest word; the trie stores every
character once and the buffer holds L letters.
Pitfalls: building the trie forward (prefix instead of suffix); storing
the whole stream; not stopping at the first terminal node (a shorter
word may match before a longer walk fails); forgetting to bound the
deque so a long stream makes the walk slow.
"""
from collections import deque
from typing import Deque, Dict, List


class StreamChecker:
    def __init__(self, words: List[str]):
        self.trie: Dict = {}
        self.max_len = 0
        for w in words:
            node = self.trie
            for ch in reversed(w):                 # reversed: the newest stream letter is matched first
                node = node.setdefault(ch, {})
            node["$"] = True
            self.max_len = max(self.max_len, len(w))
        self.recent: Deque[str] = deque()          # only the last max_len letters can matter

    def query(self, letter: str) -> bool:
        self.recent.append(letter)
        if len(self.recent) > self.max_len:
            self.recent.popleft()
        node = self.trie
        for ch in reversed(self.recent):           # walk newest -> oldest, one trie edge per letter
            if ch not in node:
                return False
            node = node[ch]
            if "$" in node:
                return True
        return False


class BruteForce:
    """Keeps the whole stream and tests endswith for every word on each query: O(W*L) per query."""

    def __init__(self, words: List[str]):
        self.words = words
        self.stream = ""

    def query(self, letter: str) -> bool:
        self.stream += letter
        return any(self.stream.endswith(w) for w in self.words)


if __name__ == "__main__":
    import random

    sc = StreamChecker(["cd", "f", "kl"])
    got = [sc.query(c) for c in "abcdefghijkl"]
    assert got == [False, False, False, True, False, True, False, False, False, False, False, True], got

    sc = StreamChecker(["ab", "ba", "aaab", "abab", "baa"])
    got = [sc.query(c) for c in "aabaaabaaa"]
    assert got == [False, False, True, True, True, False, True, True, True, False], got

    sc = StreamChecker(["a"])                     # single-letter word, every 'a' fires
    assert [sc.query(c) for c in "bab"] == [False, True, False]

    sc = StreamChecker(["abc"])                   # a prefix of a word is not a match
    assert [sc.query(c) for c in "ab"] == [False, False]

    rng = random.Random(1032)
    words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 4))) for _ in range(8)]
    fast, slow = StreamChecker(words), BruteForce(words)
    for _ in range(500):
        c = rng.choice("abc")
        assert fast.query(c) == slow.query(c), (words, c)
    print("ok")
