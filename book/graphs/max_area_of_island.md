# Max Area of Island

*LeetCode 695 · Medium · Pattern: Grid flood fill (DFS/BFS) · Reading time ~6 min*

## What the problem is really asking

A binary grid again: `1` is land, `0` water, and land cells touching up, down, left or right form an island. The area
of an island is how many cells it has. Return the largest area, or 0 if there is no land.

So we need, for every connected component, its **size**, and then the maximum. The answer is one integer.

```text
      c0 c1 c2 c3
  r0   1  1  0  0       island A: (0,0) (0,1) (1,0)   area 3
  r1   1  0  0  1       island B: (1,3) (2,3)
  r2   0  0  1  1                 (2,2) (3,2)         area 4
  r3   0  0  1  0       answer: 4
```

Compared with the previous problem, the hard part is no longer "don't count an island twice"; it is "count every cell
of an island exactly once", including cells that two different neighbours both try to reach.

## Do it by hand first

You would do what you did for counting islands: scan, and when you hit uncoloured land, colour the whole island. This
time, as you colour each cell, you tick a tally. When the island is done, you compare the tally with the best so far
and write the larger one in the margin.

```text
  island A: colour (0,0) tick, (1,0) tick, (0,1) tick  = 3
            margin: best = 3
  island B: colour (1,3) (2,3) (2,2) (3,2), 4 ticks    = 4
            margin: best = 4
```

Your hand kept the visited colouring (shared across the whole scan), a running tally for the current island, and one
number in the margin. That is the entire state of the algorithm.

## The first honest attempt

For every land cell, run a DFS with its own private visited set and measure the size of what it reaches. Take the
maximum over all starts.

```text
  island B (4 cells) measured from each of its cells:
  from (1,3): (1,3) (2,3) (2,2) (3,2)   -> 4
  from (2,3): (2,3) (1,3) (2,2) (3,2)   -> 4
  from (2,2): (2,2) (3,2) (2,3) (1,3)   -> 4
  from (3,2): (3,2) (2,2) (2,3) (1,3)   -> 4
              the same four cells walked four times
```

Correct, and O(k^2) for an island of size k, so O((m*n)^2) for a grid that is all land. The repeated work is visible:
the area is a property of the *island*, not of the cell you start from, yet it is recomputed once per cell.

## The turning point

**Claim: an island's area is the same no matter which of its cells you measure from, so measure it once, from the
first of its cells the scan reaches, and mark every cell so no other start re-measures it.**

That is the Number of Islands structure with one change: the flood is a function that returns a number. Shared marks
(sink each `1` to `0`) mean every flood covers only cells nobody has counted, every island is measured exactly once,
and the total work is O(m*n).

The subtle part is *where* you add 1 to the tally. Suppose we sank and counted on **pop**, and pushed any neighbour
still equal to `1`. A 2 x 2 block of land breaks it:

```text
  sink+count on pop, push any neighbour still 1
      c0 c1
  r0   1  1      pop (0,0): count 1, push (1,0),(0,1)
  r1   1  1      pop (0,1): count 2, push (1,1)
                 pop (1,1): count 3, (1,0) still 1: push
                 stack: [(1,0), (1,0)]  <- twice
                 pop (1,0): count 4; pop (1,0): count 5
                 area 5 for a 4-cell island
```

The fix is the same habit as before: **claim a cell at push time**. Sink it and add 1 to the area the moment you push
it. A sunk cell fails the "still 1" test, so it is never pushed again, and the tally counts each cell exactly once.

The invariant for one flood is then: `area` equals the number of cells sunk by this flood so far.

## Watch it work

`x` = sunk cell. Stack top on the right. Neighbour order is down, up, right, left.

```text
Frame 1  scan reaches (0,0)=1: sink, area=1, push
      c0 c1 c2 c3
  r0   x  1  0  0       stack: [(0,0)]
  r1   1  0  0  1       area: 1   best: 0
  r2   0  0  1  1
  r3   0  0  1  0
```

The flood for island A starts with its first cell already counted.

```text
Frame 2  pop (0,0): down (1,0)=1 sink area=2 push;
         right (0,1)=1 sink area=3 push
      c0 c1 c2 c3
  r0   x  x  0  0       stack: [(1,0), (0,1)]
  r1   x  0  0  1       area: 3   best: 0
  r2   0  0  1  1
  r3   0  0  1  0
```

Both neighbours are claimed (and counted) before either is popped.

```text
Frame 3  pop (0,1): nothing. pop (1,0): nothing. stack empty
         flood returns 3; best = max(0, 3) = 3
      c0 c1 c2 c3
  r0   x  x  0  0       stack: []
  r1   x  0  0  1       best: 3
  r2   0  0  1  1
  r3   0  0  1  0
```

Island A is done; the scan resumes and skips the sunk cells (0,1) and (1,0).

```text
Frame 4  scan reaches (1,3)=1: sink, area=1, push
         pop (1,3): down (2,3) sink area=2 push
         pop (2,3): left (2,2) sink area=3 push
      c0 c1 c2 c3
  r0   x  x  0  0       stack: [(2,2)]
  r1   x  0  0  x       area: 3   best: 3
  r2   0  0  x  x
  r3   0  0  1  0
```

(2,3) also looks up at (1,3), but it is sunk, so nothing is pushed twice.

```text
Frame 5  pop (2,2): down (3,2) sink area=4 push
         pop (3,2): nothing. flood returns 4
         best = max(3, 4) = 4; scan finds no more 1s
      c0 c1 c2 c3
  r0   x  x  0  0       stack: []
  r1   x  0  0  x       best: 4
  r2   0  0  x  x       answer: 4
  r3   0  0  x  0
```

The second island wins.

In every frame, `area` equals the number of `x` cells belonging to the current island, and `best` is the largest
finished island's `x` count.

## Why it is correct

Within one flood: a cell is counted exactly when it is sunk, and it is sunk exactly once (sunk cells are never pushed).
The flood sinks precisely the island of its start cell (flood fill correctness). So the returned area is that island's
size.

Across the scan: as in Number of Islands, each island is reached first by the scan at an unsunk cell, starts one flood
there, and is entirely sunk by it; no other cell of it starts a flood. So each island's size is computed exactly once
and compared with `best`. `best` begins at 0 and only grows, so an all-water grid correctly returns 0.

## Cost

- **Time O(m*n).** Every cell is read by the scan once and pushed at most once.
- **Space O(m*n)** for the stack in the worst case (all land). Using a `visited` grid instead of sinking costs the same.

## Variations you will meet

- **Recursive form.** `area(r, c) = 1 + area(4 neighbours)`, returning 0 for water or out of bounds, with the cell
  sunk *before* recursing. Elegant, but the recursion depth can reach m*n.
- **Making A Large Island** (LeetCode 827). You may flip one `0` to `1`; return the largest possible island. Label each
  island with an id and record its area (this problem, once). Then for each `0`, add 1 plus the areas of the *distinct*
  island ids around it. The "distinct" matters: two neighbours may belong to the same island.
- **Perimeter instead of area** (LeetCode 463). Each land cell contributes 4 minus the number of land neighbours; no
  flood is even needed.
- **Report all island sizes** (sorted, or a histogram). Same scan; append each flood's return value to a list.

## What to carry forward

A flood can return a value; to count cells exactly once, claim each cell when you push it. The next problem keeps the
flood but reverses where it starts: instead of flooding from every unvisited cell, flood from the border and count what
the border could not reach.
