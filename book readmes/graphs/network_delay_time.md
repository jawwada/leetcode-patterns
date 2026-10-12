# Network Delay Time
*LeetCode 743 · Medium · Pattern: Dijkstra (min-heap shortest paths) · Reading time ~10 min*

## The problem

There are n nodes labelled 1..n and directed edges times[i] = (u, v, w) meaning a signal takes w time units to travel
from u to v. A signal is sent from node k. Return the time at which every node has received it, or -1 if some node
never does.

```text
Example: times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2 -> 2.
```

## What the problem is really asking

There are `n` nodes, `1` to `n`, and directed edges `(u, v, w)`: a signal leaving `u`
reaches `v` after `w` time units. A signal starts at node `k` at time 0 and spreads along
every edge at once. When has every node heard it? If some node never hears it, answer `-1`.

Each node hears the signal at the length of its **shortest** path from `k`, since the
fastest copy arrives first. The whole network has heard it when the *slowest* of those
arrivals happens. So: compute shortest-path distances from `k`, return the maximum.

What makes it new: until now every edge in this chapter cost the same, so BFS layers were
distances. Here edges have different weights, and a path with more edges can be faster.

```text
   graph                        adjacency lists (storage)
          4                     1 : [(2, 4), (3, 1)]
     (1) ----> (2)              2 : [(4, 1)]
      |        ^  \             3 : [(2, 2), (4, 5)]
    1 |      2 |   \ 1          4 : []
      v        |    v
     (3) ------'   (4)          k = 1
      \             ^
       `-----5------'           answer: 4

   arrival: 1 at 0, 3 at 1, 2 at 3 (1->3->2),
            4 at 4 (1->3->2->4)
```

The direct edge `1 -> 2` costs 4, but going around through 3 costs 1 + 2 = 3. BFS would
reach 2 in one hop and call it done, which is wrong.

## Do it by hand first

Imagine you are the clock. At time 0 node 1 hears it. You write down "arrivals scheduled":
2 at time 4, 3 at time 1. Which happens first? 3, at time 1. Now 3 is certain: nothing can
beat time 1, every other signal is still in flight and has already used at least as much
time. From 3 you schedule more: 2 at time 3, 4 at time 6. The earliest pending event is now
2 at time 3, so 2 is certain. From 2: 4 at time 4. The pending list now holds "2 at 4"
(already heard, ignore), "4 at 4", "4 at 6". Take 4 at time 4. Done; the last arrival was 4.

Your hand kept a **list of pending arrival events** and always took the earliest one. That
list, with "give me the earliest" as its main operation, is a priority queue.

## The first honest attempt

Bellman-Ford: set `dist[k] = 0`, everything else infinity. Then, `n - 1` times, sweep every
edge and *relax* it: if `dist[u] + w < dist[v]`, lower `dist[v]`. After `n - 1` sweeps every
shortest path (which has at most `n - 1` edges) has been propagated.

Cost `O(n * E)`. The repeated work: each sweep re-relaxes every edge, including edges out of
nodes whose distance has not changed since the last sweep and can't produce anything new.

```text
   edges in input order: 1->2, 1->3, 3->2, 2->4, 3->4
   sweep   dist[1..4]     relaxations that changed something
     1     0  3  1  4     1->2 (4), 1->3, 3->2 (3), 2->4
     2     0  3  1  4     none -- all 5 edges re-checked
     3     0  3  1  4     none -- all 5 edges re-checked
           ^ after sweep 1 nothing can improve, yet the loop
             pays for two more full sweeps
```

(With a less lucky edge order, the values settle more slowly and the early sweeps do
useful work; but every sweep still re-relaxes edges out of nodes that have not changed.)

## The turning point

**Claim: with non-negative weights, the unsettled node with the smallest tentative distance
already has its final distance.**

Why: let `x` be that node, with tentative distance `d`. Any other route to `x` must leave
the settled region somewhere, through an unsettled node `y`. Reaching `y` already costs at
least `dist[y] >= d`, by the choice of `x`. The remaining edges after `y` cost `>= 0`. So
that route costs at least `d`. Nothing beats `d`.

```text
   settled region                     tentative
   +------------------+
   |  1 (0)   3 (1)   | ---> 2 : 3    <- smallest: FINAL
   +------------------+ ---> 4 : 6
   any detour to 2 must exit via 4 (>= 6) then add >= 0
```

This is the BFS layer property generalised: BFS settles nodes in order of hop count;
**Dijkstra's algorithm** settles them in order of distance. Each node is settled once, and
only then are its out-edges relaxed, once. No sweeps.

The remaining question is how to find "smallest tentative distance" fast. Scanning all nodes
each time is `O(n)` per step, `O(n^2)` total. The tool for this is a **binary min-heap**: a
complete binary tree where every parent is `<=` its children, so the minimum sits at the
root. It is stored as an array: the children of index `i` are `2i + 1` and `2i + 2`.

```text
   heap as a triangle                heap as its array
          (3,2)                       idx:   0      1      2
         /     \                           (3,2)  (4,2)  (6,4)
     (4,2)     (6,4)                 parent(i) = (i - 1) // 2
   entries are (distance, node); tuples compare distance first
```

- **push**: append at the end, then swap upward while smaller than the parent. `O(log n)`.
- **pop**: take index 0, move the last entry to the root, swap downward with the smaller
  child until in order. `O(log n)`.

Python's `heapq` does both on a plain list.

One wrinkle: when a node's tentative distance improves, its old entry is still in the heap.
Real heaps don't support cheap "decrease this entry". The fix is **lazy deletion**: just
push a new entry `(new_dist, v)` and leave the old one. When an entry is popped, check
whether its node is already settled; if so it is **stale**, skip it. The first pop of any
node always carries its smallest pushed distance, so the first pop is the true one.

The whole loop: pop `(d, u)`; if `u` is settled, skip; else settle `dist[u] = d` and push
`(d + w, v)` for each unsettled neighbour. At the end, if fewer than `n` nodes are settled
return `-1`, else the largest `dist`.

## Watch it work

Same graph, `k = 1`. Each frame shows the heap array after the step and the settled map.

```text
Frame 1   start
   heap:  [(0,1)]               (0,1)
   settled: {}
```
Only the source is scheduled.

```text
Frame 2   pop (0,1) -> settle 1 at 0; push (4,2), (1,3)
   heap:  [(1,3), (4,2)]           (1,3)
   settled: {1:0}                 /
                               (4,2)
```
`(1,3)` bubbled up past `(4,2)`, so the root is the earliest event.

```text
Frame 3   pop (1,3) -> settle 3 at 1; push (3,2), (6,4)
   heap:  [(3,2), (4,2), (6,4)]     (3,2)
   settled: {1:0, 3:1}             /     \
                               (4,2)    (6,4)
```
Node 2 now has two entries: 4 via the direct edge, 3 via 3.

```text
Frame 4   pop (3,2) -> settle 2 at 3; push (4,4)
   heap:  [(4,2), (6,4), (4,4)]     (4,2)
   settled: {1:0, 3:1, 2:3}        /     \
                               (6,4)    (4,4)
```
The cheaper entry for 2 came out first; `(4,2)` is now stale.

```text
Frame 5   pop (4,2) -> 2 settled: STALE, skip
          pop (4,4) -> settle 4 at 4
   heap:  [(6,4)]
   settled: {1:0, 3:1, 2:3, 4:4}
```
Tie at distance 4 broke on node id; the stale entry cost one pop and nothing else.

```text
Frame 6   pop (6,4) -> STALE, skip; heap empty
   settled 4 of 4 nodes -> answer max = 4
```
Every node was settled exactly once.

The settled distances only ever increased from frame to frame (0, 1, 3, 4): nodes are
finalised in order of arrival time, exactly like the clock in "Do it by hand first".

## Why it is correct

Invariant: every settled node holds its true shortest distance, and every settled distance
is `<=` every entry still in the heap. It holds after settling `k` at 0. When the minimum
entry `(d, x)` is popped for an unsettled `x`, the claim from "The turning point" says no
path reaches `x` for less than `d`, and `d` is achieved by the path that produced the entry.
Stale entries are skipped without effect. Since weights are non-negative, entries pushed
afterwards are `>= d`, keeping the order. A node never popped has no path from `k`, so `-1`
is correct. Negative weights break the claim (a later edge could undercut `d`), which is why
Dijkstra requires `w >= 0`.

## Cost

- **Time `O((n + E) log E)`**: each edge pushes at most one entry, and each push or pop is
  logarithmic in the heap size (`log E <= 2 log n`, so this is `O((n + E) log n)`).
- **Space `O(n + E)`**: adjacency lists plus up to `E` heap entries with lazy deletion.
- Bellman-Ford was `O(n * E)`; array-scan Dijkstra is `O(n^2)`, better for dense graphs.

## Variations you will meet

- **Weights only 0 or 1.** A deque does the heap's job: 0-edges push front, 1-edges push
  back. This is 0-1 BFS, the next problem.
- **Minimise the maximum edge on the path** (Swim in Rising Water). Same loop, but the
  priority is `max(d, w)` instead of `d + w`.
- **Cheapest flights within K stops.** The state becomes `(node, stops)`; settling by node
  alone is wrong, so either expand the state or use bounded Bellman-Ford.
- **Negative edges.** Dijkstra fails; use Bellman-Ford.

## What to carry forward

Dijkstra is BFS where the queue is a min-heap ordered by distance: pop the earliest, settle
it, skip stale entries. The next problem keeps that frontier but has only weights 0 and 1,
so a double-ended queue replaces the heap.
