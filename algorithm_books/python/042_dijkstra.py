"""
Dijkstra's Algorithm - Shortest Paths with Non-Negative Weights

A signal leaves node k of a network with nodes 1..n, and times[i] = [u, v, w]
says it takes w to cross the directed edge u -> v. Return the time until every
node has the signal, or -1 if some node never gets it: n = 4, k = 1,
[[1, 2, 4], [1, 3, 1], [3, 2, 2], [2, 4, 1], [3, 4, 5]] -> 4.
"""
import heapq            # heappush / heappop keep the smallest at index 0
import math             # math.inf: no route known yet


# --- algorithm ---
def dijkstra(graph, source):
    """Pop the closest unsettled node; its distance is final. Relax its edges.
    O((V + E) log V) time."""
    dist = [math.inf] * len(graph)
    dist[source] = 0
    heap = []
    heapq.heappush(heap, (0, source))   # (distance so far, node)
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                    # stale entry: node was settled closer
        for neighbor, weight in graph[node]:
            if d + weight < dist[neighbor]:     # relax: a shorter route
                dist[neighbor] = d + weight
                heapq.heappush(heap, (dist[neighbor], neighbor))
    return dist


def network_delay_time(times, n, k):
    """Each node hears the signal at its shortest distance; take the largest.
    O((V + E) log V)."""
    graph = []
    for _ in range(n + 1):              # nodes are 1..n; slot 0 is unused
        graph.append([])
    for u, v, w in times:
        graph[u].append((v, w))
    dist = dijkstra(graph, k)
    slowest = 0
    for node in range(1, n + 1):
        if dist[node] == math.inf:
            return -1                   # this node never gets the signal
        slowest = max(slowest, dist[node])
    return slowest


# --- try it ---
times = [[1, 2, 4], [1, 3, 1], [3, 2, 2], [2, 4, 1], [3, 4, 5]]
print(network_delay_time(times, 4, 1))                              # -> 4
print(network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))  # -> 2
print(network_delay_time([[1, 2, 1]], 2, 2))                        # -> -1
graph = [[], [(2, 4), (3, 1)], [(4, 1)], [(2, 2), (4, 5)], []]
print(dijkstra(graph, 1))                           # -> [inf, 0, 3, 1, 4]
