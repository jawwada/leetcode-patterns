"""
Word Ladder - BFS on an Implicit Graph

Turn begin_word into end_word one letter at a time, every word after the first
taken from word_list. Return the number of words in the shortest such ladder,
or 0 if there is none:
"hit" to "cog" with ["hot", "dot", "dog", "lot", "log", "cog"] -> 5.
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def ladder_length(begin_word, end_word, word_list):
    """BFS over words; neighbors differ in one letter. O(n * 26 * L^2)."""
    unvisited = set(word_list)          # dictionary words not reached yet
    if end_word not in unvisited:
        return 0
    if begin_word in unvisited:
        unvisited.remove(begin_word)    # the start counts as reached
    queue = deque([(begin_word, 1)])    # (word, words in the ladder so far)
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        for i in range(len(word)):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                candidate = word[:i] + letter + word[i + 1:]
                if candidate in unvisited:          # a word not reached yet
                    unvisited.remove(candidate)     # mark when enqueued
                    queue.append((candidate, length + 1))
    return 0


# --- try it ---
words = ["hot", "dot", "dog", "lot", "log", "cog"]
print(ladder_length("hit", "cog", words))                       # -> 5
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot"]))  # -> 0
print(ladder_length("a", "c", ["a", "b", "c"]))                 # -> 2
