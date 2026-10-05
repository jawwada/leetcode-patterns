"""
Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree (LeetCode 1489) - Hard
Chapter: graphs
Pattern: Kruskal MST (sorted edges + union-find)

A weighted undirected connected graph on n nodes has edges[i] = [u, v, w]. An edge is critical
if deleting it raises the MST weight, and pseudo-critical if it appears in some MST but not in
all of them. Return [critical indices, pseudo-critical indices].
Example: n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
-> [[0, 1], [2, 3, 4, 5]]
"""
import math                        # math.inf


# --- helpers ---
def find(parent, x):
    """Root of x in the union-find, halving the path on the way up."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


# --- brute force ---
def is_spanning_tree(n, edges, chosen):
    """Do the chosen edge indices connect all n nodes without closing a cycle?"""
    if len(chosen) != n - 1:
        return False
    parent = list(range(n))
    for i in chosen:
        root_u = find(parent, edges[i][0])
        root_v = find(parent, edges[i][1])
        if root_u == root_v:
            return False               # this edge closes a cycle
        parent[root_u] = root_v
    return True


def classify(edges, trees):
    """Edges in every minimum tree are critical; edges in some but not all are pseudo-critical."""
    critical = []
    pseudo = []
    for i in range(len(edges)):
        in_count = 0
        for tree in trees:
            if i in tree:
                in_count += 1
        if in_count == len(trees):
            critical.append(i)
        elif in_count > 0:
            pseudo.append(i)
    return [critical, pseudo]


def brute_force(n, edges):
    """List every spanning tree, keep the lightest ones, classify by all / some. O(2^E * E)."""
    best = math.inf
    trees = []
    for mask in range(1 << len(edges)):    # bit i of mask set = edge i is in the candidate tree
        chosen = []
        weight = 0
        for i in range(len(edges)):
            if (mask >> i) & 1 == 1:
                chosen.append(i)
                weight += edges[i][2]
        if weight > best or not is_spanning_tree(n, edges, chosen):
            continue
        if weight < best:              # a lighter tree: forget the heavier ones
            best = weight
            trees = []
        trees.append(chosen)
    return classify(edges, trees)


# --- optimal ---
def kruskal(n, edges, order, skip, force):
    """Kruskal MST weight, leaving edge skip out and taking edge force first; inf if not a tree."""
    parent = list(range(n))
    total = 0
    used = 0
    if force != -1:
        u, v, w = edges[force]
        parent[u] = v                  # pre-join the forced edge before any lighter edge
        total = w
        used = 1
    for i in order:
        if i == skip:
            continue
        u, v, w = edges[i]
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u != root_v:           # the edge joins two different components: take it
            parent[root_u] = root_v
            total += w
            used += 1
    if used != n - 1:
        return math.inf
    return total


def find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree(n, edges):
    """Kruskal once for the base; per edge, skip it (critical?) or force it (pseudo?). O(E^2)."""
    order = []
    for i in range(len(edges)):
        order.append((edges[i][2], i))
    order.sort()                       # by weight, remembering each edge's original index
    sorted_indices = []
    for w, i in order:
        sorted_indices.append(i)
    base = kruskal(n, edges, sorted_indices, -1, -1)
    critical = []
    pseudo = []
    for i in range(len(edges)):
        if kruskal(n, edges, sorted_indices, i, -1) > base:
            critical.append(i)         # leaving it out costs more (or disconnects the graph)
        elif kruskal(n, edges, sorted_indices, -1, i) == base:
            pseudo.append(i)           # forcing it in costs nothing extra: some MST contains it
    return [critical, pseudo]


# --- try the brute force ---
edges_a = [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]]
print(brute_force(5, edges_a))                                          # -> [[0, 1], [2, 3, 4, 5]]
print(brute_force(4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]]))      # -> [[], [0, 1, 2, 3]]
print(brute_force(2, [[0, 1, 5]]))                                       # -> [[0], []]
edges_d = [[0, 1, 1], [0, 2, 1], [0, 3, 1], [1, 2, 2], [2, 3, 2]]
print(brute_force(4, edges_d))                                           # -> [[0, 1, 2], []]


# --- try the optimal ---
edges_a = [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]]
print(find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree(5, edges_a))
# -> [[0, 1], [2, 3, 4, 5]]
edges_b = [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]]
print(find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree(4, edges_b))
# -> [[], [0, 1, 2, 3]]
edges_c = [[0, 1, 5]]
print(find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree(2, edges_c))  # -> [[0], []]
edges_d = [[0, 1, 1], [0, 2, 1], [0, 3, 1], [1, 2, 2], [2, 3, 2]]
print(find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree(4, edges_d))
# -> [[0, 1, 2], []]
