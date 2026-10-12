"""
Prim's Minimum Spanning Tree - Basics
Area: graphs
Key operations: heap of (weight, node, parent), skip a popped node already in the tree, push crossing edges

Given n nodes, weighted undirected edges (u, v, w) and a start node, grow one tree from the start:
the heap holds the edges leaving the tree, always take the cheapest, ignore it if its far end is
already inside. Return the total weight and the tree edges (parent, node, w) in the order added.
The graph is assumed connected.
Example: n=5, edges [(0,1,4),(0,2,1),(1,2,2),(1,3,5),(2,3,8),(3,4,3)], start 0
         -> (11, [(0,2,1), (2,1,2), (1,3,5), (3,4,3)])
"""
import heapq


# --- brute force ---
def brute_force(n, edges):
    """Kruskal: cheapest edges first, a tiny union-find rejects cycles. O(m log m); cross-checks the total only."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
    return total


# --- optimal ---
def solve(n, edges, start=0):
    """Pop the cheapest crossing edge; if it leads into the tree it is stale, else add the node and push its edges. O(m log m)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    seen, total, tree = set(), 0, []
    heap = [(0, start, start)]  # (weight, node, parent)
    while heap and len(seen) < n:
        w, v, u = heapq.heappop(heap)
        if v in seen:
            continue
        seen.add(v)
        if v != start:
            total += w
            tree.append((u, v, w))
        for wx, x in adj[v]:
            if x not in seen:
                heapq.heappush(heap, (wx, x, v))
    return total, tree


# --- demo ---
def demo():
    return solve(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3)], 0)


# --- bugs ---
BUGS = [
    {
        "replace": "                heapq.heappush(heap, (wx, x, v))",
        "with":    "                heapq.heappush(heap, (wx, v, x))",
        "fix": "the heap entry is (weight, far node, parent): the far node x is what gets added, v is where the edge came from",
        "why": "Every pushed entry names the node just added, so it is skipped as 'already in the tree' and the tree never grows past the start: total 0.",
        "decoys": [
            {"line": "        if v in seen:", "change": "should be if u in seen"},
            {"line": "        adj[v].append((w, u))", "change": "should append (u, w)"},
            {"line": "    heap = [(0, start, start)]  # (weight, node, parent)", "change": "should start empty"},
        ],
    },
    {
        "replace": "        if v != start:",
        "with":    "        if u != start:",
        "fix": "skip the bookkeeping only for the start's own (0, start, start) entry, i.e. when the NODE v is the start",
        "why": "Every edge leaving the start node is left out of the total and the tree: the example reports 10 instead of 11 and a 3-edge tree.",
        "decoys": [
            {"line": "        seen.add(v)", "change": "should add u"},
            {"line": "            total += w", "change": "should move before the if v in seen check"},
            {"line": "            if x not in seen:", "change": "should be if x in seen"},
        ],
    },
    {
        "replace": "    while heap and len(seen) < n:",
        "with":    "    while heap and len(seen) < n - 1:",
        "fix": "the loop runs until all n nodes are in the tree; a tree on n nodes has n - 1 edges but n nodes in seen",
        "why": "The last node is never added, so the tree has n - 2 edges and the total is short: the example stops at 8 without (3,4,3).",
        "decoys": [
            {"line": "        w, v, u = heapq.heappop(heap)", "change": "should be heap.pop()"},
            {"line": "            tree.append((u, v, w))", "change": "should append (v, u, w)"},
            {"line": "    return total, tree", "change": "should return total, seen"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
