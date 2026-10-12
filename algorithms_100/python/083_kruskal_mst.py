"""
Kruskal's Minimum Spanning Tree - Sort Edges, Let Union-Find Reject Cycles

Given n nodes and undirected edges [u, v, w], return the total weight and the
edges of a minimum spanning tree, or None if the graph is disconnected:
n = 5, edges 0-1 (4), 0-2 (1), 1-2 (2), 1-3 (5), 2-3 (8), 3-4 (3)
-> (11, [[0, 2, 1], [1, 2, 2], [3, 4, 3], [1, 3, 5]]).
"""


# --- algorithm ---
def find(parent, x):
    """Root of x; repoint the path straight at it. Near O(1) amortized."""
    if parent[x] != x:
        parent[x] = find(parent, parent[x])     # path compression
    return parent[x]


def union(parent, size, a, b):
    """Merge the components of a and b; False if they are already one."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return False                    # already one component
    if size[root_a] < size[root_b]:
        root_a, root_b = root_b, root_a     # hang the smaller tree below
    parent[root_b] = root_a
    size[root_a] += size[root_b]
    return True


def kruskal(n, edges):
    """Take edges cheapest first; keep one only if it joins two components.
    O(E log E) for the sort."""
    order = []
    for u, v, w in edges:
        order.append((w, u, v))         # weight first: sort by weight
    order.sort()                        # cheapest edge first
    parent = list(range(n))             # every node is its own root
    size = [1] * n
    total = 0
    tree = []
    for w, u, v in order:
        if union(parent, size, u, v):   # two components: edge is safe
            total += w
            tree.append([u, v, w])
            if len(tree) == n - 1:
                break                   # n - 1 edges span all n nodes
    if len(tree) < n - 1:
        return None                     # the graph is disconnected
    return total, tree


# --- try it ---
edges = [[0, 1, 4], [0, 2, 1], [1, 2, 2], [1, 3, 5], [2, 3, 8], [3, 4, 3]]
total, tree = kruskal(5, edges)
print(total)                                # -> 11
print(tree)                 # -> [[0, 2, 1], [1, 2, 2], [3, 4, 3], [1, 3, 5]]
print(kruskal(4, [[0, 1, 1], [2, 3, 1]]))   # -> None
print(kruskal(1, []))                       # -> (0, [])
