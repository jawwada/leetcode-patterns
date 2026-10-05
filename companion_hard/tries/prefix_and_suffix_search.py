"""
Prefix and Suffix Search (LeetCode 745) - Hard
Chapter: tries
Pattern: Trie over "suffix#word" rotations, max index stored per node

WordFilter(words) is built once, and f(pref, suff) returns the largest index i such that
words[i] starts with pref and ends with suff, or -1 if there is none.
Example: words = ["apple"] gives f("a", "e") = 0 and f("b", "") = -1.
"""


# --- brute force ---
class BruteForce:
    """Keep the list; each query scans it from the back. O(W * L) per query."""

    def __init__(self, words):
        self.words = words

    def f(self, pref, suff):
        for i in range(len(self.words) - 1, -1, -1):     # from the last index down to 0
            if self.words[i].startswith(pref) and self.words[i].endswith(suff):
                return i                                 # first hit from the back = largest index
        return -1


# --- optimal ---
class WordFilter:
    """Insert suffix + "#" + word for every suffix; a query is one prefix walk. O(L) per query."""

    def __init__(self, words):
        self.trie = {}
        for index in range(len(words)):             # increasing index, so overwriting keeps the max
            word = words[index]
            for k in range(len(word) + 1):          # every suffix, including the empty one
                node = self.trie
                for letter in word[k:] + "#" + word:
                    if letter not in node:
                        node[letter] = {}
                    node = node[letter]
                    node["$"] = index               # every node on the path knows its best index

    def f(self, pref, suff):
        node = self.trie
        for letter in suff + "#" + pref:            # the pair becomes a single prefix query
            if letter not in node:
                return -1
            node = node[letter]
        return node["$"]


# --- try the brute force ---
wf = BruteForce(["apple"])
print(wf.f("a", "e"))           # -> 0
print(wf.f("b", ""))            # -> -1
print(wf.f("apple", "apple"))   # -> 0
wf = BruteForce(["cabaa", "ab", "ab"])
print(wf.f("ab", ""))           # -> 2
print(wf.f("c", "aa"))          # -> 0
print(wf.f("aa", ""))           # -> -1


# --- try the optimal ---
wf = WordFilter(["apple"])
print(wf.f("a", "e"))           # -> 0
print(wf.f("b", ""))            # -> -1
print(wf.f("apple", "apple"))   # -> 0
wf = WordFilter(["cabaa", "ab", "ab"])
print(wf.f("ab", ""))           # -> 2
print(wf.f("c", "aa"))          # -> 0
print(wf.f("aa", ""))           # -> -1
