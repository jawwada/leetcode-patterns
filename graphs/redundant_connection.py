"""
Redundant Connection (LeetCode 684)  — Medium
Pattern: Union-Find (disjoint set union)

Problem
-------
A tree with n nodes (1..n) had one extra edge added, giving n edges. Return the edge that
can be removed to make it a tree again; if several, return the one appearing last in the
input.
Example: [[1,2],[1,3],[2,3]] -> [2,3].  [[1,2],[2,3],[3,4],[1,4],[1,5]] -> [1,4].

Brute force
-----------
Process edges in order; before adding edge (u, v), run a DFS/BFS over the edges added so
far to test whether v is already reachable from u. The first edge whose endpoints are
already connected is the answer. Each reachability check costs O(n) and we may do it n
times -> O(n^2) time, O(n) space. The waste: every check re-walks the same growing
component from scratch instead of remembering which nodes are already connected.

From brute force to optimal
---------------------------
The redundancy is re-deriving connectivity that was already established by earlier edges.
Observation: the only question asked is "are u and v in the same connected component?",
and the components only ever MERGE, never split. That is exactly what a disjoint-set
union supports: find(u) == find(v) answers the question in near-O(1) amortised time (with
path compression + union by rank), and union(u, v) records the merge. One pass over the
edges -> O(n * alpha(n)).

Intuition
---------
Add edges one by one into a union-find. Each edge either joins two separate components
(fine, it is a tree edge) or connects two nodes already in the same component (it closes
a cycle). Because the input has exactly one extra edge, the first edge that closes a
cycle is the one to remove; since it is the latest edge processed among those on the
cycle, it is also the last in input order.

Geometric view
--------------
Picture the nodes as islands and each processed edge as a bridge. Union-find keeps one
"flag" node per island group (the root). When a new bridge connects two islands flying
different flags, lower one flag -- they are now one group. When a bridge connects two
islands already flying the same flag, you have built a loop: that bridge is redundant.

Steps
-----
1. parent[i] = i for i in 1..n.
2. find(x): follow parents to the root, compressing the path on the way back.
3. For each edge (u, v): if find(u) == find(v) return [u, v]; else union them.

Complexity: O(n * alpha(n)) time, O(n) space — near-constant per find/union with path compression.
Pitfalls: 1-indexed nodes (allocate n + 1); forgetting path compression (degrades to O(n)
per find on chains); returning the first cycle edge in input order is correct ONLY because
there is exactly one extra edge.
"""
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        parent = list(range(len(edges) + 1))
        rank = [0] * (len(edges) + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                return [u, v]  # u and v already connected: this edge closes the cycle
            if rank[ru] < rank[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            if rank[ru] == rank[rv]:
                rank[ru] += 1
        return []


def brute_force(edges: List[List[int]]) -> List[int]:
    # Before adding each edge, DFS over the edges added so far to see if its endpoints
    # are already connected.
    adj = {}
    for u, v in edges:
        seen, stack = {u}, [u]
        while stack:
            cur = stack.pop()
            if cur == v:
                return [u, v]
            for nb in adj.get(cur, ()):
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    return []


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 2], [1, 3], [2, 3]], [2, 3]),
        ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]], [1, 4]),
        ([[1, 2], [1, 3], [3, 2]], [3, 2]),
        ([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]], [2, 5]),
    )
    for e, want in cases:
        assert brute_force(e) == want
        assert s.findRedundantConnection(e) == want
    print("ok")
