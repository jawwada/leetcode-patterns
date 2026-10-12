"""
Cycle Detection in a Directed Graph - Three Colors: White, Gray, Black

Given n nodes 0..n-1 and directed edges [u, v] meaning u -> v, report whether
some path follows the arrows back to where it started:
n = 5, [[0, 1], [0, 2], [1, 3], [2, 3], [2, 4], [4, 0]] -> True.
"""


# --- algorithm ---
WHITE = 0                           # not visited yet
GRAY = 1                            # on the current DFS path
BLACK = 2                           # finished: no cycle is reachable from it


def has_cycle(n, edges):
    """DFS from every white node; an edge into a gray node closes a cycle.
    O(V + E) time."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
    color = [WHITE] * n
    for node in range(n):
        if color[node] == WHITE and dfs(graph, node, color):
            return True
    return False


def dfs(graph, node, color):
    """True if a cycle is reachable from node; paints node black otherwise.
    O(V + E) over all calls."""
    color[node] = GRAY                  # node joins the current path
    for neighbor in graph[node]:
        if color[neighbor] == GRAY:
            return True                 # back edge to a node on the path
        if color[neighbor] == WHITE and dfs(graph, neighbor, color):
            return True
    color[node] = BLACK                 # every path out of node is cycle-free
    return False


# --- try it ---
edges = [[0, 1], [0, 2], [1, 3], [2, 3], [2, 4], [4, 0]]
print(has_cycle(5, edges))                              # -> True
print(has_cycle(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))   # -> False
print(has_cycle(2, [[1, 1]]))                           # -> True
print(has_cycle(3, []))                                 # -> False
