"""
Couples Holding Hands (LeetCode 765)  — Hard
Pattern: Union-Find (disjoint set union)

Problem
-------
2n people sit in a row; person 2k and 2k+1 are a couple. A swap exchanges any two people.
Return the minimum number of swaps so that every couple sits side by side in a pair of seats
(2i, 2i+1).
Example: row = [0,2,1,3] -> 1 (swap seats 1 and 2). row = [3,2,0,1] -> 0.

Brute force
-----------
Breadth-first search over seatings: from the current row generate every one of the C(2n, 2)
swaps, and stop at the first row in which all couples are adjacent. The state space is (2n)!
permutations, so this is exponential in time and space. The wasted work: almost all swaps move
people who are already with their partner or who do not fix anything, and the search explores
every such dead end.

From brute force to optimal
---------------------------
Look at couples instead of people. Person p belongs to couple p // 2. Build a graph whose nodes
are the n couples and which has one edge per couch (seats 2i, 2i+1) joining the two couples
seated there. Every couple has two members, so every node has degree exactly 2 and the graph
decomposes into disjoint cycles. A couch already holding a couple is a self-loop (cycle of
length 1, 0 swaps). A cycle of k couples spans k couches and can be fixed with k-1 swaps: each
swap seats one couple correctly and shrinks the cycle by one, and no single swap can finish two
couples at once without touching two cycles, so k-1 is also a lower bound. Summing k-1 over
cycles gives n - (#cycles). Counting cycles is union-find over the n couples, O(n alpha(n)); the
equally valid greedy "fix seat 2i by swapping its partner in" gives the same count in O(n) with
a position table, but union-find exposes WHY the count is optimal.

Intuition
---------
Each couple is a node; each couch is an edge between the two couples sitting on it. The mess is
a set of cycles, and untangling a cycle of k couples takes exactly k-1 swaps. So the answer is
(number of couples) - (number of cycles): the more fragmented the seating, the fewer swaps it
needs.

Geometric view
--------------
Draw n dots (couples). For each couch, draw a cord between the couples of the two people on it.
A couch seating a real couple gives a cord from a dot to itself: done. Everything else forms
closed loops of dots. Count loops: each loop of k dots costs k-1 swaps, so the total is n minus
the number of loops (self-loops included).

Steps
-----
1. n = len(row) // 2 couples; parent = list(range(n)); components = n.
2. For each couch (seats i, i+1 with i even): couples a = row[i] // 2, b = row[i+1] // 2.
3. union(a, b): if their roots differ, link them and components -= 1.
4. Return n - components.

Complexity: O(n alpha(n)) time, O(n) space — one union per couch with path compression.
Pitfalls: unioning the two seat indices instead of the two couple ids (uses the wrong node set);
          counting cycles as edges - nodes instead of n - components; forgetting that a couch
          already holding a couple is a self-loop that must still count as one component.
"""
from collections import deque
from typing import List


class Solution:
    def minSwapsCouples(self, row: List[int]) -> int:
        n = len(row) // 2                    # nodes = couples; each couch is an edge
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]   # path halving
                x = parent[x]
            return x

        components = n
        for i in range(0, len(row), 2):
            a, b = find(row[i] // 2), find(row[i + 1] // 2)   # couple ids on this couch
            if a != b:
                parent[a] = b
                components -= 1
        return n - components                # each cycle of k couples costs k-1 swaps


def brute_force(row: List[int]) -> int:
    """BFS over seatings, one swap per edge; exponential state space (2n)!."""
    def solved(state: tuple) -> bool:
        return all(state[i] // 2 == state[i + 1] // 2 for i in range(0, len(state), 2))

    start = tuple(row)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if solved(cur):
            return dist[cur]
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                nxt = list(cur)
                nxt[i], nxt[j] = nxt[j], nxt[i]
                nxt = tuple(nxt)
                if nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    queue.append(nxt)
    return -1


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([0, 2, 1, 3], 1),
        ([3, 2, 0, 1], 0),
        ([0, 1], 0),                          # edge: a single couple
        ([5, 4, 2, 6, 3, 1, 0, 7], 2),
        ([1, 4, 0, 5, 8, 7, 6, 3, 2, 9], 3),
    ]
    for row, want in cases:
        assert s.minSwapsCouples(row[:]) == want, row
    for row, want in cases[:4]:
        assert brute_force(row) == want, row

    random.seed(765)
    for _ in range(40):
        n = random.randint(1, 3)
        row = list(range(2 * n))
        random.shuffle(row)
        assert s.minSwapsCouples(row[:]) == brute_force(row), row
    print("ok")
