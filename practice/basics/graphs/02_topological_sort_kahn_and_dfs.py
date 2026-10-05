"""
Topological Sort: Kahn and DFS - Basics
Area: graphs
Key operations: count indegrees, queue of indegree-0 nodes, decrement on removal, cycle check by count

Given n tasks 0..n-1 and directed edges (u, v) meaning u must come before v, return an order that
satisfies every edge, or [] if the graph has a cycle. Kahn's algorithm is the main solution; the
brute force is the DFS version (reversed post-order) used to cross-check validity.
Example: n=6, edges [(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)] -> [4, 5, 2, 0, 3, 1]
"""
import sys
from collections import deque

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(n, edges):
    """DFS: a node is appended when all its descendants are done, reverse the post-order; a grey node seen again is a cycle. O(n + m)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n  # 0 white (unvisited), 1 grey (on the current path), 2 black (finished)
    post = []

    def visit(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1 or (color[v] == 0 and not visit(v)):
                return False
        color[u] = 2
        post.append(u)
        return True

    for u in range(n):
        if color[u] == 0 and not visit(u):
            return []
    return post[::-1]


# --- optimal ---
def solve(n, edges):
    """Kahn: repeatedly remove a node with indegree 0; if nodes are left over, they form a cycle. O(n + m)."""
    adj = [[] for _ in range(n)]
    indeg = {u: 0 for u in range(n)}
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    order = []
    log(f"indegree {indeg} | queue {list(q)}")
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
        log(f"  pop {u}: order {order} | queue {list(q)} indegree {indeg}")
    if len(order) < n:
        log(f"  removed {len(order)} of {n} nodes; {[u for u in range(n) if indeg[u] > 0]} are stuck on a cycle")
        return []
    return order


# --- demo ---
def demo():
    return solve(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)])


# --- tests ---
def tests():
    def valid(order, n, edges):
        pos = {u: i for i, u in enumerate(order)}
        return sorted(order) == list(range(n)) and all(pos[u] < pos[v] for u, v in edges)

    assert solve(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]) == [4, 5, 2, 0, 3, 1]
    assert solve(3, [(0, 1), (1, 2), (2, 0)]) == []
    assert solve(3, [(0, 1), (1, 2), (2, 1)]) == []  # a cycle plus a free node is still a cycle
    assert solve(1, []) == [0]
    assert solve(4, []) == [0, 1, 2, 3]
    assert solve(3, [(0, 1), (0, 1)]) == [0, 2, 1]  # duplicate edge: counted twice, decremented twice
    import random
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
        edges = [(u, v) for u, v in edges if u != v]
        if rng.random() < 0.5:  # force a DAG by orienting every edge low -> high
            edges = [(min(u, v), max(u, v)) for u, v in edges]
        kahn, dfs = solve(n, edges), brute_force(n, edges)
        assert (kahn == []) == (dfs == []), (n, edges)
        assert not kahn or (valid(kahn, n, edges) and valid(dfs, n, edges)), (n, edges)


# --- bugs ---
BUGS = [
    {
        "replace": "    if len(order) < n:",
        "with":    "    if not order:",
        "fix": "a cycle leaves SOME nodes unremoved; compare the count removed with n, not with zero",
        "why": "A cycle with a free node in front of it removes the free node, so the check passes and a partial order is returned: [(0,1),(1,2),(2,1)] gives [0] instead of [].",
        "decoys": [
            {"line": "    q = deque(u for u in range(n) if indeg[u] == 0)", "change": "should be indeg[u] <= 1"},
            {"line": "            indeg[v] -= 1", "change": "should decrement indeg[u]"},
            {"line": "        order.append(u)", "change": "should append after the for loop"},
        ],
    },
    {
        "replace": "        indeg[v] += 1",
        "with":    "        indeg[u] += 1",
        "fix": "an edge u -> v raises the INdegree of v, the node it points to",
        "why": "Counting outgoing edges puts sinks in the queue first and never frees their predecessors: the example removes only 0 and 1 and reports a cycle.",
        "decoys": [
            {"line": "        adj[u].append(v)", "change": "should append u to adj[v]"},
            {"line": "            if indeg[v] == 0:", "change": "should be == 1 before the decrement"},
            {"line": "        return []", "change": "should return order"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
