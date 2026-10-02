"""
Remove Max Number of Edges to Keep Graph Fully Traversable (LeetCode 1579)  — Hard
Pattern: Union-Find (disjoint set union)

Problem
-------
n nodes 1..n and edges [type, u, v]: type 1 only Alice can use, type 2 only Bob, type 3
both. Return the maximum number of edges that can be removed so that Alice and Bob can
each still reach every node, or -1 if that is impossible even with all edges.
Example: n=4, edges=[[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]] -> 2.

Brute force
-----------
Try every subset of edges to delete; for each, check with BFS that Alice's graph (types 1
and 3) and Bob's graph (types 2 and 3) are both connected, and keep the largest valid
subset. Exponential: O(2^E * (n + E)) time, O(n + E) space. The waste: almost every subset
is either obviously disconnected or dominated by another subset; the problem has a greedy
structure (a spanning forest per player) that enumeration ignores.

From brute force to optimal
---------------------------
The redundancy is enumerating subsets when the answer is "edges minus a minimal set that
keeps both players connected". Observation 1: each player needs only a spanning tree of
their usable edges, and union-find can grow one greedily -- an edge is kept iff it joins
two different components (as in Kruskal). Observation 2: a type-3 edge serves both players
at once, so it is never worse than a type-1 or type-2 edge covering the same join; process
all type-3 edges FIRST into both forests, then fill the remaining gaps with type-1 edges
(Alice) and type-2 edges (Bob). Count kept edges; if either forest ends with more than one
component return -1, else answer = E - kept. O(E * alpha(n)).

Intuition
---------
Run two union-finds, one per player. Every type-3 edge that merges two components in
Alice's forest also merges them in Bob's (both forests have seen exactly the same type-3
edges so far), so keep it once and count it once. Then a type-1 edge is kept only if it
still merges something for Alice, a type-2 edge only if it merges for Bob. Kept edges are
the minimum needed; everything else is removable.

Geometric view
--------------
Picture two transparent sheets (Alice, Bob) laid over the same dots. A type-3 edge draws a
line on both sheets at once; type 1 draws on Alice's sheet only, type 2 on Bob's. You want
each sheet to show one connected drawing using as few lines as possible. Draw the shared
lines first because each one earns credit on both sheets; then patch the gaps on each sheet
individually.

Steps
-----
1. alice = bob = identity parent arrays of size n + 1; kept = 0.
2. For each type-3 edge: if union(alice, u, v) succeeds, also union(bob, u, v); kept += 1.
3. For each type-1 edge: if union(alice, u, v) succeeds, kept += 1. Same for type 2 / bob.
4. If alice or bob has more than one root among 1..n, return -1.
5. Return len(edges) - kept.

Complexity: O(E * alpha(n)) time, O(n) space — each edge does O(1) amortised finds/unions in two arrays.
Pitfalls: processing type-1/2 edges before type-3 (greedy order matters); counting a type-3
edge twice (once per forest); returning -1 only when Alice is disconnected but forgetting
Bob; 1-indexed nodes.
"""
from itertools import combinations
from typing import List


class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        def find(parent: List[int], x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        def union(parent: List[int], a: int, b: int) -> bool:
            ra, rb = find(parent, a), find(parent, b)
            if ra == rb:
                return False  # edge is redundant in this forest
            parent[rb] = ra
            return True

        alice, bob = list(range(n + 1)), list(range(n + 1))
        kept = 0
        for t, u, v in edges:
            if t == 3 and union(alice, u, v):
                union(bob, u, v)  # both forests have seen the same type-3 edges: this merges too
                kept += 1
        for t, u, v in edges:
            if (t == 1 and union(alice, u, v)) or (t == 2 and union(bob, u, v)):
                kept += 1
        for forest in (alice, bob):
            if len({find(forest, x) for x in range(1, n + 1)}) > 1:
                return -1
        return len(edges) - kept


def brute_force(n: int, edges: List[List[int]]) -> int:
    # Try every subset of edges to KEEP (smallest first); the first subset that connects
    # both players gives the answer E - |subset|. Exponential in E.
    def connected(kept_edges, ok_types):
        adj = {x: [] for x in range(1, n + 1)}
        for t, u, v in kept_edges:
            if t in ok_types:
                adj[u].append(v)
                adj[v].append(u)
        seen, stack = {1}, [1]
        while stack:
            for nb in adj[stack.pop()]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        return len(seen) == n

    for size in range(len(edges) + 1):
        for subset in combinations(edges, size):
            if connected(subset, {1, 3}) and connected(subset, {2, 3}):
                return len(edges) - size
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = (
        (4, [[3, 1, 2], [3, 2, 3], [1, 1, 3], [1, 2, 4], [1, 1, 2], [2, 3, 4]], 2),
        (4, [[3, 1, 2], [3, 2, 3], [1, 1, 4], [2, 1, 4]], 0),
        (4, [[3, 2, 3], [1, 1, 2], [2, 3, 4]], -1),
        (3, [[1, 1, 2], [2, 1, 2], [1, 2, 3], [2, 2, 3], [3, 1, 3]], 2),
        (1, [], 0),
    )
    for n, e, want in cases:
        assert brute_force(n, e) == want
        assert s.maxNumEdgesToRemove(n, e) == want
    print("ok")
