"""
Add and Search Words with Wildcards (basics: tries)
Support add_word(word) and search(pattern), where a '.' in the pattern matches any one letter.
  add bad, dad, mad; search pad, bad, .ad, b..  ->  False, True, True, True

Idea: store the words in a trie and search it depth-first: a letter follows its one child,
      a '.' tries every child. The pattern matches only if a word ends exactly where the
      pattern ends (the end flag), not just somewhere below.

Pseudocode:
  _match(node, i):                         # does pattern[i:] match below node?
      if i == len(pattern): return node.end
      if pattern[i] == '.': return True if _match(child, i+1) for any child
      if pattern[i] not in node.children: return False
      return _match(node.children[pattern[i]], i+1)

Time O(len) to add; search O(len) without dots, up to O(26^dots * len) with them.
"""


class TrieNode:
    def __init__(self):
        self.children = {}                   # char -> TrieNode
        self.end = False                     # a word ends here


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True

    def search(self, pattern):
        return self._match(self.root, pattern, 0)

    def _match(self, node, pattern, i):
        if i == len(pattern):                # pattern used up:
            return node.end                  # a word must end right here
        ch = pattern[i]
        if ch == ".":                        # wildcard: try every child
            for child in node.children.values():
                if self._match(child, pattern, i + 1):
                    return True
            return False
        if ch not in node.children:          # letter: only one child to follow
            return False
        return self._match(node.children[ch], pattern, i + 1)


if __name__ == "__main__":
    trie = Trie()
    for word in ["bad", "dad", "mad"]:
        trie.add_word(word)
    print(trie.search("pad"), trie.search("bad"))  # False True
    print(trie.search(".ad"), trie.search("b.."))  # True True
    print(trie.search("ba"), trie.search("b."))    # False False
