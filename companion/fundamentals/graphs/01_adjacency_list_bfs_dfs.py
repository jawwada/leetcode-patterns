"""
Adjacency List, BFS and DFS - Fundamentals
Chapter: fundamentals/graphs
Key operations: build adjacency list, BFS with a queue and a visited set, DFS with a stack

Given n nodes 0..n-1, an edge list and a directed flag, build the adjacency list (neighbours
sorted), then return the BFS order and the DFS preorder from a source. Unreachable nodes never
appear in either order.
Example: n=6, edges [(0,1),(0,2),(1,3),(2,3),(3,4)], undirected, source 0
         -> BFS [0, 1, 2, 3, 4], DFS [0, 1, 3, 2, 4]   (node 5 is unreachable)
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def build_adjacency(n, edges, directed):
    """adj[u] lists u's neighbours in sorted order; an undirected edge goes both ways. O(n + m)."""
    adj = []
    for _ in range(n):
        adj.append([])
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)           # undirected: store the edge in both directions
    for neighbours in adj:
        neighbours.sort()
    return adj


def bfs(adj, source):
    """Queue; mark a node visited when it is ENQUEUED so it enters the queue once. O(n + m)."""
    order = []
    seen = {source}
    queue = deque([source])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in adj[node]:
            if neighbour not in seen:
                seen.add(neighbour)    # mark here, not when popped
                queue.append(neighbour)
    return order


def dfs(adj, source):
    """Stack; push neighbours in reverse so the smallest pops first; mark when POPPED. O(n + m)."""
    order = []
    seen = set()
    stack = [source]
    while stack:
        node = stack.pop()
        if node in seen:
            continue                   # a stale copy: the node was already reached another way
        seen.add(node)
        order.append(node)
        for neighbour in reversed(adj[node]):   # reverse so adj[node][0] ends up on top
            if neighbour not in seen:
                stack.append(neighbour)
    return order


# --- try it ---
adj = build_adjacency(6, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)], False)
print(adj)              # -> [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3], []]
print(bfs(adj, 0))      # -> [0, 1, 2, 3, 4]
print(dfs(adj, 0))      # -> [0, 1, 3, 2, 4]
directed = build_adjacency(4, [(0, 1), (0, 2), (2, 3), (3, 1)], True)
print(bfs(directed, 0)) # -> [0, 1, 2, 3]
print(dfs(directed, 0)) # -> [0, 1, 2, 3]
