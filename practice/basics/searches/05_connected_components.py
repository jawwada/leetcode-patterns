"""
Connected Components - Basics
Area: searches
Key operations: adjacency list from an edge list (both directions), BFS from every unvisited node, mark visited when enqueued, one BFS = one component

Count the connected components of an undirected graph with n nodes (0..n-1) given as an edge list.
A node with no edges is a component of its own.
Example: n=7, edges [(0, 1), (1, 2), (3, 4)] -> 4  (components {0, 1, 2}, {3, 4}, {5}, {6})
"""
from collections import deque
from typing import List, Tuple


# --- brute force ---
def brute_force(n: int, edges: List[Tuple[int, int]]) -> int:
    """Union-find: merge the endpoints of every edge, then count distinct roots. O(E * alpha(n))."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        parent[find(a)] = find(b)
    return len({find(x) for x in range(n)})


# --- optimal ---
def solve(n, edges):
    """BFS from every node not yet seen; each BFS marks exactly one component. O(V + E)."""
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen, count = set(), 0
    for s in range(n):
        if s in seen:
            continue
        count += 1
        seen.add(s)
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
    return count


# --- demo ---
def demo():
    return solve(7, [(0, 1), (1, 2), (3, 4)])


# --- bugs ---
BUGS = [
    {
        "replace": "        adj[b].append(a)",
        "with":    "        adj[a].append(b)",
        "fix": "an undirected edge goes into both adjacency lists: adj[a] gets b AND adj[b] gets a",
        "why": "Only one direction is stored, so a BFS that starts at the 'target' end never sees the other node: edges [(1, 0)] on 2 nodes counts 2.",
        "decoys": [
            {"line": "    adj = [[] for _ in range(n)]", "change": "should be [[]] * n"},
            {"line": "            u = q.popleft()", "change": "should be q.pop()"},
            {"line": "        count += 1", "change": "should be incremented after the while loop"},
        ],
    },
    {
        "replace": "        if s in seen:",
        "with":    "        if s in seen or not adj[s]:",
        "fix": "an isolated node is a component too; skip a start node only when it was already seen",
        "why": "Nodes without edges are never counted: n=3 with no edges returns 0 instead of 3.",
        "decoys": [
            {"line": "        seen.add(s)", "change": "should be done after the BFS"},
            {"line": "                if v not in seen:", "change": "should be if v != u"},
            {"line": "        q = deque([s])", "change": "should be deque(adj[s])"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
