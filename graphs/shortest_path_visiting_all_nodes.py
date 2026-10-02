"""
Shortest Path Visiting All Nodes (LeetCode 847)  — Hard
Pattern: BFS over augmented states (position + bitmask/budget)

Problem
-------
An undirected connected graph with n (<= 12) nodes is given as adjacency lists. Return the length
of the shortest walk that visits every node at least once; you may start anywhere and revisit
nodes and edges.
Example: [[1,2,3],[0],[0],[0]] -> 4 (1-0-2-0-3).  [[1],[0,2,4],[1,3,4],[2],[1,2]] -> 4 (0-1-4-2-3).

Brute force
-----------
Precompute all-pairs shortest distances with a BFS from each node, then try every order in which
the nodes could be visited for the first time: the walk cost of an order is the sum of pairwise
distances between consecutive nodes, and the answer is the minimum over all n! orders.
O(n! * n + n * (n + E)) time, O(n^2) space; exponential. The waste: orders that share the same
prefix are evaluated independently, and two prefixes that have visited the same SET of nodes and
stand on the same node are indistinguishable from then on, yet (k!)-many of them are extended
separately.

From brute force to optimal
---------------------------
The redundancy is that the future of a partial walk depends only on (current node, set of visited
nodes), not on the order those nodes were visited in. Observation: with n <= 12 that set fits in a
12-bit mask, giving at most n * 2^n = 49152 states. Every step of the walk is one unit edge
between states ((u, mask) -> (v, mask | 1 << v)), so plain BFS finds the shortest walk; starting
anywhere is modelled by seeding the queue with all n states (i, 1 << i) at distance 0. The first
dequeued state whose mask is full is the answer. The visited set is on states, so revisiting a
node with a different mask is allowed (that is what makes revisits legal) while re-entering the
same state is cut.

Intuition
---------
This is the Travelling Salesman flavour of BFS: the graph is small, so expand the node into
(node, what-I-have-seen). Unit-weight edges mean BFS gives optimal distances, and the mask makes
"have I visited everything" a single comparison. Multi-source seeding avoids running n BFSs.

Geometric view
--------------
Stack 2^n copies of the graph, one per visited-mask, and draw an edge from copy mask at node u to
copy mask | bit(v) at node v for every graph edge (u, v). The BFS wave starts on all n nodes of
the n singleton copies and climbs toward the all-ones copy; the first time it touches any node in
that top copy, the depth is the answer.

    frontier d=0: (0,0001) (1,0010) (2,0100) (3,1000)
    frontier d=1: (1,0011) (2,0101) (3,1001) (0,0011)...
    ...
    first (x,1111) popped at d=4 -> answer 4

Steps
-----
1. full = (1 << n) - 1; if n == 1 return 0.
2. queue = all (i, 1 << i, 0); seen = the same (node, mask) pairs.
3. Pop (u, mask, d); for each neighbour v: nm = mask | 1 << v; if nm == full return d + 1.
4. If (v, nm) unseen, mark and push with d + 1.
5. The graph is connected so the loop always returns.

Complexity: O(n^2 * 2^n) time, O(n * 2^n) space — each of the n * 2^n states scans up to n
neighbours once.
Pitfalls: visited on nodes instead of (node, mask) (blocks the required revisits); forgetting the
n == 1 case (answer 0); starting from node 0 only; using DFS (not shortest).
"""
from collections import deque
from itertools import permutations
from typing import List


class Solution:
    def shortestPathLength(self, graph: List[List[int]]) -> int:
        n = len(graph)
        full = (1 << n) - 1
        if n == 1:
            return 0
        queue = deque((i, 1 << i, 0) for i in range(n))     # start anywhere, distance 0
        seen = {(i, 1 << i) for i in range(n)}
        while queue:
            u, mask, d = queue.popleft()
            for v in graph[u]:
                nm = mask | (1 << v)
                if nm == full:
                    return d + 1
                if (v, nm) not in seen:                       # a node may repeat, a state may not
                    seen.add((v, nm))
                    queue.append((v, nm, d + 1))
        return -1                                             # unreachable: graph is connected


def brute_force(graph: List[List[int]]) -> int:
    # All-pairs BFS distances, then the best of all n! first-visit orders.
    n = len(graph)
    dist = [[-1] * n for _ in range(n)]
    for src in range(n):
        dist[src][src], queue = 0, deque([src])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if dist[src][v] < 0:
                    dist[src][v] = dist[src][u] + 1
                    queue.append(v)
    return min(sum(dist[a][b] for a, b in zip(order, order[1:]))   # n! orders, prefixes shared
               for order in permutations(range(n)))


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 2, 3], [0], [0], [0]], 4),
        ([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]], 4),
        ([[]], 0),                                                   # single node
        ([[1], [0]], 1),
        ([[1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5]], 6),    # path: walk straight through
        ([[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]], 5),               # triangle with two leaves
    )
    for g, want in cases:
        assert s.shortestPathLength(g) == want, g
        assert brute_force(g) == want, g
    print("ok")
