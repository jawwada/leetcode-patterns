---
rank: 117
slug: bellman_ford
---

Given `n` nodes, directed edges with weights that may be negative, and a source, return the shortest distance from the source to every node, `∞` for nodes it cannot reach, or report that a negative cycle is reachable, since circling it forever makes "shortest" meaningless. With edges `2→3 (1)`, `1→2 (-3)`, `0→1 (4)`, `0→2 (2)` and source 0 the answer is `[0, 4, 1, 2]`: the cheapest way to 2 detours through 1 and the negative edge.

Dijkstra (#42) settles nodes greedily, nearest first, which is only safe when no edge is negative, since a negative edge found later can undercut a node already settled. Bellman-Ford gives up on order and relies on counting instead. Relaxing an edge `u → v` asks whether going through `u` beats the best known way into `v`, and takes it if so. One round relaxes every edge once, in any order. After round `k`, every node whose shortest path has at most `k` edges holds its final distance, because each round relaxes the next edge of that path at the latest. Without a negative cycle, a shortest path never needs to repeat a node, so it has at most `n - 1` edges, and `n - 1` rounds settle everything.

Picture correct distances spreading out from the source like a wave, at least one edge further every round, whatever order the edges are scanned in. A round that changes nothing means the wave has stopped, so the loop ends early. If an extra round after `n - 1` still lowers a distance, some path keeps getting cheaper as it grows longer, and only a negative cycle can do that.

```text
scan order:  2→3 (1)   1→2 (-3)   0→1 (4)   0→2 (2)           source 0

          dist:  0    1    2    3     relaxed in this round
start            0    ∞    ∞    ∞
round 1          0    4    2    ∞     0→1 to 4, 0→2 to 2
round 2          0    4    1    3     2→3 to 2 + 1 = 3, then 1→2 to 4 - 3 = 1
round 3          0    4    1    2     2→3 to 1 + 1 = 2
check            no edge still improves: no negative cycle → [0, 4, 1, 2]
```

```pseudo
FUNCTION BellmanFord(n, edges, source)
    dist ← array of n copies of ∞
    dist[source] ← 0
    FOR round FROM 1 TO n - 1             // a shortest path has ≤ n - 1 edges
        changed ← false
        FOR EACH [u, v, w] IN edges
            IF dist[u] + w < dist[v]      // ∞ + w stays ∞: no false relax
                dist[v] ← dist[u] + w     // a cheaper way into v, through u
                changed ← true
        IF NOT changed
            BREAK                         // quiet round: all distances final
    FOR EACH [u, v, w] IN edges
        IF dist[u] + w < dist[v]          // still improving after n - 1 rounds
            RETURN null                   // a negative cycle is reachable
    RETURN dist
```

The work is at most `n - 1` rounds over all `E` edges, `O(V · E)` time and `O(V)` space: slower than Dijkstra, but indifferent to negative weights. Reach for it when weights can be negative, when the question is whether a negative cycle exists (an arbitrage loop in exchange rates), or when a path may use only a limited number of edges. That last case is the flights-within-`k`-stops problem: run exactly `k + 1` rounds, one per flight, and relax each round from a copy of the previous round's distances, so that a round extends paths by at most one edge. Relaxing in place there lets one round chain several edges and break the stop limit; in plain Bellman-Ford the same chaining is harmless and only speeds things up. The classic mistake in plain Bellman-Ford is an integer such as `10^9` standing in for `∞`: then `10^9 - 3 < 10^9`, so unreachable nodes relax their neighbors and a negative cycle the source cannot reach gets reported. Use a true infinity, or skip edges whose start is still unreached.

*Practice:* LC 787 Cheapest Flights Within K Stops · LC 743 Network Delay Time · LC 1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance
