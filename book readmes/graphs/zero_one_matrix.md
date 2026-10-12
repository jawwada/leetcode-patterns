# 01 Matrix
*LeetCode 542 · Medium · Pattern: Multi-source BFS (level = distance) · Reading time ~8 min*

## The problem

Given an m x n binary matrix, return a matrix where each cell holds the distance to the nearest 0, moving up, down,
left or right. At least one 0 exists.

```text
Example: [[0,0,0],[0,1,0],[1,1,1]] -> [[0,0,0],[0,1,0],[1,2,1]].
```

## What the problem is really asking

You get a grid of zeros and ones. For every cell, write down how many up/down/left/right
steps it takes to reach the **nearest** zero. Zeros get `0`. At least one zero exists, and
every cell can walk anywhere (there are no walls), so every answer is finite.

The answer is a whole grid of distances, the same shape as the input. Each output cell is a
shortest-path length, but to a **set** of targets (any zero will do), not to one target.

```text
  input                    output
        c0 c1 c2                 c0 c1 c2
  r0  [ 0  1  1 ]          r0  [ 0  1  2 ]
  r1  [ 1  1  1 ]          r1  [ 1  2  1 ]
  r2  [ 1  1  0 ]          r2  [ 2  1  0 ]

  two zeros in opposite corners; the
  middle cell is 2 steps from either
```

What makes it hard is purely cost. Asking "where is my nearest zero?" separately for each of
`m*n` cells is easy to code and far too slow on a 10^4-cell grid.

## Do it by hand first

On paper, nobody searches outward from each `1`. You look at the zeros and think the other
way round. Every zero is a `0`. Every cell touching a zero is a `1`. Every unlabelled cell
touching a `1` is a `2`. And so on.

```text
  pass 0: zeros     pass 1: next to 0   pass 2: the rest
  [ 0  .  . ]       [ 0  1  . ]         [ 0  1  2 ]
  [ .  .  . ]       [ 1  .  1 ]         [ 1  2  1 ]
  [ .  .  0 ]       [ .  1  0 ]         [ 2  1  0 ]
```

Your hand kept two things: the **set of cells labelled in the last pass** (only they can
label anything new) and the **labels already written**, which you never change once set.
The first is a BFS queue; the second is the distance grid doubling as the visited set.

It is the same move as Rotting Oranges, with the zeros playing the rotten oranges. The only
difference is what we keep: there we wanted the last minute; here we want each cell's own
minute.

## The first honest attempt

For every cell, run a BFS outward until it hits a zero, and record the depth.

```text
  BFS from (1,1)          BFS from (1,0)
  [ 0  1  1 ]             [ 0  1  1 ]
  [ 1 *S* 1 ]             [*S* 1  1 ]
  [ 1  1  0 ]             [ 1  1  0 ]
  rings: (1,1) ->         rings: (1,0) ->
  (0,1)(2,1)(1,0)(1,2)    (0,0) found at depth 1
  -> (0,0) at depth 2

  both searches walk the same cells near (0,0),
  and neither reuses the other's answer
```

One BFS can cover the whole grid, so the total is `O((m*n)^2)`. Neighbouring cells run
nearly identical searches, and the knowledge "my neighbour is 1 away from a zero" is thrown
away: the cell next to it re-derives it from scratch instead of just adding one.

## The turning point

**Claim: the distance from a cell to the nearest zero equals the distance from the set of
all zeros to that cell, and one BFS that starts from every zero at once computes it for
every cell.**

Reverse the search. Instead of `m*n` searches each looking for "any zero", run a single
search **from** the zeros. Imagine a super-source joined to every zero by an edge of length
zero. A BFS from that super-source is the same as a BFS whose initial queue holds every zero
at distance 0. BFS visits cells in non-decreasing distance order, so the first time the wave
reaches a cell, it arrived from its closest zero.

That gives the update rule directly. When a cell `u` is popped with distance `d`, each
neighbour that has not been reached yet gets `d + 1` and joins the queue. Its value is
final from that moment.

The solution file states that with a slight twist. It fills every `1` with a big sentinel
`m*n` (larger than any real distance), and a neighbour is updated only when `dist[nb] > d + 1`:

```python
if dist[nr][nc] > nd:      # nd = dist[r][c] + 1
    dist[nr][nc] = nd
    queue.append((nr, nc))
```

In a BFS that test is true exactly once per cell, the first time it is reached, because
later arrivals carry distances that are equal or larger. So the sentinel plays the role of
"unvisited" and the grid is both answer and visited set.

Note there is no explicit layer loop here. We do not need one: each cell carries its own
distance, so we never ask "which minute is it?". Rotting Oranges needed layers because it
counted time globally; here the time is stored per cell.

## Watch it work

The example grid. `?` stands for the sentinel `9` (= `m*n`). The queue is shown at layer
boundaries; it is ordered by distance at every moment.

```text
Frame 1   seed: every zero, layer 0
  [ 0  ?  ? ]     q = [ (0,0) (2,2) ]
  [ ?  ?  ? ]          d=0   d=0
  [ ?  ?  0 ]
```
Both zeros start together; neither gets priority.

```text
Frame 2   pop (0,0) d=0
  [ 0  1  ? ]     sets (1,0)=1, (0,1)=1
  [ 1  ?  ? ]     q = [ (2,2) (1,0) (0,1) ]
  [ ?  ?  0 ]          d=0   d=1   d=1
```
The top-left wave takes its first step; the other zero is still waiting its turn.

```text
Frame 3   pop (2,2) d=0  -> layer 1 complete
  [ 0  1  ? ]     sets (1,2)=1, (2,1)=1
  [ 1  ?  1 ]     q = [ (1,0) (0,1) (1,2) (2,1) ]
  [ ?  1  0 ]          all d=1
```
The queue now holds exactly the distance-1 cells: layer 1.

```text
Frame 4   pop layer 1 (four cells)
  [ 0  1  2 ]     (1,0): sets (2,0)=2, (1,1)=2
  [ 1  2  1 ]     (0,1): sets (0,2)=2
  [ 2  1  0 ]     (1,2),(2,1): every neighbour
                  already <= 2, nothing set
                  q = [ (2,0) (1,1) (0,2) ]  d=2
```
(1,1) is reached first from (1,0); when (1,2) and (2,1) look at it later, `2 > 2` is false.

```text
Frame 5   pop layer 2
  [ 0  1  2 ]     nd = 3, but every neighbour
  [ 1  2  1 ]     already holds <= 2
  [ 2  1  0 ]     q = [ ]  -> return grid
```
The last layer adds nothing; the queue empties and the grid is the answer.

Invariant across frames: the queue's distances were non-decreasing from front to back, and
never spanned more than two consecutive values. Any number written into the grid was never
changed again.

## Why it is correct

The layer property of BFS, with many sources. Say a cell has true distance `k` when its
nearest zero is `k` steps away. Claim: every cell with true distance `k` is written with `k`,
and is enqueued before any cell with true distance `k + 1`.

For `k = 0` it holds by seeding. Suppose it holds up to `k`. A cell with true distance `k + 1`
has a neighbour with true distance `k` (the next step on its shortest path). That neighbour
is popped while all queued cells have distance `k` or `k + 1`, and it writes `k + 1` into the
cell unless something already wrote a value no larger. Nothing could have written less than
`k + 1`: a smaller label would mean a neighbour at distance less than `k`, giving a true
distance below `k + 1`. So the cell ends up with exactly `k + 1`, and it was enqueued after
all distance-`k` cells.

Every cell is reachable (no walls, at least one zero), so every sentinel is overwritten.

## Cost

- **Time `O(m*n)`**: each cell is written and enqueued once and checks four neighbours.
- **Space `O(m*n)`**: the distance grid and a queue that can hold a large layer.

There is also a well-known two-pass DP: sweep top-left to bottom-right taking
`min(up, left) + 1`, then bottom-right to top-left taking `min(down, right) + 1`. Same
`O(m*n)` time, `O(1)` extra space. It works only because there are no walls; the BFS
generalises, the DP does not.

## Variations you will meet

- **Distance to the nearest 1, or to a given set of cells.** Seed the queue with that set;
  nothing else changes.
- **As far from land as possible (LeetCode 1162).** Same multi-source BFS from all land
  cells; the answer is the largest distance written, which is Rotting Oranges' question.
- **Obstacles.** Walls simply never get enqueued. That is the next problem.
- **Diagonal or 8-way moves.** Change the neighbour list; the BFS is untouched, and the DP
  needs the diagonal cells added to each sweep.

## What to carry forward

"Distance to the nearest of many targets" for every cell is one BFS seeded with all the
targets, never one BFS per cell. The next problem, Walls and Gates, runs the very same wave
but lets walls block it and some rooms stay unreachable.
