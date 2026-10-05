"""
Union-Find (Disjoint Set Union) - Fundamentals
Chapter: fundamentals/graphs
Key operations: find with path compression, union by size, connected query, component count

Maintain n elements 0..n-1 in disjoint sets. parent[x] points toward the root of x's set; a root
points to itself. union(a, b) merges two sets (smaller tree under the bigger root), connected(a, b)
says whether a and b share a set, and the component count is the number of roots.
Example: n=6, unions (0,1) (1,2) (3,4) (0,2), queries (0,2) (2,3) (4,3) (5,5)
         -> True, False, True, True; 3 components {0,1,2} {3,4} {5}
"""


# --- algorithm ---
def make_sets(n):
    """Every element starts as its own root with size 1. O(n)."""
    parent = list(range(n))
    size = [1] * n
    return parent, size


def find(parent, x):
    """Root of x; on the way back point every node straight at the root (path compression)."""
    if parent[x] != x:
        parent[x] = find(parent, parent[x])   # compress: x now points at the root directly
    return parent[x]


def union(parent, size, a, b):
    """Merge the sets of a and b; False if they were already one set. Near O(1) amortized."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return False
    if size[root_a] < size[root_b]:
        root_a, root_b = root_b, root_a   # root_a is the bigger tree; hang the smaller under it
    parent[root_b] = root_a
    size[root_a] += size[root_b]
    return True


def connected(parent, a, b):
    """Same set iff same root."""
    return find(parent, a) == find(parent, b)


def count_components(parent):
    """A root is a node that points at itself; one root per set. O(n)."""
    count = 0
    for x in range(len(parent)):
        if parent[x] == x:
            count += 1
    return count


# --- try it ---
parent, size = make_sets(6)
print(union(parent, size, 0, 1))   # -> True
print(union(parent, size, 1, 2))   # -> True
print(union(parent, size, 3, 4))   # -> True
print(union(parent, size, 0, 2))   # -> False  (0 and 2 were already joined through 1)
print(connected(parent, 0, 2))     # -> True
print(connected(parent, 2, 3))     # -> False
print(connected(parent, 4, 3))     # -> True
print(connected(parent, 5, 5))     # -> True
print(count_components(parent))    # -> 3
print(find(parent, 2) == find(parent, 0))   # -> True
