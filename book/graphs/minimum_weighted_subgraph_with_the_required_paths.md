# Minimum Weighted Subgraph With the Required Paths
*LeetCode 2203 · Hard · Pattern: Dijkstra (min-heap shortest paths) · Reading time ~10 min*

## What the problem is really asking

You get a directed graph with non-negative edge weights, two start nodes `src1` and `src2`,
and a destination `dest`. Choose a set of edges, as light as possible in total, such that
inside that set both `src1` and `src2` can reach `dest`. Return the total weight, or `-1`
if one of them cannot reach `dest` at all.

The answer is one number. The trap is that the two required paths may **share** edges, and
a shared edge is paid for once. So this is not "shortest path from `src1` plus shortest path
from `src2`".

```text
  src1=0  src2=1  dest=4

     0 --2--> 2 <--3-- 1
     |        |        |
     9        1        8
     |        v        |
     |        3        |
     |        |2       |
     |        v        |
     +------> 4 <------+

  shortest 0->4: 0,2,3,4 = 5     shortest 1->4: 1,2,3,4 = 6
  5 + 6 = 11, but edges 2->3->4 (weight 3) were counted twice
  true answer: {0->2, 1->2, 2->3, 3->4} = 2+3+1+2 = 8
```

What makes it hard is finding the best way to share. The two paths could merge at any node,
and for every merge point the three pieces must each be shortest.

## Do it by hand first

Trace the two chosen paths backwards from `dest`. They run together for a while, then at
some node they split and go their separate ways to `src1` and `src2`. Call the split node
`x`. The optimal subgraph is a **Y**:

```text
     src1          src2
        \          /
     arm1\        /arm2
          \      /
            (x)          total = d(src1,x) + d(src2,x)
             |                 + d(x,dest)
             |stem
           (dest)
```

By hand you would try each candidate `x` and add three numbers. In the example:

```text
  x = 2:  0->2 = 2,  1->2 = 3,  2->4 = 3   total 8
  x = 3:  0->3 = 3,  1->3 = 4,  3->4 = 2   total 9
  x = 4:  0->4 = 5,  1->4 = 6,  4->4 = 0   total 11
  x = 0:  1 cannot reach 0                 total inf
```

`x` may be `dest` itself (no sharing), or one of the sources (one arm has length 0). Your
hand kept **three tables of distances**: from `src1` to everything, from `src2` to
everything, and from everything to `dest`. Each candidate `x` just reads three entries.

Why must each piece be a shortest path? If any piece could be replaced by a lighter path
between the same endpoints, the Y would get lighter (overlaps only make it lighter still).
And why is a Y enough? Any valid subgraph contains a `src1 -> dest` path and a `src2 -> dest`
path; walk both backwards from `dest` and they share at least `dest`, so the first point
where they part is some `x`, and the subgraph weighs at least the Y through that `x`.

## The first honest attempt

Loop over every `x`, and for each one compute three shortest paths from scratch, say with
Bellman-Ford (`O(VE)` each).

```text
  x=0: SP(src1,*)  SP(src2,*)  SP(0,*)  -> read [0],[0],[dest]
  x=1: SP(src1,*)  SP(src2,*)  SP(1,*)  -> read [1],[1],[dest]
  x=2: SP(src1,*)  SP(src2,*)  SP(2,*)  -> read [2],[2],[dest]
  ...
       ^^^^^^^^^^  ^^^^^^^^^^
       identical every time      a fresh search per x, each
                                 one only to read [dest]
```

That is `O(V^2 E)`. The repeated work is drawn above. The arms do not depend on `x` at all:
`SP(src1, *)` is the same table on every iteration. And each stem search explores a whole
graph just to read off a single entry, the distance to `dest`.

## The turning point

**Claim: all three tables can be filled with one Dijkstra each; the stem table comes from
running Dijkstra from `dest` on the graph with every edge reversed.**

The arms are easy: hoist them out of the loop. One Dijkstra from `src1` and one from `src2`
give `d1[x]` and `d2[x]` for every `x` at once.

The stem is the interesting part. We want `x -> dest` for **every** `x`: many sources, one
target. Dijkstra answers one source, many targets. Flip every arrow. A path
`x -> a -> b -> dest` in the original graph is exactly the path `dest -> b -> a -> x` in the
reversed graph, with the same edges and the same total. So "distance from every `x` to
`dest`" equals "distance from `dest` to every `x` in the reversed graph", and that is one
Dijkstra.

```text
  forward lists              reversed lists
  0: (2,2) (4,9)             0: -
  1: (2,3) (4,8)             1: -
  2: (3,1)                   2: (0,2) (1,3)
  3: (4,2)                   3: (2,1)
  4: -                       4: (0,9) (1,8) (3,2)

  (v,w) = edge to v of weight w; the reversed list of v
  holds every u that had an edge u->v
```

Building both lists is one pass over the edges: `fwd[u]` gets `(v, w)` and `rev[v]` gets
`(u, w)`. Then

`answer = min over x of d1[x] + d2[x] + dd[x]`

with infinity meaning "unreachable", and `-1` if the minimum is still infinite.

Why not just compute all-pairs distances and read whatever we like? Floyd-Warshall is
`O(V^3)` and `V` reaches 10^5 here, so that is out by many orders of magnitude. The point of
the reversal is that we never need all pairs: only three rows of the distance matrix (from
`src1`, from `src2`) and one **column** (into `dest`). Rows are what Dijkstra produces; a
column of the original graph is a row of the reversed graph.

A word on infinities. If `src2` cannot reach some `x`, then `d2[x]` is infinite and so is
the sum; that `x` simply never wins. Using `float("inf")` makes this automatic, since
`inf + 5` is still `inf`. The only place to be careful is the end: if every sum is infinite,
one of the sources cannot reach `dest` at all, and the answer is `-1`, not `inf`. Also note
the weights can be large (up to 10^5 each over 10^5 edges), which is harmless in Python but
needs 64-bit integers in other languages.

The Dijkstra itself is the lazy-deletion version from Network Delay Time: push
`(dist, node)` on every improvement, and when popping skip any entry whose distance is
larger than the recorded one (it is stale).

## Watch it work

The three runs on the example, then the combine step. Heaps shown sorted as `dist:node`.

```text
Frame 1  d1 = Dijkstra(fwd, src=0)
  pop 0:0 -> dist[2]=2, dist[4]=9   heap [2:2 9:4]
  pop 2:2 -> dist[3]=3              heap [3:3 9:4]
  pop 3:3 -> dist[4]=5 (was 9)      heap [5:4 9:4]
  pop 5:4, then 9:4 is stale, skipped
  d1 = [0, inf, 2, 3, 5]
```
The direct edge `0->4` was beaten by the detour through 2 and 3; its heap entry went stale.

```text
Frame 2  d2 = Dijkstra(fwd, src=1)
  pop 0:1 -> dist[2]=3, dist[4]=8   heap [3:2 8:4]
  pop 3:2 -> dist[3]=4              heap [4:3 8:4]
  pop 4:3 -> dist[4]=6 (was 8)      heap [6:4 8:4]
  pop 6:4, then 8:4 stale
  d2 = [inf, 0, 3, 4, 6]
```
Same story from the other source; node 0 is unreachable from 1, so `d2[0] = inf`.

```text
Frame 3  dd = Dijkstra(rev, src=4), first two pops
  pop 0:4 -> dist[0]=9, [1]=8, [3]=2
             heap [2:3 8:1 9:0]
  pop 2:3 -> dist[2]=3
             heap [3:2 8:1 9:0]
```
Walking reversed edges out of `dest` discovers who can reach `dest`, and how cheaply.

```text
Frame 4  dd, remaining pops
  pop 3:2 -> dist[0]=5 (was 9), dist[1]=6 (was 8)
             heap [5:0 6:1 8:1 9:0]
  pop 5:0, pop 6:1, then 8:1 and 9:0 are stale
  dd = [5, 6, 3, 2, 0]
```
`dd[0] = 5` is the original path `0,2,3,4`, found backwards.

```text
Frame 5  combine
   x  | d1   d2   dd  | sum
  ----+---------------+-----
   0  |  0  inf    5  | inf
   1  | inf   0    6  | inf
   2  |  2    3    3  |  8   <- min
   3  |  3    4    2  |  9
   4  |  5    6    0  | 11
  answer = 8, the Y meets at x = 2
```
The best Y splits as early as possible here, because the shared stem `2->3->4` is paid once.

Across the frames, each Dijkstra popped nodes in non-decreasing distance and never changed a
popped node's distance; the combine step only read the three finished arrays.

## Why it is correct

Two facts, each argued above, plus Dijkstra's own correctness.

1. **Some Y is optimal.** Any feasible subgraph contains a `src1 -> dest` path `P1` and a
   `src2 -> dest` path `P2`. Let `x` be the first node of `P1` that also lies on `P2`
   (it exists: `dest` is on both). Take `P1` up to `x`, `P2` up to `x`, and `P2` from `x`
   on. These three pieces share no edge (every edge of the first piece starts at a node
   not on `P2`), so the subgraph weighs at least `d1[x] + d2[x] + dd[x]`. Conversely, gluing three shortest paths at any `x` is a feasible
   subgraph weighing at most that sum. So the minimum over `x` is exact.
2. **The reversed graph gives the stem.** Reversal is a weight-preserving bijection
   between `x -> dest` paths and `dest -> x` paths in the reversed graph, so shortest
   lengths match.

Dijkstra is correct on each run because all weights are non-negative: once a node is popped
at its recorded distance, any other route to it must pass through an unpopped node whose
distance is already at least as large.

## Cost

- **Time `O((V + E) log V)`**: three Dijkstra runs, each pushing at most once per edge
  relaxation, plus an `O(V)` combine.
- **Space `O(V + E)`**: forward and reversed adjacency lists, three distance arrays, and
  the heap.

The brute force was `O(V^2 E)`; hoisting the arms alone gives `O(V E log V)`; reversing the
graph removes the last factor of `V`.

## Variations you will meet

- **Three or more sources.** The meeting structure is no longer a single Y; it becomes a
  Steiner-tree problem, which is NP-hard in general and solved with bitmask DP over
  subsets of terminals for small counts.
- **Undirected graph.** No reversal needed, since `dist(x, dest) = dist(dest, x)`; still
  three Dijkstras.
- **"Every node's distance to a target"** in general (e.g. reachability to an exit from all
  rooms, or Network Delay Time asked in reverse). Reverse the edges and run once.
- **Paths must avoid sharing.** Then the problem becomes min-cost flow; the Y argument no
  longer applies.

## What to carry forward

When many sources need the distance to one target, reverse the edges and run one search from
the target; and when two routes may share, enumerate the meeting point and glue precomputed
distances. The next problem leaves shortest paths behind: instead of the cheapest route
between two points, it asks for the cheapest set of edges that connects **every** point.
