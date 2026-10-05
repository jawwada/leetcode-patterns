"""
Graph DFS, Recursive and Iterative - Fundamentals
Chapter: fundamentals/searches
Key operations: visited set, recurse into unvisited neighbours, stack with neighbours reversed

Visit the nodes reachable from `start` in a directed graph (adjacency lists) and return the order
of visitation. The recursive version is the definition; the explicit-stack version gives the same
order only when neighbours are pushed in REVERSE (first neighbour on top) and a node is marked when
popped, not when pushed, so a stale copy deeper in the stack is skipped.
Example: {0: [1, 2], 1: [3], 2: [3], 3: []}, start 0 -> [0, 1, 3, 2]
"""


# --- algorithm ---
def dfs_recursive(graph, node, seen, order):
    """Mark node, record it, then recurse into each neighbour not seen yet. O(V + E)."""
    seen.add(node)
    order.append(node)
    for neighbour in graph[node]:
        if neighbour not in seen:
            dfs_recursive(graph, neighbour, seen, order)
    return order


def dfs_iterative(graph, start):
    """Explicit stack; push neighbours reversed so the first is popped first; mark when popped."""
    order = []
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue                   # a stale copy: this node was already reached another way
        seen.add(node)
        order.append(node)
        for neighbour in reversed(graph[node]):   # reverse so graph[node][0] ends up on top
            stack.append(neighbour)
    return order


# --- try it ---
graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
print(dfs_recursive(graph, 0, set(), []))   # -> [0, 1, 3, 2]
print(dfs_iterative(graph, 0))              # -> [0, 1, 3, 2]
cycle = {0: [1], 1: [2], 2: [0, 3], 3: []}
print(dfs_recursive(cycle, 0, set(), []))   # -> [0, 1, 2, 3]
print(dfs_iterative(cycle, 0))              # -> [0, 1, 2, 3]
