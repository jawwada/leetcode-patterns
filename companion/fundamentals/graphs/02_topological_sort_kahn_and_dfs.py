"""
Topological Sort: Kahn and DFS - Fundamentals
Chapter: fundamentals/graphs
Key operations: count indegrees, queue of indegree-0 nodes, decrement on removal, cycle by count

Given n tasks 0..n-1 and directed edges (u, v) meaning u must come before v, return an order that
satisfies every edge, or [] if the graph has a cycle. Kahn peels off nodes with no remaining
prerequisite; the DFS version reverses the post-order and spots a cycle when it meets a grey node.
Example: n=6, edges [(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)] -> Kahn [4, 5, 2, 0, 3, 1]
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def build_adjacency(n, edges):
    """adj[u] lists the nodes that must come after u. O(n + m)."""
    adj = []
    for _ in range(n):
        adj.append([])
    for u, v in edges:
        adj[u].append(v)
    return adj


def topological_sort_kahn(n, edges):
    """Kahn: repeatedly remove a node with indegree 0; nodes left over form a cycle. O(n + m)."""
    adj = build_adjacency(n, edges)
    indegree = [0] * n
    for u, v in edges:
        indegree[v] += 1
    queue = deque()
    for node in range(n):
        if indegree[node] == 0:        # nothing has to come before it: it can go first
            queue.append(node)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in adj[node]:
            indegree[neighbour] -= 1   # one prerequisite done
            if indegree[neighbour] == 0:
                queue.append(neighbour)
    if len(order) < n:                 # some nodes never reached indegree 0: a cycle
        return []
    return order


def visit(adj, node, color, post):
    """DFS from node; color 1 = on the current path, 2 = finished. False when a cycle is found."""
    color[node] = 1
    for neighbour in adj[node]:
        if color[neighbour] == 1:      # back to a node still on the path: a cycle
            return False
        if color[neighbour] == 0 and not visit(adj, neighbour, color, post):
            return False
    color[node] = 2
    post.append(node)                  # appended after all its descendants
    return True


def topological_sort_dfs(n, edges):
    """Reverse post-order: a node is appended only after everything it points to. O(n + m)."""
    adj = build_adjacency(n, edges)
    color = [0] * n                    # 0 white (unvisited), 1 grey, 2 black
    post = []
    for node in range(n):
        if color[node] == 0 and not visit(adj, node, color, post):
            return []
    return post[::-1]


# --- try it ---
edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
print(topological_sort_kahn(6, edges))             # -> [4, 5, 2, 0, 3, 1]
print(topological_sort_dfs(6, edges))              # -> [5, 4, 2, 3, 1, 0]
print(topological_sort_kahn(3, [(0, 1), (1, 2)]))  # -> [0, 1, 2]
print(topological_sort_kahn(3, [(0, 1), (1, 2), (2, 0)]))   # -> []  (cycle)
print(topological_sort_dfs(3, [(0, 1), (1, 2), (2, 0)]))    # -> []  (cycle)
