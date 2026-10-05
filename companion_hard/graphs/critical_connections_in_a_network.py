"""
Critical Connections in a Network (LeetCode 1192) - Hard
Chapter: graphs
Pattern: Tarjan bridges (DFS low-link)

n servers 0..n-1 are joined by undirected connections forming a connected graph. A connection
is critical if removing it disconnects some pair of servers. Return all critical connections,
in any order (the demos sort them so the two answers compare).
Example: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]] -> [[1, 3]]
"""


# --- helpers ---
def sort_edges(edges):
    """Each pair as [small, big], then the pairs in order, so two answers compare easily."""
    result = []
    for u, v in edges:
        result.append([min(u, v), max(u, v)])
    result.sort()
    return result


# --- brute force ---
def all_reached(n, connections, skip):
    """DFS from node 0 using every connection except connections[skip]; did we reach all n?"""
    adj = []
    for node in range(n):
        adj.append([])
    for i in range(len(connections)):
        if i != skip:
            u, v = connections[i]
            adj[u].append(v)
            adj[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        cur = stack.pop()
        for nb in adj[cur]:
            if nb not in seen:
                seen.add(nb)
                stack.append(nb)
    return len(seen) == n


def brute_force(n, connections):
    """Remove each connection in turn; a bridge leaves node 0 unable to reach all. O(E * (V+E))."""
    bridges = []
    for skip in range(len(connections)):   # each test re-walks nearly the same graph
        if not all_reached(n, connections, skip):
            bridges.append(connections[skip])
    return bridges


# --- optimal ---
def visit(u, parent_node, adj, disc, low, timer, bridges):
    """Tarjan DFS from u: fill disc and low, record bridges; returns the next free timestamp."""
    disc[u] = timer
    low[u] = timer
    timer += 1
    for v in adj[u]:
        if v == parent_node:
            continue                   # the tree edge we came down is not a way around itself
        if disc[v] == -1:
            timer = visit(v, u, adj, disc, low, timer, bridges)
            low[u] = min(low[u], low[v])
            if low[v] > disc[u]:       # v's subtree cannot climb above u: (u, v) is the only link
                bridges.append([u, v])
        else:
            low[u] = min(low[u], disc[v])    # back edge to an ancestor
    return timer


def critical_connections_in_a_network(n, connections):
    """One DFS with discovery times and low-links finds every bridge. O(V + E)."""
    adj = []
    for node in range(n):
        adj.append([])
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
    disc = [-1] * n                    # discovery time, -1 = not visited yet
    low = [0] * n                      # earliest disc reachable from the subtree via one back edge
    bridges = []
    visit(0, -1, adj, disc, low, 0, bridges)
    return bridges


# --- try the brute force ---
print(sort_edges(brute_force(4, [[0, 1], [1, 2], [2, 0], [1, 3]])))                  # -> [[1, 3]]
print(sort_edges(brute_force(3, [[0, 1], [1, 2], [2, 0]])))                          # -> []
connections_c = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]]
print(sort_edges(brute_force(6, connections_c)))                                     # -> [[2, 3]]
print(sort_edges(brute_force(5, [[0, 1], [1, 2], [2, 3], [3, 4]])))
# -> [[0, 1], [1, 2], [2, 3], [3, 4]]


# --- try the optimal ---
connections_a = [[0, 1], [1, 2], [2, 0], [1, 3]]
print(sort_edges(critical_connections_in_a_network(4, connections_a)))      # -> [[1, 3]]
print(sort_edges(critical_connections_in_a_network(3, [[0, 1], [1, 2], [2, 0]])))           # -> []
connections_c = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]]
print(sort_edges(critical_connections_in_a_network(6, connections_c)))      # -> [[2, 3]]
print(sort_edges(critical_connections_in_a_network(5, [[0, 1], [1, 2], [2, 3], [3, 4]])))
# -> [[0, 1], [1, 2], [2, 3], [3, 4]]
