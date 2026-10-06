"""
Autocomplete: Collect Words with a Prefix (basics: tries)
Return every stored word that starts with a prefix, in sorted order (duplicates once).
  words car, card, care, cat, dog; prefix "car"  ->  ['car', 'card', 'care']

Idea: walk down to the prefix's node; every word in the subtree below it has the prefix.
      A depth-first search that visits children in alphabetical order emits them sorted.

Pseudocode:
  node = walk the prefix from the root          # missing child -> return []
  dfs(node, path):
      if node.end: output path
      for ch in sorted(node.children): dfs(child, path + ch)
  dfs(node, prefix)                             # path starts as the prefix

Time O(len(prefix)) to walk down, plus one visit per node below it; space O(total characters).
"""


class TrieNode:
    def __init__(self):
        self.children = {}                   # char -> TrieNode
        self.end = False                     # a word ends here


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True

    def words_with_prefix(self, prefix):
        node = self.root
        for ch in prefix:                    # walk down to the prefix's node
            if ch not in node.children:
                return []
            node = node.children[ch]
        out = []

        def dfs(node, path):
            if node.end:                     # a word ends here
                out.append(path)
            for ch in sorted(node.children): # alphabetical -> sorted output
                dfs(node.children[ch], path + ch)

        dfs(node, prefix)                    # path already holds the prefix
        return out


if __name__ == "__main__":
    trie = Trie()
    for word in ["car", "card", "care", "cat", "dog"]:
        trie.insert(word)
    print(trie.words_with_prefix("car"))     # ['car', 'card', 'care']
    print(trie.words_with_prefix("ca"))      # ['car', 'card', 'care', 'cat']
    print(trie.words_with_prefix("x"))       # []
