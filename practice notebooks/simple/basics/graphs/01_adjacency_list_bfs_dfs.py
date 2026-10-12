"""
Adjacency List, BFS and DFS (basics: graphs)
Build an adjacency list, then list the nodes BFS and DFS reach from src (smaller neighbors first).
  n = 6, edges [(0,1), (0,2), (1,3), (2,3), (3,4)], undirected, src = 0
    ->  BFS [0, 1, 2, 3, 4], DFS [0, 1, 3, 2, 4]   (node 5 is unreachable)

Idea: a queue makes BFS finish every node 1 hop away before any node 2 hops away;
      a stack makes DFS follow one path as deep as it can before backing up.

Pseudocode:
  build:  add v to adj[u] (and u to adj[v] if undirected); sort every adj[u]
  bfs:    seen = {src}; queue = [src]
          while queue:
              u = popleft; output u
              for each unseen v in adj[u]: mark v seen; append v    # mark when queued
  dfs:    stack = [src]
          while stack:
              u = pop; if u is seen: skip                           # mark when popped
              mark u seen; output u; push adj[u] reversed (smallest on top)

Time O(n + m) for each, space O(n + m).
"""
from collections import deque


def build_adjacency_list(n, edges, directed):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:                 # undirected: store both ways
            adj[v].append(u)
    for neighbors in adj:
        neighbors.sort()                 # smaller neighbors get visited first
    return adj


def bfs_order(adj, src):
    order, seen, queue = [], {src}, deque([src])
    while queue:
        u = queue.popleft()              # oldest first (FIFO)
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v)              # mark when queued: nobody is queued twice
                queue.append(v)
    return order


def dfs_order(adj, src):
    order, seen, stack = [], set(), [src]
    while stack:
        u = stack.pop()                  # newest first (LIFO)
        if u in seen:                    # pushed twice: skip the extra copy
            continue
        seen.add(u)                      # mark when popped
        order.append(u)
        for v in reversed(adj[u]):       # reversed: the smallest ends on top
            if v not in seen:
                stack.append(v)
    return order


if __name__ == "__main__":
    adj = build_adjacency_list(6, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)], False)
    print(adj)                # [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3], []]
    print(bfs_order(adj, 0))  # [0, 1, 2, 3, 4]
    print(dfs_order(adj, 0))  # [0, 1, 3, 2, 4]
