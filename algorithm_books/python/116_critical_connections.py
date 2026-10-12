"""
Critical Connections - Tarjan's Bridges: Discovery Time vs Low-Link

Given n nodes and an undirected edge list with no repeated edges, return every
edge whose removal splits its component in two (a bridge), each pair sorted
and the list sorted: n = 7, edges 0-1 1-2 2-0 1-3 3-4 4-5 5-3 5-6
-> [[1, 3], [5, 6]].
"""


# --- algorithm ---
def critical_connections(n, connections):
    """One DFS stamps discovery times and low-links; tree edge u-v is a bridge
    when nothing below v reaches back to u or above. O(V + E) time and space."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)                  # undirected: both directions
    disc = [-1] * n                         # discovery time, -1 = not visited
    low = [0] * n                           # lowest disc the subtree reaches
    timer = [0]                             # next discovery time, one box
    bridges = []
    for start in range(n):                  # one DFS per component
        if disc[start] == -1:
            dfs(graph, start, -1, disc, low, timer, bridges)
    bridges.sort()                          # a deterministic order
    return bridges


def dfs(graph, u, parent, disc, low, timer, bridges):
    """Stamp u, explore below it, and record every bridge in its subtree."""
    disc[u] = timer[0]
    low[u] = timer[0]
    timer[0] += 1
    for v in graph[u]:
        if v == parent:
            continue                        # the tree edge we came down by
        if disc[v] == -1:                   # tree edge: explore v first
            dfs(graph, v, u, disc, low, timer, bridges)
            low[u] = min(low[u], low[v])
            if low[v] > disc[u]:            # nothing below v reaches u or above
                bridges.append([min(u, v), max(u, v)])
        else:
            low[u] = min(low[u], disc[v])   # back edge to an ancestor


# --- try it ---
edges = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4], [4, 5], [5, 3], [5, 6]]
print(critical_connections(7, edges))       # -> [[1, 3], [5, 6]]
print(critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))   # -> [[1, 3]]
print(critical_connections(3, [[0, 1], [1, 2], [2, 0]]))           # -> []
forest = [[3, 2], [1, 0], [2, 4]]           # two trees: every edge is a bridge
print(critical_connections(5, forest))      # -> [[0, 1], [2, 3], [2, 4]]
