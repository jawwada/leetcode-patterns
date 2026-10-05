"""
Word Ladder (LeetCode 127) - Hard
Chapter: graphs
Pattern: BFS on implicit graph (wildcard buckets)

Given beginWord, endWord and a wordList, one transformation changes exactly one letter and the
result must be in wordList. Return the number of words in the shortest transformation sequence
from beginWord to endWord (counting both ends), or 0 if there is none.
Example: "hit" -> "cog" with ["hot","dot","dog","lot","log","cog"] -> 5 (hit,hot,dot,dog,cog).
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
def one_letter_apart(a, b):
    """True when the two words differ in exactly one position."""
    differences = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            differences += 1
    return differences == 1


# --- brute force ---
def brute_force(begin_word, end_word, word_list):
    """BFS, but find neighbours by scanning the whole word list. O(N^2 * L) time, O(N) space."""
    if end_word not in word_list:
        return 0
    queue = deque([(begin_word, 1)])          # (word, number of words so far)
    visited = {begin_word}
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        for candidate in word_list:           # scan every word to find the neighbours
            if candidate not in visited and one_letter_apart(word, candidate):
                visited.add(candidate)
                queue.append((candidate, length + 1))
    return 0


# --- optimal ---
def word_ladder(begin_word, end_word, word_list):
    """Bucket words by wildcard patterns like h*t, then BFS. O(N * L^2) time, O(N * L) space."""
    if end_word not in word_list:
        return 0
    size = len(begin_word)
    buckets = {}                              # "h*t" -> [hit, hot, ...]
    for word in word_list:
        for i in range(size):
            pattern = word[:i] + "*" + word[i + 1:]
            if pattern not in buckets:
                buckets[pattern] = []
            buckets[pattern].append(word)
    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        for i in range(size):
            pattern = word[:i] + "*" + word[i + 1:]
            for neighbour in buckets.get(pattern, []):   # neighbours share a pattern with word
                if neighbour not in visited:              # mark on push, not on pop
                    visited.add(neighbour)
                    queue.append((neighbour, length + 1))
    return 0


# --- try the brute force ---
print(brute_force("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))   # -> 5
print(brute_force("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))          # -> 0
print(brute_force("a", "c", ["a", "b", "c"]))                                  # -> 2
print(brute_force("hot", "dog", ["hot", "dog"]))                               # -> 0


# --- try the optimal ---
print(word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))   # -> 5
print(word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))          # -> 0
print(word_ladder("a", "c", ["a", "b", "c"]))                                  # -> 2
print(word_ladder("hot", "dog", ["hot", "dog"]))                               # -> 0
