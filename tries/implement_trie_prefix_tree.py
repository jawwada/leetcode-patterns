"""
Implement Trie (Prefix Tree) (LeetCode 208)  — Medium
Pattern: Trie (prefix tree)

Problem
-------
Design a Trie with insert(word), search(word) -> bool (exact word present)
and startsWith(prefix) -> bool (some inserted word begins with prefix).
Example: insert("apple"); search("apple") -> True; search("app") -> False;
startsWith("app") -> True; insert("app"); search("app") -> True.

Brute force
-----------
Keep the inserted words in a list. search scans the list comparing whole
strings; startsWith scans the list calling w.startswith(prefix) on every
word. O(1) insert, but O(N * L) per query (N words, L = max length). The
repeated work: words that share a prefix ("apple", "apply", "app") are
compared character by character against the same query over and over;
the shared letters are re-read once per word instead of once in total.

From brute force to optimal
---------------------------
Shared prefixes should be stored once. A tree whose edges are labelled by
characters does exactly that: the path from the root spelling "app" is
shared by every word starting with "app", and "apple" / "apply" only
branch after it. A query then follows at most len(query) edges regardless
of how many words are stored: startsWith is "can I walk the whole
prefix?", search is "can I walk the whole word AND is the last node marked
as a word end?". The end marker is what distinguishes a stored word from
a mere prefix of one. Invariant: node reached by walking s exists iff some
inserted word has s as a prefix.

Intuition
---------
A trie is a dictionary of dictionaries keyed by character. Walking a
string is a chain of lookups; inserting creates missing links on the way.
A sentinel key ("$") at a node says "a word ends here", which is the only
difference between search and startsWith.

Geometric view
--------------
Picture words laid out as paths fanning out from a single root: "app",
"apple", "apply" share the trunk a-p-p, then split. Each query is a finger
tracing one path from the root; if the finger runs off the tree the answer
is False, and search additionally checks for an end-of-word mark on the
last node.

Steps
-----
1. root = {} (char -> child dict); "$" key marks end of word.
2. insert: node = root; for ch in word: node = node.setdefault(ch, {}); node["$"] = True.
3. _walk(s): follow s from root; return the node or None if a char is missing.
4. search(word): node = _walk(word); return node is not None and "$" in node.
5. startsWith(prefix): return _walk(prefix) is not None.

Complexity: O(L) time per operation, O(total characters) space — each
operation touches one node per character; nodes are shared across words
with common prefixes.
Pitfalls: forgetting the end marker (search("app") would be True after
inserting only "apple"); letting "$" collide with a real character
(fine for lowercase inputs, use a dedicated attribute otherwise).
"""
from typing import List, Optional


class Trie:
    def __init__(self):
        self.root: dict = {}          # char -> child dict; "$" marks the end of a word

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def _walk(self, s: str) -> Optional[dict]:
        # node reached by spelling s from the root, or None if the path breaks
        node = self.root
        for ch in s:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and "$" in node

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None


class BruteForce:
    # Plain list of words: search scans every word, startsWith re-compares every prefix.
    def __init__(self):
        self.words: List[str] = []

    def insert(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        return any(w == word for w in self.words)

    def startsWith(self, prefix: str) -> bool:
        return any(w.startswith(prefix) for w in self.words)


if __name__ == "__main__":
    for cls in (Trie, BruteForce):
        t = cls()
        assert t.search("apple") is False           # empty structure
        assert t.startsWith("a") is False
        t.insert("apple")
        assert t.search("apple") is True
        assert t.search("app") is False             # prefix only, not a word
        assert t.startsWith("app") is True
        assert t.startsWith("apl") is False
        t.insert("app")
        assert t.search("app") is True
        t.insert("apply")
        assert t.search("apply") is True and t.search("appl") is False
        assert t.startsWith("appl") is True and t.startsWith("b") is False
    print("ok")
