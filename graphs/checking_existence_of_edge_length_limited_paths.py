"""
Checking Existence of Edge Length Limited Paths (LeetCode 1697)  — Hard
Pattern: Union-Find (disjoint set union)

Problem
-------
An undirected graph on n nodes with weighted edgeList (parallel edges allowed) and queries
[p, q, limit]. For each query, answer whether a path exists from p to q using only edges of
weight strictly less than limit. Return the boolean answers in query order.
Example: n=3, edgeList=[[0,1,2],[1,2,4],[2,0,8],[1,0,16]], queries=[[0,1,2],[0,2,5]]
-> [false, true].

Brute force
-----------
For every query, BFS from p over only the edges whose weight < limit and check whether q is
reached. O(Q * (n + E)) time, O(n + E) space. The waste: two queries with similar limits
rebuild nearly identical connectivity; the BFS redoes the same component discovery from
scratch Q times.

From brute force to optimal
---------------------------
The redundancy is recomputing connectivity under a threshold for each query. Observation:
the graph "edges with weight < limit" only GROWS as limit increases -- components merge,
never split. So answer the queries OFFLINE in increasing order of limit, maintaining one
union-find into which edges are added in increasing weight order; before answering a query
with limit L, add every unseen edge with weight < L. Each edge is added once, each query
is a single find/find comparison -> O((E + Q) log(E + Q)) from the two sorts.

Intuition
---------
Sort edges by weight and queries by limit, then sweep a weight threshold upward. A pointer
j walks the edges; whenever the next query's limit exceeds edgeList[j].weight, union that
edge and advance. The query is then answered by find(p) == find(q). Because results must
be returned in the original order, sort query INDICES and write each answer into its slot.

Geometric view
--------------
Picture the edges laid along a number line by weight and the queries as flags planted at
their limits. Sweep from left to right: every edge you pass gets glued into the union-find,
and every flag you reach asks "are p and q in the same glued blob right now?". Nothing
ever has to be un-glued because the threshold only moves right.

Steps
-----
1. edges = edgeList sorted by weight; order = query indices sorted by limit.
2. parent = identity array; j = 0; ans = [False] * Q.
3. For qi in order: while edges[j].weight < limit, union its endpoints, j += 1.
4. ans[qi] = find(p) == find(q).
5. Return ans.

Complexity: O(E log E + Q log Q) time, O(n + Q) space — two sorts dominate; the sweep is near-linear with union-find.
Pitfalls: using <= instead of strictly < for the limit; sorting queries and then returning
answers in sorted order instead of original order; resetting the union-find per query
(that is the brute force again).
"""
from typing import List


class Solution:
    def distanceLimitedPathsExist(self, n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        edges = sorted(edgeList, key=lambda e: e[2])
        order = sorted(range(len(queries)), key=lambda i: queries[i][2])
        ans = [False] * len(queries)
        j = 0
        for qi in order:
            p, q, limit = queries[qi]
            while j < len(edges) and edges[j][2] < limit:
                u, v, _ = edges[j]
                parent[find(u)] = find(v)  # every edge lighter than this limit is glued in
                j += 1
            ans[qi] = find(p) == find(q)
        return ans


def brute_force(n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
    # Per query: BFS over only the edges with weight < limit.
    ans = []
    for p, q, limit in queries:
        adj = [[] for _ in range(n)]
        for u, v, w in edgeList:
            if w < limit:
                adj[u].append(v)
                adj[v].append(u)
        seen, stack = {p}, [p]
        while stack:
            for nb in adj[stack.pop()]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        ans.append(q in seen)
    return ans


if __name__ == "__main__":
    s = Solution()
    cases = (
        (3, [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]], [[0, 1, 2], [0, 2, 5]], [False, True]),
        (5, [[0, 1, 10], [1, 2, 5], [2, 3, 9], [3, 4, 13]], [[0, 4, 14], [1, 4, 13]], [True, False]),
        (3, [[0, 1, 5], [0, 1, 1]], [[0, 1, 2], [1, 2, 100]], [True, False]),
        (2, [], [[0, 1, 1]], [False]),
    )
    for n, e, q, want in cases:
        assert brute_force(n, e, q) == want
        assert s.distanceLimitedPathsExist(n, e, q) == want
    print("ok")
