"""
Redundant Connection (LeetCode 684)
A tree got one extra edge; return the edge whose removal leaves a tree (the last such edge).
  edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]  ->  [1, 4]

Idea: union-find. Add edges one by one; if both ends already share a root,
      they were connected before, so this edge closes the cycle.

Pseudocode:
  parent[x] = x for every node
  for u, v in edges:
      if find(u) == find(v): return [u, v]   # already connected
      union(u, v)

Time ~O(n) (with path compression), space O(n).
"""


def find_redundant_connection(edges):
    parent = list(range(len(edges) + 1))         # nodes are 1..n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]        # path compression
            x = parent[x]
        return x

    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:                     # already connected: cycle edge
            return [u, v]
        parent[root_v] = root_u                  # union the two components
    return []


if __name__ == "__main__":
    print(find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))  # [1, 4]
    print(find_redundant_connection([[1, 2], [1, 3], [2, 3]]))                  # [2, 3]
