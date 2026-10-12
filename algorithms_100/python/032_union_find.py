"""
Union-Find - Path Compression + Union by Size

Keep nodes 0..n-1 in disjoint groups: union(a, b) merges two groups, find(x)
names the root of x's group, and a count tracks how many groups remain. Five
nodes joined by [0, 1], [2, 3], [0, 2], [3, 1] (the last edge is redundant)
form two groups: count_components(5, edges) -> 2.
"""


# --- algorithm ---
class UnionFind:
    """Each group is a tree of parent pointers, named by its root."""

    def __init__(self, n):
        self.parent = list(range(n))    # every node starts as its own root
        self.size = [1] * n             # tree sizes, read only at roots
        self.count = n                  # number of separate groups

    def find(self, x):
        """Root of x; repoint the path straight at it. Near O(1) amortized."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])    # path compression
        return self.parent[x]

    def union(self, a, b):
        """Hang the smaller tree under the bigger root; False if already one.
        Near O(1) amortized."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False                # already connected: a cycle edge
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a     # root_a is the bigger tree
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        self.count -= 1
        return True


def count_components(n, edges):
    """Union the ends of every edge; count what is left. Near O(n + E)."""
    uf = UnionFind(n)
    for a, b in edges:
        uf.union(a, b)
    return uf.count


def find_redundant_connection(edges):
    """Nodes are 1..n; the first edge inside one group closes the cycle.
    Near O(n) for n edges."""
    uf = UnionFind(len(edges) + 1)      # slot 0 is never used
    for a, b in edges:
        if not uf.union(a, b):
            return [a, b]
    return []


# --- try it ---
print(count_components(5, [[0, 1], [2, 3], [0, 2], [3, 1]]))    # -> 2
print(count_components(4, []))                                  # -> 4
print(find_redundant_connection([[1, 2], [1, 3], [2, 3]]))      # -> [2, 3]
edges = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
print(find_redundant_connection(edges))                         # -> [1, 4]
