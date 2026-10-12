---
rank: 81
slug: directed_cycle_detection
---

Given a directed graph on nodes `0` to `n - 1`, decide whether it contains a cycle, a path that follows the arrows back to where it started. With the edges `0→1`, `0→2`, `1→3`, `2→3`, `2→4` and `4→0` the answer is yes, `0 → 2 → 4 → 0`. Without `4→0` the answer is no, even though node `3` can be reached two ways.

In an undirected graph, running into an already visited node signals a cycle, as long as it is not the parent just left (#115). In a directed graph it signals nothing: the diamond `0→1→3`, `0→2→3` reaches `3` twice and has no cycle. What matters is whether that node is still on the current path. The brute force asks every node whether it can reach itself, one search per node, `O(V · (V + E))`. A single DFS with three colors does better. White means not visited yet. Gray means entered but not finished: exactly the current recursion path. Black means finished: everything reachable from the node has been explored and holds no cycle. An edge into a gray node points back at an ancestor on the current path, and that back edge plus the path down from the ancestor is a cycle. An edge into a black node is harmless and never followed, which keeps the search linear.

Picture the gray nodes as a rope paid out behind the search: entering a node adds it to the rope, and finishing it reels it back in and paints it black. A cycle is an edge that lands back on the rope. In the trace, `2→3` lands on black `3`, finished and off the rope, where a plain visited set would wrongly report a cycle. Then `4→0` lands on `0`, still on the rope, and the rope from `0` to `4` plus that edge is the cycle.

```text
  ┌──────────────┐
  ↓              │       event       gray: the current path   black
  0 ──→ 1 ──→ 3  │       enter 0     0                        -
  │           ↑  │       enter 1     0 1                      -
  └──→ 2 ─────┘  │       enter 3     0 1 3                    -
       │         │       finish 3    0 1                      3
       └──→ 4 ───┘       finish 1    0                        3 1
                         enter 2     0 2                      3 1
                         edge 2→3    3 is black: skip it
                         enter 4     0 2 4                    3 1
                         edge 4→0    0 is gray: cycle 0 → 2 → 4 → 0 ✓
```

```pseudo
WHITE ← 0                                  // not visited yet
GRAY ← 1                                   // on the current DFS path
BLACK ← 2                                  // finished: no cycle reachable

FUNCTION HasCycle(n, edges)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)
    color ← array of n copies of WHITE
    FOR node FROM 0 TO n - 1
        IF color[node] = WHITE AND DFS(graph, node, color)
            RETURN true
    RETURN false

FUNCTION DFS(graph, node, color)
    color[node] ← GRAY                     // node joins the current path
    FOR EACH neighbor IN graph[node]
        IF color[neighbor] = GRAY
            RETURN true                    // back edge to a node on the path
        IF color[neighbor] = WHITE AND DFS(graph, neighbor, color)
            RETURN true
    color[node] ← BLACK                    // every path out of node is safe
    RETURN false
```

Every node and every edge is handled once, so the search costs `O(V + E)` time and `O(V)` space beyond the graph, for the colors and the recursion. Reach for three colors whenever dependencies, prerequisites or state transitions must be checked for a loop, or when the nodes that can never reach a cycle are wanted: in Find Eventual Safe States those are exactly the nodes that end black. Kahn's algorithm (#40) answers the same question without recursion, since a cycle exists exactly when fewer than `n` nodes get peeled; that matters in Python, where a chain of about a thousand nodes overflows the default recursion limit. The classic mistake is the plain visited set, which calls the diamond a cycle. Never painting finished nodes black is the same mistake in disguise: they stay gray, and any later visit looks like a cycle.

*Practice:* LC 207 Course Schedule · LC 802 Find Eventual Safe States · LC 1059 All Paths from Source Lead to Destination
