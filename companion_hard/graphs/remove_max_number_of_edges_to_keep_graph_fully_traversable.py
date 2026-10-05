"""
Remove Max Number of Edges to Keep Graph Fully Traversable (LeetCode 1579) - Hard
Chapter: graphs
Pattern: Union-Find (disjoint set union)

n nodes 1..n and edges [type, u, v]: type 1 only Alice can use, type 2 only Bob, type 3 both.
Return the maximum number of edges that can be removed so that Alice and Bob can each still
reach every node, or -1 if that is impossible even with all the edges.
Example: n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]] -> 2
"""


# --- brute force ---
def connected(n, edges, mask, allowed_types):
    """Can a player who may use allowed_types reach every node with the edges chosen by mask?"""
    adj = []
    for node in range(n + 1):
        adj.append([])
    for i in range(len(edges)):
        kind, u, v = edges[i]
        if (mask >> i) & 1 == 1 and kind in allowed_types:
            adj[u].append(v)
            adj[v].append(u)
    seen = {1}
    stack = [1]
    while stack:
        cur = stack.pop()
        for nb in adj[cur]:
            if nb not in seen:
                seen.add(nb)
                stack.append(nb)
    return len(seen) == n


def brute_force(n, edges):
    """Try every subset of edges to keep; the smallest serving both players wins. O(2^E * E)."""
    best_kept = -1
    for mask in range(1 << len(edges)):    # bit i of mask set = edge i is kept
        kept = 0
        for i in range(len(edges)):
            if (mask >> i) & 1 == 1:
                kept += 1
        if best_kept != -1 and kept >= best_kept:
            continue                   # cannot beat the best subset found so far
        if connected(n, edges, mask, (1, 3)) and connected(n, edges, mask, (2, 3)):
            best_kept = kept
    if best_kept == -1:
        return -1
    return len(edges) - best_kept


# --- optimal ---
def find(parent, x):
    """Root of x in the union-find, halving the path on the way up."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent, a, b):
    """Join a and b; True if they were in different components (the edge was needed)."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return False                   # the edge is redundant in this forest
    parent[root_b] = root_a
    return True


def count_roots(parent, n):
    """How many separate components the nodes 1..n fall into."""
    roots = set()
    for x in range(1, n + 1):
        roots.add(find(parent, x))
    return len(roots)


def remove_max_number_of_edges_to_keep_graph_fully_traversable(n, edges):
    """Kruskal-style: shared edges into both forests first, then each player's own edges. O(E)."""
    alice = list(range(n + 1))         # one union-find per player
    bob = list(range(n + 1))
    kept = 0
    for kind, u, v in edges:
        if kind == 3 and union(alice, u, v):   # shared edges first: one edge serves both players
            union(bob, u, v)
            kept += 1
    for kind, u, v in edges:
        if kind == 1 and union(alice, u, v):
            kept += 1
        if kind == 2 and union(bob, u, v):
            kept += 1
    if count_roots(alice, n) > 1 or count_roots(bob, n) > 1:
        return -1                      # someone still cannot reach every node
    return len(edges) - kept


# --- try the brute force ---
print(brute_force(4, [[3, 1, 2], [3, 2, 3], [1, 1, 3], [1, 2, 4], [1, 1, 2], [2, 3, 4]]))   # -> 2
print(brute_force(4, [[3, 1, 2], [3, 2, 3], [1, 1, 4], [2, 1, 4]]))                         # -> 0
print(brute_force(4, [[3, 2, 3], [1, 1, 2], [2, 3, 4]]))                                    # -> -1
print(brute_force(3, [[1, 1, 2], [2, 1, 2], [1, 2, 3], [2, 2, 3], [3, 1, 3]]))              # -> 2


# --- try the optimal ---
edges_a = [[3, 1, 2], [3, 2, 3], [1, 1, 3], [1, 2, 4], [1, 1, 2], [2, 3, 4]]
print(remove_max_number_of_edges_to_keep_graph_fully_traversable(4, edges_a))        # -> 2
edges_b = [[3, 1, 2], [3, 2, 3], [1, 1, 4], [2, 1, 4]]
print(remove_max_number_of_edges_to_keep_graph_fully_traversable(4, edges_b))        # -> 0
edges_c = [[3, 2, 3], [1, 1, 2], [2, 3, 4]]
print(remove_max_number_of_edges_to_keep_graph_fully_traversable(4, edges_c))        # -> -1
edges_d = [[1, 1, 2], [2, 1, 2], [1, 2, 3], [2, 2, 3], [3, 1, 3]]
print(remove_max_number_of_edges_to_keep_graph_fully_traversable(3, edges_d))        # -> 2
