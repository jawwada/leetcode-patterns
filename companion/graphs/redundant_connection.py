"""
Redundant Connection (LeetCode 684) - Medium
Chapter: graphs
Pattern: Union-Find (disjoint set union)

A tree with n nodes labelled 1..n had one extra edge added, so the input has n edges. Return the
edge that can be removed to make it a tree again; if several work, return the one that appears
last in the input.
Example: [[1,2],[1,3],[2,3]] -> [2,3]; [[1,2],[2,3],[3,4],[1,4],[1,5]] -> [1,4].
"""


# --- brute force ---
def brute_force(edges):
    """Before adding an edge, DFS over the edges so far: are its ends already joined? O(n^2)."""
    neighbours = {}                  # node -> its neighbours among the edges accepted so far
    for u, v in edges:
        seen = {u}
        stack = [u]
        while stack:
            cur = stack.pop()
            if cur == v:
                return [u, v]        # v is already reachable from u: this edge closes a cycle
            for nb in neighbours.get(cur, []):
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if u not in neighbours:
            neighbours[u] = []
        if v not in neighbours:
            neighbours[v] = []
        neighbours[u].append(v)
        neighbours[v].append(u)
    return []


# --- optimal ---
def find(parent, x):
    """Follow parent pointers up to the root, shortcutting the path on the way. Near O(1)."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]    # path halving: point x at its grandparent
        x = parent[x]
    return x


def redundant_connection(edges):
    """Union-find over the edges in order: first edge whose ends share a root wins. O(n a(n))"""
    n = len(edges)
    parent = list(range(n + 1))      # nodes are 1..n, so index 0 is unused
    rank = [0] * (n + 1)
    for u, v in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u == root_v:
            return [u, v]            # u and v already connected: this edge closes the cycle
        if rank[root_u] < rank[root_v]:
            root_u, root_v = root_v, root_u
        parent[root_v] = root_u      # merge: hang the shorter tree under the taller one
        if rank[root_u] == rank[root_v]:
            rank[root_u] += 1
    return []


# --- try the brute force ---
print(brute_force([[1, 2], [1, 3], [2, 3]]))                          # -> [2, 3]
print(brute_force([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))          # -> [1, 4]
print(brute_force([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]]))          # -> [2, 5]


# --- try the optimal ---
print(redundant_connection([[1, 2], [1, 3], [2, 3]]))                 # -> [2, 3]
print(redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]])) # -> [1, 4]
print(redundant_connection([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]])) # -> [2, 5]
