"""
Kruskal's Minimum Spanning Tree (basics: graphs)
Find the cheapest set of undirected edges (u, v, w) connecting all n nodes (a forest if it can't).
  n = 5, edges [(0,1,4), (0,2,1), (1,2,2), (1,3,5), (2,3,8), (3,4,3)]
    ->  (11, [(0, 2, 1), (1, 2, 2), (3, 4, 3), (1, 3, 5)])   (0,1,4) is skipped: 0, 1 already joined

Idea: try edges cheapest first and keep one only if it joins two different components
      (union-find answers that in near O(1)). A tree on n nodes has n - 1 edges, so stop there.

Pseudocode:
  sort edges by weight
  for u, v, w in edges:
      if find(u) == find(v): skip                  # same component: would close a cycle
      union(u, v); total += w; keep (u, v, w)
      if n - 1 edges kept: stop
  return total, kept edges

Time O(m log m) for the sort, space O(n + m).
"""


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]    # path halving: skip a level
        x = parent[x]
    return x


def kruskal_mst(n, edges):
    parent = list(range(n))              # union-find: every node is its own root
    total, tree = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):   # cheapest edge first
        ru, rv = find(parent, u), find(parent, v)
        if ru == rv:                     # already connected: would close a cycle
            continue
        parent[ru] = rv                  # merge the two components (link the roots)
        total += w
        tree.append((u, v, w))
        if len(tree) == n - 1:           # spanning tree complete
            break
    return total, tree


if __name__ == "__main__":
    edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3)]
    print(kruskal_mst(5, edges))   # (11, [(0, 2, 1), (1, 2, 2), (3, 4, 3), (1, 3, 5)])
    two_parts = [(0, 1, 7), (2, 3, 2)]
    print(kruskal_mst(4, two_parts))  # (9, [(2, 3, 2), (0, 1, 7)])
