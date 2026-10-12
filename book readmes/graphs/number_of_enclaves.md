# Number of Enclaves

*LeetCode 1020 · Medium · Pattern: Multi-source reverse BFS/DFS from the boundary · Reading time ~6 min*

## The problem

In an m x n grid, 1 is land and 0 is sea. A move goes to a 4-adjacent land cell or off the edge of the grid. Return
the number of land cells from which you cannot walk off the grid.

```text
Example: [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]] -> 3; the
  land at (1,0) is on the border, the other three cells are
  enclosed.
```

## What the problem is really asking

In a grid of `1` (land) and `0` (sea), you may walk from a land cell to an adjacent land cell, or step off the edge of
the grid if you are standing on a border cell. Count the land **cells** from which you can never leave the grid.

A land cell can leave exactly when its island touches the border somewhere. So the answer is the total number of cells
in islands that do not touch the border. It is a count of cells, not of islands.

```text
      c0 c1 c2 c3 c4
  r0   0  0  0  0  0
  r1   1  1  0  1  0     island A: (1,0) (1,1) (2,1)
  r2   0  1  0  1  0       (1,0) is on the border -> escapes
  r3   0  0  1  1  0     island B: (1,3) (2,3) (3,3) (3,2)
  r4   0  0  0  0  0       no border cell -> trapped
                         answer: 4 cells
```

The trap is that "can this cell escape?" sounds like a question about one cell, and invites one search per cell.

## Do it by hand first

Look at island A on paper. You do not trace a route from (2,1) to the edge and then another from (1,1). You see that the
island has a cell on the rim, so the whole island is free. Then you look at B, see no rim cell, and count its four
cells.

A faster way with a pen: run your finger around the frame of the grid. Wherever the frame touches land, scribble out
that whole island. Then count the land still visible.

```text
  finger along the rim finds land at (1,0)
  scribble out its island:     0 0 0 0 0
                               x x 0 1 0
                               0 x 0 1 0
                               0 0 1 1 0
                               0 0 0 0 0
  visible land left: 4
```

Your hand kept a list of "rim land to start scribbling from", plus the scribbles themselves as the visited marks.

## The first honest attempt

For each land cell, run a DFS with a private visited set and stop as soon as some step would leave the grid. Count the
cells whose search never escapes.

```text
  searches for island B, each one walks all of B
  from (1,3): (1,3) (2,3) (3,3) (3,2)  trapped
  from (2,3): (2,3) (3,3) (3,2) (1,3)  trapped
  from (3,3): ...                     trapped
  from (3,2): ...                     trapped
  every cell of B re-proves the same fact
```

An island of k cells costs up to k^2, so O((m*n)^2) for a big trapped island. The waste is that every cell of an
island shares one answer, but each cell computes it again.

## The turning point

**Claim: a land cell can reach the border if and only if the border can reach it, so one flood started from every
border land cell at once marks exactly the cells that escape.**

Walking on land is undirected: if there is a land path from cell c to border cell b, the same path read backwards goes
from b to c. So "which cells can reach some border cell?" is the same set as "which cells are reachable from some border
cell?". The second question needs one traversal with many starting points, not one traversal per cell.

This is a **multi-source** flood. Put every border land cell on the stack at the beginning. They behave like one
imaginary "outside" node joined to all of them. Sink everything the flood reaches. What is still `1` afterwards is
precisely the land the outside cannot reach: the enclaves. Count them with one sum.

The solution writes the flood in a slightly different style from the previous problems: it pushes all four neighbours
unconditionally and does the check when it pops (in bounds? still land?). That is the "validate on pop" style. It is
safe here because checking and sinking happen together at pop time, so a duplicate copy of a cell is popped, found
already sunk, and skipped. Nothing is counted during the flood, so duplicates cannot inflate any tally. It costs a few
extra stack entries (at most four per sunk cell), still O(m*n).

## Watch it work

Grid as above. `x` = sunk. Stack top on the right; `(1,-1)` is an out-of-bounds coordinate pushed unconditionally.

```text
Frame 1  seed: every border cell that is land
      c0 c1 c2 c3 c4
  r0   0  0  0  0  0
  r1   1  1  0  1  0     stack: [(1,0)]
  r2   0  1  0  1  0
  r3   0  0  1  1  0
  r4   0  0  0  0  0
```

Only (1,0) is land on the rim. B has no rim cell, so it is never seeded.

```text
Frame 2  pop (1,0): land -> sink; push up, down, left, right
      c0 c1 c2 c3 c4
  r0   0  0  0  0  0     stack: [(0,0), (2,0),
  r1   x  1  0  1  0             (1,-1), (1,1)]
  r2   0  1  0  1  0
  r3   0  0  1  1  0
  r4   0  0  0  0  0
```

All four neighbours go on the stack without checks.

```text
Frame 3  pop (1,1): land -> sink; push its 4 neighbours
      c0 c1 c2 c3 c4
  r0   0  0  0  0  0     stack: [(0,0), (2,0), (1,-1),
  r1   x  x  0  1  0             (0,1), (2,1), (1,0),
  r2   0  1  0  1  0             (1,2)]
  r3   0  0  1  1  0
  r4   0  0  0  0  0
```

(1,0) is pushed again; it is already sunk, so it will be skipped.

```text
Frame 4  pop (1,2): sea, skip. pop (1,0): sunk, skip.
         pop (2,1): land -> sink; push 4 neighbours
      c0 c1 c2 c3 c4
  r0   0  0  0  0  0     stack: [(0,0), (2,0), (1,-1),
  r1   x  x  0  1  0             (0,1), (1,1), (3,1),
  r2   0  x  0  1  0             (2,0), (2,2)]
  r3   0  0  1  1  0
  r4   0  0  0  0  0
```

Island A is fully sunk now; the stack holds only sea, sunk cells and an out-of-bounds pair.

```text
Frame 5  pop the 8 remaining entries: each is sea, sunk,
         or out of bounds -> skip. stack empty
         count remaining 1s
      c0 c1 c2 c3 c4
  r0   0  0  0  0  0
  r1   x  x  0  1  0     1s left: (1,3) (2,3)
  r2   0  x  0  1  0              (3,3) (3,2)
  r3   0  0  1  1  0     answer: 4
  r4   0  0  0  0  0
```

The trapped island was never touched by the flood.

Invariant through the frames: every sunk cell is connected to the border, and every land cell connected to a sunk cell
is either sunk or on the stack.

## Why it is correct

*Every sunk cell escapes*: a cell is sunk only if it was popped as land, and it was pushed by a sunk neighbour or seeded
as a border cell. Induction from the seeds gives a land path from the border to it.

*Every escaping cell is sunk*: take an escaping cell c and a land path from some border land cell b to c. b was seeded.
Walking along the path, each cell is a neighbour of the previous one; when the previous one was sunk, it pushed its
neighbours, so this one was popped later and, being land, sunk. So c is sunk.

Therefore the land left at the end is exactly the land that cannot escape, and the sum counts it.

## Cost

- **Time O(m*n).** Each cell is sunk at most once; each sinking pushes 4 entries; each pop is O(1).
- **Space O(m*n)** for the stack: up to the border seeds plus 4 entries per sunk cell.

## Variations you will meet

- **Number of Closed Islands** (LeetCode 1254). Same border flood, but then count *islands* left (a second scan with a
  flood per island, as in Number of Islands) instead of cells. Note the colours are swapped there: `0` is land.
- **Surrounded Regions** (next problem). Same border flood, but instead of counting the trapped cells you rewrite them,
  and the escaping cells must be restored, not destroyed.
- **Check during the flood instead.** Flood each island from the scan and record "touched the border?" and its size;
  add the size if it did not. Also O(m*n), but you must finish the flood even after seeing the border, or leftover
  cells will start a second flood and be miscounted.
- **BFS instead of DFS.** A deque seeded with the border cells gives the same set. With BFS you would additionally learn
  each cell's distance to the nearest border exit, which problems 7 to 9 build on.

## What to carry forward

When the question is "can this reach the boundary?", flip it to "what can the boundary reach?" and run one flood seeded
from the entire boundary. The next problem runs the same border flood but has to keep the escaping cells intact,
so it marks them with a temporary sentinel and rewrites the board at the end.
