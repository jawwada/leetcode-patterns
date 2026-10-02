"""
Alien Dictionary (LeetCode 269)  — Hard
Pattern: Topological sort (Kahn's BFS) / cycle detection

Problem
-------
Given a list of words sorted lexicographically by an unknown alphabet, return a string
of the unique letters in a valid alphabet order, or "" if the ordering is inconsistent.
Any valid order is accepted.
Example: ["wrt","wrf","er","ett","rftt"] -> "wertf".  ["z","x","z"] -> "".

Brute force
-----------
Extract the pairwise constraints a < b by comparing ADJACENT words (the first differing
letter). Then build the order by repeatedly scanning all letters for one that never
appears on the right side of a remaining constraint; emit it and delete its constraints;
if no such letter exists, there is a cycle. Each round rescans all constraints: O(U * C)
with U unique letters and C constraints, plus the O(total chars) extraction; O(U + C)
space. The waste is rescanning every constraint each round when only the ones leaving the
just-emitted letter changed.

From brute force to optimal
---------------------------
The constraints form a directed graph on letters, so "pick a letter with no remaining
incoming constraint" is exactly Kahn's topological sort. Maintain in-degree per letter and
a queue of zero-in-degree letters; when a letter is emitted, decrement only its direct
successors. Each edge is touched once -> O(total chars + U + C) time. If fewer than U
letters are emitted, the leftover letters sit on a cycle -> "". The subtle input check
("abc" before "ab" is invalid: a prefix must come first) is caught during extraction.

Intuition
---------
Each adjacent pair of words gives at most one fact: at the first position they differ,
the earlier word's letter comes first. Collect those facts as edges, then take letters in
any order that respects every edge, which is a topological sort. Use a queue of letters
with no pending predecessors; if you get stuck before using all letters, the facts
contradict each other.

Geometric view
--------------
Draw a node per letter, an arrow per constraint, and write the in-degree beside each
node. Letters labelled 0 sit in the queue and are written to the output; popping one
deletes its outgoing arrows and lowers the labels at the tips. Output grows as the labels
drain to 0; a ring of arrows whose labels never reach 0 is a contradiction.

Steps
-----
1. Init adj and indeg for every letter in every word.
2. For each adjacent pair (w1, w2): find first differing index j; add edge w1[j] -> w2[j]
   (once); if none differs and len(w1) > len(w2) return "".
3. Kahn: enqueue in-degree-0 letters, pop, append to result, decrement successors.
4. Return result if it contains every letter else "".

Complexity: O(S + U + C) time, O(U + C) space — S total characters scanned once; graph has U nodes, C <= number of word pairs edges.
Pitfalls: adding duplicate edges (double counts in-degree -> never reaches 0); forgetting
letters that appear only in words with no constraints; missing the invalid prefix case.
"""
from collections import defaultdict, deque
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        adj = defaultdict(set)
        indeg = {ch: 0 for w in words for ch in w}
        for w1, w2 in zip(words, words[1:]):
            for a, b in zip(w1, w2):
                if a != b:
                    if b not in adj[a]:  # avoid double-counting duplicate constraints
                        adj[a].add(b)
                        indeg[b] += 1
                    break
            else:
                if len(w1) > len(w2):
                    return ""  # "abc" before "ab" is impossible
        queue = deque(ch for ch, d in indeg.items() if d == 0)
        order = []
        while queue:
            ch = queue.popleft()
            order.append(ch)
            for nxt in adj[ch]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
        return "".join(order) if len(order) == len(indeg) else ""


def brute_force(words: List[str]) -> str:
    # Extract constraints, then each round rescan all remaining constraints to find a
    # letter that is never on the right-hand side.
    letters = {ch for w in words for ch in w}
    constraints = set()
    for w1, w2 in zip(words, words[1:]):
        for a, b in zip(w1, w2):
            if a != b:
                constraints.add((a, b))
                break
        else:
            if len(w1) > len(w2):
                return ""
    order = []
    while letters:
        blocked = {b for a, b in constraints if a in letters}
        free = sorted(letters - blocked)
        if not free:
            return ""
        ch = free[0]
        order.append(ch)
        letters.remove(ch)
        constraints = {(a, b) for a, b in constraints if a != ch}
    return "".join(order)


def valid(order: str, words: List[str]) -> bool:
    letters = {ch for w in words for ch in w}
    if set(order) != letters or len(order) != len(letters):
        return False
    pos = {ch: i for i, ch in enumerate(order)}
    return all([pos[c] for c in w1] <= [pos[c] for c in w2] for w1, w2 in zip(words, words[1:]))


if __name__ == "__main__":
    s = Solution()
    for words in (["wrt", "wrf", "er", "ett", "rftt"], ["z", "x"], ["z", "z"], ["ab", "adc"]):
        got, bf = s.alienOrder(words), brute_force(words)
        assert valid(got, words) and valid(bf, words), (words, got, bf)
    assert s.alienOrder(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    for words in (["z", "x", "z"], ["abc", "ab"]):
        assert s.alienOrder(words) == "" and brute_force(words) == ""
    print("ok")
