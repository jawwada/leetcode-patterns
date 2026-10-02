"""
Clone Graph (LeetCode 133)  — Medium
Pattern: Graph traversal with old->new node map

Problem
-------
Given a reference to a node in a connected undirected graph (each node has `val` and a
list `neighbors`), return a deep copy of the graph. Node values are 1..n and unique.
Example: adjacency [[2,4],[1,3],[2,4],[1,3]] -> an identical but freshly allocated graph.

Brute force
-----------
Two passes with no mapping: first traverse the graph to collect every node, create a new
node for each, then for every original edge (u, v) linearly search the list of new nodes
for the one whose val matches v and append it. The search is the waste: each of the E
edge endpoints scans up to V nodes -> O(V*E) time, O(V) space.

From brute force to optimal
---------------------------
The redundancy is the linear lookup "which clone corresponds to this original node?".
Observation: that is a pure key -> value question, so a hash map old_node -> clone answers
it in O(1). Once the map exists, cloning and wiring can even happen in a single traversal:
when we first meet an original node we create its clone and store it; when we meet it
again (via another edge) we just look it up. The map doubles as the visited set, which
is also what stops the traversal from looping forever on cycles.

Intuition
---------
Walk the graph once. For each node, make sure its clone exists (create on first sight),
then for each neighbour make sure the neighbour's clone exists and link clone -> clone.
The map is the only state; it guarantees every original node maps to exactly one clone,
so shared neighbours and cycles are copied correctly.

Geometric view
--------------
Picture the original graph and a "shadow" graph growing beside it. A BFS frontier sweeps
the original; each time the frontier touches a node it casts a shadow node (if not already
cast) and draws a shadow edge parallel to the original edge. When the frontier has swept
everything, the shadow is a complete isomorphic copy.

Steps
-----
1. If node is None return None.
2. Create clones = {node: Node(node.val)} and a queue with node.
3. Pop u; for each neighbour v: if v not in clones, clone it and enqueue v.
4. Append clones[v] to clones[u].neighbors.
5. Return clones[node].

Complexity: O(V + E) time, O(V) space — each node and edge is processed once; the map holds V entries.
Pitfalls: creating a clone twice for a node reached via two edges (always check the map first);
appending the ORIGINAL neighbour instead of its clone; forgetting the None input.
"""
from collections import deque
from typing import List, Optional


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if node is None:
            return None
        clones = {node: Node(node.val)}  # original -> copy; also the visited set
        queue = deque([node])
        while queue:
            cur = queue.popleft()
            for nb in cur.neighbors:
                if nb not in clones:
                    clones[nb] = Node(nb.val)
                    queue.append(nb)
                clones[cur].neighbors.append(clones[nb])
        return clones[node]


def brute_force(node: Optional[Node]) -> Optional[Node]:
    # Pass 1: collect all original nodes. Pass 2: build clones in a list.
    # Pass 3: for every edge, linearly scan the clone list to find the matching endpoint.
    if node is None:
        return None
    originals, stack = [], [node]
    while stack:
        cur = stack.pop()
        if cur in originals:
            continue
        originals.append(cur)
        stack.extend(cur.neighbors)
    copies = [Node(o.val) for o in originals]
    for o, c in zip(originals, copies):
        for nb in o.neighbors:
            c.neighbors.append(next(cp for cp in copies if cp.val == nb.val))
    return copies[0]


def build(adj: List[List[int]]) -> Optional[Node]:
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nbs in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nbs]
    return nodes[0]


def to_adj(node: Optional[Node]) -> List[List[int]]:
    if node is None:
        return []
    seen, out, stack = {}, {}, [node]
    while stack:
        cur = stack.pop()
        if cur.val in seen:
            continue
        seen[cur.val] = cur
        out[cur.val] = sorted(n.val for n in cur.neighbors)
        stack.extend(cur.neighbors)
    return [out[k] for k in sorted(out)]


def all_fresh(orig: Optional[Node], copy: Optional[Node]) -> bool:
    # every node reachable in the copy must be a different Python object from every original
    def nodes(n):
        seen, st = set(), [n]
        while st:
            c = st.pop()
            if id(c) in seen:
                continue
            seen.add(id(c))
            st.extend(c.neighbors)
        return seen

    return orig is None or not (nodes(orig) & nodes(copy))


if __name__ == "__main__":
    s = Solution()
    for adj in ([[2, 4], [1, 3], [2, 4], [1, 3]], [[]], [], [[2], [1, 3], [2]]):
        o = build(adj)
        c = s.cloneGraph(o)
        assert to_adj(c) == adj and all_fresh(o, c)
        b = brute_force(build(adj))
        assert to_adj(b) == to_adj(c)
    print("ok")
