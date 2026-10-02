"""
Critical Connections in a Network (LeetCode 1192)  — Hard
Pattern: Tarjan bridges (DFS low-link)

Problem
-------
n servers 0..n-1 are joined by undirected connections forming a connected graph. A
connection is critical if removing it disconnects some pair of servers. Return all
critical connections (any order).
Example: n=4, connections=[[0,1],[1,2],[2,0],[1,3]] -> [[1,3]].

Brute force
-----------
For every edge, delete it and run a BFS from node 0; if fewer than n nodes are reached the
edge was a bridge. E traversals of O(V + E) each -> O(E * (V + E)) time, O(V + E) space.
The waste: each BFS re-walks essentially the same graph; the information "is there another
route around this edge?" is recomputed from scratch for every edge instead of being read
off one traversal.

From brute force to optimal
---------------------------
The redundancy is testing each edge in isolation. Observation: in a DFS tree, a tree edge
(u, v) with v the child is a bridge exactly when nothing in v's subtree has a back edge to
u or above -- i.e. no way around the edge. Record disc[x] = DFS discovery time and
low[x] = the smallest disc value reachable from x's subtree using at most one back edge.
Then low[v] > disc[u] means the subtree under v cannot climb past u, so (u, v) is a bridge.
One DFS computes disc and low for every node -> O(V + E).

Intuition
---------
Number the nodes in the order DFS first visits them. While unwinding, every node reports
upward the earliest-visited node its subtree can reach "around the side" through a back
edge. If a child's subtree can reach something at or above the parent, there is a cycle
through the parent edge and it is safe; if it cannot even reach the parent, that edge is
the only link and is critical. Non-tree edges (to already-visited nodes) only lower low[];
they are never bridges themselves because they close a cycle.

Geometric view
--------------
Picture the DFS tree drawn top-down with disc increasing downwards, and back edges as
ropes tied from a deep node to an ancestor. low[v] is the highest point any rope from v's
subtree reaches. Cut the tree edge above v: the subtree stays attached iff some rope
reaches above the cut, i.e. low[v] <= disc[u]. Edges with no rope spanning them are the
bridges.

Steps
-----
1. Build adjacency; disc = [-1]*n, low = [0]*n, timer = 0.
2. dfs(u, parent): disc[u] = low[u] = timer; timer += 1.
3. For each neighbour v != parent: if unvisited, dfs(v, u), low[u] = min(low[u], low[v]),
   and if low[v] > disc[u] record (u, v); else low[u] = min(low[u], disc[v]).
4. dfs(0, -1); return the recorded bridges.

Complexity: O(V + E) time, O(V + E) space — one DFS; adjacency list plus disc/low arrays.
Pitfalls: using min(low[u], low[v]) for a BACK edge (must be disc[v], or articulation
logic breaks); skipping the parent by node rather than by edge id when parallel edges may
exist (not an issue here: connections are distinct); recursion depth on long chains --
raise the limit or go iterative.
"""
import sys
from typing import List


class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        sys.setrecursionlimit(max(n + 1000, 10**5))
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)
        disc = [-1] * n  # discovery time, -1 = unvisited
        low = [0] * n  # earliest discovery time reachable via subtree + one back edge
        bridges = []
        timer = 0

        def dfs(u: int, parent: int) -> None:
            nonlocal timer
            disc[u] = low[u] = timer
            timer += 1
            for v in adj[u]:
                if v == parent:
                    continue
                if disc[v] == -1:
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        bridges.append([u, v])  # subtree of v cannot climb above u
                else:
                    low[u] = min(low[u], disc[v])  # back edge to an ancestor

        dfs(0, -1)
        return bridges


def brute_force(n: int, connections: List[List[int]]) -> List[List[int]]:
    # Remove each edge in turn and BFS from 0; the edge is a bridge if not all n are reached.
    bridges = []
    for skip in range(len(connections)):
        adj = [[] for _ in range(n)]
        for i, (u, v) in enumerate(connections):
            if i != skip:
                adj[u].append(v)
                adj[v].append(u)
        seen, stack = {0}, [0]
        while stack:
            cur = stack.pop()
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if len(seen) < n:
            bridges.append(connections[skip])
    return bridges


if __name__ == "__main__":
    s = Solution()

    def canon(edges):
        return sorted(tuple(sorted(e)) for e in edges)

    cases = (
        (4, [[0, 1], [1, 2], [2, 0], [1, 3]], [[1, 3]]),
        (2, [[0, 1]], [[0, 1]]),
        (3, [[0, 1], [1, 2], [2, 0]], []),
        (6, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]], [[2, 3]]),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]], [[0, 1], [1, 2], [2, 3], [3, 4]]),
    )
    for n, conns, want in cases:
        assert canon(brute_force(n, conns)) == canon(want)
        assert canon(s.criticalConnections(n, conns)) == canon(want)
    print("ok")
