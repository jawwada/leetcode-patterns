"""
Design Add and Search Words Data Structure (LeetCode 211) - Medium
Chapter: tries
Pattern: Trie with wildcard DFS

Design WordDictionary with addWord(word) and search(pattern), where the pattern may
contain '.' matching any single letter.
Example: add bad, dad, mad; search("pad") -> False; search("bad") -> True;
search(".ad") -> True; search("b..") -> True.
"""


# --- brute force ---
def matches(pattern, word):
    """True if word has the pattern's length and every character fits ('.' fits anything)."""
    if len(word) != len(pattern):
        return False
    for i in range(len(pattern)):
        if pattern[i] != "." and pattern[i] != word[i]:
            return False
    return True


class BruteForce:
    """Keep a list of words; search compares the pattern with every word. O(N * L) per search."""

    def __init__(self):
        self.words = []

    def addWord(self, word):
        self.words.append(word)

    def search(self, pattern):
        for stored in self.words:
            if matches(pattern, stored):
                return True
        return False


# --- optimal ---
def dfs(node, pattern, i):
    """True if some word stored below node spells pattern[i:]."""
    if i == len(pattern):
        return "$" in node                  # the whole pattern is used: is this a word end?
    ch = pattern[i]
    if ch != ".":
        if ch not in node:
            return False                    # a literal mismatch prunes this whole subtree
        return dfs(node[ch], pattern, i + 1)
    for key in node:                        # wildcard: try every real child
        if key == "$":
            continue
        if dfs(node[key], pattern, i + 1):
            return True
    return False


class WordDictionary:
    """Trie; search is a DFS that only branches at '.'. O(L) per search without wildcards."""

    def __init__(self):
        self.root = {}            # char -> child dict; "$" marks where a word ends

    def addWord(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node["$"] = True

    def search(self, pattern):
        return dfs(self.root, pattern, 0)


# --- try the brute force ---
words = BruteForce()
print(words.search("."))      # -> False
words.addWord("bad")
words.addWord("dad")
words.addWord("mad")
print(words.search("pad"))    # -> False
print(words.search("bad"))    # -> True
print(words.search(".ad"))    # -> True
print(words.search("b.."))    # -> True
print(words.search("...."))   # -> False
print(words.search("ba"))     # -> False


# --- try the optimal ---
words = WordDictionary()
print(words.search("."))      # -> False
words.addWord("bad")
words.addWord("dad")
words.addWord("mad")
print(words.search("pad"))    # -> False
print(words.search("bad"))    # -> True
print(words.search(".ad"))    # -> True
print(words.search("b.."))    # -> True
print(words.search("...."))   # -> False
print(words.search("ba"))     # -> False
