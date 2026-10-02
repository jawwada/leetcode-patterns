# Pacific Atlantic Water Flow

*LeetCode 417 · Medium · Pattern: Multi-source reverse BFS/DFS from the boundary · Reading time ~8 min*

## What the problem is really asking

You get a grid of heights. The Pacific Ocean touches the top and left edges; the Atlantic touches the bottom and right
edges. Rain on a cell flows to any up/down/left/right neighbour whose height is **less than or equal** to the current
cell's height, and from a border cell straight into the ocean on that side. Return every cell from which water can
reach **both** oceans.

The answer is a list of coordinates. In graph terms, each cell has a directed edge to each neighbour it can flow into
(downhill or level). We want the cells that can reach a Pacific-border cell and also an Atlantic-border cell.

```text
               Pacific
          c0  c1  c2  c3
     r0    2   5   5   2
 Pac r1    3   5   4   6   Atl
     r2    5   1   5   1
               Atlantic

  both oceans: (0,1) (0,2) (0,3) (1,1) (1,3) (2,0)
  e.g. (1,1)=5 -> (1,0)=3 -> Pacific (left edge)
       (1,1)=5 -> (2,1)=1 -> Atlantic (bottom edge)
  (1,2)=4 is a pit: every neighbour is higher, no ocean
```

Two things make it harder than enclaves. Edges are now **one-way** (water does not flow uphill), and there are two
targets whose results must be combined.

## Do it by hand first

Pick (0,2), height 5. By hand, you would trace water downhill: left to (0,1)=5 (level is fine), which is on the top
edge, so Pacific. For the Atlantic: right to (0,3)=2, which is on the right edge. Both. Now (1,1): down to 1 on the
bottom edge (Atlantic), left to 3 on the left edge (Pacific). Both.

```text
  tracing from each cell by hand:
  (0,2)=5 -> (0,1)=5 top edge         Pacific
  (0,2)=5 -> (0,3)=2 right edge       Atlantic
  (1,1)=5 -> (1,0)=3 left edge        Pacific
  (1,1)=5 -> (2,1)=1 bottom edge      Atlantic
  ... and again for each of the 12 cells
```

You quickly notice you keep re-walking the same downhill slopes: the three 5s on the plateau reach exactly the
same downhill region every time. What your hand wanted was a map of "already known to reach the Pacific" and "already known to reach the
Atlantic", filled in once.

## The first honest attempt

For each of the m*n cells, run a downhill DFS with its own visited set and record whether it touched a top/left cell
and a bottom/right cell.

```text
  cells reached by a downhill search (sorted):
  from (0,1)=5: (0,0) (0,1) (0,2) (0,3)
                (1,0) (1,1) (1,2) (2,1)
  from (0,2)=5: (0,0) (0,1) (0,2) (0,3)
                (1,0) (1,1) (1,2) (2,1)
  from (1,1)=5: (0,0) (0,1) (0,2) (0,3)
                (1,0) (1,1) (1,2) (2,1)
  three searches, the identical 8-cell region each time
```

Each search is O(m*n), so the total is O((m*n)^2). The repeated work: the three plateau cells (connected by level
edges) have exactly the same downhill region, and nothing learned by one search is reused by the next.

## The turning point

**Claim: reverse the edges. A cell can drain to the Pacific exactly when it can be reached from a Pacific-border cell
by walking *uphill or level* (to neighbours of height >= current), so one multi-source search per ocean answers the
question for every cell at once.**

Why: a drainage path is a sequence of cells c0 -> c1 -> ... -> ck where each step goes to a height <= the previous, and
ck is on the Pacific border. Read it backwards: ck -> ... -> c0, each step goes to a height >= the previous. So the
cells that can drain into the Pacific are exactly the cells reachable from the Pacific border under the reversed rule.

Unlike enclaves, the edges are directed, so we cannot just say "symmetric". We reverse them explicitly. That is the
general move: **"which nodes can reach the target set?" equals "which nodes can the target set reach in the reversed
graph?"**

So the algorithm is:

1. Seed a queue with every Pacific-border cell (top row, left column). BFS uphill; mark everything reached in `pac`.
2. Seed another queue with every Atlantic-border cell (bottom row, right column). BFS uphill; mark in `atl`.
3. Return the cells marked in both.

Each BFS visits each cell at most once, so the total is O(m*n). The intersection is the "combine two targets" step:
two independent reachability sets, then an AND.

The comparison is `>=`, not `>`. Equal heights flow both ways, and dropping the equal case loses whole plateaus. You
will see it matter in Frame 5.

## Watch it work

`P` / `A` mark cells reached by the Pacific / Atlantic climb. Queue front on the left. A corner cell can sit in the seed
list twice; it is marked once and its second pop finds nothing new.

```text
Frame 1  Pacific seeds: column 0 and row 0, all marked
        c0  c1  c2  c3          pac:  P  P  P  P
   r0    2   5   5   2                P  .  .  .
   r1    3   5   4   6                P  .  .  .
   r2    5   1   5   1
  queue: [(0,0) (1,0) (2,0) (0,0) (0,1) (0,2) (0,3)]
```

The whole top and left rim drains into the Pacific trivially.

```text
Frame 2  pop (0,0)=2: nothing new
         pop (1,0)=3: right (1,1)=5 >= 3 -> mark
        c0  c1  c2  c3          pac:  P  P  P  P
   r0    2   5   5   2                P  P  .  .
   r1    3   5   4   6                P  .  .  .
   r2    5   1   5   1
  queue: [(2,0) (0,0) (0,1) (0,2) (0,3) (1,1)]
```

Climbing from 3 to 5 means water on (1,1) can run down to (1,0) and out.

```text
Frame 3  pop (2,0) (0,0) (0,1) (0,2): nothing new
         ((0,2)=5 cannot climb to (1,2)=4)
         pop (0,3)=2: down (1,3)=6 >= 2 -> mark
         pop (1,1)=5, (1,3)=6: no higher neighbour
        c0  c1  c2  c3          pac:  P  P  P  P
   r0    2   5   5   2                P  P  .  P
   r1    3   5   4   6                P  .  .  .
   r2    5   1   5   1
  queue: []   Pacific done
```

(1,2)=4, (2,1)=1, (2,2)=5 and (2,3)=1 are never reached: they cannot drain to the Pacific.

```text
Frame 4  Atlantic seeds: column 3 and row 2, all marked
         pop (0,3)=2: left (0,2)=5 >= 2 -> mark
         pop (1,3) (2,3) (2,0): nothing new
         pop (2,1)=1: up (1,1)=5 >= 1 -> mark
        c0  c1  c2  c3          atl:  .  .  A  A
   r0    2   5   5   2                .  A  .  A
   r1    3   5   4   6                A  A  A  A
   r2    5   1   5   1
  queue: [(2,2) (2,3) (0,2) (1,1)]
```

The Atlantic climb enters the interior from two sides.

```text
Frame 5  pop (2,2)=5, (2,3): nothing new
         pop (0,2)=5: left (0,1)=5 >= 5 -> mark (level!)
         pop (1,1)=5, (0,1)=5: (0,0)=2, (1,0)=3 lower
        c0  c1  c2  c3          atl:  .  A  A  A
   r0    2   5   5   2                .  A  .  A
   r1    3   5   4   6                A  A  A  A
   r2    5   1   5   1
  queue: []   Atlantic done
```

(0,1) joins only because 5 >= 5. With a strict `>` it would be lost from the answer.

```text
Frame 6  answer = cells marked in both grids
        pac           atl           both
     P  P  P  P    .  A  A  A    .  B  B  B
     P  P  .  P    .  A  .  A    .  B  .  B
     P  .  .  .    A  A  A  A    B  .  .  .
  answer: (0,1) (0,2) (0,3) (1,1) (1,3) (2,0)
```

This matches the solution's output on this grid.

Across both climbs, every marked cell can drain to that ocean, and every cell in the queue is marked but has not yet
tried its four neighbours.

## Why it is correct

Consider the Pacific climb (the Atlantic one is identical). Invariant: a cell is marked in `pac` only if there is a
non-increasing drainage path from it to the Pacific border.

*Marked implies drains*: seeds lie on the border. A cell (nr, nc) is marked from a marked (r, c) only when
`h[nr][nc] >= h[r][c]`, so water on (nr, nc) can step to (r, c) and then follow (r, c)'s path.

*Drains implies marked*: take a drainage path from cell c to border cell b. Reverse it; it climbs from b to c with every
step `>=`. b is a seed. When each cell on the reversed path is popped, the next one passes the height test and is
either marked then or already marked. So c is marked.

Hence `pac` and `atl` are exactly the drain-to-Pacific and drain-to-Atlantic sets, and their intersection is the answer.

## Cost

- **Time O(m*n).** Each climb pushes every cell at most once (plus the duplicated corner seeds); the intersection is
  one more pass.
- **Space O(m*n)** for the two boolean grids and the queues.

The brute force was O((m*n)^2); on a 200 x 200 grid that is 1.6 billion against 80,000.

## Variations you will meet

- **DFS instead of BFS.** Same marks; the queue becomes a stack or recursion. Order does not matter for reachability.
- **Three or more targets.** One reversed flood per target, then intersect (or count how many targets each cell
  reaches). Cost grows linearly in the number of targets, not in the number of cells.
- **Trapping Rain Water II.** Also starts from the border and works inward by height, but needs a min-heap (the lowest
  wall leaks first) because it asks *how much* water stays, not *whether* water escapes.
- **Strictly downhill flow.** Change `>=` to `>` in the climb. Plateaus then become separate pits.

## What to carry forward

To find everything that can reach a target set, reverse the edges and flood once from the whole target set; with two
targets, flood twice and intersect. The next problem keeps the multi-source start but finally makes the order matter:
rotting oranges spread one layer per minute, and the number of BFS layers is the answer.
