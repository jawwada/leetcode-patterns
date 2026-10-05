"""
Topological Sort: Kahn and DFS - Basics
Area: graphs
Key operations: count indegrees, queue of indegree-0 nodes, decrement on removal, cycle check by count

Given n tasks 0..n-1 and directed edges (u, v) meaning u must come before v, return an order that
satisfies every edge, or [] if the graph has a cycle. Kahn's algorithm is the main solution; the
brute force is the DFS version (reversed post-order) used to cross-check validity.
Example: n=6, edges [(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)] -> [4, 5, 2, 0, 3, 1]
"""
from collections import deque


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
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) < n:
        return []
    return order


# --- demo ---
def demo():
    return solve(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)])


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
    print("result:", demo())
