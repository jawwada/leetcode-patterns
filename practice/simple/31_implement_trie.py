"""
Implement Trie (Prefix Tree) (LeetCode 208)
Support insert(word), search(word) and startsWith(prefix).
  insert("apple"), search("apple"), search("app"), startsWith("app")  ->  True, False, True

Idea: words sharing a prefix share one path of nodes, one node per character.
      Every operation walks one node per character, so it costs O(L).

Pseudocode:
  insert(word): walk chars, creating missing children; mark last node end = True
  _walk(s):     follow chars; return None if a child is missing, else the last node
  search(word): node = _walk(word); return node exists and node.end
  startsWith(p): return _walk(p) exists

Time O(L) per op, space O(total characters).
"""


class TrieNode:
    def __init__(self):
        self.children = {}               # char -> TrieNode
        self.end = False                 # a word ends here


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:  # create missing path
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True                  # mark the word's end

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:  # path breaks: not present
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    print(trie.search("apple"), trie.search("app"), trie.startsWith("app"))  # True False True
    trie.insert("app")
    print(trie.search("app"))                                                # True
