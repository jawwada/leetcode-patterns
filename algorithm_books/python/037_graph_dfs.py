"""
Depth-First Search on a Graph - Recursive and Iterative

Given an undirected graph with nodes 0..n-1 as an edge list, list the nodes in
the order a depth-first search from start first reaches them: n = 5,
edges [[0, 1], [0, 4], [0, 2], [1, 3], [3, 2]], start 0 -> [0, 1, 3, 2, 4].
"""


# --- algorithm ---
def build_graph(n, edges):
    """Adjacency list: graph[u] lists u's neighbors in edge order. O(V + E)."""
    graph = []
    for i in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)                  # undirected: both directions
    return graph


def dfs_recursive(n, edges, start):
    """Visit a node, then dive into each unvisited neighbor. O(V + E)."""
    graph = build_graph(n, edges)
    visited = set()
    order = []
    visit(graph, start, visited, order)
    return order


def visit(graph, node, visited, order):
    """Mark node on entry, record it, recurse into unvisited neighbors."""
    visited.add(node)                       # mark first: cycles cannot re-enter
    order.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            visit(graph, neighbor, visited, order)


def dfs_iterative(n, edges, start):
    """Explicit stack; mark when popped to match the recursion. O(V + E)."""
    graph = build_graph(n, edges)
    visited = set()
    order = []
    stack = []
    stack.append(start)
    while stack:
        node = stack.pop()
        if node in visited:
            continue                        # a stale copy, reached another way
        visited.add(node)                   # mark when popped
        order.append(node)
        for neighbor in reversed(graph[node]):  # first neighbor ends on top
            if neighbor not in visited:
                stack.append(neighbor)
    return order


# --- try it ---
edges = [[0, 1], [0, 4], [0, 2], [1, 3], [3, 2]]
print(dfs_recursive(5, edges, 0))           # -> [0, 1, 3, 2, 4]
print(dfs_iterative(5, edges, 0))           # -> [0, 1, 3, 2, 4]
print(dfs_iterative(4, [[0, 1], [2, 3]], 0))    # -> [0, 1]
print(dfs_recursive(1, [], 0))              # -> [0]
