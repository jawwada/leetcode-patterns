"""
Prim's Minimum Spanning Tree - Grow One Tree with a Min-Heap

Given n nodes and undirected edges [u, v, w], return the total weight of a
minimum spanning tree, or None if the graph is disconnected: n = 5,
edges 0-1 (4), 0-2 (1), 1-2 (2), 1-3 (5), 2-3 (8), 3-4 (3) -> 11.
"""
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def prim(n, edges):
    """Grow one tree from node 0, always adding the cheapest edge that
    leaves it. O(E log V) time, O(V + E) space."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))         # undirected: store both directions
    in_tree = [False] * n
    heap = []
    heapq.heappush(heap, (0, 0))        # (cost to attach, node): start at 0
    total = 0
    count = 0
    while heap and count < n:
        cost, node = heapq.heappop(heap)
        if in_tree[node]:
            continue                    # stale: joined by a cheaper edge
        in_tree[node] = True            # mark when popped, not when pushed
        total += cost
        count += 1
        for weight, neighbor in graph[node]:
            if not in_tree[neighbor]:
                heapq.heappush(heap, (weight, neighbor))
    if count < n:
        return None                     # some node was never reached
    return total


# --- try it ---
edges = [[0, 1, 4], [0, 2, 1], [1, 2, 2], [1, 3, 5], [2, 3, 8], [3, 4, 3]]
print(prim(5, edges))                               # -> 11
print(prim(4, [[0, 1, 1], [2, 3, 1]]))              # -> None
print(prim(3, [[0, 1, 5], [1, 2, -2], [0, 2, 1]]))  # -> -1
print(prim(1, []))                                  # -> 0
