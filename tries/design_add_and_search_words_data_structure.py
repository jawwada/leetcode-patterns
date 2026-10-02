"""
Design Add and Search Words Data Structure (LeetCode 211)  — Medium
Pattern: Trie with wildcard DFS

Problem
-------
Design WordDictionary with addWord(word) and search(word) -> bool, where
the search pattern may contain '.' matching any single letter.
Example: add "bad","dad","mad"; search("pad") -> False; search("bad") ->
True; search(".ad") -> True; search("b..") -> True.

Brute force
-----------
Store the words in a list. search compares the pattern against every
stored word character by character, treating '.' as a free match.
O(1) add, O(N * L) per search. The repeated work: every word is checked
in full against the pattern, even though many words share long prefixes
and could be rejected (or accepted) as a group after one comparison.

From brute force to optimal
---------------------------
A trie stores shared prefixes once, so a literal character in the pattern
is one dictionary lookup that discards every word not continuing with
that letter, all at once. The wildcard is the only place where several
branches remain viable, and there the search must try each child: a DFS
over (trie node, pattern index) that branches only at '.'. A literal
mismatch prunes the whole subtree immediately. The "$" end marker again
distinguishes a full word from a prefix. Invariant: dfs(node, i) is True
iff some word in node's subtree spells pattern[i:].

Intuition
---------
Literal characters follow exactly one edge; a dot fans out over all
edges. Because literals dominate most patterns, the fan-out is usually
small, and the search touches only the part of the trie consistent with
the pattern so far.

Geometric view
--------------
Picture the trie as a branching diagram and the pattern as a path
description. Literal letters lock you onto one branch; each '.' is a fork
where you send a scout down every branch and succeed if any scout reaches
a word-end exactly when the pattern runs out.

Steps
-----
1. addWord: standard trie insert, mark the last node with "$".
2. search: dfs(node, i): if i == len(word) return "$" in node.
3. ch = word[i]; if ch != '.': return ch in node and dfs(node[ch], i+1).
4. Else: return any(dfs(child, i+1) for every child key except "$").

Complexity: O(L) per add; search O(L) for literal patterns, up to
O(26^d * L) with d dots in the worst case (bounded by trie size), space
O(total characters).
Pitfalls: recursing into the "$" marker as if it were a child; matching
"..." against a longer word (length must match exactly); returning True at
a prefix node that is not a word end.
"""
from typing import List


class WordDictionary:
    def __init__(self):
        self.root: dict = {}          # char -> child dict; "$" marks the end of a word

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        def dfs(node: dict, i: int) -> bool:
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch != ".":
                return ch in node and dfs(node[ch], i + 1)
            # wildcard: branch into every real child (skip the end marker)
            return any(dfs(child, i + 1) for key, child in node.items() if key != "$")

        return dfs(self.root, 0)


class BruteForce:
    # Keep a list; every search compares the pattern against every stored word.
    def __init__(self):
        self.words: List[str] = []

    def addWord(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        def matches(w: str) -> bool:
            return len(w) == len(word) and all(p == "." or p == c for p, c in zip(word, w))

        return any(matches(w) for w in self.words)


if __name__ == "__main__":
    for cls in (WordDictionary, BruteForce):
        d = cls()
        assert d.search("a") is False and d.search(".") is False
        for w in ("bad", "dad", "mad"):
            d.addWord(w)
        assert d.search("pad") is False
        assert d.search("bad") is True
        assert d.search(".ad") is True
        assert d.search("b..") is True
        assert d.search("...") is True
        assert d.search("....") is False      # length must match
        assert d.search("ba") is False        # prefix is not a word
        assert d.search("..d") is True and d.search("..x") is False
    print("ok")
