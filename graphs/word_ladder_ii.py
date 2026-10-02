"""
Word Ladder II (LeetCode 126)  — Hard
Pattern: Layered BFS with a parents map, then backtrack the paths

Problem
-------
Given beginWord, endWord and a wordList, a transformation changes one letter and must land in the
list. Return ALL shortest transformation sequences from beginWord to endWord (each as a list of
words including both ends), or [] if none exists.
Example: "hit" -> "cog", ["hot","dot","dog","lot","log","cog"] ->
[["hit","hot","dot","dog","cog"], ["hit","hot","lot","log","cog"]].

Brute force
-----------
DFS from beginWord enumerating every simple path to endWord (neighbours found by comparing against
every dictionary word), remember the shortest length seen and keep the paths of that length.
Exponential: O(N! * N * L) time in the worst case, O(N) space for the current path. The waste:
the same word is reached at many different depths along many different paths, and every path
through it re-explores its whole subtree; paths longer than the shortest are explored to the end
before being discarded.

From brute force to optimal
---------------------------
Redundancy 1 is exploring paths that cannot be shortest. Observation: BFS visits words in order of
distance, so a word first reached in layer k has distance k; any path arriving later is not
shortest and can be ignored. Redundancy 2 is storing whole paths. Observation: a shortest path to
w consists of a shortest path to some parent p in layer k-1 plus the edge p -> w. So record, for
each word, the SET of parents in the previous layer that reach it (not just one, not from the same
layer), and remove a layer's words from the dictionary only after the whole layer is processed so
that siblings in the same layer can all register as parents. Stop the BFS at the layer that
contains endWord, then backtrack from endWord through the parents map to enumerate the paths. The
BFS is O(N * L * 26) and the backtracking is proportional to the output size.

Intuition
---------
Two phases: a BFS that builds the DAG of shortest-path edges (every edge goes from layer k-1 to
layer k), then a DFS over that DAG from endWord back to beginWord. The DAG is what makes the output
complete without ever generating a non-shortest path.

Geometric view
--------------
Picture the words in horizontal layers by BFS distance. Edges only run downward one layer. The
parents map stores the upward arrows; every shortest path is a downward route in this layered DAG,
and backtracking from endWord follows the upward arrows in all combinations.

    hit                     layer 0
     |
    hot                     layer 1
    /  \\
  dot  lot                  layer 2
   |    |
  dog  log                  layer 3
    \\  /
    cog                     layer 4   -> 2 paths

Steps
-----
1. words = set(wordList); return [] if endWord is missing. layer = {beginWord}; parents = {}.
2. While layer is non-empty and endWord not yet found: for each word in layer, for each position
   and letter, if the neighbour is in words, add word to nxt[neighbour].
3. Remove all keys of nxt from words at once; merge nxt into parents; layer = keys of nxt.
4. If endWord was never reached return []. Otherwise DFS from endWord: for each parent, recurse;
   at beginWord record the reversed path.
5. Return the collected paths.

Complexity: O(N * L^2 * 26 + P * L) time, O(N * L) space — each of N words generates 26L
neighbour strings of length L once; P is the number of output paths; parents hold at most one
entry per DAG edge.
Pitfalls: removing a word from the dictionary as soon as it is seen (loses parents from the same
layer); storing a single parent per word (loses paths); forgetting to stop at the endWord layer
(deeper layers waste time but also can never add paths); using lists for the dictionary.
"""
from collections import defaultdict
from typing import Dict, List, Set


class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        words = set(wordList)
        if endWord not in words:
            return []
        L = len(beginWord)
        parents: Dict[str, Set[str]] = {}               # word -> words in the previous layer
        layer, found = {beginWord}, False
        words.discard(beginWord)
        while layer and not found:
            nxt = defaultdict(set)
            for w in layer:
                for i in range(L):
                    for ch in "abcdefghijklmnopqrstuvwxyz":
                        nb = w[:i] + ch + w[i + 1:]
                        if nb in words:
                            nxt[nb].add(w)
            words -= nxt.keys()                         # remove the whole layer, not word by word
            parents.update(nxt)
            layer, found = set(nxt), endWord in nxt

        paths: List[List[str]] = []

        def backtrack(w: str, path: List[str]) -> None:
            if w == beginWord:
                paths.append(path[::-1])
                return
            for p in parents[w]:
                backtrack(p, path + [p])

        if found:
            backtrack(endWord, [endWord])
        return paths


def brute_force(beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
    # Enumerate every simple path with DFS (neighbours by pairwise comparison); keep the shortest.
    best: List[List[str]] = []

    def dfs(word: str, path: List[str]) -> None:
        if word == endWord:
            if not best or len(path) < len(best[0]):
                best.clear()
            if not best or len(path) == len(best[0]):
                best.append(path[:])
            return
        for cand in wordList:                             # exponential: all simple paths
            if cand not in path and sum(a != b for a, b in zip(word, cand)) == 1:
                dfs(cand, path + [cand])

    dfs(beginWord, [beginWord])
    return best


if __name__ == "__main__":
    s = Solution()
    cases = (
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"],
         [["hit", "hot", "dot", "dog", "cog"], ["hit", "hot", "lot", "log", "cog"]]),
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"], []),
        ("a", "c", ["a", "b", "c"], [["a", "c"]]),
        ("red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"],
         [["red", "ted", "tad", "tax"], ["red", "ted", "tex", "tax"], ["red", "rex", "tex", "tax"]]),
        ("hot", "dog", ["hot", "dog"], []),
    )
    for b, e, wl, want in cases:
        assert sorted(s.findLadders(b, e, wl)) == sorted(want), (b, e)
        assert sorted(brute_force(b, e, wl)) == sorted(want), (b, e)
    print("ok")
