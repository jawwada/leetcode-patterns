"""
Network Delay Time (LeetCode 743) - Medium
Chapter: graphs
Pattern: Dijkstra (min-heap shortest paths)

There are n nodes labelled 1..n and directed edges times[i] = (u, v, w) meaning a signal takes w
time units to travel from u to v. A signal is sent from node k. Return the time at which every
node has received it, or -1 if some node never does.
Example: times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2 -> 2.
"""
import heapq                       # heappush / heappop keep the smallest at index 0
import math                        # math.inf


# --- brute force ---
def brute_force(times, n, k):
    """Bellman-Ford: n - 1 rounds, and every round relaxes every edge. O(V*E) time."""
    dist = [math.inf] * (n + 1)      # nodes are 1..n; index 0 is unused
    dist[k] = 0
    for _ in range(n - 1):           # a shortest path uses at most n - 1 edges
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w    # found a faster way to reach v
    worst = max(dist[1:])
    if worst == math.inf:
        return -1                    # some node is unreachable
    return worst


# --- optimal ---
def network_delay_time(times, n, k):
    """Dijkstra: settle nodes in order of arrival time using a min-heap. O((V+E) log V) time."""
    neighbours = {}                  # u -> list of (v, w)
    for u, v, w in times:
        if u not in neighbours:
            neighbours[u] = []
        neighbours[u].append((v, w))
    arrival = {}                     # node -> final arrival time, once settled
    heap = [(0, k)]                  # (time, node) candidates; the smallest time is on top
    while heap:
        time, u = heapq.heappop(heap)
        if u in arrival:
            continue                 # stale entry: u was settled earlier with a smaller time
        arrival[u] = time            # smallest candidate = final: no later path can beat it
        for v, w in neighbours.get(u, []):
            if v not in arrival:
                heapq.heappush(heap, (time + w, v))
    if len(arrival) < n:
        return -1                    # some node was never reached
    return max(arrival.values())


# --- try the brute force ---
print(brute_force([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))      # -> 2
print(brute_force([[1, 2, 1]], 2, 1))                            # -> 1
print(brute_force([[1, 2, 1]], 2, 2))                            # -> -1
print(brute_force([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1))      # -> 3


# --- try the optimal ---
print(network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))      # -> 2
print(network_delay_time([[1, 2, 1]], 2, 1))                            # -> 1
print(network_delay_time([[1, 2, 1]], 2, 2))                            # -> -1
print(network_delay_time([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1))      # -> 3
