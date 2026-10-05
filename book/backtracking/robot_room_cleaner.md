# Robot Room Cleaner
*LeetCode 489 · Hard · Pattern: Blind DFS with relative coordinates and turn-around backtrack · Reading time ~11 min*

## The problem

A robot is in an unknown grid room with open and blocked cells. It exposes only move() -> bool (step forward if
possible), turnLeft(), turnRight() and clean(). You know neither the map, your position nor your heading. Clean every
cell reachable from the start.

```text
Example: in a 5x8 room starting at row 1, col 3 facing up, every
  open cell connected to the start must end up cleaned.
```

## What the problem is really asking

A robot sits somewhere in a room made of grid cells, some open and some blocked. You cannot
see the room. You do not know its size, the robot's position, or which way it faces. You
can only call four methods:

```text
  robot.move()       step one cell forward; returns False
                     (and stays put) if the cell is blocked
  robot.turnLeft()   rotate 90 degrees in place
  robot.turnRight()  rotate 90 degrees in place
  robot.clean()      clean the cell it stands on
```

Clean every open cell reachable from the start. There is no return value; the judge checks
which cells were cleaned.

The room we will follow (you see it, the robot does not):

```text
        c0 c1 c2
  r0  [ 1  1  0 ]      1 = open, 0 = blocked
  r1  [ 0  1  1 ]      start: r1 c1, facing up

        c0 c1 c2
  r0  [ .  .  # ]      . = open, # = blocked
  r1  [ #  ^  . ]      ^ = robot facing up
                       4 open cells to clean
```

What makes it hard: this is just "visit every node of a connected graph", which DFS does in
its sleep, except that two things DFS takes for granted are gone. There are no coordinates
to put in a visited set, and backtracking is not free. When ordinary recursion returns, the
caller is "back" at the parent for nothing. Here the robot is physically standing in the
child cell, facing some direction, and it has to walk back.

## Do it by hand first

Imagine you are blindfolded in a dark room with a broom. What would you do?

You would invent your own coordinates: "where I started is (0,0), the way I am facing is
up". Every step forward changes your position by the direction you face, and every turn
changes the direction. Now you can remember which spots you have swept.

```text
  dead reckoning: start = (0,0), heading 0 = up

  heading   0 up     1 right   2 down    3 left
  delta    (-1,0)    (0,1)     (1,0)     (0,-1)
  turnRight:  heading -> (heading + 1) % 4
```

Then you would explore: try a direction, step if you can, sweep, keep going, and when you
are stuck you would **walk back to where you came from** and try something else from there.
The question you would face at each dead end: how do I get back, and which way am I facing
when I get there?

What you kept track of: your **invented position and heading**, the **set of swept spots**,
and the **way back**. The way back is the new ingredient this problem adds to backtracking.

## The first honest attempt

Run DFS with a visited set of relative coordinates. When a child is finished, you need to
be on the parent again. The straightforward way: remember the full path from the start as a
list of headings; to return, walk the whole path in reverse back to the start, then replay
the path up to the parent.

```text
  a corridor of N cells, start at the left end

  [S][1][2][3][4] ... [N-1]

  return from cell 4 to cell 3:
    walk 4 -> 3 -> 2 -> 1 -> S     (4 moves back)
    walk S -> 1 -> 2 -> 3          (3 moves forward)
  every backtrack re-walks the whole path: O(depth) moves
```

It is correct, but the cost is `O(N^2)` moves: on a 10-cell corridor this version makes 90
moves where 18 suffice, and at 20 cells it makes 380 against 38. The waste is plain in the
drawing: the parent is **one cell behind you**, yet you walk all the way to the start and
back again just to reach it.

## The turning point

**Claim: when DFS has just entered a child by moving forward in direction `d`, the parent is
directly behind the robot, so "turn around, move, turn around" returns it to the parent
facing `d` again; with headings kept in sync, the recursion stack is the path and every
backtrack costs a constant number of commands.**

The return trip, `go_back`, is four turns and one move:

```python
def go_back():
    robot.turnRight(); robot.turnRight()   # face the parent
    robot.move()                           # step onto it
    robot.turnRight(); robot.turnRight()   # face d again
```

The last two turns matter. After `go_back` the robot is on the parent cell facing exactly
the direction the parent's loop expects. That leads to the second ingredient: **keeping the
physical heading equal to the heading the code believes in**.

Inside `dfs(r, c, d)` (robot on `(r, c)` facing `d`), loop `k = 0, 1, 2, 3`:

- The direction being tried is `nd = (d + k) % 4`, and the robot is physically facing it.
- If the cell ahead is not in `visited` and `move()` returns True, recurse with
  `dfs(nr, nc, nd)` and then `go_back()`. The child, by the same rule, hands the robot back
  facing `nd`, and `go_back` keeps it facing `nd`.
- Either way, call `turnRight()` so the robot now faces `(d + k + 1) % 4`.

After four iterations the robot has turned right four times, a full circle, so it faces
`d` again. That is the contract each call keeps: **it returns the robot to the same cell
with the same heading it was given**. The caller can then do its own `go_back` and turn
without ever asking the robot where it is.

Two small but real details:

- Check `visited` **before** calling `move()`. If you move first, you have walked into an
  already cleaned cell and must walk back out, wasting two moves and four turns.
- A wall is never added to `visited`. A blocked cell might be probed from several
  neighbours, each costing one failed `move()`, which is cheap and keeps the code simple.

Now each cell is entered once (the visited set guarantees it) and each tree edge is walked
twice, once forward and once by `go_back`. The number of moves is `2 * (N - 1)` for `N`
cells. The corridor of 10 cells costs exactly 18 moves.

## Watch it work

Relative coordinates: start A = (0,0). The other cells are B = (-1,0), C = (-1,-1),
D = (0,1). The robot faces `U R D L` for headings 0 to 3. `*` marks cleaned cells, `@` the
robot, `x` a pruned branch (wall, blocked move, or already visited).

```text
Frame 1   dfs(A, U): clean A; k=0 try U: (-1,0) unvisited,
          move() -> True, enter B facing U
    room     . @ #        stack: A
             # * .        visited {A, B}
```
The first try succeeds; the robot is one cell up and the recursion is one level deeper.

```text
Frame 2   dfs(B, U): clean B
          U: move() False (wall)      x   turnRight -> R
          R: move() False (blocked)   x   turnRight -> D
          D: A is visited, no move    x   turnRight -> L
          L: C unvisited, move() True -> enter C facing L
    room     @ * #        stack: A B
             # * .
```
Two failed moves and one skipped visited cell, then the left branch opens.

```text
Frame 3   dfs(C, L): clean C; L x, U x, R (B visited) x,
          D x; four turnRight -> facing L again
          go_back: R R (face R), move -> B, R R (face L)
    room     * @ #        stack: A B
             # * .        robot on B facing L
```
C is a dead end; the constant-size `go_back` returns the robot to B facing the way B's loop
left it.

```text
Frame 4   back in dfs(B): after k=3, turnRight -> U
          (B's original heading). dfs(B) returns.
          go_back: R R, move -> A, R R -> facing U
    room     * * #        stack: A
             # @ .        robot on A facing U
```
B kept its contract: it handed the robot back on A facing U, exactly as it received it.

```text
Frame 5   dfs(A): turnRight -> R; k=1 try R: D unvisited,
          move() True. dfs(D, R): clean D; R x, D x,
          L (A visited) x, U x; heading back to R.
          go_back -> on A facing R
    room     * * #        stack: A
             # @ *        all 4 cells cleaned
```
The right branch is a one-cell dead end; D's four tries end where they started.

```text
Frame 6   dfs(A): turnRight -> D: move() False   x
                  turnRight -> L: move() False   x
                  turnRight -> U   (heading restored)
    totals: 4 cleans, 6 successful moves (3 out, 3 back),
            10 failed moves, 28 turnRight calls
```
The root finishes its four directions and returns; every reachable cell is clean.

Across all frames, each `dfs` call returned the robot to its own cell with the heading it
was called with, and the cells on the recursion stack were exactly the path from the start
to the robot.

## Why it is correct

**Position invariant.** At every moment, `(r, c)` in the running call is the robot's true
position relative to the start, and `d` plus the number of `turnRight` calls made so far in
the loop is its true heading. Forward moves change `(r, c)` by the heading's delta only
when `move()` returned True; turns change only the heading. So relative coordinates never
drift.

**Return contract.** `dfs(r, c, d)` ends with the robot on `(r, c)` facing `d`. Proof by
induction on the depth: each child call honours the contract, so after the child, the robot
is on the child cell facing `nd`; `go_back` turns 180, steps onto `(r, c)` (it is directly
behind), turns 180, ending on `(r, c)` facing `nd`. The four `turnRight` calls add up to a
full turn, so the loop ends facing `d`.

**Coverage.** This is DFS on the graph of open cells, with an edge between orthogonal
neighbours. Every reachable cell has a path from the start; by the usual DFS argument, each
unvisited neighbour of a visited cell is tried, so every reachable cell is entered and
cleaned. The visited set makes each cell entered at most once.

## Cost

- **Time `O(N)` robot commands** for `N` reachable cells: each cell is entered once and its
  loop costs at most 4 turns and 4 move attempts, plus `go_back` (4 turns, 1 move).
- **Space `O(N)`** for the visited set and recursion depth (a corridor is `N` deep).
- The retrace-the-path version is `O(N^2)` moves in the worst case.

## Variations you will meet

- **No visited set allowed (constant memory).** You would need wall-following or a
  pledge-style algorithm, and you lose the guarantee for rooms with interior obstacles;
  interviewers rarely go here, but it shows why the visited set is essential.
- **Iterative version.** Replace recursion with an explicit stack of `(r, c, d, k)` frames;
  the `go_back` call happens when a frame is popped.
- **Unknown grid, shortest path to a target (LeetCode 1810, Minimum Path Cost in a Hidden
  Grid).** First run this exact exploration to map the room, then BFS or Dijkstra on the
  map you built.
- **Rooms and Islands problems (Number of Islands, Walls and Gates).** The same traversal
  with the map visible: backtracking is free there because no body has to walk back.

## What to carry forward

When undo is not free, design the undo: here, the parent is always directly behind you, and
each call promises to return the robot exactly as it found it.

That closes the chapter, and you now hold the whole toolkit. You can grow any choice tree
with **choose, explore, unchoose**, and you can recognise its three standard shapes:
subsets (include or skip), permutations (pick an unused item) and combinations (pick from
an index onward). You can deduplicate by sorting and skipping equal siblings. You can prune
at the node rather than the leaf: a letter mismatch, an owed-cell counter, column and
diagonal sets, bitmasks with the most constrained cell first, deletion budgets computed
before the search, an incrementally carried value with a `last` term, a table of values
that shrinks by one per level. And you can make the undo itself cheap, whether it is a
cleared mark on a grid, an XOR on a mask, or a robot turning around. Faced with a fresh
hard search problem, ask three questions: what is the state, what makes a branch dead as
early as possible, and how do I undo one step?
