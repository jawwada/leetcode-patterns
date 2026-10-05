"""
Adjacency List, BFS and DFS - Basics
Area: graphs
Key operations: build adjacency list, BFS with a queue and a visited set, DFS with an explicit stack

Given n nodes 0..n-1, an edge list and a directed flag, build the adjacency list (neighbors sorted),
then return the BFS order and the DFS preorder from a source. Unreachable nodes never appear.
Example: n=6, edges [(0,1),(0,2),(1,3),(2,3),(3,4)], undirected, source 0
         -> BFS [0, 1, 2, 3, 4], DFS [0, 1, 3, 2, 4]   (node 5 is unreachable)
"""
import sys
from collections import deque

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(n, edges, directed, src):
    """Recursive preorder for DFS; hop counts by relaxing every edge n times (BFS order must be sorted by hops). O(n*m)."""
    nbrs = {u: set() for u in range(n)}
    for u, v in edges:
        nbrs[u].add(v)
        if not directed:
            nbrs[v].add(u)
    order = []

    def rec(u):
        order.append(u)
        for v in sorted(nbrs[u]):
            if v not in order:
                rec(v)

    rec(src)
    hops = {src: 0}
    for _ in range(n):
        for u in list(hops):
            for v in nbrs[u]:
                hops[v] = min(hops.get(v, n), hops[u] + 1)
    return hops, order


# --- optimal ---
def build_adj(n, edges, directed):
    """Adjacency list; an undirected edge is stored in both directions. O(n + m)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    for nbrs in adj:
        nbrs.sort()
    log("adjacency:", {u: adj[u] for u in range(n)})
    return adj


def bfs(adj, src):
    """Queue; mark a node visited when it is ENQUEUED so it enters the queue once. O(n + m)."""
    order, seen, q = [], {src}, deque([src])
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
        log(f"  BFS pop {u}: order {order} | queue {list(q)} seen {sorted(seen)}")
    return order


def dfs(adj, src):
    """Stack; push neighbors in reverse so the smallest comes out first, mark when POPPED. O(n + m)."""
    order, seen, stack = [], set(), [src]
    while stack:
        u = stack.pop()
        if u in seen:
            log(f"  DFS pop {u}: already seen, skip | stack {stack}")
            continue
        seen.add(u)
        order.append(u)
        for v in reversed(adj[u]):
            if v not in seen:
                stack.append(v)
        log(f"  DFS pop {u}: order {order} | stack top->bottom {stack[::-1]} seen {sorted(seen)}")
    return order


def solve(n, edges, directed, src):
    """Build the graph once, then run both traversals from src."""
    adj = build_adj(n, edges, directed)
    return bfs(adj, src), dfs(adj, src)


# --- demo ---
def demo():
    return solve(6, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)], False, 0)


# --- tests ---
def tests():
    assert solve(6, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)], False, 0) == ([0, 1, 2, 3, 4], [0, 1, 3, 2, 4])
    assert solve(3, [(0, 1), (1, 2)], True, 2) == ([2], [2])  # directed: nothing leaves node 2
    assert solve(3, [(0, 1), (1, 2)], False, 2) == ([2, 1, 0], [2, 1, 0])
    assert solve(1, [], False, 0) == ([0], [0])
    assert solve(4, [(0, 1), (1, 2), (2, 0), (0, 3)], True, 0) == ([0, 1, 3, 2], [0, 1, 2, 3])  # cycle: visited once
    import random
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))]
        edges = [(u, v) for u, v in edges if u != v]
        directed, src = rng.random() < 0.5, rng.randrange(n)
        bfs_order, dfs_order = solve(n, edges, directed, src)
        hops, preorder = brute_force(n, edges, directed, src)
        assert dfs_order == preorder, (n, edges, directed, src)
        assert sorted(bfs_order) == sorted(hops), (n, edges, directed, src)
        assert all(hops[a] <= hops[b] for a, b in zip(bfs_order, bfs_order[1:])), (n, edges, directed, src)


# --- bugs ---
BUGS = [
    {
        "replace": "        if not directed:",
        "with":    "        if directed:",
        "fix": "add the reverse edge v -> u only when the graph is UNdirected",
        "why": "Undirected graphs lose every reverse edge: from 0 in the example, DFS becomes [0, 1, 3, 4, 2] because 3 no longer knows 2.",
        "decoys": [
            {"line": "        nbrs.sort()", "change": "should sort in reverse"},
            {"line": "        adj[u].append(v)", "change": "should append (u, v)"},
            {"line": "    adj = [[] for _ in range(n)]", "change": "should be [[]] * n"},
        ],
    },
    {
        "replace": "        u = q.popleft()",
        "with":    "        u = q.pop()",
        "fix": "BFS takes from the FRONT of the queue (popleft); pop() turns it into a stack",
        "why": "Popping from the right explores the newest node first, so the order is no longer by distance: the example gives [0, 2, 3, 4, 1].",
        "decoys": [
            {"line": "                seen.add(v)", "change": "should mark u instead of v"},
            {"line": "    order, seen, q = [], {src}, deque([src])", "change": "seen should start empty"},
            {"line": "                q.append(v)", "change": "should be appendleft(v)"},
        ],
    },
    {
        "replace": "        for v in reversed(adj[u]):",
        "with":    "        for v in adj[u]:",
        "fix": "push neighbors in REVERSE so the smallest neighbor is on top and is explored first",
        "why": "Pushing in sorted order puts the largest neighbor on top, so the preorder differs from recursive DFS: the example gives [0, 2, 3, 4, 1].",
        "decoys": [
            {"line": "        if u in seen:", "change": "should be if u not in seen"},
            {"line": "                stack.append(v)", "change": "should also mark v as seen here"},
            {"line": "        seen.add(u)", "change": "should move after the for loop"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
