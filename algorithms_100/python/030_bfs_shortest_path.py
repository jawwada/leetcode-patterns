"""
BFS Shortest Path - Unweighted Graphs, Layer by Layer

Given an undirected graph on nodes 0..n-1 as an edge list, return a shortest
path from source to target as a list of nodes, or [] if there is none:
edges 0-1 1-2 2-3 3-4 0-5 5-4, source 0, target 4 -> [0, 5, 4].
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def shortest_path(n, edges, source, target):
    """BFS; the first time a node is reached is by a shortest path. O(V + E)."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)              # undirected: store both directions
        graph[v].append(u)
    dist = [-1] * n                     # -1 means not reached yet
    parent = [-1] * n                   # the node that first reached it
    dist[source] = 0
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:    # first visit is a shortest one
                dist[neighbor] = dist[node] + 1     # mark when enqueued
                parent[neighbor] = node
                queue.append(neighbor)
    if dist[target] == -1:
        return []                       # target is in another component
    return build_path(parent, target)


def build_path(parent, target):
    """Follow parent pointers back to the source, then reverse. O(V)."""
    path = []
    node = target
    while node != -1:                   # only the source has no parent
        path.append(node)
        node = parent[node]
    return path[::-1]


# --- try it ---
edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 4]]
print(shortest_path(6, edges, 0, 4))        # -> [0, 5, 4]
print(shortest_path(6, edges, 0, 3))        # -> [0, 1, 2, 3]
print(shortest_path(3, [[0, 1]], 0, 2))     # -> []
print(shortest_path(1, [], 0, 0))           # -> [0]
