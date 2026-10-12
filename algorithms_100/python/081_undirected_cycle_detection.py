"""
Cycle Detection in an Undirected Graph - DFS That Skips the Parent Edge

Given n nodes and an undirected edge list (no repeated edges), decide whether
the graph has a cycle; it may be disconnected:
n = 6, edges 0-1, 2-3, 3-4, 4-5, 5-2 -> True (2, 3, 4, 5 form a square).
"""


# --- algorithm ---
def has_cycle(n, edges):
    """DFS from every unvisited node; a visited neighbor that is not the
    parent closes a cycle. O(V + E) time, O(V + E) space."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)              # undirected: store both directions
    visited = [False] * n
    for start in range(n):              # a cycle can be in any component
        if visited[start]:
            continue
        visited[start] = True
        stack = []
        stack.append((start, -1))       # (node, the node we came from)
        while stack:
            node, parent = stack.pop()
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True    # mark when discovered
                    stack.append((neighbor, node))
                elif neighbor != parent:
                    return True         # reached again, not via parent
    return False


# --- try it ---
print(has_cycle(6, [[0, 1], [2, 3], [3, 4], [4, 5], [5, 2]]))   # -> True
print(has_cycle(5, [[0, 1], [0, 2], [0, 3], [1, 4]]))           # -> False
print(has_cycle(4, [[0, 1], [2, 3]]))                           # -> False
print(has_cycle(3, [[0, 1], [1, 2], [2, 0]]))                   # -> True
