"""
Dijkstra's Shortest Paths (basics: graphs)
Shortest distance from src to every reachable node over directed edges (u, v, w) with w >= 0.
  n = 5, edges [(0,1,4), (0,2,1), (2,1,2), (1,3,1), (2,3,5), (3,4,3)], src = 0
    ->  {0: 0, 1: 3, 2: 1, 3: 4, 4: 7}

Idea: the closest unsettled node is final: with no negative edges, any other route to it is
      at least as long. A min-heap of (dist, node) hands out that node; an entry with a bigger
      distance than dist[u] is stale.

Pseudocode:
  dist = {src: 0}; heap = [(0, src)]
  while heap:
      d, u = pop the smallest
      if d > dist[u]: skip                         # stale: u was settled closer
      for v, w in adj[u]:
          if d + w < dist.get(v, inf): dist[v] = d + w; push (d + w, v)
  return dist

Time O((n + m) log m), space O(n + m).
"""
import heapq


def dijkstra(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = {src: 0}                      # best distance found so far
    heap = [(0, src)]                    # (distance, node)
    while heap:
        d, u = heapq.heappop(heap)       # closest node not settled yet
        if d > dist[u]:                  # stale entry: a shorter one came first
            continue
        for v, w in adj[u]:
            if d + w < dist.get(v, float("inf")):   # relax: shorter way to v via u
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist


if __name__ == "__main__":
    edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]
    print(dijkstra(5, edges, 0))                   # {0: 0, 1: 3, 2: 1, 3: 4, 4: 7}
    print(dijkstra(3, [(0, 1, 5), (2, 0, 1)], 0))  # {0: 0, 1: 5}
