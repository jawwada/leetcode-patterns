"""
Minimum Weighted Subgraph With the Required Paths (LeetCode 2203) - Hard
Chapter: graphs
Pattern: Dijkstra (min-heap shortest paths)

A weighted directed graph on n nodes is given as edges [u, v, w]. Return the minimum total
weight of a subgraph in which both src1 and src2 can reach dest, or -1 if none exists.
Example: n = 6, edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]],
src1 = 0, src2 = 1, dest = 5 -> 9 (edges 1->0, 0->2, 2->3, 3->4, 4->5)
"""
import heapq                       # heappush / heappop keep the smallest at index 0
import math                        # math.inf


# --- brute force ---
def bellman_ford(n, edges, src):
    """Shortest distances from src by relaxing every edge n - 1 times. O(V * E)."""
    dist = [math.inf] * n
    dist[src] = 0
    for sweep in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def brute_force(n, edges, src1, src2, dest):
    """Per meeting node x, three Bellman-Fords: src1 -> x, src2 -> x, x -> dest. O(V^2 * E)."""
    best = math.inf
    for x in range(n):                 # the two paths merge at x and share the tail x -> dest
        total = bellman_ford(n, edges, src1)[x] + bellman_ford(n, edges, src2)[x]
        total += bellman_ford(n, edges, x)[dest]
        if total < best:
            best = total
    if best == math.inf:
        return -1
    return best


# --- optimal ---
def dijkstra(adj, src):
    """Shortest distances from src over adjacency lists of (neighbour, weight). O(E log V)."""
    dist = [math.inf] * len(adj)
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                   # stale entry: u was already settled with a smaller distance
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


def minimum_weighted_subgraph_with_the_required_paths(n, edges, src1, src2, dest):
    """Dijkstra from src1, from src2 and from dest on the reversed graph; min over x. O(E log V)"""
    forward = []
    backward = []
    for node in range(n):
        forward.append([])
        backward.append([])
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))     # reversed: a walk from dest here is a walk to dest there
    d1 = dijkstra(forward, src1)
    d2 = dijkstra(forward, src2)
    dd = dijkstra(backward, dest)      # dd[x] = shortest x -> dest in the original graph
    best = math.inf
    for x in range(n):                 # x is where the two paths merge
        if d1[x] + d2[x] + dd[x] < best:
            best = d1[x] + d2[x] + dd[x]
    if best == math.inf:
        return -1
    return best


# --- try the brute force ---
edges_a = [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3], [2, 3, 4], [3, 4, 2],
           [4, 5, 1]]
print(brute_force(6, edges_a, 0, 1, 5))                                               # -> 9
print(brute_force(3, [[0, 1, 1], [2, 1, 1]], 0, 1, 2))                                # -> -1
print(brute_force(4, [[0, 3, 10], [1, 3, 10], [0, 2, 1], [1, 2, 1], [2, 3, 1]], 0, 1, 3))  # -> 3
print(brute_force(2, [[0, 1, 4]], 0, 1, 1))                                           # -> 4


# --- try the optimal ---
edges_a = [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3], [2, 3, 4], [3, 4, 2],
           [4, 5, 1]]
print(minimum_weighted_subgraph_with_the_required_paths(6, edges_a, 0, 1, 5))         # -> 9
edges_b = [[0, 1, 1], [2, 1, 1]]
print(minimum_weighted_subgraph_with_the_required_paths(3, edges_b, 0, 1, 2))         # -> -1
edges_c = [[0, 3, 10], [1, 3, 10], [0, 2, 1], [1, 2, 1], [2, 3, 1]]
print(minimum_weighted_subgraph_with_the_required_paths(4, edges_c, 0, 1, 3))         # -> 3
print(minimum_weighted_subgraph_with_the_required_paths(2, [[0, 1, 4]], 0, 1, 1))     # -> 4
