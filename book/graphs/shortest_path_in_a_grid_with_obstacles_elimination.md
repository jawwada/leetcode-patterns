# Shortest Path in a Grid with Obstacles Elimination
*LeetCode 1293 · Hard · Pattern: BFS over augmented states (position + bitmask/budget) · Reading time ~10 min*

## What the problem is really asking

A grid of 0s (open) and 1s (obstacles). You start at the top-left, want the bottom-right,
and move one cell up, down, left or right per step. You may walk onto at most `k` obstacle
cells; each one you walk onto is destroyed and costs one unit of your budget. Return the
fewest steps, or -1.

The answer is a shortest-path length, so BFS is the obvious tool. What breaks plain grid
BFS is that the cost of a route is not only its length: it also spends a resource. Two
walks can stand on the same cell after the same number of steps and still have different
futures, because one has a demolition left and the other does not.

```text
  grid (k = 1)          c0 c1 c2

                  r0     S  .  .        S = start (0,0)
                  r1     #  #  .        T = target (4,2)
                  r2     .  .  .        # = obstacle (1)
                  r3     .  #  #
                  r4     .  .  T

  route A: right, right, down, down, down*, down         6 steps
           (smash (3,2))
  route B: down*, down, down, down, right, right         6 steps
           (smash (1,0))
  no smashing: around the bottom-left, 10 steps
```

Constraints: up to 40 x 40 grid, `k` up to 1600 (the number of cells). So `k` can be big,
and a direct "try every set of obstacles" idea is out of the question for the real limits.

## Do it by hand first

With no budget the wall in row 1 forces you to the right edge, and the wall in row 3
forces you back to the left edge: 10 steps. With one smash you look for the single
obstacle that saves the most. Smashing (3,2) lets you drop straight down the right edge.
Smashing (1,0) lets you drop straight down the left edge. Either saves 4 steps.

```text
  smash (3,2)              smash (1,0)
   0  1  2                  0  .  .
   #  #  3                  1  #  .
   .  .  4                  2  .  .
   .  #  5*                 3  #  #
   .  .  6                  4  5  6
```

What did your hand keep track of as it walked? Where you are, how many steps you have
taken, and **whether you still have the smash in your pocket**. When you stood at (2,2)
after 4 steps, the question "can I go down?" had a different answer depending on whether
you had already used the smash. That third number is the seed of the solution.

## The first honest attempt

Decide in advance which obstacles to destroy. For every subset of at most `k` obstacles,
clear them, run an ordinary grid BFS, and keep the best result.

```text
  obstacles: (1,0) (1,1) (3,1) (3,2)     k = 1

  clear {}       -> BFS -> 10
  clear {(1,0)}  -> BFS -> 6
  clear {(1,1)}  -> BFS -> 8
  clear {(3,1)}  -> BFS -> 8
  clear {(3,2)}  -> BFS -> 6       best = 6

  5 full BFS runs; the top-right corridor
  (0,0)->(0,1)->(0,2)->(1,2)->(2,2) is walked in
  every single one of them
```

It is correct and costs C(B, <= k) x m x n, where B is the number of obstacles. With 800
obstacles and k = 5 that is more than 10^12 BFS runs. The repeated work is easy to see:
every run re-walks the same open region from scratch, and most subsets clear obstacles
nowhere near any good path. The search decides *which* obstacles before knowing *where*
the walk will go.

## The turning point

**Claim: the future of a walk depends only on (row, column, smashes left), not on which
obstacles were smashed. So make that triple the node, and run one BFS over it.**

Why only the count? Once you are standing on a cell, the obstacles behind you no longer
matter (walking back onto a smashed cell is pointless for a shortest path). What the
future needs is where you are and how many more obstacles you may walk through. Two walks
that agree on those three numbers have exactly the same set of possible continuations.

So the real graph is the grid copied `k + 1` times, once per remaining budget. Picture the
copies stacked:

```text
  the thing: k+1 stacked copies of the grid

     budget 1   S . .       inside a copy: move on 0-cells
                # # .
                . . .       step onto a # : fall one copy
                . # #       down (budget - 1), same step
                . . T       count + 1
                    |
                    v  (stepping on (3,2))
     budget 0   . . .
                . . .       in budget 0, # is a wall
                . . .
                . # #
                . . T

  how it is stored: one queue of (r, c, left)
                    seen = set of (r, c, left)
```

Every edge is still exactly one step. Moving onto a 0 keeps `left`; moving onto a 1 makes
it `left - 1`, and is forbidden if that would be negative. Because all edges cost one
step, ordinary BFS over the triples finds the fewest steps, and the first time *any* copy
of the target cell is popped, that depth is the answer.

This is the chapter's refrain, applied literally: **the graph is not the grid, the graph is
the state.** The grid is just the floor plan; the state is where you are plus what you
still carry.

The visited set must be keyed on the full triple. It is tempting to mark cells, because
"we already reached this cell sooner" sounds like it should dominate. It does not. A walk
that got somewhere one step later with more budget can be the only one that gets through.
Smallest case:

```text
  k = 1        c0 c1 c2 c3
          r0    S  .  #  #
          r1    #  .  #  T

  cell-only seen:   (1,0) smashed first, reaches (1,1)
                    with 0 left and claims the cell;
                    (0,1) -> (1,1) with 1 left is
                    rejected -> answer -1  (wrong)
  triple seen:      (1,1,left=1) is a new state ->
                    smash (1,2) -> T in 4  (right)
```

One more observation, a cheap shortcut: any shortest path has at least m + n - 2 steps,
and the plain staircase path uses exactly that many cells after the start. If `k >= m + n
- 2` you can afford to smash every cell on it, so the answer is m + n - 2 immediately. This
also handles the 1 x 1 grid (answer 0) and keeps the state space small in the worst case.

## Watch it work

Each frame shows both copies. A number is the BFS depth at which that (cell, budget)
state was first reached; `#` is an obstacle not stood on in that copy; `.` is not yet
reached.

```text
Frame 1  depth 0 -> 1
        budget 1      budget 0
   r0   0 1 .         . . .
   r1   # # .         1 # .
   r2   . . .         . . .
   r3   . # #         . # #
   r4   . . .         . . .
```

From the start, right is free (stays in copy 1) and down is an obstacle, so that step
lands at (1,0) in copy 0.

```text
Frame 2  depth 2
        budget 1      budget 0
   r0   0 1 2         2 . .
   r1   # # .         1 2 .
   r2   . . .         2 . .
```

Copy 1 creeps along the top. Smashing (1,1) from (0,1) lands in copy 0 at depth 2, and copy
0 spreads from (1,0), including back to (0,0): a new state, since the budget differs.

```text
Frame 3  depth 3
        budget 1      budget 0
   r0   0 1 2         2 3 .
   r1   # # 3         1 2 3
   r2   . . .         2 3 .
   r3   . # #         3 # #
```

Copy 1 turns the corner at (1,2). Copy 0 now covers most of the top half; its wave also
reaches (1,2), but with no budget left.

```text
Frame 4  depth 4
        budget 1      budget 0
   r1   # # 3         1 2 3
   r2   . . 4         2 3 4
   r3   . # #         3 # #
   r4   . . .         4 . .
```

Copy 1 reaches (2,2) with the smash still in hand. In copy 0 the row 3 obstacles are
walls, so the wave goes down the left edge.

```text
Frame 5  depth 5
        budget 1      budget 0
   r2   . 5 4         2 3 4
   r3   . # #         3 # 5
   r4   . . .         4 5 .
```

From (2,2,left=1) the step down onto (3,2) costs the smash and lands in copy 0 at depth 5.
Copy 0 also reached (4,1) along the bottom.

```text
Frame 6  depth 6
        budget 1      budget 0
   r3   . # #         3 6 5
   r4   . . .         4 5 6   <- (4,2) target
```

(4,2) in copy 0 is reached at depth 6 (from (3,2) and from (4,1) alike); when layer 6 is
popped, the target check fires: answer 6. 22 states were created in total.

Across the frames each copy filled in like an ordinary BFS wave, and the only flow between
copies went downward at obstacles. Depth always meant "steps taken", whichever copy a
state sat in.

## Why it is correct

The state graph has a node for every (r, c, left) with 0 <= left <= k, and an edge of
length 1 for each legal move. A walk in the real grid that spends at most k smashes
corresponds exactly to a path in this graph from (0, 0, k), and the two have the same
number of steps. So the shortest legal walk to the target is the shortest path from
(0, 0, k) to any node (m - 1, n - 1, *).

BFS on a unit-weight graph pops nodes in non-decreasing distance, and when a node is first
pushed its depth is its true distance (the layer property: anything closer would have been
discovered from an earlier layer). The first popped node at the target cell therefore has
the minimum distance over all budgets. Marking seen on the triple means no state is lost:
two states that differ in budget are different nodes and both get explored. If the queue
empties, no legal walk exists and -1 is right.

The shortcut is safe because the staircase path has m + n - 2 steps, every walk needs at
least that many, and with k >= m + n - 2 even an all-obstacle staircase is affordable.

## Cost

- **Time O(m x n x k)**: there are at most m x n x (k + 1) states, each popped once and
  checking four neighbours. With the shortcut, k is effectively capped at m + n - 2, so
  this is at most O(m x n x (m + n)).
- **Space O(m x n x k)** for `seen` and the queue.
- A sharper version keeps, for each cell, only the *largest* budget seen so far and skips
  arrivals with no more budget (they are dominated). It has the same worst case but often
  visits far fewer states.

## Variations you will meet

- **Cost to smash instead of a budget.** "Minimum obstacles to remove to reach the corner"
  (LeetCode 2290) drops the step count: moving onto 0 costs 0, onto 1 costs 1. That is 0-1
  BFS on plain cells, no budget dimension needed.
- **Fuel, keys, or a carried item.** Any finite resource that changes what moves are legal
  joins the state: Shortest Path to Get All Keys (next) carries a set of keys; a fuel tank
  would carry an integer like `left` here.
- **Time-dependent cells.** If cells open and close over time, time (mod the period) joins
  the state. Same stacking picture, with copies per time step.
- **Two kinds of edge weight.** If smashing also cost extra time, edges would no longer be
  uniform, and BFS turns into Dijkstra over the same triples.

## What to carry forward

When a constraint depends on history, put the part of the history that matters into the
node: (cell, budget left) turns a constrained walk into a plain BFS over stacked copies of
the grid. The next problem, Shortest Path to Get All Keys, carries a *set* (the keys held)
instead of a counter, stored as a bitmask, and here walking back over old cells really is
needed.
