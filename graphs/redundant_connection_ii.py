"""
Redundant Connection II (LeetCode 685)  — Hard
Pattern: Union-Find (disjoint set union)

Problem
-------
A rooted tree on nodes 1..n (every node except the root has exactly one parent) had one
extra DIRECTED edge u -> v added, giving n edges. Return the edge whose removal restores a
rooted tree; if several work, return the one appearing last in the input.
Example: [[1,2],[1,3],[2,3]] -> [2,3].  [[1,2],[2,3],[3,4],[4,1],[1,5]] -> [4,1].

Brute force
-----------
For each edge, from last to first, delete it and test whether the remaining n-1 edges form
a rooted tree: exactly one node has in-degree 0, every other node has in-degree 1, and all
n nodes are reachable from the root. Each test is O(n), done up to n times -> O(n^2) time,
O(n) space. The waste: n near-identical reachability walks, when the shape of the fault is
fixed by one quick scan of in-degrees.

From brute force to optimal
---------------------------
The redundancy is testing every edge when only one or two edges can possibly be at fault.
Observation: adding one edge to a rooted tree produces exactly one of two defects --
(A) some node v now has two parents (in-degree 2), or (B) no node has in-degree 2 but a
directed cycle through the root was formed. In case (A) only the two edges into v are
candidates: cand1 (earlier) and cand2 (later). Drop cand2 provisionally and union-find the
rest: if no cycle appears, cand2 was the culprit; if a cycle still appears, cand1 is. In
case (B) there are no candidates and the answer is simply the edge that closes the cycle
under union-find, as in Redundant Connection I. One in-degree scan plus one union-find
pass -> O(n * alpha(n)).

Intuition
---------
First ask "does any node have two parents?" If yes, one of those two edges must go; prefer
the later one unless removing it leaves a cycle, in which case the earlier one is the
real problem. If no node has two parents, the extra edge made a cycle, and the first edge
union-find sees that joins two already-connected nodes is the one to remove.

Geometric view
--------------
Picture the tree hanging from its root. The extra arrow either lands on a node that
already has an arrow coming in (a node with two incoming arrows: cut one of them) or lands
on the root, making a loop that runs up the trunk and back down (cut the arrow that closes
the loop). Union-find, ignoring direction, detects the loop; the in-degree scan detects the
double arrow.

Steps
-----
1. Scan edges, recording parent_of[v]. On a second parent for v, set cand1 = earlier edge,
   cand2 = this edge.
2. Union-find over all edges except cand2.
3. If a union finds u and v already connected: return cand1 if cand2 exists, else [u, v].
4. If no cycle appeared, return cand2.

Complexity: O(n * alpha(n)) time, O(n) space — one in-degree scan and one union-find pass.
Pitfalls: returning cand2 blindly without checking the cycle (fails when cand1 is on the
cycle); skipping BOTH candidates in the union-find pass; treating the problem as
undirected (case B with a directed cycle through the root needs the in-degree test first).
"""
from typing import List


class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent_of = [0] * (n + 1)
        cand1 = cand2 = None
        for u, v in edges:
            if parent_of[v]:
                cand1, cand2 = [parent_of[v], v], [u, v]  # v has two parents
            else:
                parent_of[v] = u

        uf = list(range(n + 1))

        def find(x: int) -> int:
            while uf[x] != x:
                uf[x] = uf[uf[x]]  # path halving
                x = uf[x]
            return x

        for u, v in edges:
            if [u, v] == cand2:
                continue  # provisionally drop the later of the two parent edges
            ru, rv = find(u), find(v)
            if ru == rv:
                return cand1 if cand2 else [u, v]  # cycle survives: blame the earlier edge
            uf[rv] = ru
        return cand2


def brute_force(edges: List[List[int]]) -> List[int]:
    # Try removing each edge (last to first); accept the first leftover that is a rooted tree.
    n = len(edges)
    for skip in range(n - 1, -1, -1):
        kept = [e for i, e in enumerate(edges) if i != skip]
        indeg = [0] * (n + 1)
        children = [[] for _ in range(n + 1)]
        for u, v in kept:
            indeg[v] += 1
            children[u].append(v)
        roots = [x for x in range(1, n + 1) if indeg[x] == 0]
        if len(roots) != 1 or any(indeg[x] != 1 for x in range(1, n + 1) if x != roots[0]):
            continue
        seen, stack = {roots[0]}, [roots[0]]
        while stack:
            for c in children[stack.pop()]:
                if c not in seen:
                    seen.add(c)
                    stack.append(c)
        if len(seen) == n:
            return edges[skip]
    return []


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 2], [1, 3], [2, 3]], [2, 3]),
        ([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]], [4, 1]),
        ([[2, 1], [3, 1], [4, 2], [1, 4]], [2, 1]),
        ([[4, 2], [1, 5], [5, 2], [5, 3], [2, 4]], [4, 2]),
        ([[1, 2], [2, 1]], [2, 1]),
    )
    for e, want in cases:
        assert brute_force(e) == want, (e, brute_force(e))
        assert s.findRedundantDirectedConnection(e) == want, (e, s.findRedundantDirectedConnection(e))
    print("ok")
