---
rank: 82
slug: dfs_topological_sort
---

Given `n` nodes `0` to `n - 1` and directed edges `[u, v]` meaning `u` must come before `v`, return an order of all the nodes that respects every edge, or an empty list if a cycle makes that impossible. On the graph of Kahn's example (#40), with edges `0→3`, `1→3`, `3→4`, `3→2`, `4→5` and `2→5`, one valid order is `[1, 0, 3, 2, 4, 5]`.

Kahn's algorithm builds the order from the front, by repeatedly taking a node that nothing points to. Depth-first search builds it from the back. In a graph without cycles, a DFS finishes a node only after everything reachable from it has finished, so the order in which nodes finish, the postorder, lists every node after all of its descendants, and reversing it lists every node before them. The proof takes one edge at a time. When the search examines `u → v`, the node `v` is white, and is then entered and finished before `u` is; or black, and finished already; or gray, which makes `v` an ancestor of `u` on the current path and the edge part of a cycle. In every acyclic case `v` finishes before `u`, so in the reversed list `u` comes first. The colors are those of cycle detection (#81), and the same gray test triggers the `[]`.

Picture the answer being written from right to left. The first node to finish is a dead end, `5`, which belongs at the far right; each later finisher goes to the left of everything placed so far, because everything it leads to is already placed. Node `1` finishes last; its only edge leads into the black `3`. The result differs from Kahn's `[0, 1, 3, 4, 2, 5]` and is just as valid, since a graph can have many topological orders.

```text
    0 ──┐            ┌──→ 4 ──┐
        ├──→ 3 ──────┤        ├──→ 5
    1 ──┘            └──→ 2 ──┘

enter 0, 3, 4, 5
finish 5                                finished [5]
finish 4                                finished [5, 4]
enter 2; edge 2→5: 5 is black, skip
finish 2                                finished [5, 4, 2]
finish 3                                finished [5, 4, 2, 3]
finish 0                                finished [5, 4, 2, 3, 0]
enter 1; edge 1→3: 3 is black, skip
finish 1                                finished [5, 4, 2, 3, 0, 1]
reverse                                 order    [1, 0, 3, 2, 4, 5]
```

```pseudo
WHITE ← 0                                  // not visited yet
GRAY ← 1                                   // on the current DFS path
BLACK ← 2                                  // finished: after its descendants

FUNCTION TopologicalSort(n, edges)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)
    color ← array of n copies of WHITE
    finished ← empty list                  // nodes in the order they finish
    FOR node FROM 0 TO n - 1
        IF color[node] = WHITE AND NOT DFS(graph, node, color, finished)
            RETURN empty list              // a cycle: no order exists
    RETURN reverse(finished)

FUNCTION DFS(graph, node, color, finished)
    color[node] ← GRAY                     // node joins the current path
    FOR EACH neighbor IN graph[node]
        IF color[neighbor] = GRAY
            RETURN false                   // back edge: a cycle
        IF color[neighbor] = WHITE
            IF NOT DFS(graph, neighbor, color, finished)
                RETURN false
    color[node] ← BLACK
    finished.append(node)                  // its descendants are all in already
    RETURN true
```

Every node and every edge is handled once, so the sort costs `O(V + E)` time and `O(V)` extra space. Choose between the two sorts by the shape of the problem. Kahn's needs no recursion, which matters in Python on long chains, hands out the order front to back, and peels the graph level by level, which counting semesters needs. The DFS version fits when a DFS is already running, as in Longest Increasing Path in a Matrix, which computes each cell only after the cells it can step to: exactly this postorder. Sort Items by Groups Respecting Dependencies needs either sort twice, once for the groups and once for the items inside each group. The classic mistake is recording a node when the search enters it instead of when it finishes: the entry order here is `[0, 3, 4, 5, 2, 1]`, which puts `3` before its prerequisite `1`.

*Practice:* LC 210 Course Schedule II · LC 269 Alien Dictionary · LC 1203 Sort Items by Groups Respecting Dependencies · LC 329 Longest Increasing Path in a Matrix
