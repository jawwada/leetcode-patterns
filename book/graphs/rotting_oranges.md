# Rotting Oranges
*LeetCode 994 · Medium · Pattern: Multi-source BFS (level = distance) · Reading time ~8 min*

## What the problem is really asking

You have a grid of cells. Some are empty (`0`), some hold a fresh orange (`1`), some hold a
rotten orange (`2`). Every minute, every rotten orange infects the fresh oranges directly
above, below, left and right of it. All infections in one minute happen at the same instant.
How many minutes until no fresh orange is left? If some fresh orange can never be reached,
answer `-1`.

The answer is one number: a time. Behind it sits a distance question. Each fresh orange rots
at the minute equal to its grid distance (through orange-holding cells) from the **closest**
rotten orange it started with. The total time is the **largest** of those distances. So the
question is "how far is the farthest fresh orange from the nearest source of rot?"

```text
        c0 c1 c2          R = rotten   F = fresh   . = empty
  r0  [ R  F  F ]
  r1  [ F  F  . ]         answer: 4 minutes
  r2  [ .  F  F ]         (the orange at r2c2 is last)
```

What makes it awkward: there can be several rotten oranges at the start, all spreading at
once, and the rot cannot jump across empty cells. Two waves can collide, and an orange
walled in by empties is never reached.

## Do it by hand first

Take the grid above. With a pencil, write the minute each orange turns rotten. Start: the
one rotten orange at r0c0 gets a `0`. Look at its neighbours: r0c1 and r1c0 are fresh, so
write `1` on both. Now look only at the cells you just wrote `1` on. Their fresh neighbours
are r0c2 and r1c1: write `2`. From those, only r2c1 is new: `3`. From r2c1, r2c2: `4`.

```text
  minute each orange rots
        c0 c1 c2
  r0  [ 0  1  2 ]
  r1  [ 1  2  . ]       largest number = 4
  r2  [ .  3  4 ]
```

Notice what your eye was doing. At each step you did not rescan the whole grid; you only
looked at **the cells you marked in the previous step**. Your hand kept a short list, "the
oranges that turned rotten last minute", plus a count of how many fresh oranges remained.
That list is the frontier, and it is the seed of the data structure: a queue.

## The first honest attempt

Simulate the clock literally. Each minute, scan every cell of the grid; for each rotten
orange, mark its fresh neighbours as rotten in a **copy** of the grid (the copy keeps the
minute simultaneous, so rot does not travel two cells in one tick). Stop when a minute
changes nothing; then if any fresh orange remains, return `-1`.

Each minute costs `O(m*n)`. How many minutes can there be? Picture a snake of oranges that
winds back and forth across the grid: the rot crawls along it one cell per minute, so there
can be `O(m*n)` minutes. Total `O((m*n)^2)`.

```text
  snake grid, rot enters at top-left
  [ R F F F F ]
  [ . . . . F ]       every minute the scan
  [ F F F F F ]       re-reads all 25 cells,
  [ F . . . . ]       but only ONE cell
  [ F F F F F ]       can actually change
            ^ last orange: minute 16
```

The repeated work is obvious in the drawing. A rotten orange that turned rotten ten minutes
ago gets re-examined every minute even though all its neighbours are already rotten or
empty. Only the oranges that turned rotten in the **previous** minute can infect anyone new.

## The turning point

**Claim: the only oranges that can rot something at minute `t` are the ones that became
rotten at minute `t - 1`.**

Why: an orange that became rotten earlier, at minute `t - 2` or before, already had its
chance to infect its four neighbours in the minute right after it turned. Any neighbour
that was fresh then is rotten now. Nothing about a cell's neighbourhood changes later in a
way that would give an old rotten orange new work.

So keep exactly those oranges in a queue. That is breadth-first search, with one twist:
there is not one starting node but **many**, all the initially rotten oranges, and they all
start at the same time. Put all of them in the queue before the loop begins. Then each
**layer** of the BFS, meaning the batch of cells that were in the queue when the layer
started, is one minute.

Separating layers is the detail that matters here. The loop reads `len(queue)` at the start
of a minute and pops exactly that many cells. Anything those pops add belongs to the next
minute. Without this, you would have no way to know when a minute ends.

Two more pieces finish the design:

- **A fresh counter.** Count fresh oranges once at the start and decrement whenever one
  rots. Then the `-1` check is just `fresh > 0` at the end; no second scan.
- **Overwrite as you go.** Writing `2` into a cell the moment it is enqueued doubles as the
  visited mark. A cell is fresh at most once, so it enters the queue at most once.

The loop runs `while queue and fresh`. Stopping when `fresh` hits zero avoids counting an
extra empty minute after the last orange rots, which is the classic off-by-one here.

## Watch it work

Same grid. `q` is the queue at the start of the minute, `fresh` the count of fresh oranges.
New rot in each frame is shown in lowercase `r`.

```text
Frame 1   setup (minute 0)
  [ R F F ]      q     = [ (0,0) ]
  [ F F . ]      fresh = 6
  [ . F F ]      layer = 0
```
One scan finds the single rotten orange and counts six fresh ones.

```text
Frame 2   pop layer 0 -> minute 1
  [ R r F ]      popped (0,0): rots (1,0), (0,1)
  [ r F . ]      q     = [ (1,0), (0,1) ]
  [ . F F ]      fresh = 4
```
The source infects its two fresh neighbours; they form layer 1.

```text
Frame 3   pop layer 1 -> minute 2
  [ R R r ]      popped (1,0): rots (1,1)
  [ R r . ]      popped (0,1): rots (0,2)
  [ . F F ]      q = [ (1,1), (0,2) ]   fresh = 2
```
(0,1) also touches (1,1), but (1,1) was already marked by (1,0), so it is not added twice.

```text
Frame 4   pop layer 2 -> minute 3
  [ R R R ]      popped (1,1): rots (2,1)
  [ R R . ]      popped (0,2): nothing (right is
  [ . r F ]      off grid, below is empty)
                 q = [ (2,1) ]   fresh = 1
```
The wave narrows to one cell because the empty cell at (1,2) blocks the right side.

```text
Frame 5   pop layer 3 -> minute 4
  [ R R R ]      popped (2,1): rots (2,2)
  [ R R . ]      q = [ (2,2) ]   fresh = 0
  [ . R r ]      loop stops: fresh == 0
```
`fresh` is zero, so the loop exits without popping (2,2); the answer is `minutes = 4`.

Across every frame the queue held cells of exactly one minute, and every cell in it was
marked rotten the moment it entered. The layer number and the minute counter never drifted
apart.

For the `-1` case, take `[[2,1,1],[0,1,1],[1,0,1]]`: the wave rots five oranges in four
minutes, then the queue empties with `fresh = 1`, because the orange at r2c0 is surrounded
by empties and the grid edge.

## Why it is correct

The BFS **layer property**: when layer `k` is popped, every cell in it is at distance exactly
`k` from the nearest initially rotten orange, and every cell at distance `k` is in it.

Before the loop this holds for `k = 0`: the queue is exactly the starting rotten oranges.
Suppose it holds for layer `k`. A fresh cell at distance `k + 1` has some neighbour at
distance `k`, which is in layer `k` and will rot it during this pass. A fresh cell at
distance greater than `k + 1` has no neighbour in layer `k`, so it is not touched. A cell at
distance `k` or less is already rotten, so it is not added again. Hence layer `k + 1` is
exactly the set at distance `k + 1`.

This BFS distance is precisely the minute the real process rots that orange, since the real
process is the same "neighbours of last minute's new rot" rule. The last minute anything
rots is the maximum distance, which is the counter when `fresh` hits zero. If the queue
empties first, the remaining fresh oranges have no path from any source, so `-1` is right.

## Cost

- **Time `O(m*n)`**: one scan to seed, then each cell enters the queue at most once and
  checks four neighbours.
- **Space `O(m*n)`**: the queue can hold a whole layer, which in the worst case is a
  constant fraction of the grid (the grid itself is reused as the visited mark).

## Variations you will meet

- **Return the minute each orange rots, not just the max.** Same BFS; write the layer number
  into a result grid. That is exactly the next problem.
- **Diagonal spread (8 directions).** Only the neighbour list changes; the layer argument is
  identical.
- **Rot needs two rotten neighbours.** Now a cell's rot time depends on the second-nearest
  source, so plain BFS fails; keep a per-cell counter of rotten neighbours and enqueue when
  it reaches two.
- **Different spread speeds per source.** Edges are no longer all one minute apart, so BFS
  layers stop meaning time; this becomes Dijkstra (see Network Delay Time later).

## What to carry forward

Many sources that start at the same instant are one BFS with all of them in the initial
queue; each layer is one tick. The next problem, 01 Matrix, keeps the same wave but asks for
every cell's own distance instead of only the largest one.
