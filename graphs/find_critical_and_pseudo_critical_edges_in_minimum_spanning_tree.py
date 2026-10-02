"""
Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree (LeetCode 1489)  — Hard
Pattern: Kruskal MST (sorted edges + union-find)

Problem
-------
A weighted undirected connected graph on n nodes, edges[i] = [u, v, w]. An edge is
critical if deleting it raises the MST weight; pseudo-critical if it appears in some MST
but not all. Return [critical indices, pseudo-critical indices].
Example: n=5, edges=[[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
-> [[0,1],[2,3,4,5]].

Brute force
-----------
Enumerate every subset of n-1 edges, keep those that form a spanning tree, and find the
minimum total weight W. Critical edges appear in every tree of weight W; pseudo-critical
edges appear in at least one but not all. Exponential: O(C(E, n-1) * n) time, O(n) space.
The waste: almost all subsets are not trees or are far from minimal; Kruskal builds a
minimal tree directly, and the "every / some MST" questions can each be answered by a
single modified Kruskal run.

From brute force to optimal
---------------------------
The redundancy is enumerating trees. Observation 1 (Kruskal): sort edges by weight and
union-find them in order, taking each edge that joins two components; this yields an MST
of weight W in O(E log E). Observation 2: edge i is critical iff running Kruskal WITHOUT
edge i yields a weight > W (or fails to connect). Observation 3: edge i is pseudo-critical
iff it is not critical but FORCING it in first (union its endpoints, add its weight) and
then running Kruskal still yields exactly W -- some MST contains it. So one base run plus
two runs per edge -> O(E^2 log E), which beats enumeration by an exponential factor.

Intuition
---------
Kruskal is greedy and any MST can be produced by Kruskal with a suitable tie-break. If
excluding an edge forces a heavier tree, every MST needed it. If including it up front
costs nothing extra, at least one MST uses it. An edge that is neither is simply never in
an MST (it is too heavy for the cut it crosses).

Geometric view
--------------
Picture Kruskal as filling the graph from the lightest edge upward, like water rising
through a landscape of weights; the tree is the set of edges that first connect two
puddles. A critical edge is the only bridge at its water level between two puddles --
remove it and the puddles can only be joined later at a higher level. A pseudo-critical
edge is one of several equal-weight bridges that could have been chosen first.

Steps
-----
1. order = edge indices sorted by weight.
2. mst(skip, force): fresh union-find; if force >= 0 union its endpoints and add its weight;
   then walk order skipping `skip`, taking edges that merge components. Return the total
   if n-1 edges were used, else infinity.
3. base = mst(-1, -1).
4. For each i: if mst(skip=i) > base -> critical; elif mst(force=i) == base ->
   pseudo-critical.

Complexity: O(E^2 * log E) time, O(n) space — one sort, then two O(E * alpha(n)) Kruskal runs per edge.
Pitfalls: sorting the edge list in place and losing original indices (sort indices
instead); treating an edge as pseudo-critical without first ruling out critical; a run
that uses fewer than n-1 edges must count as infinite, not as a small weight.
"""
from itertools import combinations
from typing import List


class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        order = sorted(range(len(edges)), key=lambda i: edges[i][2])

        def mst(skip: int = -1, force: int = -1) -> float:
            parent = list(range(n))

            def find(x: int) -> int:
                while parent[x] != x:
                    parent[x] = parent[parent[x]]  # path halving
                    x = parent[x]
                return x

            total, used = 0, 0
            if force >= 0:
                u, v, w = edges[force]
                parent[u] = v  # pre-join the forced edge before any lighter edge
                total, used = w, 1
            for i in order:
                if i == skip:
                    continue
                u, v, w = edges[i]
                ru, rv = find(u), find(v)
                if ru != rv:
                    parent[ru] = rv
                    total += w
                    used += 1
            return total if used == n - 1 else float("inf")

        base = mst()
        critical, pseudo = [], []
        for i in range(len(edges)):
            if mst(skip=i) > base:
                critical.append(i)
            elif mst(force=i) == base:
                pseudo.append(i)
        return [critical, pseudo]


def brute_force(n: int, edges: List[List[int]]) -> List[List[int]]:
    # Enumerate every (n-1)-edge subset, keep the spanning trees of minimum weight, then
    # classify edges by whether they appear in all / some of them. Exponential.
    def is_tree(idxs) -> bool:
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for i in idxs:
            ru, rv = find(edges[i][0]), find(edges[i][1])
            if ru == rv:
                return False
            parent[ru] = rv
        return True

    best, trees = float("inf"), []
    for idxs in combinations(range(len(edges)), n - 1):
        if not is_tree(idxs):
            continue
        w = sum(edges[i][2] for i in idxs)
        if w < best:
            best, trees = w, [set(idxs)]
        elif w == best:
            trees.append(set(idxs))
    in_all = set.intersection(*trees)
    in_some = set.union(*trees)
    return [sorted(in_all), sorted(in_some - in_all)]


if __name__ == "__main__":
    s = Solution()
    cases = (
        (5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]], [[0, 1], [2, 3, 4, 5]]),
        (4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]], [[], [0, 1, 2, 3]]),
        (2, [[0, 1, 5]], [[0], []]),
        (4, [[0, 1, 1], [0, 2, 1], [0, 3, 1], [1, 2, 2], [2, 3, 2]], [[0, 1, 2], []]),
    )
    for n, e, want in cases:
        assert brute_force(n, e) == want
        assert s.findCriticalAndPseudoCriticalEdges(n, e) == want
    print("ok")
