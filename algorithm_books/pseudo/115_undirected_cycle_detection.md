---
rank: 115
slug: undirected_cycle_detection
---

Given `n` nodes and a list of undirected edges with no edge repeated, decide whether the graph contains a cycle. The graph may be disconnected. With 6 nodes and edges `0-1, 2-3, 3-4, 4-5, 5-2` the answer is `true`: nodes 2, 3, 4 and 5 form a square, even though the component `0-1` is a plain tree.

A DFS marks each node the moment it discovers it and remembers the node it came from, its parent. The discovery edges form a spanning tree of each component, and a tree has no cycle, so a cycle must use some edge outside that tree. Such an edge joins two nodes that the tree already connects, and together with the tree path between them it closes a loop. So while a node scans its neighbors, there are three cases. An unmarked neighbor is discovered through a new tree edge. The parent is reached through the tree edge the search walked in on, seen again from the other end, because an undirected edge sits in both endpoints' lists. Any other neighbor that is already marked is an extra edge, and that is a cycle.

Picture unrolling a thread through the graph. Each edge out of the current node leads either to fresh ground, where the thread goes next, or to a node the thread already reaches. The edge you arrived on always leads back, so it proves nothing; any other edge to a marked node means the graph loops back on itself. An outer loop starts a fresh search from every unmarked node, because the cycle can sit in any component.

```text
  0 ─ 1          2 ─ 3
                 │   │
                 5 ─ 4

start   pop (node, parent)   neighbors   action
  0         (0, -1)          1           discover 1
            (1, 0)           0           0 is the parent: skip
  1     already visited
  2         (2, -1)          3, 5        discover 3, discover 5
            (5, 2)           4, 2        discover 4; 2 is the parent: skip
            (4, 5)           3, 5        3 is marked and is not the parent:
                                         edge 4-3 closes the square → true
```

```pseudo
FUNCTION HasCycle(n, edges)
    graph ← array of n empty lists
    FOR EACH [u, v] IN edges
        graph[u].append(v)
        graph[v].append(u)                    // undirected: both directions
    visited ← array of n copies of false
    FOR start FROM 0 TO n - 1                 // a cycle can be in any component
        IF visited[start]
            CONTINUE
        visited[start] ← true
        stack ← empty stack
        stack.push((start, -1))               // (node, the node we came from)
        WHILE stack is not empty
            (node, parent) ← stack.pop()
            FOR EACH neighbor IN graph[node]
                IF NOT visited[neighbor]
                    visited[neighbor] ← true  // mark when discovered
                    stack.push((neighbor, node))
                ELSE IF neighbor ≠ parent
                    RETURN true               // reached again, not via parent
    RETURN false
```

Each node is pushed once and each edge is scanned twice, once from each end, so the check runs in `O(V + E)` time and `O(V + E)` space for the lists. The explicit stack replaces recursion, whose depth reaches `n` on a long path and overflows Python's default limit; the recursive DFS makes exactly the same test. Union-find (#41) answers the question edge by edge instead: an edge whose two ends already share a root closes a cycle, and that edge is the answer to Redundant Connection. A graph is a valid tree exactly when it has `n - 1` edges and no cycle, or equivalently `n - 1` edges and a single component. In a directed graph a marked neighbor does not prove a cycle, which is why #81 needs three colors. The classic mistake is forgetting to skip the parent, which reports a cycle on the first tree edge seen from its child; the other is searching only from node 0 and missing a cycle in another component.

*Practice:* LC 261 Graph Valid Tree · LC 684 Redundant Connection · LC 1559 Detect Cycles in 2D Grid
