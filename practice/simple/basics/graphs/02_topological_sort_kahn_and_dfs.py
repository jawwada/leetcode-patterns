"""
Topological Sort: Kahn and DFS (basics: graphs)
Order tasks 0..n-1 so every edge (u, v) puts u before v; return [] if the edges contain a cycle.
  n = 6, edges [(5,2), (5,0), (4,0), (4,1), (2,3), (3,1)]
    ->  Kahn [4, 5, 2, 0, 3, 1], DFS [5, 4, 2, 3, 1, 0]   (both are valid orders)

Idea: Kahn: a node with indegree 0 has nothing left before it, so it can go next.
      DFS: a node finishes after everything it leads to, so reversed finish order works.
      On a cycle, Kahn never frees its nodes and DFS steps back onto a node still on its path.

Pseudocode:
  kahn:  queue = every node with indegree 0
         while queue:
             u = popleft; output u
             for v in adj[u]: indegree[v] -= 1; if it is now 0: append v
         if fewer than n nodes came out: return []          # the rest sit on a cycle
  dfs:   has_cycle(u): mark u ON PATH
                       for v in adj[u]: ON PATH -> cycle; NEW -> has_cycle(v)
                       mark u DONE; append u to post
         run it from every NEW node; return [] on a cycle, else post reversed

Time O(n + m) for each, space O(n + m).
"""
from collections import deque


def topo_sort_kahn(n, edges):
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:                   # u must come before v
        adj[u].append(v)
        indegree[v] += 1
    queue = deque(u for u in range(n) if indegree[u] == 0)   # nothing before them
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1             # u is done: v waits on one fewer
            if indegree[v] == 0:         # v is free now
                queue.append(v)
    return order if len(order) == n else []   # leftovers sit on a cycle


def topo_sort_dfs(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    state, post = [0] * n, []            # state: 0 new, 1 on the path, 2 done

    def has_cycle(u):                    # DFS from u, recording finish order
        state[u] = 1
        for v in adj[u]:
            if state[v] == 1:            # back onto the current path: cycle
                return True
            if state[v] == 0 and has_cycle(v):   # new node: explore it
                return True
        state[u] = 2
        post.append(u)                   # u finishes after all it leads to
        return False

    for u in range(n):
        if state[u] == 0 and has_cycle(u):
            return []
    return post[::-1]                    # reversed finish order


if __name__ == "__main__":
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    print(topo_sort_kahn(6, edges))  # [4, 5, 2, 0, 3, 1]
    print(topo_sort_dfs(6, edges))   # [5, 4, 2, 3, 1, 0]
    cycle = [(0, 1), (1, 2), (2, 1)]
    print(topo_sort_kahn(3, cycle), topo_sort_dfs(3, cycle))  # [] []
