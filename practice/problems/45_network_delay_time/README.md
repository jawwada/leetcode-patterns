# Network Delay Time (LeetCode 743)

**Area:** graphs · **Difficulty:** Medium · **Key operations:** heap pop the closest node, skip stale entries, relax out-edges, push improved arrival times

## Problem

A network has `n` nodes labelled `1..n` and directed edges `times[i] = [u, v, w]`: a signal sent from `u` arrives at `v` after `w` time units. A signal is sent from node `k`. Return the time at which every node has received it, or `-1` if some node never does.

## Example

```
times = [[1,2,4],[1,3,1],[3,2,1],[2,4,2]], n = 4, k = 1 -> 4

   1 --4--> 2 --2--> 4
   |        ^
   1        1
   v        |
   3 -------+
```

The direct edge `1 -> 2` costs 4, but going `1 -> 3 -> 2` costs 2. Node 4 is reached at `2 + 2 = 4`, which is the last arrival.

## Brute force

Bellman-Ford. Set `dist[k] = 0` and everything else to infinity, then repeat `n - 1` times: for every edge `(u, v, w)`, set `dist[v] = min(dist[v], dist[u] + w)`. After `n - 1` rounds every shortest path (which has at most `n - 1` edges) has been found.

O(V·E) time, O(V) space. The wasted work: every round rescans *all* edges, including edges leaving nodes whose distance did not change since the last round, so most relaxations do nothing.

## From brute force to optimal

With non-negative weights, the unsettled node with the smallest tentative distance is already final: no later path can undercut it, because every other path would have to pass through a node that is at least as far. So settle nodes in increasing order of distance and relax each node's out-edges exactly once. That is Dijkstra.

Picking the minimum efficiently is the job of a min-heap of `(arrival time, node)`. When a relaxation improves `dist[v]`, push the new time; the old entry stays in the heap and is simply skipped when it surfaces, because by then `d > dist[v]`. O((V + E) log V).

## Intuition

Picture the signal as a wavefront whose radius is "time". The heap is the list of scheduled arrival events, earliest first. Popping the earliest event advances the wavefront to that node; its arrival time is now final, so schedule new events for each outgoing edge. A node can be scheduled several times (once per improving path), but only its earliest event counts; later events for the same node are stale and are discarded on sight. The answer is the time of the last node to be reached, or `-1` if some node never gets an event.

## Walkthrough

Heap shown as its array (smallest at index 0). `dist` is the best arrival time found so far.

```
start        heap [(0,1)]                dist {1:0}
pop (0,1)    relax 1->2 w=4: dist[2]=4   push (4,2)     heap [(4,2)]
             relax 1->3 w=1: dist[3]=1   push (1,3)     heap [(1,3),(4,2)]
pop (1,3)    relax 3->2 w=1: 1+1=2 < 4   dist[2]=2      push (2,2)   heap [(2,2),(4,2)]
pop (2,2)    relax 2->4 w=2: dist[4]=4   push (4,4)     heap [(4,2),(4,4)]
pop (4,2)    4 > dist[2]=2 -> STALE, skip               heap [(4,4)]
pop (4,4)    no out-edges                               heap []
dist {1:0, 2:2, 3:1, 4:4}, 4 nodes == n -> return max = 4
```

The entry `(4,2)` is the direct edge's promise; it was superseded by the cheaper route through 3 and is thrown away when popped.

## Steps

1. Build the adjacency list `u -> [(v, w)]`.
2. `dist = {k: 0}`, `heap = [(0, k)]`.
3. Pop `(d, u)`. If `d > dist[u]` the entry is stale: skip it.
4. For each edge `u -> v` with weight `w`: if `d + w < dist.get(v, inf)`, set `dist[v] = d + w` and push `(d + w, v)`.
5. When the heap is empty: if `len(dist) == n` return `max(dist.values())`, else `-1`.

## Complexity

O((V + E) log V) time: each edge pushes at most one heap entry and each pop costs log of the heap size. O(V + E) space for the adjacency list, the heap and `dist`.

## Pitfalls

- **`d >= dist[u]` for the stale check.** Every entry is popped with `d == dist[u]` the first time, so `>=` skips every node including the source; nothing is relaxed and the result is `-1`.
- **Recording only the first time a node is seen (`if v not in dist`).** That is BFS, not Dijkstra: a long direct edge then beats a shorter two-hop path, as in `1 -> 3 -> 2` above.
- **Pushing the edge weight instead of the arrival time.** The heap then orders by last hop, nodes settle in the wrong order and the recorded times are wrong.
- **Forgetting the unreachable case.** `max(dist.values())` without checking `len(dist) == n` returns a time even when some node never received the signal.
- **1-indexed nodes.** Nodes are `1..n`; a dict for `dist` sidesteps the off-by-one of a list sized `n`.
