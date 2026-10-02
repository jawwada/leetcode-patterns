# Swim in Rising Water
*LeetCode 778 · Hard · Pattern: Minimax path via min-heap (bottleneck Dijkstra) · Reading time ~11 min*

## What the problem is really asking

An `n x n` grid holds distinct elevations `0 .. n*n-1`. Rain raises the water level by one
unit per second. At time `t` you may swim between two 4-adjacent cells when both have
elevation `<= t`, and swimming itself is instantaneous. You start at the top-left; when is
the earliest moment you can be at the bottom-right?

Rephrase it. Any route from corner to corner becomes swimmable the moment the water covers
its **highest** cell. So the answer is: over all routes, the smallest possible maximum
elevation on the route. A route's cost is not a sum; it is a maximum. This is called a
**bottleneck** or **minimax** path.

```text
  our grid                 three candidate routes
      c0 c1 c2
  r0 [ 0  6  4 ]           down the left:  0 1 5 8 2  max 8
  r1 [ 1  7  3 ]           across the top: 0 6 4 3 2  max 6
  r2 [ 5  8  2 ]           through middle: 0 1 7 3 2  max 7

  answer: 6  (wait until t=6, then swim the top route)
```

The answer is one number, an elevation. What makes it hard: the low cells near the start
(`1`, `5`) are bait. A greedy "always step to the lowest neighbour" walks down the left side
and gets trapped behind the `8`. And the number of routes is exponential.

## Do it by hand first

Imagine actually flooding the board. At `t = 0` only the start is wet. Raise the level one
unit at a time, and each time shade every cell that is under water **and** touches the
shaded region.

```text
  t=1          t=5          t=6
  # . .        # . .        # # #
  # . .        # . .        # . #
  . . .        # . .        # . #   <- corner reached
  wet: 2       wet: 3       wet: 7

  (t=2,3,4 add nothing: cells 2,3,4 are wet but not yet
   connected to the shaded region)
```

Your hand kept **the region connected to the start** and **the current water level**. The
level that first connects the region to the far corner is the answer. Notice that cells
`2`, `3`, `4` sat under water for a while doing nothing; they joined only when the `6`
opened a path to them, and then they all joined at once.

## The first honest attempt

Try `t = 0, 1, 2, ...`; for each `t` run a BFS from the start through cells with elevation
`<= t`, and stop at the first `t` whose BFS reaches the corner.

```text
  t=0  BFS visits {0}
  t=1  BFS visits {0,1}
  t=2  BFS visits {0,1}           <- same region again
  t=3  BFS visits {0,1}           <- same region again
  t=4  BFS visits {0,1}           <- same region again
  t=5  BFS visits {0,1,5}
  t=6  BFS visits {0,1,5,6,4,3,2} <- reached
```

Up to `n^2` values of `t`, each BFS `O(n^2)`: `O(n^4)`. Two kinds of waste are visible.
Most levels do not change the region at all, and every BFS re-walks the cells the previous
one already proved reachable.

**First fix: binary search on `t`.** The predicate `reachable(t)` is monotone: water only
rises, so once a route is open it stays open.

```text
  t:          0 1 2 3 4 5 6 7 8
  reachable:  F F F F F F T T T
                          ^ first T = answer

  lo=0 hi=8: probe 4 -> F, lo=5
             probe 6 -> T, hi=6
             probe 5 -> F, lo=6   answer 6
```

Three BFS runs instead of seven: `O(n^2 log n)` overall. This is a perfectly good interview
answer. Yet each probe still starts from scratch, and the search learns nothing about
*where* the bottleneck is. Can one traversal compute it directly?

## The turning point

**Claim: if you grow the region by always absorbing the lowest cell on its border, the
highest cell absorbed so far, at the moment the corner is absorbed, is the answer.**

That is the flooding picture from the hand solution, but without stepping `t` by one: we
jump straight to the next cell that matters. To find "the lowest border cell" quickly, keep
the border in a min-heap.

The key stored with each border cell is not its own elevation but

```python
key = max(t, grid[nr][nc])   # t = key of the cell we came from
```

the water level needed to reach this cell along the route we found. This is Dijkstra from
Network Delay Time with one change: where Dijkstra computes `dist + weight`, we compute
`max(level, elevation)`. Dijkstra only needs the combining rule to be **monotone**
(extending a route never makes it cheaper) and `max` qualifies just as `+` does with
non-negative weights. So the first time the corner is popped, its key is the true minimax
value.

Why not something simpler, such as walking greedily to the lowest neighbour of where you
stand? Because a walker has one position, and the bottleneck may sit on a branch it has
already left. From `0` the walker goes to `1`, then `5`, and then its only new neighbour is
`8`. It reaches the corner at level 8, never reconsidering the `6` back at the top. The heap version has no single position:
its "position" is the whole flooded region, so any border cell, near or far, can be the
next one absorbed.

Look again at cell `4` in the example. Its elevation is 4 but it can only be reached
through `6`, so its key is `max(6, 4) = 6`. That is how the heap "remembers" the bottleneck
already paid on the way in.

One subtle detail differs from the previous problem. Here a cell is marked `seen` the
moment it is **pushed**, and never pushed again. That is safe because a cell's key depends
only on the popped key `t` and its own elevation, and popped keys never decrease, so the
first push gives the smallest key the cell will ever be offered. In 0-1 BFS the edge weight
depended on the direction, so a later push could be cheaper; there we had to allow
improvements.

## Watch it work

The heap is shown sorted as `key:cell`. `seen` grows on every push.

```text
Frame 1  start
  [ 0  6  4 ]   heap: [ 0:(0,0) ]
  [ 1  7  3 ]   level so far: -
  [ 5  8  2 ]   seen: (0,0)
```
The start's own elevation counts, so its key is `grid[0][0]`.

```text
Frame 2  pop 0:(0,0)
  [*0  6  4 ]   push (1,0) key max(0,1)=1
  [ 1  7  3 ]   push (0,1) key max(0,6)=6
  [ 5  8  2 ]   heap: [ 1:(1,0) 6:(0,1) ]
```
Both neighbours enter the border; the low one is on top.

```text
Frame 3  pop 1:(1,0)
  [*0  6  4 ]   push (2,0) key 5
  [*1  7  3 ]   push (1,1) key 7
  [ 5  8  2 ]   heap: [ 5:(2,0) 6:(0,1) 7:(1,1) ]
```
The bait is taken: `1` is cheapest, so the search tries the left side first.

```text
Frame 4  pop 5:(2,0)
  [*0  6  4 ]   push (2,1) key 8
  [*1  7  3 ]   heap: [ 6:(0,1) 7:(1,1) 8:(2,1) ]
  [*5  8  2 ]
```
The left side dead-ends behind the `8`; nothing new is cheap.

```text
Frame 5  pop 6:(0,1)
  [*0 *6  4 ]   push (0,2) key max(6,4)=6
  [*1  7  3 ]   heap: [ 6:(0,2) 7:(1,1) 8:(2,1) ]
  [*5  8  2 ]
```
The level jumps to 6, and the `4` behind it inherits that level.

```text
Frame 6  pop 6:(0,2), then pop 6:(1,2)
  [*0 *6 *4 ]   (0,2) pushes (1,2) key max(6,3)=6
  [*1  7 *3 ]   (1,2) pushes (2,2) key max(6,2)=6
  [*5  8  2 ]   heap: [ 6:(2,2) 7:(1,1) 8:(2,1) ]
```
Once over the ridge, the downhill cells all ride at level 6.

```text
Frame 7  pop 6:(2,2) -> goal
  [*0 *6 *4 ]   return 6
  [*1  7 *3 ]   7 and 8 were never popped
  [*5  8 *2 ]
```
The corner comes off the heap with key 6, the answer.

Across frames the popped keys read `0, 1, 5, 6, 6, 6, 6`: never decreasing. That is the
invariant that makes "first pop of the goal" final, and it is the same order in which the
hand flooding shaded cells.

## Why it is correct

Define `best(x)` as the minimax value of the best route from the start to cell `x`.

Invariant: every popped key equals `best` of the popped cell, and popped keys come out in
non-decreasing order.

Suppose a cell `x` is popped with key `k` but `best(x) < k`. Take an optimal route to `x`
with maximum `best(x)`. It starts in the popped region and ends outside it, so somewhere it
crosses from a popped cell `p` to an unpopped cell `y`. Every cell on that route up to `y`
has elevation `<= best(x)`, and `p` was popped with key `<= best(x)` (by induction), so `y`
was pushed with key `max(key(p), elev(y)) <= best(x) < k`. Then `y` would have been popped
before `x`, contradicting that `x` is the current minimum. So `k = best(x)`, and in
particular the goal's first pop is the answer.

The binary-search version is correct for a simpler reason: `reachable(t)` is false below
the answer and true from it onward (`F...FT...T`), and binary search finds the first true.

## Cost

- **Binary search + BFS:** `O(n^2 log n)` time (`log(n^2)` probes, each an `O(n^2)` BFS),
  `O(n^2)` space for the visited set.
- **Bottleneck Dijkstra:** `O(n^2 log n)` time (each cell pushed and popped once on a heap
  of `O(n^2)` entries), `O(n^2)` space. Same bound, but one traversal, and it usually stops
  long before touching the whole grid.

## Variations you will meet

- **Path With Minimum Effort (LeetCode 1631).** The cost of a route is its largest
  height **difference** between neighbours. Same bottleneck Dijkstra; the edge value is
  `abs(h[a] - h[b])` and the key is `max(level, edge)`.
- **Union-find instead of a heap.** Sort cells by elevation and switch them on one at a
  time, unioning with switched-on neighbours, until start and corner share a root. The
  elevation that did it is the answer. It is Kruskal's idea, which Find Critical and
  Pseudo-Critical Edges builds on.
- **Path With Maximum Minimum Value (LeetCode 1102).** Maximise the smallest cell on a
  route: use a max-heap and `min` instead of `max`.
- **Many queries on the same grid.** Offline: sort queries by level and add cells in
  order, as in Checking Existence of Edge Length Limited Paths.

## What to carry forward

Dijkstra works for any route cost that never decreases as you extend the route; for a
"highest point on the route" cost, store `max(level, cell)` in the heap and the first pop
of the goal is optimal. The next problem goes back to ordinary summed weights but runs
Dijkstra three times, once on a reversed graph, and glues the results at a meeting node.
