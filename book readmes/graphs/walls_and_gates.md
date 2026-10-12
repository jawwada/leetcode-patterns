# Walls and Gates
*LeetCode 286 · Medium · Pattern: Multi-source BFS (level = distance) · Reading time ~8 min*

## The problem

Given an m x n grid where -1 is a wall, 0 is a gate and INF (2^31 - 1) is an empty room, fill every empty room with
the distance to its nearest gate, leaving unreachable rooms as INF. Modify in place.

```text
Example:
  [[INF,-1,0,INF],
   [INF,INF,INF,-1],
   [INF,-1,INF,-1],
   [0,-1,INF,INF]]
  becomes [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]].
```

## What the problem is really asking

A floor plan is a grid. `-1` is a wall, `0` is a gate, and `INF` (the number `2^31 - 1`) is
an empty room. Replace every empty room's `INF` with the number of steps to its nearest gate,
moving up/down/left/right and never through a wall. A room no gate can reach keeps `INF`.
You edit the grid in place; nothing is returned.

The answer is the same grid with numbers filled in: a field of shortest distances to a set
of targets, exactly like 01 Matrix, except that walls cut the floor into pieces and some
pieces may hold no gate at all.

```text
  input (# = wall, G = gate, . = INF room)
        c0 c1 c2 c3                  c0 c1 c2 c3
  r0  [ .  #  G  . ]           r0  [ 3  #  0  1 ]
  r1  [ .  .  .  # ]    ->     r1  [ 2  2  1  # ]
  r2  [ .  #  .  # ]           r2  [ 1  #  2  # ]
  r3  [ G  #  .  . ]           r3  [ 0  #  3  4 ]
```

Two things to notice. The walls bend the shortest paths: r3c3 sits only 3 columns from the
bottom gate, but the wall at r3c1 blocks that route, so its answer is 4 (from the top gate). And the sentinel `INF` is doing a job:
it already marks "not yet reached".

## Do it by hand first

You would not stand in each room and search for a door. You would stand at the gates and
pour water. Every gate fills its neighbouring rooms with `1`, those fill theirs with `2`,
and walls stop the water.

```text
  after step 1       after step 2       after steps 3, 4
  [ .  #  0  1 ]     [ .  #  0  1 ]     [ 3  #  0  1 ]
  [ .  .  1  # ]     [ 2  2  1  # ]     [ 2  2  1  # ]
  [ 1  #  .  # ]     [ 1  #  2  # ]     [ 1  #  2  # ]
  [ 0  #  .  . ]     [ 0  #  .  . ]     [ 0  #  3  4 ]
```

Your hand tracked the **rim of the water** (the rooms filled in the last step) and used the
rule "only write into a room that still says `INF`". That rim is the BFS queue. The rule is
the visited check, and it lives in the grid itself.

## The first honest attempt

For every empty room, run a BFS that stops at the first gate it meets, and write that depth.

```text
  BFS from r1c0           BFS from r1c1
  [ .  #  G  . ]          [ .  #  G  . ]
  [ S  .  .  # ]          [ .  S  .  # ]
  [ .  #  .  # ]          [ .  #  .  # ]
  [ G  #  .  . ]          [ G  #  .  . ]
  visits r0c0 r1c1 r2c0   visits r1c0 r1c2 r0c0
  then finds r3c0 (d 2)   r2c0 r0c2 ... (d 2)

  neighbouring rooms explore nearly the same
  cells and rediscover the same gates
```

With up to `m*n` rooms and each BFS up to `O(m*n)`, that is `O((m*n)^2)`. The waste is the
same as in 01 Matrix: every room re-discovers its gate from scratch, though its neighbour
already knows how far that gate is.

## The turning point

**Claim: the distance from a room to its nearest gate equals the BFS depth at which a wave
started from all gates simultaneously first reaches that room.**

This is the 01 Matrix idea with two adjustments, and they are worth stating precisely.

First, walls. A wall is a cell the wave may never enter. The update rule only writes into a
neighbour whose value is exactly `INF`, and a wall holds `-1`, so walls are skipped for free.
Gates hold `0` and filled rooms hold small numbers; they are skipped by the same test. One
comparison, `rooms[nr][nc] == INF`, answers "is it in bounds of the floor, is it a room, and
is it still unvisited?"

Second, unreachable rooms. A room sealed off by walls is in a connected component with no
gate. No wave ever enters that component, so its `INF` stays. The problem asks for exactly
that, so no special handling is needed.

The rule itself is one line: when a cell is popped, each `INF` neighbour receives
`rooms[r][c] + 1` and is enqueued. As in 01 Matrix, the distance travels **with the cell**,
so there is no need for a layer loop or a minute counter. The queue happens to be ordered by
distance anyway, which is what makes "first write is final" true.

A tempting mistake is to test `rooms[nr][nc] != -1` ("not a wall") instead of `== INF`. That
lets the wave overwrite gates with `1` and rewrite rooms already holding their true distance
with larger values.

## Watch it work

The example grid. `#` is a wall, `.` is `INF`. The queue is shown at each layer boundary.

```text
Frame 1   seed both gates, layer 0
  [ .  #  0  . ]     q = [ (0,2) (3,0) ]
  [ .  .  .  # ]
  [ .  #  .  # ]
  [ 0  #  .  . ]
```
Both gates enter the queue before anything is popped.

```text
Frame 2   pop layer 0 -> layer 1
  [ .  #  0  1 ]     (0,2): writes (1,2)=1, (0,3)=1
  [ .  .  1  # ]     (3,0): writes (2,0)=1
  [ 1  #  .  # ]     q = [ (1,2) (0,3) (2,0) ]
  [ 0  #  .  . ]
```
(0,2)'s left neighbour is a wall, and (3,0)'s right neighbour too; `-1 != INF` keeps them out.

```text
Frame 3   pop layer 1 -> layer 2
  [ .  #  0  1 ]     (1,2): writes (2,2)=2, (1,1)=2
  [ 2  2  1  # ]     (0,3): nothing (wall below)
  [ 1  #  2  # ]     (2,0): writes (1,0)=2
  [ 0  #  .  . ]     q = [ (2,2) (1,1) (1,0) ]
```
The two waves now touch along row 1: r1c1 came from the top gate, r1c0 from the bottom one.

```text
Frame 4   pop layer 2 -> layer 3
  [ 3  #  0  1 ]     (2,2): writes (3,2)=3
  [ 2  2  1  # ]     (1,1): nothing (all filled)
  [ 1  #  2  # ]     (1,0): writes (0,0)=3
  [ 0  #  3  . ]     q = [ (3,2) (0,0) ]
```
When (1,1) looks at (1,0), that cell already says `2`, so it is left alone.

```text
Frame 5   pop layer 3 -> layer 4 -> done
  [ 3  #  0  1 ]     (3,2): writes (3,3)=4
  [ 2  2  1  # ]     (0,0): nothing
  [ 1  #  2  # ]     q = [ (3,3) ] then (3,3)
  [ 0  #  3  4 ]     adds nothing; q = [ ]
```
The last room is reached by snaking around two walls; the queue empties and the grid is final.

Across all frames: every number written was never changed, and the queue held at most two
consecutive distances. Walls and gates were never written.

## Why it is correct

The **BFS layer property** with many sources. Define a room's true distance as the length of
the shortest wall-free path to any gate. Seeded with all gates at distance 0, the queue pops
cells in non-decreasing order of the value written in them. A room at true distance `k + 1`
has a neighbour on its shortest path at true distance `k`; by induction that neighbour holds
`k` and is popped before any cell holding `k + 1`, so it writes `k + 1` into the room unless
the room was already written. It could not have been written with something smaller, since
that would imply a shorter path. So every reachable room holds its true distance.

A room in a component with no gate has no path to a gate, never has a neighbour that gets
popped, and keeps `INF`, as required.

## Cost

- **Time `O(m*n)`**: only `INF` cells are written and enqueued, each once; every pop checks
  four neighbours.
- **Space `O(m*n)`**: the queue; the grid itself is the distance store and the visited set.

## Variations you will meet

- **Shortest Distance from All Buildings (LeetCode 317).** Now the target is the empty cell
  that minimises the **sum** of distances to every building. Seeding all buildings in one
  wave mixes their distances, so you run one BFS per building and accumulate; the
  multi-source trick applies only when you need the nearest source, not all of them.
- **Return the nearest gate's id, not just the distance.** Carry the gate id in the queue
  along with the cell; first arrival also decides the owner (a Voronoi partition of the
  floor).
- **Moving costs differ per room.** The wave no longer advances in unit steps, so use
  Dijkstra; BFS order would be wrong.
- **Doors that open only one way.** The grid becomes a directed graph; BFS still works if
  you run it on reversed edges from the gates.

## What to carry forward

Flip "every room searches for a gate" into "all gates flood at once", and let the sentinel
in the grid be the visited set. The next problem, Clone Graph, leaves the grid: the graph is
a web of pointers, and the visited set grows into a map from each original node to its copy.
