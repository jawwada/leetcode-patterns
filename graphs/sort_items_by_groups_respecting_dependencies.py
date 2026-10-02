"""
Sort Items by Groups Respecting Dependencies (LeetCode 1203)  — Hard
Pattern: Topological sort (Kahn's BFS) / cycle detection

Problem
-------
n items; item i belongs to group[i] (or -1 for no group, m groups total). beforeItems[i]
lists items that must come before i. Return an ordering of all items such that items of the
same group are adjacent and every before-constraint holds, or [] if impossible.
Example: n=8, m=2, group=[-1,-1,1,0,0,1,0,-1],
beforeItems=[[],[6],[5],[6],[3,6],[],[],[]] -> [6,3,4,1,5,2,0,7] (one valid answer).

Brute force
-----------
Enumerate every permutation of the n items and keep the first one in which each group's
items are contiguous and every (before, after) pair is in the right order. Exponential:
O(n! * (n + E)) time, O(n) space. The waste: a permutation that violates a constraint
early is still generated in full, and the same violation is re-checked across the
(n-k)! permutations sharing its prefix.

From brute force to optimal
---------------------------
The redundancy is searching over orderings when the constraints already dictate a valid
one greedily. Observation 1: ignoring groups, "x before y" edges form a DAG whose any
topological order is valid, found in O(n + E) by Kahn's algorithm (repeatedly emit a node
of in-degree 0). Observation 2: the group-contiguity rule is itself a dependency between
GROUPS -- if x (group A) must precede y (group B != A), then all of A precedes all of B.
So topologically sort the groups too, then output groups in that order, each group's
items in the item-level order. Items with group -1 each get a fresh singleton group so
they behave like any other block. Either sort hitting a cycle means [].

Intuition
---------
Two Kahn passes. Item graph: u -> v for each u in beforeItems[v]. Group graph: group[u] ->
group[v] whenever the groups differ. If both graphs are acyclic, bucket the item order by
group and concatenate buckets in group order: within a bucket the item order already
respects intra-group constraints, and across buckets the group order respects every
inter-group constraint.

Geometric view
--------------
Picture each group as a box and items as beads inside the boxes. An arrow between beads of
different boxes forces the whole first box left of the whole second box; arrows inside a
box only order beads within it. Sorting the boxes (coarse) then pouring beads in the
already-sorted item order (fine) lays everything on one line with no arrow pointing
backwards.

Steps
-----
1. Give every item with group -1 a new unique group id; m grows accordingly.
2. Build item adjacency and in-degrees; build group adjacency and in-degrees for cross-group
   edges.
3. topo(adj, deg): queue all zero in-degree nodes, pop, decrement children, enqueue zeros;
   fail if fewer than all nodes were emitted.
4. If either sort fails, return [].
5. Bucket the item order by group; concatenate buckets in group order.

Complexity: O(n + m + E) time, O(n + m + E) space — two linear Kahn passes over item and group graphs.
Pitfalls: forgetting to assign singleton groups to -1 items (they would all collapse into
one fake group); adding a group self-edge when u and v share a group (creates a bogus
cycle); duplicate group edges are fine as long as in-degree is incremented per edge.
"""
from itertools import permutations
from typing import List


class Solution:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        group = group[:]
        for i in range(n):
            if group[i] == -1:
                group[i], m = m, m + 1  # fresh singleton group
        item_adj = [[] for _ in range(n)]
        item_deg = [0] * n
        group_adj = [[] for _ in range(m)]
        group_deg = [0] * m
        for v in range(n):
            for u in beforeItems[v]:
                item_adj[u].append(v)
                item_deg[v] += 1
                if group[u] != group[v]:
                    group_adj[group[u]].append(group[v])
                    group_deg[group[v]] += 1

        def topo(adj: List[List[int]], deg: List[int]) -> List[int]:
            order = [x for x in range(len(deg)) if deg[x] == 0]
            for u in order:  # list grows while iterating: it doubles as the queue
                for v in adj[u]:
                    deg[v] -= 1
                    if deg[v] == 0:
                        order.append(v)
            return order if len(order) == len(deg) else []

        item_order = topo(item_adj, item_deg)
        group_order = topo(group_adj, group_deg)
        if not item_order or not group_order:
            return []
        buckets = [[] for _ in range(m)]
        for i in item_order:
            buckets[group[i]].append(i)
        return [i for g in group_order for i in buckets[g]]


def brute_force(n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
    # Try every permutation; return the first that keeps groups contiguous and respects
    # all before-constraints. Exponential: n! orderings.
    for perm in permutations(range(n)):
        pos = {item: idx for idx, item in enumerate(perm)}
        if any(pos[u] > pos[v] for v in range(n) for u in beforeItems[v]):
            continue
        contiguous = True
        for g in set(group) - {-1}:
            idxs = [pos[i] for i in range(n) if group[i] == g]
            if max(idxs) - min(idxs) + 1 != len(idxs):
                contiguous = False  # a foreign item sits inside this group's run
                break
        if contiguous:
            return list(perm)
    return []


def is_valid(n, group, beforeItems, order):
    if sorted(order) != list(range(n)):
        return False
    pos = {item: idx for idx, item in enumerate(order)}
    if any(pos[u] > pos[v] for v in range(n) for u in beforeItems[v]):
        return False
    for g in set(group) - {-1}:
        idxs = [pos[i] for i in range(n) if group[i] == g]
        if max(idxs) - min(idxs) + 1 != len(idxs):
            return False
    return True


if __name__ == "__main__":
    s = Solution()
    cases = (
        (8, 2, [-1, -1, 1, 0, 0, 1, 0, -1], [[], [6], [5], [6], [3, 6], [], [], []], True),
        (8, 2, [-1, -1, 1, 0, 0, 1, 0, -1], [[], [6], [5], [6], [3], [], [4], []], False),
        (3, 1, [0, -1, 0], [[], [0], [1]], False),
        (4, 2, [0, 1, 0, 1], [[], [], [1], []], True),
        (1, 1, [-1], [[]], True),
    )
    for n, m, group, before, possible in cases:
        got = s.sortItems(n, m, group, before)
        bf = brute_force(n, m, group, before)
        assert bool(got) == bool(bf) == possible
        if possible:
            assert is_valid(n, group, before, got) and is_valid(n, group, before, bf)
    print("ok")
