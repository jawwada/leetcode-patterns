"""
Trie - Insert, Search, Starts With

Store words so that search(word) says whether that exact word was inserted
and starts_with(prefix) whether any inserted word begins with prefix: after
inserting apple, app, apt and bat, search("ap") -> False and
starts_with("ap") -> True.
"""


# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}              # letter -> TrieNode
        self.is_end = False             # True if a word ends at this node


# --- algorithm ---
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Walk down the letters, creating missing children. O(L)."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True              # flag the node where the word stops

    def walk(self, prefix):
        """Follow the letters of prefix; the last node, or None. O(L)."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None             # the path breaks off
            node = node.children[ch]
        return node

    def search(self, word):
        """The path must exist and end on a flagged node. O(L)."""
        node = self.walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """The path existing is enough. O(L)."""
        return self.walk(prefix) is not None


# --- try it ---
trie = Trie()
for word in ["apple", "app", "apt", "bat"]:
    trie.insert(word)
print(trie.search("app"))           # -> True
print(trie.search("ap"))            # -> False
print(trie.starts_with("ap"))       # -> True
print(trie.search("apl"))           # -> False
print(trie.starts_with("c"))        # -> False
