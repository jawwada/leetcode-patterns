"""
Graph Valid Tree (LeetCode 261)  — Medium
Pattern: Union-Find (disjoint set union)

Problem
-------
Given n nodes 0..n-1 and a list of undirected edges, return True iff the edges form a
valid tree: connected and acyclic.
Example: n=5, [[0,1],[0,2],[0,3],[1,4]] -> True.  n=5, [[0,1],[1,2],[2,3],[1,3],[1,4]] -> False.

Brute force
-----------
Build the adjacency list. Check connectivity with one DFS from node 0 (all n reached?).
Check acyclicity by, for every edge (u, v), temporarily removing it and testing whether
v is still reachable from u -- if so, that edge closes a cycle. Each test is O(V + E) and
there are E tests -> O(E * (V + E)) time, O(V + E) space. The waste: each per-edge
reachability test re-walks essentially the whole graph.

From brute force to optimal
---------------------------
The redundancy is testing for cycles one edge at a time with full traversals.
Observation 1 (counting): a tree on n nodes has exactly n - 1 edges, so if
len(edges) != n - 1 the answer is False immediately; with exactly n - 1 edges,
"connected" and "acyclic" become equivalent, so we only need to check one.
Observation 2: a cycle appears exactly when an edge joins two nodes already in the same
component, which union-find detects in amortised near-O(1). So: edge count check, then
union all edges; if any union finds equal roots -> cycle -> False. Otherwise, n - 1
successful merges on n nodes leave one component -> True.

Intuition
---------
A tree is "just enough" edges to connect everything: n - 1 of them, none wasted on a
loop. Count the edges first. Then feed them to union-find: every edge must merge two
different components; the moment one does not, there is a cycle.

Geometric view
--------------
Picture n separate dots with self-pointing parent arrows. Each edge redirects one root
arrow to another root, gluing two trees into one. After n - 1 gluings with no "already
same root" collision, all dots hang under a single root: a tree. A collision means the
edge connected two dots already hanging under the same root -- that is a cycle.

Steps
-----
1. If len(edges) != n - 1: return False.
2. parent = list(range(n)); define find with path compression.
3. For each (u, v): if find(u) == find(v) return False; else union.
4. Return True.

Complexity: O(n * alpha(n)) time, O(n) space — n - 1 edges, each one find/union.
Pitfalls: skipping the edge-count check (then you must ALSO verify connectivity);
n = 1 with no edges is a valid tree; self-loops / duplicate edges appear as cycles and
the edge-count check or union collision catches them.
"""
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False  # a tree has exactly n-1 edges
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                return False  # edge joins an existing component to itself: cycle
            if rank[ru] < rank[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            if rank[ru] == rank[rv]:
                rank[ru] += 1
        return True  # n-1 merges with no collision => one component


def brute_force(n: int, edges: List[List[int]]) -> bool:
    # Connectivity via one DFS; acyclicity by removing each edge in turn and testing
    # whether its endpoints are still connected.
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def reachable(src: int, dst: int, skip: tuple) -> bool:
        seen, stack = {src}, [src]
        while stack:
            cur = stack.pop()
            if cur == dst:
                return True
            for nb in adj[cur]:
                if (cur, nb) in (skip, skip[::-1]):
                    continue
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        return False

    if not all(reachable(0, t, (-1, -1)) for t in range(n)):
        return False
    return not any(reachable(u, v, (u, v)) for u, v in edges)


if __name__ == "__main__":
    s = Solution()
    cases = (
        (5, [[0, 1], [0, 2], [0, 3], [1, 4]], True),
        (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], False),
        (1, [], True),
        (4, [[0, 1], [2, 3]], False),
        (3, [[0, 1], [1, 2], [2, 0]], False),
    )
    for n, e, want in cases:
        assert brute_force(n, e) == want
        assert s.validTree(n, e) == want
    print("ok")
