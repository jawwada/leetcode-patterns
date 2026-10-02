"""
Replace Words (LeetCode 648)  — Medium
Pattern: Trie (prefix tree)

Problem
-------
Given a dictionary of roots and a sentence, replace every word that
starts with a root by its SHORTEST such root.
Example: dictionary=["cat","bat","rat"],
sentence="the cattle was rattled by the battery"
-> "the cat was rat by the bat".

Brute force
-----------
For every word in the sentence, test every root with word.startswith(root)
and keep the shortest match. O(W * D * L) time (W words, D roots, L max
length), O(1) extra space. The repeated work is the startswith calls: a
word is compared against the first letters of every root, even though
roots that share a first letter re-read the same characters of the word,
and roots that cannot match are still tested in full.

From brute force to optimal
---------------------------
All roots can be stored once in a trie, so a word is compared against
ALL roots at the same time by walking a single path: at each character
there is exactly one edge to follow or none. The "shortest root" is simply
the FIRST node on that path that carries an end-of-word marker, so the
walk can stop as soon as one is seen; if the path breaks before reaching
any marker, no root is a prefix and the word is kept unchanged. Each word
costs O(len(word)) regardless of dictionary size. Invariant: the node
reached after i characters exists iff some root begins with word[:i].

Intuition
---------
Looking for the shortest root that is a prefix of a word is the same as
walking the word down a trie of roots and stopping at the first terminal
node. Storing roots in a trie turns "compare with each root" into "follow
one path", and shortest-first comes for free from stopping early.

Geometric view
--------------
Draw the roots as a branching diagram from a single root node with the
end markers highlighted. Each sentence word is a finger tracing its
letters from the top; the finger either hits a marked node (replace by
the letters traced so far) or falls off the diagram (keep the word).

Steps
-----
1. Insert every root into a dict-of-dicts trie; mark terminal nodes with "$".
2. For each word: node = root; for i, ch in enumerate(word):
3.   if ch not in node: keep the word (no root is a prefix); break.
4.   node = node[ch]; if "$" in node: replace with word[:i+1]; break.
5. Join the processed words with single spaces.

Complexity: O(sum of root lengths + sum of word lengths) time, O(sum of root
lengths) space — building the trie is linear in the dictionary; each word
walks at most its own length.
Pitfalls: not stopping at the first terminal (picks a longer root); testing
"$" before descending (would match the empty root); replacing with the root
when the word is shorter than the root (the walk cannot reach the marker,
so this is naturally handled).
"""
from typing import List


class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        trie: dict = {}
        for root in dictionary:
            node = trie
            for ch in root:
                node = node.setdefault(ch, {})
            node["$"] = True                    # a root ends here

        def shortest_root(word: str) -> str:
            node = trie
            for i, ch in enumerate(word):
                if ch not in node:
                    return word                 # path breaks: no root is a prefix
                node = node[ch]
                if "$" in node:
                    return word[:i + 1]         # first terminal on the path = shortest root
            return word

        return " ".join(shortest_root(w) for w in sentence.split())


def brute_force(dictionary: List[str], sentence: str) -> str:
    # For every word test every root with startswith and keep the shortest: O(W * D * L).
    out = []
    for word in sentence.split():
        best = word
        for root in dictionary:
            if word.startswith(root) and len(root) < len(best):
                best = root
        out.append(best)
    return " ".join(out)


if __name__ == "__main__":
    s = Solution()
    cases = [(["cat", "bat", "rat"], "the cattle was rattled by the battery",
              "the cat was rat by the bat"),
             (["a", "b", "c"], "aadsfasf absbs bbab cadsfafs", "a a b c"),
             (["a", "aa", "aaa", "aaaa"], "a aa a aaaa aaa aaa aaa aaaaaa bbb baba ababa",
              "a a a a a a a a bbb baba a"),
             (["catt", "cat", "bat", "rat"], "the cattle was rattled by the battery",
              "the cat was rat by the bat"),                                      # shortest wins
             (["ac", "ab"], "it is abnormal that this solution is accepted", "it is ab that this solution is ac"),
             (["xyz"], "no root matches here", "no root matches here")]
    for dictionary, sentence, want in cases:
        assert s.replaceWords(dictionary, sentence) == want, sentence
        assert brute_force(dictionary, sentence) == want, sentence
    print("ok")
