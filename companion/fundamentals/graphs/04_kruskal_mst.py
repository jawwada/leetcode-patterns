"""
Kruskal's Minimum Spanning Tree - Fundamentals
Chapter: fundamentals/graphs
Key operations: sort edges by weight, union-find accept/reject, stop at n-1 edges

Given n nodes and weighted undirected edges (u, v, w), return the total weight of a minimum
spanning tree and the accepted edges in the order they were taken. Kruskal scans the edges cheapest
first and keeps an edge iff it joins two different components. Disconnected input gives a forest.
Example: n=5, edges [(0,1,4),(0,2,1),(1,2,2),(1,3,5),(2,3,8),(3,4,3)]
         -> (11, [(0,2,1), (1,2,2), (3,4,3), (1,3,5)])   edge (0,1,4) is rejected
"""


# --- algorithm ---
def find(parent, x):
    """Root of x with path halving: every node on the way skips to its grandparent."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def kruskal(n, edges):
    """Cheapest edge first; accept it iff its endpoints are in different components. O(m log m)."""
    by_weight = []
    for u, v, w in edges:
        by_weight.append((w, u, v))
    by_weight.sort()                   # weight first, so the cheapest edges come out first
    parent = list(range(n))
    total = 0
    tree = []
    for w, u, v in by_weight:
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u == root_v:
            continue                   # already connected: this edge would close a cycle
        parent[root_u] = root_v        # merge the two components
        total += w
        tree.append((u, v, w))
        if len(tree) == n - 1:         # a spanning tree on n nodes has exactly n - 1 edges
            break
    return total, tree


# --- try it ---
print(kruskal(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3)]))
# -> (11, [(0, 2, 1), (1, 2, 2), (3, 4, 3), (1, 3, 5)])
print(kruskal(4, [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4)]))
# -> (7, [(0, 1, 1), (1, 2, 2), (2, 3, 4)])
print(kruskal(3, [(0, 1, 5)]))                                    # -> (5, [(0, 1, 5)])  (a forest)
