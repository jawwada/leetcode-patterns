"""
Trie: Insert, Search, Starts With (basics: tries)
Store words so you can ask "was this exact word inserted?" and "does any word start with p?".
  insert apple; search apple, search app, starts_with app  ->  True, False, True

Idea: words with a common prefix share one path of nodes, one node per character.
      Each node has a dict of children and an end flag ("a word ends here").
      search needs the end flag; starts_with only needs the path to exist.

Pseudocode:
  insert(word):   walk the chars, creating missing children; set end = True on the last node
  _find(s):       walk the chars; return None if a child is missing, else the last node
  search(word):   node = _find(word); return node exists and node.end
  starts_with(p): return _find(p) exists

Time O(len) per operation, space O(total characters).
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
            if ch not in node.children:  # create the missing child
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True                  # mark the word's end

    def _find(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:  # path breaks: s is not there
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._find(word)
        return node is not None and node.end   # whole word, not just a prefix

    def starts_with(self, prefix):
        return self._find(prefix) is not None  # the path alone is enough


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    print(trie.search("apple"), trie.search("app"), trie.starts_with("app"))  # True False True
    trie.insert("app")
    print(trie.search("app"), trie.starts_with("b"))                          # True False
