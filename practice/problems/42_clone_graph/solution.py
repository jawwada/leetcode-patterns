"""
Clone Graph (LeetCode 133) - Medium
Area: graphs
Key operations: BFS from the start node, old -> new dict as the visited set, create a clone on first sight, wire clone -> clone edges

Given a node of a connected undirected graph (each node has a value and a list of neighbours),
return a deep copy: the same shape built from brand-new nodes, none shared with the input.
Here solve returns the copy read back as {value: sorted neighbour values} so it can be checked.
Example: the 4-cycle {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]} -> the same dict, from fresh nodes
"""
import sys
from collections import deque
from typing import Dict, List, Optional

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
class Node:
    def __init__(self, val: int):
        self.val, self.neighbors = val, []


def build(adj: Dict[int, List[int]]) -> Optional[Node]:
    """{value: [neighbour values]} -> the Node with the smallest value (None for an empty graph)."""
    nodes = {v: Node(v) for v in adj}
    for v, nbs in adj.items():
        nodes[v].neighbors = [nodes[u] for u in nbs]
    return nodes[min(nodes)] if nodes else None


def to_adj(node: Optional[Node]) -> Dict[int, List[int]]:
    """Walk from node and read the graph back as {value: sorted neighbour values}."""
    adj, stack = {}, ([node] if node else [])
    while stack:
        cur = stack.pop()
        if cur.val in adj:
            continue
        adj[cur.val] = sorted(nb.val for nb in cur.neighbors)
        stack.extend(cur.neighbors)
    return dict(sorted(adj.items()))


# --- brute force ---
def brute_force(node: Optional[Node]) -> Optional[Node]:
    """Three passes with no map: collect every original node, make one fresh copy per original, then for
    every edge scan the copy list for the endpoint with the matching value. O(V * E): the scan is the
    waste that the old -> new dict turns into an O(1) lookup."""
    if node is None:
        return None
    originals, stack = [], [node]
    while stack:
        cur = stack.pop()
        if cur not in originals:
            originals.append(cur)
            stack.extend(cur.neighbors)
    copies = [Node(o.val) for o in originals]
    for o, c in zip(originals, copies):
        for nb in o.neighbors:
            c.neighbors.append(next(cp for cp in copies if cp.val == nb.val))
    return copies[0]


# --- optimal ---
def clone_graph(node: Optional[Node]) -> Optional[Node]:
    """BFS from node; clones maps original -> copy and doubles as the visited set, so each original is
    copied exactly once and every edge is wired clone -> clone. O(V + E) time, O(V) space."""
    if node is None:
        return None
    clones = {node: Node(node.val)}
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        log(f"pop {cur.val}; queue {[q.val for q in queue]}; cloned so far {sorted(c.val for c in clones.values())}")
        for nb in cur.neighbors:
            if nb not in clones:
                clones[nb] = Node(nb.val)
                queue.append(nb)
                log(f"  {nb.val} seen for the first time: new Node({nb.val}), enqueue it")
            clones[cur].neighbors.append(clones[nb])
            log(f"  wire clone {cur.val} -> clone {nb.val}; copy so far {to_adj(clones[node])}")
    return clones[node]


def solve(node: Optional[Node]) -> Dict[int, List[int]]:
    """Clone, then read the copy back as {value: sorted neighbour values}."""
    return to_adj(clone_graph(node))


# --- demo ---
def demo():
    return solve(build({1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}))


# --- tests ---
def tests():
    def ids(node):
        seen, stack = set(), [node]
        while stack:
            cur = stack.pop()
            if id(cur) not in seen:
                seen.add(id(cur))
                stack.extend(cur.neighbors)
        return seen

    adj = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
    start = build(adj)
    assert solve(start) == adj
    copy = clone_graph(start)
    assert copy is not start and to_adj(copy) == adj
    assert not (ids(start) & ids(copy))                        # no node object shared
    assert to_adj(start) == adj                                # input untouched
    assert solve(None) == {}
    assert solve(build({1: []})) == {1: []}                    # single node
    assert solve(build({1: [2], 2: [1]})) == {1: [2], 2: [1]}
    assert solve(build({1: [2, 3], 2: [1, 3], 3: [1, 2]})) == {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    import random
    for _ in range(200):
        n = random.randint(1, 6)
        edges = {v: set() for v in range(1, n + 1)}
        for v in range(2, n + 1):                              # a random tree keeps it connected
            u = random.randint(1, v - 1)
            edges[v].add(u); edges[u].add(v)
        for _ in range(random.randint(0, n) if n > 1 else 0):  # extra edges
            u, v = random.sample(range(1, n + 1), 2)
            edges[v].add(u); edges[u].add(v)
        adj = {v: sorted(s) for v, s in edges.items()}
        start = build(adj)
        copy = clone_graph(start)
        assert to_adj(copy) == adj and not (ids(start) & ids(copy)), adj
        assert solve(start) == to_adj(brute_force(build(adj))) == adj, adj


# --- bugs ---
BUGS = [
    {
        "replace": "            clones[cur].neighbors.append(clones[nb])",
        "with":    "            clones[cur].neighbors.append(nb)",
        "fix": "link the clone of nb, not nb itself: the copy may contain only new nodes",
        "why": "The copy points at original nodes, so the adjacency reads the same but the two graphs share objects; the no-shared-node assert fails.",
        "decoys": [
            {"line": "    clones = {node: Node(node.val)}", "change": "should start as an empty dict"},
            {"line": "                queue.append(nb)", "change": "should append cur"},
            {"line": "    return clones[node]", "change": "should return clones"},
        ],
    },
    {
        "replace": "                queue.append(nb)",
        "with":    "                queue.append(cur)",
        "fix": "enqueue the newly seen neighbour so that its own edges get wired when it is popped",
        "why": "nb is cloned but never popped, so its clone keeps no neighbours and nodes two steps away are never cloned: the 4-cycle comes back as {1: [2, 2, 4, 4], 2: [], 4: []}.",
        "decoys": [
            {"line": "            if nb not in clones:", "change": "should be if nb not in queue"},
            {"line": "        cur = queue.popleft()", "change": "should be queue.pop()"},
            {"line": "                clones[nb] = Node(nb.val)", "change": "should be Node(cur.val)"},
        ],
    },
    {
        "replace": "    return clones[node]",
        "with":    "    return node",
        "fix": "return the clone of the start node, not the original",
        "why": "The adjacency matches, but the returned graph is the input itself: every node is shared, so the no-shared-node assert fails.",
        "decoys": [
            {"line": "    if node is None:", "change": "should be if not node.neighbors"},
            {"line": "    queue = deque([node])", "change": "should start empty"},
            {"line": "    return to_adj(clone_graph(node))", "change": "should be to_adj(node)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
