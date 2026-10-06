"""
Connected Components (basics: searches)
Count the connected components of an undirected graph with nodes 0..n-1 and an edge list.
  n = 7, edges = [(0, 1), (1, 2), (3, 4)]  ->  4   ({0, 1, 2}, {3, 4}, {5}, {6})

Idea: one BFS from a node reaches exactly that node's component. So start a BFS from
      every node that no earlier BFS reached: each such start is a new component.
      A node with no edges is a component on its own.

Pseudocode:
  adj = adjacency lists, every edge stored in both directions
  for s in 0..n-1:
      if s is seen: continue
      count += 1; mark s; queue = [s]
      while queue:
          u = pop front
          for v in adj[u]: if v not seen: mark v, enqueue v
  return count

Time O(V + E), space O(V + E).
"""
from collections import deque


def count_components(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)                 # undirected: store both directions
        adj[b].append(a)
    seen, count = set(), 0
    for s in range(n):
        if s in seen:
            continue                     # already inside a counted component
        count += 1                       # unreached node: a new component
        seen.add(s)
        queue = deque([s])
        while queue:                     # BFS marks the whole component
            u = queue.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)          # mark when enqueued
                    queue.append(v)
    return count


if __name__ == "__main__":
    print(count_components(7, [(0, 1), (1, 2), (3, 4)]))  # 4
    print(count_components(3, []))                        # 3
    print(count_components(2, [(1, 0)]))                  # 1
