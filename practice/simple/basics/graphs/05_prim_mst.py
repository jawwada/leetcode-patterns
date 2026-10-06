"""
Prim's Minimum Spanning Tree (basics: graphs)
Grow a minimum spanning tree from a start node in a connected graph of undirected edges (u, v, w).
  n = 5, edges [(0,1,4), (0,2,1), (1,2,2), (1,3,5), (2,3,8), (3,4,3)], start = 0
    ->  (11, [(0, 2, 1), (2, 1, 2), (1, 3, 5), (3, 4, 3)])   tree edges as (parent, node, w)

Idea: the cheapest edge leaving the tree is always safe to add. A min-heap holds the edges
      leaving the tree; if an edge's far node has joined in the meantime, the entry is stale.

Pseudocode:
  heap = [(0, start, start)]                       # (weight, node, parent)
  until all n nodes are in the tree (or the heap is empty):
      w, v, parent = pop the cheapest
      if v is already in the tree: skip            # stale entry
      add v; if v != start: total += w; keep (parent, v, w)
      for each edge (v, x, wx) with x outside the tree: push (wx, x, v)
  return total, kept edges

Time O(m log m), space O(n + m).
"""
import heapq


def prim_mst(n, edges, start=0):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:                # undirected: store both ways
        adj[u].append((w, v))
        adj[v].append((w, u))
    in_tree, total, tree = set(), 0, []
    heap = [(0, start, start)]           # (weight, node, parent)
    while heap and len(in_tree) < n:
        w, v, parent = heapq.heappop(heap)   # cheapest edge leaving the tree
        if v in in_tree:                 # stale: v already joined
            continue
        in_tree.add(v)
        if v != start:                   # the start joins without an edge
            total += w
            tree.append((parent, v, w))
        for wx, x in adj[v]:             # offer v's edges to the outside nodes
            if x not in in_tree:
                heapq.heappush(heap, (wx, x, v))
    return total, tree


if __name__ == "__main__":
    edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3)]
    print(prim_mst(5, edges, 0))  # (11, [(0, 2, 1), (2, 1, 2), (1, 3, 5), (3, 4, 3)])
    print(prim_mst(5, edges, 4))  # (11, [(4, 3, 3), (3, 1, 5), (1, 2, 2), (2, 0, 1)])
