---
rank: 33
slug: dijkstra
---

A signal leaves node `k` of a network with nodes `1` to `n`, and each directed edge `[u, v, w]` takes `w ≥ 0` units of time to cross. Return the time until every node has the signal, or `-1` if some node never gets it. Each node hears the signal at its shortest distance from `k`, so the answer is the largest of those distances. With `k = 1` and the edges `1→2 (4)`, `1→3 (1)`, `3→2 (2)`, `2→4 (1)` and `3→4 (5)`, the distances to nodes `1` to `4` are `0, 3, 1, 4`, and the answer is `4`.

Relaxing every edge again and again until nothing improves works, and it is Bellman-Ford (#82), at `O(V · E)`. Dijkstra relaxes each edge once, by settling nodes in order of distance, the way BFS (#30) settles them in order of hop count, with a min-heap in place of the queue. The heap holds candidate distances `(d, node)`, and the first entry it pops for a node is final. Any other route to that node must leave the settled region somewhere, and by the time it does it already costs at least `d`, since every node just outside the region waits in the heap at a distance no smaller than `d`; non-negative weights can only add to that. Settling a node relaxes its edges: when `d + w` beats the best known distance to a neighbor, the neighbor's distance drops and a new entry goes on the heap. A plain binary heap cannot lower an entry in place, so the old entry stays behind, and when it surfaces later its `d` is larger than `dist[node]` and it is skipped. That is lazy deletion, and its whole cost is a heap that can hold one entry per edge.

Picture a frontier that only ever moves outward, always at its nearest point. Node `2` first hears of the direct route at distance 4, then the detour through `3` lowers it to 3 and the entry `(4, 2)` goes stale. A negative edge is exactly what breaks this picture, because a step outside the frontier can now lead back to a shorter route. With edges `1→2 (2)`, `1→3 (3)`, `3→2 (-2)` and `2→4 (1)`, node `2` is settled at 2 and hands 3 on to node `4` before the route through `3` shows that `2` is really at 1 and `4` at 2. A version that never reopens a settled node answers 3 for node `4`. The lazy version below reopens `2` and recovers, but nodes can then be popped many times, the time bound is gone, and a negative cycle keeps improving forever: negative weights need Bellman-Ford.

```text
   1 ──(4)──→ 2 ──(1)──→ 4
   │          ↑          ↑
  (1)        (2)        (5)
   ↓          │          │
   3 ─────────┴──────────┘

pop      what happens                     dist of 1..4    heap after, sorted
(0, 1)   settle 1: 2 ← 4, 3 ← 1           [0, 4, 1, ∞]    (1,3) (4,2)
(1, 3)   settle 3: 2 ← 3, 4 ← 6           [0, 3, 1, 6]    (3,2) (4,2) (6,4)
(3, 2)   settle 2: 4 ← 4                  [0, 3, 1, 4]    (4,2) (4,4) (6,4)
(4, 2)   stale: 4 > dist[2] = 3, skip     [0, 3, 1, 4]    (4,4) (6,4)
(4, 4)   settle 4: no edges out           [0, 3, 1, 4]    (6,4)
(6, 4)   stale: 6 > dist[4] = 4, skip     [0, 3, 1, 4]    empty
answer: the largest distance, 4
```

```pseudo
FUNCTION Dijkstra(graph, source)
    dist ← array of len(graph) copies of ∞
    dist[source] ← 0
    heap ← empty min-heap
    heap.push((0, source))                 // (distance so far, node)
    WHILE heap is not empty
        (d, node) ← heap.pop()
        IF d > dist[node]
            CONTINUE                       // stale entry: node settled closer
        FOR EACH (neighbor, weight) IN graph[node]
            IF d + weight < dist[neighbor]         // relax: a shorter route
                dist[neighbor] ← d + weight
                heap.push((dist[neighbor], neighbor))
    RETURN dist

FUNCTION NetworkDelayTime(times, n, k)
    graph ← array of n + 1 empty lists     // nodes are 1..n; slot 0 unused
    FOR EACH (u, v, w) IN times
        graph[u].append((v, w))
    dist ← Dijkstra(graph, k)
    slowest ← 0
    FOR node FROM 1 TO n
        IF dist[node] = ∞
            RETURN -1                      // this node never gets the signal
        slowest ← max(slowest, dist[node])
    RETURN slowest
```

Each node is settled once, so each edge pushes at most one entry; at most `E + 1` pushes and pops at `O(log E) = O(log V)` each give `O((V + E) log V)` time and `O(V + E)` space. Reach for Dijkstra when edges carry non-negative costs, times or distances and the question is the cheapest route. The variants change what a route costs: Path With Minimum Effort minimizes the largest single step, Path with Maximum Probability multiplies probabilities and pops the largest first, and Number of Ways to Arrive at Destination carries a count of shortest routes beside each distance. The classic mistake is borrowing BFS's habit of finalizing a node when it is first pushed: here node `2` would keep distance 4 instead of 3, and node `4` would get 6.

*Practice:* LC 743 Network Delay Time · LC 1514 Path with Maximum Probability · LC 1631 Path With Minimum Effort · LC 1976 Number of Ways to Arrive at Destination
