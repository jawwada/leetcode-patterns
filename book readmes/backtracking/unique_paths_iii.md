# Unique Paths III
*LeetCode 980 · Hard · Pattern: Grid DFS backtracking with in-place visited marking · Reading time ~10 min*

## The problem

A grid holds exactly one start (1), one end (2), empty cells (0) and obstacles (-1). Count the 4-directional walks
from start to end that visit every empty cell exactly once and never touch an obstacle or repeat a cell.

```text
Example: [[1,0,0,0],[0,0,0,0],[0,0,2,-1]] -> 2; [[0,1],[2,0]] ->
  0, because whichever empty cell the start steps to first, its
  only onward move is the end, leaving the other empty cell
  unvisited.
```

## What the problem is really asking

A small grid holds one start cell (`1`), one end cell (`2`), empty cells (`0`) and walls
(`-1`). Count the walks that go from start to end, moving up, down, left or right, that step
on **every** empty cell exactly once and never touch a wall or repeat a cell.

The answer is a number: how many such walks exist. Each walk is a snake that starts on the
`1`, eats the whole floor, and finishes with its head on the `2`.

```text
       c0  c1  c2              order of visits
  r0 [ S   .   . ]          [ 0   3   4 ]
  r1 [ .   .   E ]          [ 1   2   5 ]

  S = start (1)   E = end (2)   . = empty (0)
  walk: (0,0)->(1,0)->(1,1)->(0,1)->(0,2)->(1,2)
  answer = 1
```

What makes it hard: "visit every cell exactly once" is the Hamiltonian path problem, and for
general graphs nobody knows a polynomial algorithm. There is no greedy rule and no clever
formula. The grid is tiny on purpose (at most 20 cells), which is the problem telling you
that an exhaustive search is expected. The job is to make that search clean and to stop each
doomed walk as early as possible.

## Do it by hand first

Take the 2 x 3 grid above. Put a pencil on `S`. You can go down to (1,0) or right to (0,1).

Try down. From (1,0) the only fresh neighbour is (1,1). From (1,1) you could go up to (0,1)
or right to `E`. If you go right to `E` now, you are finished, but (0,1) and (0,2) were never
visited. That walk does not count. So go up to (0,1), then right to (0,2), then down to `E`.
Every empty cell is used: one walk.

Now try right first. From (0,1): down to (1,1) or right to (0,2). Going to (0,2) leaves only
`E` as a neighbour, and stepping there leaves three cells unvisited. Going to (1,1): then
either `E` (too early) or (1,0), which is a corner with nowhere to go. Nothing works.

```text
  tracing by hand, cells numbered in visiting order

  down first:      right first, then (1,1), then (1,0):
  [ 1  4  5 ]      [ 1  2  . ]
  [ 2  3  6=E ]    [ 4  3  E ]     stuck at 4: no fresh cell,
                                   and (0,2) never visited
```

What did your pencil keep track of? Where the head is, which cells are already on the walk
(so you do not reuse them), and, at the moment you touched `E`, **whether anything was left
over**. That last check is the new seed: a single counter of cells still owed.

## The first honest attempt

A valid walk is just an ordering of the empty cells: start, then the empties in some order,
then end. So enumerate every permutation of the `k` empty cells and check that consecutive
cells in `start, perm..., end` are adjacent. Count the orderings that pass.

That costs `O(k! * k)`. Our grid has `k = 4`, so 24 orderings. Look at where they die:

```text
  start S = (0,0) touches only (0,1) and (1,0)

  orderings beginning with (1,1):  6 of them  all dead at link 1
  orderings beginning with (0,2):  6 of them  all dead at link 1
       S -> (1,1)  not adjacent   x  -- yet 3! tails generated
       S -> (0,2)  not adjacent   x  -- yet 3! tails generated

  12 of 24 orderings are rejected for the SAME first-link reason
```

The repeated work is the same as in every brute force in this chapter: a prefix that is
already impossible is completed in all `(k - 2)!` ways and each completion is rejected
separately, at the end. On a 20-cell grid that is billions of orderings, almost all dead
after two or three steps.

## The turning point

**Claim: grow the walk one step at a time, only into fresh non-wall neighbours, and carry a
count of cells still to visit; then a walk is counted exactly when it reaches the end with
the count at zero.**

Two prunings fall out of growing the walk step by step instead of choosing an ordering.

First, adjacency is enforced by construction. You only ever step to a neighbour, so the
"not adjacent" orderings are never generated. That kills the 12 dead orderings above at
their first step.

Second, the end cell is a **sink**. Once the walk touches `E` it cannot continue (the walk
must finish there), so touching `E` is always a leaf. It is a success only if nothing is
owed. This is where the counter comes in. Before the search, count the empty cells and add
one for the end cell itself: call this `todo`. Every step decrements it. Arriving at `E`
with `todo == 0` means every empty cell and the end were stepped on exactly once, because
the walk never repeats a cell. Arriving with `todo > 0` means the walk took a shortcut: it
returns 0 without exploring further. The "all cells used" test, which the brute force had
to do by checking the whole permutation, is now one integer comparison.

Why add one for the end cell? Because the step onto `E` also decrements `todo`. With 4
empties, `todo` starts at 5; the valid walk makes 5 steps (four empties plus the end), so it
arrives at 0. Forgetting the `+1` makes every valid walk arrive at `-1` and you count zero.
This off-by-one is the most common bug in this problem.

The visited set is handled exactly as in Word Search: overwrite the current cell with `-1`
(a wall) when the head enters it, and write the original value back when the head leaves.
Neighbour filtering then needs one test, "is the value 0 or 2?", which rejects walls,
visited cells, and the start cell all at once (the start is marked too while the walk is
alive).

The state of the search is therefore just `(r, c, todo)` plus the marks on the floor, which
are the recursion stack drawn on the grid. Each call: if standing on `E`, return 1 or 0;
otherwise mark, sum the results of the up to four fresh neighbours with `todo - 1`, unmark,
return the sum. Counting, not deciding, means no short-circuit: every branch is explored.

## Watch it work

Grid `[[1,0,0],[0,0,2]]`, `todo = 5`. Neighbours are tried down, up, right, left.
`#` marks cells on the current walk (stored as `-1`), `H` is the head, `x` is a pruned
branch.

```text
Frame 1   head at S, todo 5; mark S, try down
  [ #  .  . ]      walk: (0,0)
  [ H  .  E ]      next: (1,0) with todo 4
```
The start is marked like any other walk cell so the snake can never return to it.

```text
Frame 2   (1,0) todo 4 -> (1,1) todo 3 -> (0,1) todo 2
          -> (0,2) todo 1 -> E todo 0
  [ #  #  # ]      at E with todo == 0  -> return 1
  [ #  #  E ]      count = 1
```
The snake covered the whole floor and reached the end with nothing owed: one walk counted.

```text
Frame 3   unwind to (1,1) (todo 3): its next try is
          right -> E with todo 2
  [ #  .  . ]      E reached early, todo 2 != 0  x
  [ #  H  E ]      left (1,0) is marked: skip
```
Touching `E` with cells still owed returns 0 at once; (1,1) and then (1,0) have no fresh
neighbours left, so they unmark and return.

```text
Frame 4   back at S: try right. (0,1) todo 4,
          down -> (1,1) todo 3
  [ #  #  . ]      right: E with todo 2   x
  [ .  H  E ]      left:  (1,0) todo 2
```
The second subtree starts; the early-`E` branch dies on the counter check.

```text
Frame 5   (1,0) todo 2: down off grid, up S marked,
          right (1,1) marked, left off grid
  [ #  #  . ]      no fresh neighbour: dead end  x
  [ H  #  E ]      returns 0, unmark (1,0), (1,1)
```
A corner with no fresh neighbours sums nothing and returns 0; the snake retracts.

```text
Frame 6   (0,1) tries right: (0,2) todo 3 -> down E todo 2
  [ #  #  H ]      E with todo 2   x
  [ .  .  E ]      every branch of S exhausted
                   total = 1 + 0 = 1
```
The last branch hits `E` early. Unwinding restores the grid to its original values.

Invariant across frames: the marked cells formed a single chain from `S` to the head, and
`todo` equalled the number of unmarked empty cells plus one for `E`. Every return left the
grid exactly as it was on entry.

## Why it is correct

**Invariant.** When `dfs(r, c, todo)` is entered, the marked cells are a self-avoiding walk
from start to the cell before (r, c), and `todo` is the number of not-yet-stepped cells
among the empties and the end, counting (r, c) as already stepped. Stepping to a fresh
neighbour extends the walk by one cell and lowers `todo` by one, preserving it. Unmarking on
return restores the walk of the caller, so siblings explore from the correct state.

**Soundness.** A 1 is returned only on `E` with `todo == 0`. By the invariant every empty
cell is on the walk, each once (no repeats are possible), so the walk is valid.

**Completeness.** Any valid walk is a sequence of steps, each into a fresh non-wall
neighbour, never touching `E` before the last step. The DFS tries every fresh neighbour at
every step, so it follows that sequence. The only pruned branches are walls, repeats, and
early arrivals at `E`, none of which a valid walk takes.

**No double counting.** Two different walks diverge at some first step; the DFS reaches
them through different children of that node, so each walk is counted exactly once.

## Cost

- **Time `O(3^(R*C))` in practice, `O(4^(R*C))` as a loose bound.** Each step has at most
  three fresh directions (the cell behind you is marked); depth is at most the cell count.
  With at most 20 cells and heavy pruning, real runs are tiny.
- **Space `O(R*C)`.** Recursion depth equals the walk length; marks live in the grid.
- The permutation brute force is `O(k! * k)` for `k` empty cells.

## Variations you will meet

- **Memoise with a bitmask.** State `(cell, set of visited cells)` determines the number of
  completions. With at most 20 cells, `2^20 * 20` states fit, and `dp[mask][cell]` counts
  walks in `O(2^n * n)`. That is the same idea as Shortest Path Visiting All Nodes (847):
  when the visited set is small, turn it into a bitmask index.
- **Parity pruning.** Colour the grid like a chessboard. Each step flips colour, so if the
  walk length and the colours of start and end disagree, the answer is 0 before searching.
- **Unique Paths I and II.** Only right and down moves, no "cover everything" rule: the
  count of a cell depends only on the cell, so it becomes a simple grid DP.
- **Return the walks, not the count.** Keep a path list, append on entry, pop on exit, copy
  it at each valid leaf.

## What to carry forward

When the walk must use everything, carry a single "still owed" counter so that the leaf
test is one comparison, and treat the goal as a sink you may only enter with the debt at
zero. Next, N-Queens leaves the walk behind: instead of moving a head through cells, it
places one piece per row and asks three sets which squares are still safe.
