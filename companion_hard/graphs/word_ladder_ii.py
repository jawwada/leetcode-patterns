"""
Word Ladder II (LeetCode 126) - Hard
Chapter: graphs
Pattern: Layered BFS + parents DAG, then backtrack paths

Given beginWord, endWord and a wordList, one transformation changes exactly one letter and must
land on a word in the list. Return every shortest transformation sequence from beginWord to
endWord (each including both ends), or [] if there is none.
Example: "hit" -> "cog" with ["hot","dot","dog","lot","log","cog"]
-> [["hit","hot","dot","dog","cog"], ["hit","hot","lot","log","cog"]].
"""


# --- helpers ---
def one_letter_apart(a, b):
    """True when the two words differ in exactly one position."""
    differences = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            differences += 1
    return differences == 1


# --- brute force ---
def all_paths(word, path, end_word, word_list, best):
    """DFS over every simple path; best holds the shortest complete paths found so far."""
    if word == end_word:
        if not best or len(path) < len(best[0]):
            best.clear()                              # a strictly shorter path: forget the rest
        if not best or len(path) == len(best[0]):
            best.append(path[:])
        return
    for candidate in word_list:                       # neighbours by comparing every word
        if candidate not in path and one_letter_apart(word, candidate):
            all_paths(candidate, path + [candidate], end_word, word_list, best)


def brute_force(begin_word, end_word, word_list):
    """Enumerate every simple path with DFS and keep the shortest ones. Exponential time."""
    if end_word not in word_list:
        return []
    best = []
    all_paths(begin_word, [begin_word], end_word, word_list, best)
    return best


# --- optimal ---
def build_paths(word, path, begin_word, parents, paths):
    """Walk back from word through its parents until beginWord; each route is one answer."""
    if word == begin_word:
        paths.append(path[::-1])                      # path was built end -> begin
        return
    for parent in parents[word]:
        build_paths(parent, path + [parent], begin_word, parents, paths)


def grow_layer(layer, words):
    """The unused words one letter away from the layer, each mapped to its parents in the layer."""
    next_layer = {}
    for word in layer:
        for i in range(len(word)):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                neighbour = word[:i] + letter + word[i + 1:]
                if neighbour in words:
                    if neighbour not in next_layer:
                        next_layer[neighbour] = set()
                    next_layer[neighbour].add(word)   # every parent in this layer is recorded
    return next_layer


def word_ladder_ii(begin_word, end_word, word_list):
    """BFS layer by layer, recording each word's parents; backtrack from endWord. O(N * L * 26)."""
    words = set(word_list)
    if end_word not in words:
        return []
    parents = {}                                      # word -> set of words one layer earlier
    layer = {begin_word}
    found = False
    words.discard(begin_word)
    while layer and not found:
        next_layer = grow_layer(layer, words)
        for word in next_layer:                       # remove the whole layer, not word by word
            words.discard(word)
            parents[word] = next_layer[word]
        layer = set(next_layer)
        found = end_word in next_layer
    paths = []
    if found:
        build_paths(end_word, [end_word], begin_word, parents, paths)
    return paths


# --- try the brute force ---
print(sorted(brute_force("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])))
# -> [['hit', 'hot', 'dot', 'dog', 'cog'], ['hit', 'hot', 'lot', 'log', 'cog']]
print(sorted(brute_force("hit", "cog", ["hot", "dot", "dog", "lot", "log"])))    # -> []
print(sorted(brute_force("a", "c", ["a", "b", "c"])))                            # -> [['a', 'c']]
print(sorted(brute_force("red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex"])))
# -> [['red', 'rex', 'tex', 'tax'], ['red', 'ted', 'tad', 'tax'], ['red', 'ted', 'tex', 'tax']]


# --- try the optimal ---
print(sorted(word_ladder_ii("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])))
# -> [['hit', 'hot', 'dot', 'dog', 'cog'], ['hit', 'hot', 'lot', 'log', 'cog']]
print(sorted(word_ladder_ii("hit", "cog", ["hot", "dot", "dog", "lot", "log"])))    # -> []
print(sorted(word_ladder_ii("a", "c", ["a", "b", "c"])))                    # -> [['a', 'c']]
print(sorted(word_ladder_ii("red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex"])))
# -> [['red', 'rex', 'tex', 'tax'], ['red', 'ted', 'tad', 'tax'], ['red', 'ted', 'tex', 'tax']]
