"""
Prefix and Suffix Search (LeetCode 745)  — Hard
Pattern: Trie over "suffix#word" rotations, max index stored per node

Problem
-------
WordFilter(words) is built once; f(pref, suff) returns the largest index
i such that words[i] starts with pref and ends with suff, or -1.
Example: words=["apple"]; f("a","e") -> 0; f("b","") -> -1.
Example: words=["cabaa","ab","ab"]; f("ab","") -> 2 (later duplicate wins).

Brute force
-----------
Store the list. For each query scan the words from the last index
backwards and return the first that satisfies startswith(pref) and
endswith(suff). O(W * L) per query, O(W * L) space. The wasted work is
that every query re-tests all W words although the set of words with a
given prefix (or suffix) never changes after construction; with up to
10^4 queries the same prefix tests are repeated thousands of times.

From brute force to optimal
---------------------------
Two prefix tries (one on words, one on reversed words) give the index
SETS for pref and for suff, but intersecting two sets per query is still
O(W). The trick is to make the pair (suff, pref) a single prefix query.
For each word, insert every string suff + "#" + word where suff ranges
over all its suffixes (including the empty one); "#" is a separator that
cannot appear in a word. Then f(pref, suff) is exactly "does the trie
contain the prefix suff + '#' + pref?" — the part before "#" pins the
suffix and the part after pins the prefix. Because we want the largest
index, each trie node stores the maximum index of any word inserted
through it, and inserting words in increasing index order makes a plain
overwrite correct. Build is O(W * L^2) once; each query is an O(L) walk.

Intuition
---------
Turn a two-sided constraint into a one-sided one by rotating the word:
"ends with e and starts with a" becomes "has prefix e#a" in the family of
strings {e#apple, le#apple, ple#apple, ...}. One trie, one walk, no set
intersection, and the answer rides along in the nodes.

Geometric view
--------------
Picture the trie as a branching diagram whose top layers spell suffixes
read forward, then a "#" rung, then layers spelling the word from its
first letter. Every word hangs from the trie L+1 times, once per
suffix. A query is a single path: down the suffix letters, through "#",
down the prefix letters; the number written on the node you stop at is
the answer, and falling off the diagram means -1.

Steps
-----
1. For each (i, word): for k in 0..len(word): key = word[k:] + "#" + word.
2. Walk/create the trie along key; set node.index = i at every node
   (later i overwrites earlier, so max is automatic).
3. f(pref, suff): walk suff + "#" + pref; return -1 on a missing edge.
4. Return the index stored at the final node.

Complexity: O(W * L^2) build, O(L) per query, O(W * L^2) space — each
word contributes L+1 keys of length up to 2L+1; a query touches at most
2L+1 nodes.
Pitfalls: storing the index only at terminal nodes (queries end
mid-path); picking a separator that can appear in words; forgetting the
empty suffix (f("ab","") must work); using min instead of max for
duplicate words.
"""
from typing import Dict, List


class WordFilter:
    def __init__(self, words: List[str]):
        self.trie: Dict = {}
        for index, word in enumerate(words):             # increasing index: overwrite == max
            for k in range(len(word) + 1):               # every suffix, including the empty one
                node = self.trie
                for ch in word[k:] + "#" + word:
                    node = node.setdefault(ch, {})
                    node["$"] = index                    # every node on the path knows its best index

    def f(self, pref: str, suff: str) -> int:
        node = self.trie
        for ch in suff + "#" + pref:                     # the pair becomes one prefix query
            if ch not in node:
                return -1
            node = node[ch]
        return node["$"]


class BruteForce:
    """Scans the whole word list from the back for each query: O(W*L) per query."""

    def __init__(self, words: List[str]):
        self.words = words

    def f(self, pref: str, suff: str) -> int:
        for i in range(len(self.words) - 1, -1, -1):
            if self.words[i].startswith(pref) and self.words[i].endswith(suff):
                return i
        return -1


if __name__ == "__main__":
    import random

    wf = WordFilter(["apple"])
    assert wf.f("a", "e") == 0
    assert wf.f("b", "") == -1
    assert wf.f("", "") == 0                             # empty prefix and suffix match everything
    assert wf.f("apple", "apple") == 0                   # prefix and suffix may overlap fully

    wf = WordFilter(["cabaa", "ab", "ab"])
    assert wf.f("ab", "") == 2                           # the later duplicate wins
    assert wf.f("c", "aa") == 0
    assert wf.f("ab", "ab") == 2
    assert wf.f("aa", "") == -1

    rng = random.Random(745)
    words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 5))) for _ in range(30)]
    fast, slow = WordFilter(words), BruteForce(words)
    for _ in range(500):
        pref = "".join(rng.choice("ab") for _ in range(rng.randint(0, 3)))
        suff = "".join(rng.choice("ab") for _ in range(rng.randint(0, 3)))
        assert fast.f(pref, suff) == slow.f(pref, suff), (pref, suff)
    print("ok")
