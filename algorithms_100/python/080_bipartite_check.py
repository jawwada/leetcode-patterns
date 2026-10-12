"""
Bipartite Check - BFS Two-Coloring

Given an undirected graph as an adjacency list (graph[u] lists the neighbors
of u), decide whether its nodes split into two sides with every edge running
between the sides. A square 0-1-2-3 plus a separate triangle 4-5-6:
[[1, 3], [0, 2], [1, 3], [0, 2], [5, 6], [4, 6], [4, 5]] -> False.
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def is_bipartite(graph):
    """BFS each component, giving every neighbor the opposite color; an edge
    inside one color means an odd cycle. O(V + E) time."""
    n = len(graph)
    color = [-1] * n                    # -1 uncolored, else side 0 or 1
    for start in range(n):
        if color[start] != -1:
            continue                    # colored by an earlier search
        color[start] = 0                # a new component: either side works
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]   # the other side
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False        # an edge inside one side
    return True


# --- try it ---
graph = [[1, 3], [0, 2], [1, 3], [0, 2], [5, 6], [4, 6], [4, 5]]
print(is_bipartite(graph))                                  # -> False
print(is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]))       # -> True
print(is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]))  # -> False
print(is_bipartite([[], [2], [1]]))                         # -> True
