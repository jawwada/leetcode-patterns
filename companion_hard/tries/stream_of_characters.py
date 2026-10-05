"""
Stream of Characters (LeetCode 1032) - Hard
Chapter: tries
Pattern: Reversed trie walked backwards over a bounded recent-history buffer

StreamChecker(words) is fed one character at a time through query(letter), which returns
True when some word is a suffix of everything queried so far.
Example: words = ["cd", "f", "kl"] with the stream a..l returns True exactly at d, f and l.
"""
from collections import deque


# --- helpers ---
def run_stream(checker, text):
    """Feed the letters of text one by one and collect the answer after each."""
    answers = []
    for letter in text:
        answers.append(checker.query(letter))
    return answers


# --- brute force ---
class BruteForce:
    """Keep the whole stream; test endswith for every word on each query. O(W * L) per query."""

    def __init__(self, words):
        self.words = words
        self.stream = ""

    def query(self, letter):
        self.stream += letter                   # the stream only grows
        for word in self.words:
            if self.stream.endswith(word):
                return True
        return False


# --- optimal ---
class StreamChecker:
    """Reversed words in a trie, walked newest letter first over the last L letters. O(L)."""

    def __init__(self, words):
        self.trie = {}
        self.max_len = 0
        for word in words:
            node = self.trie
            for letter in word[::-1]:           # reversed: the newest stream letter matches first
                if letter not in node:
                    node[letter] = {}
                node = node[letter]
            node["$"] = True
            self.max_len = max(self.max_len, len(word))
        self.recent = deque()                   # deque: popleft is O(1); the last max_len letters

    def query(self, letter):
        self.recent.append(letter)
        if len(self.recent) > self.max_len:
            self.recent.popleft()               # older letters can never be part of a match
        node = self.trie
        for i in range(len(self.recent) - 1, -1, -1):     # newest to oldest
            if self.recent[i] not in node:
                return False
            node = node[self.recent[i]]
            if "$" in node:
                return True                     # some word ends exactly here
        return False


# --- try the brute force ---
print(run_stream(BruteForce(["cd", "f", "kl"]), "abcdefghijkl"))
# -> [False, False, False, True, False, True, False, False, False, False, False, True]
print(run_stream(BruteForce(["ab", "ba", "aaab", "abab", "baa"]), "aabaaabaaa"))
# -> [False, False, True, True, True, False, True, True, True, False]
print(run_stream(BruteForce(["a"]), "bab"))        # -> [False, True, False]
print(run_stream(BruteForce(["abc"]), "ab"))       # -> [False, False]


# --- try the optimal ---
print(run_stream(StreamChecker(["cd", "f", "kl"]), "abcdefghijkl"))
# -> [False, False, False, True, False, True, False, False, False, False, False, True]
print(run_stream(StreamChecker(["ab", "ba", "aaab", "abab", "baa"]), "aabaaabaaa"))
# -> [False, False, True, True, True, False, True, True, True, False]
print(run_stream(StreamChecker(["a"]), "bab"))     # -> [False, True, False]
print(run_stream(StreamChecker(["abc"]), "ab"))    # -> [False, False]
