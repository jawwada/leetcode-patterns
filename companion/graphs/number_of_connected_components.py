"""
Number of Connected Components in an Undirected Graph (LeetCode 323) - Medium
Chapter: graphs
Pattern: Union-Find (disjoint set union)

Given n nodes labelled 0..n-1 and a list of undirected edges, return the number of connected
components.
Example: n=5, edges=[[0,1],[1,2],[3,4]] -> 2; n=5, edges=[[0,1],[1,2],[2,3],[3,4]] -> 1.
"""


# --- brute force ---
def brute_force(n, edges):
    """DFS from every node with a private visited set; count only the smallest node. O(V(V+E))"""
    neighbours = []
    for _ in range(n):
        neighbours.append([])
    for u, v in edges:
        neighbours[u].append(v)
        neighbours[v].append(u)
    count = 0
    for start in range(n):
        seen = {start}
        stack = [start]
        while stack:
            cur = stack.pop()
            for nb in neighbours[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if min(seen) == start:       # count each component once, from its smallest node
            count += 1
    return count


# --- optimal ---
def find(parent, x):
    """Follow parent pointers up to the root, shortcutting the path on the way. Near O(1)."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]    # path halving: point x at its grandparent
        x = parent[x]
    return x


def number_of_connected_components(n, edges):
    """Union-find: start with n components; merging two different roots removes one. O(E a(n))"""
    parent = list(range(n))          # parent[x] = x: every node is its own root at first
    rank = [0] * n                   # rough tree height, to keep the trees shallow
    count = n
    for u, v in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u == root_v:
            continue                 # already in the same component: nothing to merge
        if rank[root_u] < rank[root_v]:
            root_u, root_v = root_v, root_u
        parent[root_v] = root_u      # hang the shorter tree under the taller one
        if rank[root_u] == rank[root_v]:
            rank[root_u] += 1
        count -= 1                   # one merge = one component fewer
    return count


# --- try the brute force ---
print(brute_force(5, [[0, 1], [1, 2], [3, 4]]))             # -> 2
print(brute_force(5, [[0, 1], [1, 2], [2, 3], [3, 4]]))     # -> 1
print(brute_force(4, []))                                   # -> 4
print(brute_force(4, [[0, 1], [1, 0], [2, 3], [0, 1]]))     # -> 2


# --- try the optimal ---
print(number_of_connected_components(5, [[0, 1], [1, 2], [3, 4]]))             # -> 2
print(number_of_connected_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]))     # -> 1
print(number_of_connected_components(4, []))                                   # -> 4
print(number_of_connected_components(4, [[0, 1], [1, 0], [2, 3], [0, 1]]))     # -> 2
