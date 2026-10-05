"""
Connected Components - Fundamentals
Chapter: fundamentals/searches
Key operations: adjacency list from edges (both directions), BFS from every unvisited node, count

Count the connected components of an undirected graph with n nodes (0..n-1) given as an edge list.
Every BFS that starts from a node not seen yet marks exactly one whole component. A node with no
edges is a component of its own.
Example: n=7, edges [(0, 1), (1, 2), (3, 4)] -> 4  (components {0, 1, 2}, {3, 4}, {5}, {6})
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def build_adjacency(n, edges):
    """adj[u] lists the neighbours of u; an undirected edge is stored both ways. O(n + m)."""
    adj = []
    for _ in range(n):
        adj.append([])
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)               # both directions, or the answer depends on edge order
    return adj


def count_components(n, edges):
    """BFS from every node not yet seen; each BFS marks exactly one component. O(V + E)."""
    adj = build_adjacency(n, edges)
    seen = set()
    count = 0
    for start in range(n):
        if start in seen:
            continue
        count += 1                     # a fresh start node means a brand-new component
        seen.add(start)
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbour in adj[node]:
                if neighbour not in seen:
                    seen.add(neighbour)   # mark when enqueued so it enters the queue once
                    queue.append(neighbour)
    return count


# --- try it ---
print(count_components(7, [(0, 1), (1, 2), (3, 4)]))   # -> 4
print(count_components(3, []))                         # -> 3
print(count_components(4, [(0, 1), (1, 2), (2, 3)]))   # -> 1
print(count_components(5, [(0, 1), (2, 3), (3, 4)]))   # -> 2
