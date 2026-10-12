---
rank: 30
slug: bfs_shortest_path
---

Given an unweighted graph, find a shortest path from a source node to a target node, where the length of a path is its number of edges. On six nodes with the undirected edges `0-1`, `1-2`, `2-3`, `3-4`, `0-5` and `5-4`, the shortest path from `0` to `4` is `[0, 5, 4]`, two edges, while the long way round, `0-1-2-3-4`, takes four.

The brute force lets a depth-first search enumerate every simple path and keeps the shortest, and the number of simple paths can grow exponentially with the graph. Breadth-first search never compares routes, because it explores in order of distance. The queue is first in, first out, so every node at distance `d` leaves it before any node at distance `d + 1`, and a node is first discovered by a neighbor from the lowest possible layer: the distance it receives at that moment is final. Two arrays hold the whole answer. `dist[v]` doubles as the visited mark, with `-1` for not reached yet, and `parent[v]` records which node discovered `v`. Following parents back from the target walks a shortest path in reverse.

Picture a stone dropped on the source. The ripples are the layers, `{0}`, then `{1, 5}`, then `{2, 4}`, then `{3}`, and each node belongs to the first ripple that touches it. Node `4` is touched at distance 2 by the ripple through `5`, while the wave along the top is still two steps away, and its parent pointer remembers the route it came by.

```text
  0 ── 1 ── 2 ── 3         layer 0: 0
  │              │         layer 1: 1, 5
  5 ──────────── 4         layer 2: 2, 4
                           layer 3: 3
pop  dist  newly reached: node (dist, parent)    queue after
 0    0    1 (1, 0)   5 (1, 0)                   [1, 5]
 1    1    2 (2, 1)                              [5, 2]
 5    1    4 (2, 5)                              [2, 4]
 2    2    3 (3, 2)                              [4, 3]
 4    2    none: 3 and 5 are already marked      [3]
 3    3    none                                  []
dist   = [0, 1, 2, 3, 2, 1]
parent = [-1, 0, 1, 2, 5, 0]
path: 4 → 5 → 0 by parents, reversed: [0, 5, 4]
```

```pseudo
FUNCTION ShortestPath(n, edges, source, target)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)                 // undirected: both directions
        graph[v].append(u)
    dist ← array of n copies of -1         // -1 means not reached yet
    parent ← array of n copies of -1       // the node that first reached it
    dist[source] ← 0
    queue ← empty queue
    queue.enqueue(source)
    WHILE queue is not empty
        node ← queue.dequeue()
        FOR EACH neighbor IN graph[node]
            IF dist[neighbor] = -1         // first visit is a shortest one
                dist[neighbor] ← dist[node] + 1     // mark when enqueued
                parent[neighbor] ← node
                queue.enqueue(neighbor)
    IF dist[target] = -1
        RETURN empty list                  // target is in another component
    RETURN BuildPath(parent, target)

FUNCTION BuildPath(parent, target)
    path ← empty list
    node ← target
    WHILE node ≠ -1                        // only the source has no parent
        path.append(node)
        node ← parent[node]
    RETURN reverse(path)
```

Every node enters the queue at most once and every edge is examined once from each end, so the search costs `O(V + E)` time and `O(V)` space beyond the graph. Reach for it whenever a problem asks for the fewest steps, moves, hops or edits and every step costs the same; weighted edges need Dijkstra (#33). A grid is the same graph in disguise: in LC 1091 the nodes are the open cells, the neighbors are the eight cells around each one, and the loop runs unchanged on `(row, col)` pairs, though that problem counts the cells on the path, one more than its edges. When only one target matters, the loop may stop the moment the target is marked. The classic mistake is marking a node when it leaves the queue instead of when it enters. Until it leaves, every frontier node that touches it enqueues it again and rewrites its `dist`, so a longer route can overwrite the right answer: searching from `0` over the edges `0-1`, `0-2`, `1-3`, `2-4`, `3-4`, node `4` ends at distance 3 instead of 2.

*Practice:* LC 1091 Shortest Path in Binary Matrix · LC 1971 Find if Path Exists in Graph · LC 433 Minimum Genetic Mutation · LC 286 Walls and Gates
