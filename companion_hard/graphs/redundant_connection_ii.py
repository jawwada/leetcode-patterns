"""
Redundant Connection II (LeetCode 685) - Hard
Chapter: graphs
Pattern: Union-Find (disjoint set union)

A rooted tree on nodes 1..n (every node but the root has exactly one parent) had one extra
directed edge u -> v added, giving n edges. Return the edge whose removal restores a rooted
tree; if several work, return the one that appears last in the input.
Example: [[1,2],[1,3],[2,3]] -> [2,3];  [[1,2],[2,3],[3,4],[4,1],[1,5]] -> [4,1]
"""


# --- brute force ---
def is_rooted_tree(n, kept):
    """True when the kept edges form a rooted tree: one root, one parent elsewhere, all reached."""
    indeg = [0] * (n + 1)
    children = []
    for node in range(n + 1):
        children.append([])
    for u, v in kept:
        indeg[v] += 1
        children[u].append(v)
    root = -1
    for node in range(1, n + 1):
        if indeg[node] == 0:
            if root != -1:
                return False           # two roots
            root = node
        elif indeg[node] != 1:
            return False               # a node with two parents
    if root == -1:
        return False
    seen = {root}
    stack = [root]
    while stack:
        cur = stack.pop()
        for child in children[cur]:
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return len(seen) == n              # every node hangs below the root


def brute_force(edges):
    """Delete each edge, last first, and test whether a rooted tree is left. O(n^2)."""
    n = len(edges)
    for skip in range(n - 1, -1, -1):  # later edges first: the answer must be the last valid one
        kept = []
        for i in range(n):
            if i != skip:
                kept.append(edges[i])
        if is_rooted_tree(n, kept):
            return edges[skip]
    return []


# --- optimal ---
def find(parent, x):
    """Root of x in the union-find, halving the path on the way up."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def redundant_connection_ii(edges):
    """One in-degree scan finds a node with two parents; one union-find pass finds a cycle. O(n)"""
    n = len(edges)
    parent_of = [0] * (n + 1)
    cand1 = None                       # earlier edge into the node that has two parents
    cand2 = None                       # later edge into that node
    for u, v in edges:
        if parent_of[v] != 0:
            cand1 = [parent_of[v], v]
            cand2 = [u, v]
        else:
            parent_of[v] = u
    parent = list(range(n + 1))
    for u, v in edges:
        if [u, v] == cand2:
            continue                   # provisionally drop the later of the two parent edges
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u == root_v:           # a cycle survives even without cand2
            if cand2 is not None:
                return cand1           # so the earlier parent edge is the culprit
            return [u, v]              # no double parent: the edge that closes the cycle is it
        parent[root_v] = root_u
    return cand2                       # no cycle without cand2: cand2 was the extra edge


# --- try the brute force ---
print(brute_force([[1, 2], [1, 3], [2, 3]]))                      # -> [2, 3]
print(brute_force([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]))      # -> [4, 1]
print(brute_force([[2, 1], [3, 1], [4, 2], [1, 4]]))              # -> [2, 1]
print(brute_force([[4, 2], [1, 5], [5, 2], [5, 3], [2, 4]]))      # -> [4, 2]


# --- try the optimal ---
print(redundant_connection_ii([[1, 2], [1, 3], [2, 3]]))                      # -> [2, 3]
print(redundant_connection_ii([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]))      # -> [4, 1]
print(redundant_connection_ii([[2, 1], [3, 1], [4, 2], [1, 4]]))              # -> [2, 1]
print(redundant_connection_ii([[4, 2], [1, 5], [5, 2], [5, 3], [2, 4]]))      # -> [4, 2]
