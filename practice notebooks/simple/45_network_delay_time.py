"""
Network Delay Time (LeetCode 743)
A signal leaves node k along weighted directed edges; how long until all n nodes hear it (-1 if never)?
  times = [[1,2,4],[1,3,1],[3,2,1],[2,4,2]], n = 4, k = 1  ->  4

Idea: Dijkstra. The node with the smallest known arrival time can't be reached any faster,
      so pop it from a min-heap, fix its time, and relax its outgoing edges.

Pseudocode:
  dist = {k: 0}; heap = [(0, k)]
  while heap:
      d, u = pop smallest
      if d > dist[u]: skip (stale entry)
      for v, w in adj[u]:
          if d + w < dist[v]: dist[v] = d + w; push (d + w, v)
  return max(dist) if all n reached else -1

Time O((V + E) log V), space O(V + E).
"""
import heapq
from collections import defaultdict


def network_delay_time(times, n, k):
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
    dist = {k: 0}                                # best arrival time so far
    heap = [(0, k)]                              # (arrival time, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                          # stale entry, skip
            continue
        for v, w in adj[u]:
            if d + w < dist.get(v, float("inf")):    # found a faster way to v
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1


if __name__ == "__main__":
    print(network_delay_time([[1, 2, 4], [1, 3, 1], [3, 2, 1], [2, 4, 2]], 4, 1))  # 4
    print(network_delay_time([[1, 2, 1]], 2, 2))                                   # -1
