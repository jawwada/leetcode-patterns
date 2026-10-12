"""
Topological Sort with DFS - Reverse Postorder

Given n nodes 0..n-1 and directed edges [u, v] meaning u must come before v,
return an order of all the nodes that respects every edge, or [] if a cycle
makes that impossible:
n = 6, [[0, 3], [1, 3], [3, 4], [3, 2], [4, 5], [2, 5]] -> [1, 0, 3, 2, 4, 5].
"""


# --- algorithm ---
WHITE = 0                           # not visited yet
GRAY = 1                            # on the current DFS path
BLACK = 2                           # finished: placed after its descendants


def topological_sort(n, edges):
    """List nodes as they finish in a DFS, then reverse; [] on a cycle.
    O(V + E) time."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
    color = [WHITE] * n
    finished = []                       # nodes in the order they finish
    for node in range(n):
        if color[node] == WHITE and not dfs(graph, node, color, finished):
            return []                   # a cycle: no order exists
    return finished[::-1]


def dfs(graph, node, color, finished):
    """Finish node after everything it points to; False if a cycle is found.
    O(V + E) over all calls."""
    color[node] = GRAY                  # node joins the current path
    for neighbor in graph[node]:
        if color[neighbor] == GRAY:
            return False                # back edge: a cycle
        if color[neighbor] == WHITE:
            if not dfs(graph, neighbor, color, finished):
                return False
    color[node] = BLACK
    finished.append(node)               # its descendants are all in already
    return True


# --- try it ---
edges = [[0, 3], [1, 3], [3, 4], [3, 2], [4, 5], [2, 5]]
print(topological_sort(6, edges))                       # -> [1, 0, 3, 2, 4, 5]
print(topological_sort(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))  # -> [0, 2, 1, 3]
print(topological_sort(3, [[0, 1], [1, 2], [2, 0]]))    # -> []
print(topological_sort(2, []))                          # -> [1, 0]
