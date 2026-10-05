"""
Dijkstra's Shortest Paths - Fundamentals
Chapter: fundamentals/graphs
Key operations: heap of (dist, node), skip stale entries, relax out-edges, final when popped

Given n nodes, directed edges (u, v, w) with w >= 0 and a source, return {node: shortest distance}
for every node reachable from the source. The heap always yields the closest unsettled node; an
entry whose distance is larger than the recorded one is stale and skipped.
Example: n=5, edges [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3)], source 0
         -> {0: 0, 1: 3, 2: 1, 3: 4, 4: 7}   (node 1 is reached via 2: 1 + 2 = 3)
"""
import heapq                       # heappush / heappop keep the smallest at index 0
import math                        # math.inf for "no distance known yet"


# --- algorithm ---
def build_adjacency(n, edges):
    """adj[u] lists (neighbour, weight) pairs for the directed edges out of u. O(n + m)."""
    adj = []
    for _ in range(n):
        adj.append([])
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def dijkstra(n, edges, source):
    """Pop the closest unsettled node: its distance is final; relax its out-edges. O(m log m)."""
    adj = build_adjacency(n, edges)
    dist = {source: 0}
    heap = [(0, source)]               # (distance so far, node)
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                   # stale: a shorter route to node was found after this push
        for neighbour, w in adj[node]:
            if d + w < dist.get(neighbour, math.inf):   # relax: a shorter way to neighbour
                dist[neighbour] = d + w
                heapq.heappush(heap, (d + w, neighbour))
    return dist


# --- try it ---
print(dijkstra(5, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)], 0))
# -> {0: 0, 1: 3, 2: 1, 3: 4, 4: 7}
print(dijkstra(3, [(0, 1, 1), (1, 2, 1), (0, 2, 5)], 0))   # -> {0: 0, 1: 1, 2: 2}
print(dijkstra(3, [(0, 1, 7)], 0))                         # -> {0: 0, 1: 7}  (node 2 unreachable)
