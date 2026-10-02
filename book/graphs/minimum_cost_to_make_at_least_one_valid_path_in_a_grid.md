# Minimum Cost to Make at Least One Valid Path in a Grid
*LeetCode 1368 · Hard · Pattern: 0-1 BFS (deque shortest path) · Reading time ~11 min*

## What the problem is really asking

Every cell of an `m x n` grid holds an arrow: `1` right, `2` left, `3` down, `4` up. You
stand on the top-left cell and blindly follow arrows. Walking along an arrow is free. You
may repaint any cell's arrow for a cost of 1. What is the least you must pay so that blind
arrow-following carries you from `(0,0)` to `(m-1,n-1)`?

Here is the grid we will use all the way through, with `>` `<` `v` `^` for the four arrows.

```text
  values            arrows           free walk from (0,0)
      c0 c1 c2         c0 c1 c2
  r0 [ 1  4  4 ]   r0   >  ^  ^      (0,0) -> (0,1) -> off
  r1 [ 1  3  1 ]   r1   >  v  >      the top edge: stuck
  r2 [ 4  2  1 ]   r2   ^  <  >

  answer: 2   e.g. repaint (0,1) to v, then (1,1) v takes
              you to (2,1); repaint (2,1) to > -> (2,2)
```

The answer is a single number: a shortest-path length. Rephrase the rules as a graph and it
becomes plain. Each cell is a node with up to four out-edges. The edge in the direction of
its arrow weighs 0; the three other edges weigh 1 (moving that way means you repainted the
arrow). "Fewest repaints" is "cheapest path from corner to corner".

What makes it hard is that the edges are weighted, so plain BFS, which counts edges, gives
wrong answers; and the grid can have 10^4 cells, so anything quadratic in cells hurts.

## Do it by hand first

On paper you would first ride the free arrows from the start and shade every cell you reach
for nothing. Then you ask: "if I pay once, from any shaded cell, where can I get to?" and
from each of those you ride free arrows again. Then pay a second time, and so on.

```text
  cost 0 region     cost <= 1 region     cost <= 2 region
    0  0  .           0  0  1              0  0  1
    .  .  .           1  1  .              1  1  2
    .  .  .           1  1  .              1  1  2

  pay 0: (0,0),(0,1)
  pay 1: step off them once, then ride free arrows:
         (1,1) v -> (2,1) < -> (2,0) all cost 1
  pay 2: everything left, including the target
```

Your hand kept two things: **the cheapest known cost of every cell** and **a to-do list of
cells, grouped by how much you paid to reach them**, always working on the cheapest group
first. A cost grid and a cost-ordered to-do list: that is Dijkstra. The question is how
cheap the to-do list can be made.

## The first honest attempt

Write `cost[0][0] = 0` and infinity elsewhere. Then sweep the whole grid again and again;
for each cell try its four moves and lower a neighbour's cost if `cost + step` beats it.
Stop when a full sweep changes nothing. This is Bellman-Ford.

```text
  sweep 1: relax all 9 cells     (some costs drop)
  sweep 2: relax all 9 cells     (a few drop again)
  sweep 3: relax all 9 cells     (nothing changes, stop)

  (0,0) has cost 0 from the very beginning, yet every sweep
  re-relaxes its four moves. So does (0,1). Most of the work
  in later sweeps is re-checking cells that are already final.
```

A sweep is `O(mn)` and up to `mn` sweeps can be needed, so `O((mn)^2)`. The waste is the
**order**: cells are relaxed in row-major order rather than in order of cost, so a cheap
cell discovered late forces another full sweep to propagate.

The textbook fix is Dijkstra from Network Delay Time: a min-heap of `(cost, cell)`, always
settle the cheapest. That gives `O(mn log mn)` and is already accepted. But look at what the
heap is being asked to do.

## The turning point

**Claim: when every edge weighs 0 or 1, the to-do list never holds more than two distinct
costs, `d` and `d + 1`, so a double-ended queue can keep it sorted without a heap.**

Why only two values? Dijkstra pops the smallest cost `d`. Relaxing a 0-edge produces a cell
at cost `d`; relaxing a 1-edge produces cost `d + 1`. Everything already in the list was
produced the same way from earlier pops whose cost was at most `d`, so it holds `d` or
`d + 1` too. Two values, and we know which is which at the moment we create the entry.

That makes the sorting trivial:

- a **free** move (weight 0) yields a cell exactly as cheap as the one being expanded: put
  it at the **front**, it belongs with the current group;
- a **paid** move (weight 1) yields a cell one more expensive: put it at the **back**,
  behind every `d` entry and alongside the other `d + 1` entries.

Popping from the front always returns a minimum-cost entry, which is precisely what the
heap was for, but each push and pop is `O(1)`.

```text
        front                               back
  dq: [ d  d  d  d | d+1  d+1  d+1 ]
        ^ 0-moves appendleft    ^ 1-moves append
        pop here: always cheapest
```

Two details from the solution file matter. First, there is no `visited` set. A cell can be
discovered at cost 2 and later improved to cost 1 (a free arrow leads into it from a cell
that turned out cheaper). The relaxation test `cost[r][c] + step < cost[nr][nc]` handles
that, and the cell is simply pushed again. Second, the old entry stays in the deque as a
stale duplicate; when it is popped, its relaxations all fail, so it costs only a few
comparisons. Marking cells visited when first pushed would freeze that early cost 2 and
give a wrong answer.

This is BFS's layer picture with a twist. Ordinary BFS has one layer per distance and a
FIFO queue. 0-1 BFS has one layer per **cost**, and a free move does not start a new layer:
it extends the current one, so it must jump the queue.

## Watch it work

`cost` grid on the left (`.` is infinity), arrows on the right, deque below as
`cell:cost` from front to back.

```text
Frame 1  start
  cost      arrows
  0 . .     > ^ ^
  . . .     > v >
  . . .     ^ < >
  dq: [ (0,0):0 ]
```
Only the start is known; it costs nothing to stand there.

```text
Frame 2  pop (0,0):0, arrow >
  0 0 .     right (0,1): free, 0  -> FRONT
  1 . .     down  (1,0): paid, 1  -> BACK
  . . .
  dq: [ (0,1):0 | (1,0):1 ]
```
The free neighbour joins the cost-0 group ahead of the paid one.

```text
Frame 3  pop (0,1):0, arrow ^ (points off-grid)
  0 0 1     right (0,2): paid, 1 -> BACK
  1 1 .     down  (1,1): paid, 1 -> BACK
  . . .
  dq: [ (1,0):1 (0,2):1 (1,1):1 ]
```
Cost-0 group exhausted; the deque now holds exactly the cost-1 group.

```text
Frame 4  pop (1,0):1 then (0,2):1
  0 0 1     (1,0) arrow >, but (1,1) already 1;
  1 1 2     down (2,0) paid: 2 -> BACK
  2 . .     (0,2): down (1,2) paid: 2 -> BACK
  dq: [ (1,1):1 | (2,0):2 (1,2):2 ]
```
Two cells get a provisional cost of 2; one of them is wrong.

```text
Frame 5  pop (1,1):1, arrow v
  0 0 1     down (2,1): free, 1 -> FRONT
  1 1 2     (it jumps ahead of both 2s)
  2 1 .
  dq: [ (2,1):1 | (2,0):2 (1,2):2 ]
```
A cost-1 cell reached a new cell for free, so that cell is still cost 1 and goes first.

```text
Frame 6  pop (2,1):1, arrow <
  0 0 1     left (2,0): free, 1 < 2 -> improve,
  1 1 2       FRONT (old 2-entry now stale)
  1 1 2     right (2,2): paid, 2 -> BACK
  dq: [ (2,0):1 | (2,0)stale (1,2):2 (2,2):2 ]
```
(2,0) drops from 2 to 1, which is why no visited set is used.

```text
Frame 7  drain
  0 0 1     pop (2,0):1, nothing improves
  1 1 2     pop (2,0) stale copy, nothing improves
  1 1 2     pop (1,2):2, (2,2):2, nothing improves
  dq: [ ]   return cost[2][2] = 2
```
The target was settled at 2, and the grid matches the hand-drawn regions.

Across every frame the deque read as a run of cost `d` followed by a run of cost `d + 1`,
never anything else. Each pop therefore took a cheapest entry, exactly as a heap would.

## Why it is correct

It is Dijkstra's argument with a different container. Dijkstra is correct as long as every
pop returns an entry whose cost is minimal among all entries waiting, and all weights are
non-negative. So the only thing to prove is that the deque front is always minimal.

Invariant: the deque, read front to back, is non-decreasing in cost, and the last cost is
at most the first plus 1. It holds at the start (one entry). When we pop the front with
cost `d`, the rest are `d` or `d + 1`. An `appendleft` adds cost `d` at the front: still
sorted, still within `d..d+1`. An `append` adds `d + 1` at the back: still sorted, still
within the window. Stale entries break nothing: they are judged by the cost recorded with
them when pushed, which also sat in the right place.

Given that the front is always a minimum, the first time a cell is popped at its final
cost, no cheaper route can appear later, since every later pop is at least as expensive and
edges never make things cheaper. When the deque empties every cell holds its true minimum,
including the target.

## Cost

- **Time `O(mn)`**: each cell is pushed at most twice (its first cost is at most one
  above the front, so it can improve at most once), each push or pop is `O(1)`, and each
  pop checks 4 neighbours.
- **Space `O(mn)`**: the cost grid and the deque.

For comparison: Bellman-Ford `O((mn)^2)`, Dijkstra with a heap `O(mn log mn)`.

## Variations you will meet

- **Minimum Obstacle Removal to Reach Corner (LeetCode 2290).** Entering an empty cell
  costs 0, entering an obstacle costs 1. Identical 0-1 BFS; only the weight rule changes.
- **Weights in `{0, 1, ..., k}` with small `k`.** Generalise the deque to `k + 1` buckets
  (Dial's algorithm), cycling through them; still linear.
- **Arbitrary non-negative weights.** Back to the heap: Network Delay Time.
- **Fewest edges with a fuel or key budget.** The state gains a dimension, as in Shortest
  Path with Obstacles Elimination; the 0-1 trick still applies if the weights are 0 or 1.

## What to carry forward

Two possible weights, 0 and 1: free moves go to the front of a deque, paid moves to the
back, and you have Dijkstra in linear time. The next problem, Swim in Rising Water, keeps
the heap-driven search on a grid but changes what a path costs: not a sum of edges but the
highest cell you pass through.
