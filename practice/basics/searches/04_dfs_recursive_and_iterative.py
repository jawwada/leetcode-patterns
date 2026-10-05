"""
Graph DFS, Recursive and Iterative - Basics
Area: searches
Key operations: visited set, recurse into each unvisited neighbour, explicit stack with neighbours pushed in reverse, skip a node already visited when popped

Visit the nodes reachable from `start` in a directed graph (adjacency lists) and return the order of
visitation. The recursive version is the definition; the explicit-stack version must produce the same
order, which only works when neighbours are pushed in REVERSE so the first neighbour is on top, and a
node is marked when popped (not when pushed) so a stale copy deeper in the stack is skipped.
Example: {0: [1, 2], 1: [3], 2: [3], 3: []}, start 0 -> [0, 1, 3, 2]
"""


# --- brute force ---
def brute_force(graph, start):
    """Reference: simulate the call stack with a stack of neighbour iterators, exactly what recursion does underneath. O(V + E)."""
    order, seen, stack = [start], {start}, [iter(graph[start])]
    while stack:
        v = next(stack[-1], None)
        if v is None:
            stack.pop()
        elif v not in seen:
            seen.add(v)
            order.append(v)
            stack.append(iter(graph[v]))
    return order


# --- optimal ---
def solve(graph, start):
    """Recursive DFS, then an explicit-stack DFS that must visit in the same order. Both O(V + E)."""
    order, seen = [], set()

    def dfs(u, depth):
        seen.add(u)
        order.append(u)
        for v in graph[u]:
            if v not in seen:
                dfs(v, depth + 1)
    dfs(start, 0)
    it_order, done, stack = [], set(), [start]
    while stack:
        u = stack.pop()
        if u in done:
            continue
        done.add(u)
        it_order.append(u)
        stack.extend(reversed(graph[u]))
    assert it_order == order, (order, it_order)
    return order


# --- demo ---
def demo():
    return solve({0: [1, 2], 1: [3], 2: [3], 3: []}, 0)


# --- bugs ---
BUGS = [
    {
        "replace": "        stack.extend(reversed(graph[u]))",
        "with":    "        stack.extend(graph[u])",
        "fix": "push the neighbours in reverse so the FIRST neighbour ends on top and is explored next, like the recursion",
        "why": "The last neighbour pops first, so the iterative order differs from the recursive one: {0: [1, 2], ...} visits 2 before 1.",
        "decoys": [
            {"line": "        done.add(u)", "change": "should mark when pushing instead"},
            {"line": "        u = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "            if v not in seen:", "change": "should be if v not in order"},
        ],
    },
    {
        "replace": "    it_order, done, stack = [], set(), [start]",
        "with":    "    it_order, done, stack = [], {start}, [start]",
        "fix": "mark a node when it is POPPED, not when it is pushed; the stack is seeded unmarked",
        "why": "The BFS habit of marking on push: the start is popped, seen as already visited and skipped, so the iterative order is [] and the assert fails.",
        "decoys": [
            {"line": "        if u in done:", "change": "should be if u in seen"},
            {"line": "    dfs(start, 0)", "change": "should be dfs(start, 1)"},
            {"line": "        it_order.append(u)", "change": "should append before the done check"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
