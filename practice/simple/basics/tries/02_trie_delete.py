"""
Trie: Delete a Word with Pruning (basics: tries)
Delete a word from a trie and remove the nodes that no other word needs.
  insert apple, app, ape; delete apple, app, cat  ->  {'a': {'p': {'e': {'$': True}}}}

Idea: clear the word's end flag, then walk back up its path removing every node that now
      has no children and ends no word. Stop at the first node another word still needs.

Pseudocode:
  delete(word):
      path = [root] + the node after each char          # a char is missing -> return False
      if the last node is not a word end: return False
      clear its end flag
      for i from len(word)-1 down to 0:                 # walk back up
          if path[i+1] has children or ends a word: stop
          remove word[i] from path[i].children          # prune it
      return True

Time O(len(word)) per operation, space O(total characters).
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

    def delete(self, word):
        path = [self.root]                   # path[i + 1] = node after word[i]
        for ch in word:
            if ch not in path[-1].children:  # word is not stored
                return False
            path.append(path[-1].children[ch])
        if not path[-1].end:                 # only a prefix, not a word
            return False
        path[-1].end = False                 # unmark the word
        for i in range(len(word) - 1, -1, -1):   # walk back up
            child = path[i + 1]
            if child.children or child.end:  # still needed: stop pruning
                break
            del path[i].children[word[i]]    # prune the useless node
        return True


def to_dict(node):
    d = {"$": True} if node.end else {}      # "$" marks a word end
    for ch, child in node.children.items():
        d[ch] = to_dict(child)
    return d


if __name__ == "__main__":
    trie = Trie()
    for word in ["apple", "app", "ape"]:
        trie.insert(word)
    print(trie.delete("apple"), trie.delete("app"))  # True True
    print(trie.delete("cat"))                        # False
    print(to_dict(trie.root))                        # {'a': {'p': {'e': {'$': True}}}}
