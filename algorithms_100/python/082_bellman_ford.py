"""
Bellman-Ford - Relax Every Edge n - 1 Times

Given n nodes, directed edges [u, v, w] whose weights may be negative, and a
source, return the shortest distance to every node (inf if unreachable), or
None if a negative cycle is reachable: n = 4, source 0,
edges [[2, 3, 1], [1, 2, -3], [0, 1, 4], [0, 2, 2]] -> [0, 4, 1, 2].
"""
import math                             # math.inf: no path found yet


# --- algorithm ---
def bellman_ford(n, edges, source):
    """Relax every edge, round after round, at most n - 1 rounds; a later
    improvement means a negative cycle. O(V * E) time, O(V) space."""
    dist = [math.inf] * n
    dist[source] = 0
    for _ in range(n - 1):              # a shortest path has <= n - 1 edges
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:   # inf + w stays inf: no false relax
                dist[v] = dist[u] + w   # a cheaper way into v, through u
                changed = True
        if not changed:
            break                       # quiet round: all distances final
    for u, v, w in edges:
        if dist[u] + w < dist[v]:       # still improving after n - 1 rounds
            return None                 # a negative cycle is reachable
    return dist


# --- try it ---
edges = [[2, 3, 1], [1, 2, -3], [0, 1, 4], [0, 2, 2]]
print(bellman_ford(4, edges, 0))                    # -> [0, 4, 1, 2]
print(bellman_ford(3, [[0, 1, 5]], 0))              # -> [0, 5, inf]
reachable_cycle = [[0, 1, 1], [1, 2, -1], [2, 1, -1]]
print(bellman_ford(3, reachable_cycle, 0))          # -> None
unreachable_cycle = [[0, 1, 2], [2, 3, -1], [3, 2, -1]]
print(bellman_ford(4, unreachable_cycle, 0))        # -> [0, 2, inf, inf]
