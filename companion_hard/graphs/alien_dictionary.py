"""
Alien Dictionary (LeetCode 269) - Hard
Chapter: graphs
Pattern: Topological sort (Kahn's BFS) / cycle detection

Given a list of words sorted lexicographically according to an unknown alphabet, return a string
of the unique letters in a valid alphabet order, or "" if the ordering is contradictory. Any valid
order is accepted.
Example: ["wrt","wrf","er","ett","rftt"] -> "wertf"; ["z","x","z"] -> "".
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
def first_difference(word_a, word_b):
    """The (letter_a, letter_b) pair at the first position where the words differ, or None."""
    for i in range(min(len(word_a), len(word_b))):
        if word_a[i] != word_b[i]:
            return (word_a[i], word_b[i])
    return None


def unique_letters(words):
    """Every letter that appears in words, in order of first appearance."""
    letters = []
    for word in words:
        for letter in word:
            if letter not in letters:
                letters.append(letter)
    return letters


# --- brute force ---
def brute_force(words):
    """Collect a < b constraints; each round rescan them all for a free letter. O(U * C) time."""
    letters = unique_letters(words)
    constraints = set()                                # (a, b) means a comes before b
    for i in range(len(words) - 1):
        pair = first_difference(words[i], words[i + 1])
        if pair is not None:
            constraints.add(pair)
        elif len(words[i]) > len(words[i + 1]):
            return ""                                  # "abc" before "ab" is impossible
    order = ""
    while letters:
        blocked = set()
        for before, after in constraints:              # every constraint rescanned each round
            if before in letters:
                blocked.add(after)
        free = None
        for letter in letters:
            if letter not in blocked:
                free = letter
                break
        if free is None:
            return ""                                  # everyone is blocked: a cycle
        order += free
        letters.remove(free)
    return order


# --- optimal ---
def letter_graph(words):
    """(comes_after, in_degree) from adjacent word pairs; None if a word precedes its prefix."""
    comes_after = {}                                   # letter -> set of letters that follow it
    in_degree = {}                                     # letter -> how many letters must precede it
    for letter in unique_letters(words):
        comes_after[letter] = set()
        in_degree[letter] = 0
    for i in range(len(words) - 1):
        pair = first_difference(words[i], words[i + 1])
        if pair is None:
            if len(words[i]) > len(words[i + 1]):
                return None                            # "abc" before "ab" is impossible
            continue
        before, after = pair
        if after not in comes_after[before]:           # count a duplicate constraint only once
            comes_after[before].add(after)
            in_degree[after] += 1
    return (comes_after, in_degree)


def alien_order(words):
    """Build the letter graph, then Kahn's topological sort by in-degree. O(S + U + C) time."""
    graph = letter_graph(words)
    if graph is None:
        return ""
    comes_after, in_degree = graph
    queue = deque()
    for letter in in_degree:
        if in_degree[letter] == 0:
            queue.append(letter)
    order = ""
    while queue:
        letter = queue.popleft()
        order += letter
        for follower in comes_after[letter]:           # only the direct successors change
            in_degree[follower] -= 1
            if in_degree[follower] == 0:
                queue.append(follower)
    if len(order) != len(in_degree):
        return ""                                      # letters left over sit on a cycle
    return order


# --- try the brute force ---
print(brute_force(["wrt", "wrf", "er", "ett", "rftt"]))   # -> wertf
print(brute_force(["z", "x"]))                            # -> zx
print(brute_force(["z", "x", "z"]))                       # -> (empty line: contradiction)
print(brute_force(["abc", "ab"]))                         # -> (empty line: invalid prefix order)


# --- try the optimal ---
print(alien_order(["wrt", "wrf", "er", "ett", "rftt"]))   # -> wertf
print(alien_order(["z", "x"]))                            # -> zx
print(alien_order(["z", "x", "z"]))                       # -> (empty line: contradiction)
print(alien_order(["abc", "ab"]))                         # -> (empty line: invalid prefix order)
