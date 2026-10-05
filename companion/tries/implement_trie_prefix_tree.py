"""
Implement Trie (Prefix Tree) (LeetCode 208) - Medium
Chapter: tries
Pattern: Trie (prefix tree)

Design a Trie with insert(word), search(word) (is this exact word stored?) and
startsWith(prefix) (does any stored word begin with prefix?).
Example: insert("apple"); search("apple") -> True; search("app") -> False;
startsWith("app") -> True; insert("app"); search("app") -> True.
"""


# --- brute force ---
class BruteForce:
    """Keep a plain list of words; every query scans the whole list. O(N * L) per query."""

    def __init__(self):
        self.words = []

    def insert(self, word):
        self.words.append(word)

    def search(self, word):
        for stored in self.words:
            if stored == word:
                return True
        return False

    def startsWith(self, prefix):
        for stored in self.words:
            if stored.startswith(prefix):   # the same prefix is re-read once per word
                return True
        return False


# --- optimal ---
class Trie:
    """Nested dicts keyed by character; "$" marks where a word ends. O(L) per operation."""

    def __init__(self):
        self.root = {}            # char -> child dict

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                node[ch] = {}     # create the missing link
            node = node[ch]
        node["$"] = True          # a word ends at this node

    def walk(self, text):
        # follow text down from the root; return the node reached, or None if the path breaks
        node = self.root
        for ch in text:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word):
        node = self.walk(word)
        return node is not None and "$" in node   # the path exists AND a word ends there

    def startsWith(self, prefix):
        return self.walk(prefix) is not None


# --- try the brute force ---
trie = BruteForce()
print(trie.search("apple"))      # -> False
trie.insert("apple")
print(trie.search("apple"))      # -> True
print(trie.search("app"))        # -> False
print(trie.startsWith("app"))    # -> True
trie.insert("app")
print(trie.search("app"))        # -> True


# --- try the optimal ---
trie = Trie()
print(trie.search("apple"))      # -> False
trie.insert("apple")
print(trie.search("apple"))      # -> True
print(trie.search("app"))        # -> False
print(trie.startsWith("app"))    # -> True
trie.insert("app")
print(trie.search("app"))        # -> True
