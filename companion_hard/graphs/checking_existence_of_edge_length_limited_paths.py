"""
Checking Existence of Edge Length Limited Paths (LeetCode 1697) - Hard
Chapter: graphs
Pattern: Union-Find (disjoint set union)

An undirected graph on n nodes has weighted edgeList (parallel edges allowed) and queries
[p, q, limit]. For each query answer whether a path from p to q exists that uses only edges of
weight strictly less than limit; return the booleans in query order.
Example: n = 3, edgeList = [[0,1,2],[1,2,4],[2,0,8],[1,0,16]], queries = [[0,1,2],[0,2,5]]
-> [False, True]
"""


# --- brute force ---
def brute_force(n, edge_list, queries):
    """Per query, DFS from p over only the edges lighter than the limit. O(Q * (n + E))."""
    answers = []
    for p, q, limit in queries:
        adj = []                       # rebuilt from scratch for every query
        for node in range(n):
            adj.append([])
        for u, v, w in edge_list:
            if w < limit:
                adj[u].append(v)
                adj[v].append(u)
        seen = {p}
        stack = [p]
        while stack:
            cur = stack.pop()
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        answers.append(q in seen)
    return answers


# --- optimal ---
def find(parent, x):
    """Root of x in the union-find, halving the path on the way up."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def checking_existence_of_edge_length_limited_paths(n, edge_list, queries):
    """Sort edges and queries by weight; glue edges in as the limit sweeps up. O((E + Q) log)."""
    parent = list(range(n))
    edges = []
    for u, v, w in edge_list:
        edges.append((w, u, v))
    edges.sort()                       # lightest edge first
    order = []
    for i in range(len(queries)):
        order.append((queries[i][2], i))
    order.sort()                       # answer by increasing limit, remembering each slot
    answers = [False] * len(queries)
    j = 0
    for limit, qi in order:
        while j < len(edges) and edges[j][0] < limit:
            w, u, v = edges[j]
            parent[find(parent, u)] = find(parent, v)   # every lighter edge is glued in
            j += 1
        p = queries[qi][0]
        q = queries[qi][1]
        answers[qi] = find(parent, p) == find(parent, q)
    return answers


# --- try the brute force ---
print(brute_force(3, [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]], [[0, 1, 2], [0, 2, 5]]))
# -> [False, True]
print(brute_force(5, [[0, 1, 10], [1, 2, 5], [2, 3, 9], [3, 4, 13]], [[0, 4, 14], [1, 4, 13]]))
# -> [True, False]
print(brute_force(3, [[0, 1, 5], [0, 1, 1]], [[0, 1, 2], [1, 2, 100]]))      # -> [True, False]
print(brute_force(2, [], [[0, 1, 1]]))                                       # -> [False]


# --- try the optimal ---
edges_a = [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]]
print(checking_existence_of_edge_length_limited_paths(3, edges_a, [[0, 1, 2], [0, 2, 5]]))
# -> [False, True]
edges_b = [[0, 1, 10], [1, 2, 5], [2, 3, 9], [3, 4, 13]]
print(checking_existence_of_edge_length_limited_paths(5, edges_b, [[0, 4, 14], [1, 4, 13]]))
# -> [True, False]
edges_c = [[0, 1, 5], [0, 1, 1]]
print(checking_existence_of_edge_length_limited_paths(3, edges_c, [[0, 1, 2], [1, 2, 100]]))
# -> [True, False]
print(checking_existence_of_edge_length_limited_paths(2, [], [[0, 1, 1]]))   # -> [False]
