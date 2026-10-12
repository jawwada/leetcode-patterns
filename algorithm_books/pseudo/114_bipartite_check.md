---
rank: 114
slug: bipartite_check
---

Given an undirected graph as an adjacency list, `graph[u]` holding the neighbors of `u`, decide whether its nodes can be split into two sides so that every edge runs between the sides and none runs inside one. A square is bipartite, with `{0, 2}` on one side and `{1, 3}` on the other; a triangle is not, because its three corners cannot alternate between two sides. So the graph made of a square `0-1-2-3` and a triangle `4-5-6`, `[[1, 3], [0, 2], [1, 3], [0, 2], [5, 6], [4, 6], [4, 5]]`, is not bipartite.

The brute force tries all `2^n` ways to assign the sides. But within a connected piece one choice forces all the others: once a node is put on side 0, each neighbor must go on side 1, and each of their neighbors on side 0. BFS spreads that forced choice layer by layer, giving every newly reached node `1 - color[node]`, the opposite of the node that reached it. An edge to a node already on the other side is consistent. An edge to a node on the same side is a contradiction that no recoloring can fix, because every color in the component was forced by the first one. The graph may be disconnected, so the outer loop starts a fresh BFS from every node still uncolored, and each component gets its own free first choice.

Picture the BFS layers as rings around the start, colored alternately. In the square the rings are `0`, then `1` and `3`, then `2`, and every edge joins two neighboring rings. In the triangle, `5` and `6` land on the same ring, and the edge between them stays inside it. That edge betrays an odd cycle, and bipartite means exactly no odd cycle: walking around any cycle switches sides at every step, so it returns home only after an even number of steps, while a same-colored edge plus the two BFS paths back to the start closes a walk of odd length, which always contains an odd cycle.

```text
  0 ── 1          4
  │    │         / \
  3 ── 2        5 ─ 6

start 0: color[0] ← 0
  pop 0   1 ← 1   3 ← 1
  pop 1   0 is 0 ✓   2 ← 0
  pop 3   0 is 0 ✓   2 is 0 ✓
  pop 2   1 is 1 ✓   3 is 1 ✓          the square splits {0, 2} | {1, 3}
start 4: color[4] ← 0
  pop 4   5 ← 1   6 ← 1
  pop 5   4 is 0 ✓   6 is 1, the same as 5 ✗   return false
```

```pseudo
FUNCTION IsBipartite(graph)
    n ← len(graph)
    color ← array of n copies of -1        // -1 uncolored, else side 0 or 1
    FOR start FROM 0 TO n - 1
        IF color[start] ≠ -1
            CONTINUE                       // colored by an earlier search
        color[start] ← 0                   // new component: either side
        queue ← empty queue
        queue.enqueue(start)
        WHILE queue is not empty
            node ← queue.dequeue()
            FOR EACH neighbor IN graph[node]
                IF color[neighbor] = -1
                    color[neighbor] ← 1 - color[node]   // the other side
                    queue.enqueue(neighbor)
                ELSE IF color[neighbor] = color[node]
                    RETURN false           // an edge inside one side
    RETURN true
```

Each node is colored once and each edge is examined from both ends, so the check costs `O(V + E)` time and `O(V)` space. Reach for two-coloring whenever a problem splits things into two groups under "these two must differ" constraints, such as the dislikes of Possible Bipartition, or asks whether a graph has an odd cycle. Flower Planting With No Adjacent is the many-color cousin: every garden has at most three neighbors, so choosing any flower its neighbors do not use always succeeds with four. The classic mistake is searching only from node `0`: that colors the square, never visits the triangle, and returns `true` for this graph.

*Practice:* LC 785 Is Graph Bipartite? · LC 886 Possible Bipartition · LC 1042 Flower Planting With No Adjacent
