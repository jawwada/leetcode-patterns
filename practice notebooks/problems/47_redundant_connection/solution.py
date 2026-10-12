"""
Redundant Connection (LeetCode 684) - Medium
Area: graphs / union find
Key operations: find the root of each endpoint, compare roots, union by attaching one root under the other

A tree with n nodes labelled 1..n had one extra edge added, giving n undirected edges. Return the
edge that can be removed so that the result is a tree again; if several work, return the one that
appears last in the input.
Example: [[1,2],[2,3],[3,4],[1,4],[1,5]] -> [1,4]
"""
from collections import deque
from typing import List


# --- brute force ---
def brute_force(edges: List[List[int]]) -> List[int]:
    """Before adding each edge, BFS over the edges added so far to see whether its endpoints are
    already connected. O(n) per check, n checks: O(n^2). The waste: every check re-walks the same
    growing component from scratch instead of remembering which nodes are already joined."""
    adj = {}
    for u, v in edges:
        seen, queue = {u}, deque([u])
        while queue:
            cur = queue.popleft()
            for nb in adj.get(cur, ()):
                if nb not in seen:
                    seen.add(nb)
                    queue.append(nb)
        if v in seen:
            return [u, v]
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    return []


# --- optimal ---
def solve(edges: List[List[int]]) -> List[int]:
    """Union-find: each edge either joins two components (a tree edge) or connects two nodes that
    already share a root (closes the cycle). Near O(n) with path compression."""
    n = len(edges)
    parent = list(range(n + 1))  # parent[x] == x means x is a root; nodes are 1..n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression: skip a generation
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[rv] = ru
    return []


# --- demo ---
def demo():
    return solve([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]])


# --- bugs ---
BUGS = [
    {
        "replace": "        ru, rv = find(u), find(v)",
        "with":    "        ru, rv = parent[u], parent[v]",
        "fix": "compare roots, not direct parents: ru, rv = find(u), find(v)",
        "why": "Two nodes in the same component can have different parents (3 -> 2 -> 1 and 1), so the cycle edge is missed and a root gets re-parented: [[2,3],[1,2],[1,3]] returns [] instead of [1,3].",
        "decoys": [
            {"line": "        parent[rv] = ru", "change": "should be parent[ru] = rv"},
            {"line": "            x = parent[x]", "change": "should be x = parent[parent[x]]"},
            {"line": "    return []", "change": "should return edges[-1]"},
        ],
    },
    {
        "replace": "        parent[rv] = ru",
        "with":    "        parent[v] = ru",
        "fix": "attach the ROOT of v under the root of u: parent[rv] = ru",
        "why": "Re-parenting the node v instead of its root splits v off its old component, so earlier connections are forgotten: [[1,2],[3,2],[1,3]] returns [] instead of [1,3].",
        "decoys": [
            {"line": "        if ru == rv:", "change": "should be if u == v"},
            {"line": "            parent[x] = parent[parent[x]]  # path compression: skip a generation", "change": "should be parent[x] = x"},
            {"line": "        return x", "change": "should return parent[x]"},
        ],
    },
    {
        "replace": "    parent = list(range(n + 1))  # parent[x] == x means x is a root; nodes are 1..n",
        "with":    "    parent = list(range(n))  # parent[x] == x means x is a root; nodes are 1..n",
        "fix": "nodes are labelled 1..n, so the array needs n + 1 slots",
        "why": "Node n has no slot, so find(n) raises IndexError on every input, including [[1,2],[1,3],[2,3]].",
        "decoys": [
            {"line": "    n = len(edges)", "change": "should be n = len(edges) + 1"},
            {"line": "        while parent[x] != x:", "change": "should be if parent[x] != x"},
            {"line": "            return [u, v]", "change": "should return [ru, rv]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
