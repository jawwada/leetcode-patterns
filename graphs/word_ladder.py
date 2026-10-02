"""
Word Ladder (LeetCode 127)  — Hard
Pattern: BFS on implicit graph (wildcard buckets)

Problem
-------
Given beginWord, endWord and a wordList, each step changes one letter and the result must
be in wordList. Return the number of words in the shortest transformation sequence
(including both ends), or 0 if none exists.
Example: "hit" -> "cog", ["hot","dot","dog","lot","log","cog"] -> 5 (hit->hot->dot->dog->cog).

Brute force
-----------
BFS from beginWord where, to find the neighbours of a word, you compare it against EVERY
word in the list and keep the ones that differ in exactly one position. With N words of
length L, each expansion costs O(N*L) and there are up to N expansions -> O(N^2 * L)
time, O(N) space. The waste: for every word we rescan the whole dictionary, even though
almost all of those comparisons fail.

From brute force to optimal
---------------------------
The redundancy is the all-pairs comparison to discover edges. Observation: two words are
adjacent iff they share a wildcard pattern such as "h*t" (same letters except one slot).
Pre-bucket every word under each of its L patterns in a hash map; then the neighbours of
a word are the union of its L buckets, found in O(L) lookups instead of O(N*L) scans.
BFS over this implicit graph visits each word once, so the total is O(N * L^2) (the L^2
comes from building L patterns of length L per word). Marking words visited when
enqueued keeps the frontier layer-clean so the depth is the shortest path.

Intuition
---------
Shortest path with unit edges means BFS. The trick is generating neighbours cheaply: a
word's neighbours are the words that share one of its "one letter blanked out" forms.
Index the dictionary by those forms once, then BFS layer by layer; the first time endWord
is dequeued, the current layer count is the answer.

Geometric view
--------------
Picture words as nodes and wildcard patterns as hub nodes ("h*t" connects hit, hot, hat).
Each real word hangs off L hubs. BFS ripples outward from beginWord: layer 1 = beginWord,
layer 2 = everything sharing a hub, and so on. The queue is the current ripple. Stepping
through a hub costs one unit, so BFS depth on the word nodes equals ladder length.

Steps
-----
1. If endWord not in wordList return 0. Build buckets: pattern -> [words].
2. queue = [(beginWord, 1)], visited = {beginWord}.
3. Pop (word, d); if word == endWord return d.
4. For each position i build pattern word[:i] + '*' + word[i+1:]; for each unvisited
   neighbour in that bucket mark visited and enqueue with d + 1.
5. Return 0 if the queue empties.

Complexity: O(N * L^2) time, O(N * L) space — N words each produce L patterns of length L; buckets hold N*L entries.
Pitfalls: forgetting the endWord-not-in-list check; marking visited on pop instead of on
push (blows up the queue); clearing a bucket after use is a valid speedup but never
re-adding beginWord to the list (it need not be in wordList).
"""
from collections import defaultdict, deque
from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        L = len(beginWord)
        buckets = defaultdict(list)  # "h*t" -> [hit, hot, ...]
        for w in wordList:
            for i in range(L):
                buckets[w[:i] + "*" + w[i + 1:]].append(w)
        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            word, dist = queue.popleft()
            if word == endWord:
                return dist
            for i in range(L):
                for nb in buckets[word[:i] + "*" + word[i + 1:]]:
                    if nb not in visited:
                        visited.add(nb)
                        queue.append((nb, dist + 1))
        return 0


def brute_force(beginWord: str, endWord: str, wordList: List[str]) -> int:
    # BFS, but discover neighbours by comparing against every dictionary word.
    def adjacent(a: str, b: str) -> bool:
        return sum(x != y for x, y in zip(a, b)) == 1

    queue, visited = deque([(beginWord, 1)]), {beginWord}
    while queue:
        word, dist = queue.popleft()
        if word == endWord:
            return dist
        for cand in wordList:
            if cand not in visited and adjacent(word, cand):
                visited.add(cand)
                queue.append((cand, dist + 1))
    return 0


if __name__ == "__main__":
    s = Solution()
    cases = (
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"], 5),
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"], 0),
        ("a", "c", ["a", "b", "c"], 2),
        ("hot", "dog", ["hot", "dog"], 0),
    )
    for b, e, wl, want in cases:
        assert brute_force(b, e, wl) == want
        assert s.ladderLength(b, e, wl) == want
    print("ok")
