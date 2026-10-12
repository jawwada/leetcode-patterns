## Bridges and Low-Link DFS

A bridge is an edge whose removal disconnects part of a graph. A DFS discovery time and a low-link value tell whether a subtree can reach above its parent edge.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Critical Connections in a Network gives a connected network of servers and asks for every cable whose removal disconnects some pair: in a triangle 0-1-2 with server 3 hanging off 1, only `[1, 3]` is critical. Removing each edge and re-running a BFS costs O(E · (V + E)); one DFS does it all.

Picture the DFS tree with every non-tree edge as a *rope* from a deep node up to an ancestor: cut the tree edge above v, and v's subtree stays attached exactly when some rope from inside it reaches above the cut.

```text
        0 <------+      tree edges go down; the non-tree edge 2-0 is a rope from 2 up to 0
        |        |
        1        |      cut 0-1 or 1-2: the rope from 2 still holds that piece, so neither is a bridge
       / \       |
      2   3      |      cut 1-3: nothing below 3 climbs above 1, so 3 falls off: a bridge
      |          |
      +----------+      disc = visiting order; low[v] = the smallest disc a rope from v's subtree reaches
```

In the code, `disc[v]` is the order in which the DFS visits v, and `low[v]` is the smallest `disc` a rope from v's subtree reaches. The tree edge (u, v) is a bridge exactly when `low[v] > disc[u]`: nothing below v climbs back to u or above it.

<!-- cell -->

```python
def critical_connections(n, connections):
    graph = [[] for _ in range(n)]
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)
    disc = [-1] * n                               # discovery time; -1 = not visited yet
    low = [0] * n                                 # smallest disc reachable from u's subtree with one back edge
    bridges, timer = [], 0

    def dfs(u, parent):
        nonlocal timer
        disc[u] = low[u] = timer
        timer += 1
        for v in graph[u]:
            if v == parent:
                continue                          # do not count the edge we came in on
            if disc[v] == -1:                     # tree edge: explore the child first
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:              # v's subtree cannot get back to u or above it
                    bridges.append([u, v])
            else:                                 # visited: an ancestor (back edge) or a finished descendant (larger disc: harmless)
                low[u] = min(low[u], disc[v])

    dfs(0, -1)
    return bridges


print(critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))           # [[1, 3]]
print(critical_connections(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))   # [[3, 4], [1, 3]]
```

<!-- cell -->

**Try it**
- Delete the `if v == parent: continue` lines: the first example returns `[]`. The edge back to the parent looks like a rope, so every subtree seems to have a way around.
- Change `low[v] > disc[u]` to `>=`: `[0, 1]` is reported too, although it sits on the triangle. `>=` belongs to the test for an articulation *node* (one whose removal disconnects; the root has its own rule), not to the bridge test.
- Print `disc` and `low` after `dfs(0, -1)`: `[0, 1, 2, 3]` and `[0, 0, 0, 3]`. Node 3's low (3) is bigger than node 1's disc (1): nothing below 3 reaches back, so 1-3 is a bridge.
- `critical_connections(5000, [[i, i + 1] for i in range(4999)])` raises `RecursionError`. Run `import sys; sys.setrecursionlimit(20_000)` first and it returns all 4999 edges. LeetCode allows n = 10⁵: raise the limit or make the DFS iterative.

<!-- cell -->

Two more limits of this version. Parallel edges: `critical_connections(2, [[0, 1], [0, 1]])` gives `[[0, 1]]`, but removing one copy disconnects nothing; skip the parent *edge id*, not the parent node. A disconnected graph: `critical_connections(4, [[0, 1], [2, 3]])` misses the bridge 2-3, because the DFS has to be started from every unvisited node.
