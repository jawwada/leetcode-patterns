"""
Kruskal's Minimum Spanning Tree - Basics
Area: graphs
Key operations: sort edges by weight, union-find accept/reject, stop at n-1 edges

Given n nodes and weighted undirected edges (u, v, w), return the total weight of a minimum spanning
tree and the accepted edges in the order they were taken. Kruskal scans the edges cheapest first and
keeps an edge iff it joins two different components. On a disconnected graph it returns the spanning forest.
Example: n=5, edges [(0,1,4),(0,2,1),(1,2,2),(1,3,5),(2,3,8),(3,4,3)]
         -> (11, [(0,2,1), (1,2,2), (3,4,3), (1,3,5)])   edge (0,1,4) is rejected: 0 and 1 already joined
"""
import heapq


# --- brute force ---
def brute_force(n, edges):
    """Prim from every unvisited node: grow a tree by the cheapest crossing edge. O(m log m); cross-checks the total only."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    seen, total = set(), 0
    for s in range(n):
        if s in seen:
            continue
        heap = [(0, s)]
        while heap:
            w, u = heapq.heappop(heap)
            if u in seen:
                continue
            seen.add(u)
            total += w
            for wv, v in adj[u]:
                if v not in seen:
                    heapq.heappush(heap, (wv, v))
    return total


# --- optimal ---
def find(parent, x):
    """Root of x with path halving. Near O(1) amortized."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def solve(n, edges):
    """Cheapest edge first; accept it iff its endpoints are in different components. O(m log m)."""
    parent = list(range(n))
    total, tree = 0, []
    for w, u, v in sorted((w, u, v) for u, v, w in edges):
        ru, rv = find(parent, u), find(parent, v)
        if ru == rv:
            continue
        parent[ru] = rv
        total += w
        tree.append((u, v, w))
        if len(tree) == n - 1:
            break
    return total, tree


# --- demo ---
def demo():
    return solve(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3)])


# --- bugs ---
BUGS = [
    {
        "replace": "    for w, u, v in sorted((w, u, v) for u, v, w in edges):",
        "with":    "    for w, u, v in ((w, u, v) for u, v, w in edges):",
        "fix": "the edges must be taken in increasing weight; without the sort the greedy choice is wrong",
        "why": "In input order the example accepts (0,1,4) first and then rejects (1,2,2), giving 13 instead of 11.",
        "decoys": [
            {"line": "        if len(tree) == n - 1:", "change": "should be == n"},
            {"line": "        total += w", "change": "should move before the if ru == rv check"},
            {"line": "        x = parent[x]", "change": "should be x = parent[parent[x]]"},
        ],
    },
    {
        "replace": "        parent[ru] = rv",
        "with":    "        parent[u] = rv",
        "fix": "link the ROOT ru under rv; re-pointing the element u leaves its old root as a separate component",
        "why": "When u is not a root its component is never merged, so a later edge between the two components is accepted and closes a cycle: n=4, edges (0,1,1),(0,2,2),(1,2,3),(2,3,4) gives 6 instead of 7.",
        "decoys": [
            {"line": "        ru, rv = find(parent, u), find(parent, v)", "change": "should be parent[u], parent[v]"},
            {"line": "        tree.append((u, v, w))", "change": "should append (ru, rv, w)"},
            {"line": "        parent[x] = parent[parent[x]]", "change": "should be parent[x] = x"},
        ],
    },
    {
        "replace": "        if ru == rv:",
        "with":    "        if u == v:",
        "fix": "compare the ROOTS of the two endpoints; equal endpoints only catch self-loops",
        "why": "Every edge is accepted, so cycles are closed and the total is too large: the example accepts (0,1,4) and stops at 4 edges with total 10 instead of 11.",
        "decoys": [
            {"line": "    parent = list(range(n))", "change": "should be [0] * n"},
            {"line": "    while parent[x] != x:", "change": "should be while parent[x] != 0"},
            {"line": "            continue", "change": "should be break"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
