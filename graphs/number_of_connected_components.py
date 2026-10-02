"""
Number of Connected Components in an Undirected Graph (LeetCode 323)  — Medium
Pattern: Union-Find (disjoint set union)

Problem
-------
Given n nodes 0..n-1 and a list of undirected edges, return the number of connected
components.
Example: n=5, edges=[[0,1],[1,2],[3,4]] -> 2.  n=5, edges=[[0,1],[1,2],[2,3],[3,4]] -> 1.

Brute force
-----------
For every node, DFS over the adjacency list with a FRESH visited set and collect the set
of nodes reached; count a node only if it is the smallest id in its component. Each DFS
is O(V + E) and there are V of them -> O(V*(V+E)) time, O(V) space. The waste is walking
the same component once per node it contains.

From brute force to optimal
---------------------------
The redundancy is re-discovering a component from each of its members. Two fixes exist.
(1) Share one visited set: a DFS from an unvisited node explores its whole component and
marks it, so no member starts another DFS; count the DFS launches -> O(V + E). (2) Avoid
building the graph at all: start with n singleton components and process edges with
union-find; every union that actually merges two different roots reduces the component
count by one. Union-find needs only the edge list, is O(E * alpha(n)), and extends to
streaming/dynamic edges, which is why interviewers like it here.

Intuition
---------
Start by assuming every node is its own component (count = n). Each edge is a merge
request: if its endpoints are already in the same set the edge changes nothing;
otherwise it glues two components together and count drops by one. After all edges,
count is the answer.

Geometric view
--------------
Draw n dots, each labelled with its own id as "parent". Processing an edge draws an arrow
from one root to the other, so the two trees of parent pointers become one tree. The
number of dots that still point to themselves (roots) is the number of components; we
track it with a counter instead of rescanning.

Steps
-----
1. parent = list(range(n)); count = n.
2. For each edge (u, v): ru, rv = find(u), find(v).
3. If ru != rv: parent[rv] = ru (by rank), count -= 1.
4. Return count.

Complexity: O(V + E * alpha(V)) time, O(V) space — each edge is one find/union; parent array of size V.
Pitfalls: counting edges that connect already-joined nodes; forgetting isolated nodes
(they are components too, hence start count at n); recursion-depth find on long chains
without compression.
"""
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        count = n  # every node starts as its own component
        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                continue
            if rank[ru] < rank[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            if rank[ru] == rank[rv]:
                rank[ru] += 1
            count -= 1
        return count


def brute_force(n: int, edges: List[List[int]]) -> int:
    # DFS from every node with a private visited set; count the node only if it is the
    # smallest id in the component it reaches.
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    count = 0
    for start in range(n):
        seen, stack = {start}, [start]
        while stack:
            cur = stack.pop()
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if min(seen) == start:
            count += 1
    return count


if __name__ == "__main__":
    s = Solution()
    cases = (
        (5, [[0, 1], [1, 2], [3, 4]], 2),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]], 1),
        (1, [], 1),
        (4, [], 4),
        (4, [[0, 1], [1, 0], [2, 3], [0, 1]], 2),
    )
    for n, e, want in cases:
        assert brute_force(n, e) == want
        assert s.countComponents(n, e) == want
    print("ok")
