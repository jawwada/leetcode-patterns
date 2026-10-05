# Number of Islands

*LeetCode 200 · Medium · Pattern: Grid flood fill (DFS/BFS) · Reading time ~7 min*

## The problem

Given an m x n grid of '1' (land) and '0' (water), count the islands, where an island is a maximal group of '1' cells
connected horizontally or vertically.

```text
Example: [["1","1","0"],["0","1","0"],["0","0","1"]] has 2
  islands: the L-shape in the top-left and the lone cell at the
  bottom-right.
```

## What the problem is really asking

The grid is a map: `'1'` is land, `'0'` is water. Land cells that touch up, down, left or right belong to the same
island. Count the islands.

In graph words: nodes are land cells, edges join side-by-side land cells, and the question is **how many connected
components** this graph has. The answer is a single integer.

```text
      c0 c1 c2 c3
  r0   1  1  0  0         island A: (0,0) (0,1) (1,1)
  r1   0  1  0  1         island B: (1,3) (2,3)
  r2   1  0  0  1         island C: (2,0)
                          answer: 3
  (2,0) touches (1,1) only diagonally: separate island
```

What makes it more than a flood fill is that nobody tells you where the islands are. You have to discover them, and you
must not count the same island twice just because you stumbled onto it from two of its cells.

## Do it by hand first

Give a child a printed map and a highlighter and ask "how many islands?". They scan from the top-left. On the first bit
of land they say "one", and then, crucially, they colour in the whole island so they will not count it again. They
carry on scanning. Each time the scan finds land that is *not yet coloured*, they say the next number and colour that
island too.

```text
  scan ->  1 1 0 0      "one!" colour it:   # # 0 0
           0 1 0 1                          0 # 0 1
           1 0 0 1                          1 0 0 1
  scan continues past # cells, hits (1,3): "two!" ...
```

The hand kept track of two things: where the scan is, and which land is already coloured. The coloured set is the
visited set; the colouring is a flood fill. The count is the number of times you uncapped the highlighter.

## The first honest attempt

A natural first version: for each land cell, run a fresh DFS that collects the whole island it belongs to, with a
private visited set. To avoid counting an island once per cell, count the cell only if it is the "first" cell of its
island (say, the smallest `(row, col)` in the set the DFS returned).

```text
  island A has 3 cells; the brute force walks it 3 times
  from (0,0): visits (0,0) (0,1) (1,1)  -> min is (0,0), count
  from (0,1): visits (0,1) (0,0) (1,1)  -> min is (0,0), skip
  from (1,1): visits (1,1) (0,1) (0,0)  -> min is (0,0), skip
                    \_____ same walk, three times _____/
```

It is correct. Its cost is the problem: an island of k cells is explored k times, k^2 work. A grid that is one giant
island of m*n cells costs O((m*n)^2). On a 300 x 300 grid that is 8 billion steps. The repeated work is the same island
being re-walked from each of its cells, and the only reason is that the visited sets are private and thrown away.

## The turning point

**Claim: once a flood from any cell of an island finishes, every cell of that island is known; so if the visited marks
are shared across the whole scan, a new flood starts exactly once per island.**

Why it holds: a flood from cell s reaches every cell connected to s and nothing else (that is what flood fill does,
from the previous problem). So after it finishes, the island containing s is fully marked. Later, the scan reaches other
cells of that island; they are marked, so they do not start a flood. The scan eventually reaches some cell of every
island, so every island starts exactly one flood. Hence:

```text
  count = number of floods started
        = number of times the scan finds an unmarked '1'
```

Which structure makes it work? A single visited marker shared by the scan and every flood. The cheapest is the grid
itself: overwrite `'1'` with `'0'` when you first touch a cell ("sink" it). A sunk cell looks like water to both the
scan and later floods, so nothing can re-enter it.

As in Flood Fill, sink on **push**. If you sink on pop, a cell between two already-stacked cells can be pushed twice.
That is harmless for counting islands but wasteful, and in the next problem (which counts cells) it becomes a bug.

Each cell is now entered at most once by any flood, and the scan touches each cell once. Total O(m*n).

## Watch it work

Grid as above. `x` marks a sunk cell (was `'1'`, now `'0'`). The scan visits cells in row order. Stack top on the right.

```text
Frame 1  scan reaches (0,0)='1': count=1, sink, push
      c0 c1 c2 c3
  r0   x  1  0  0       stack: [(0,0)]
  r1   0  1  0  1       count: 1
  r2   1  0  0  1
```

The first unmarked land cell starts the first flood.

```text
Frame 2  pop (0,0): down (1,0)=0; right (0,1)=1 sink+push
         pop (0,1): down (1,1)=1 sink+push
         pop (1,1): all neighbours water. stack empty
      c0 c1 c2 c3
  r0   x  x  0  0       stack: []
  r1   0  x  0  1       count: 1
  r2   1  0  0  1
```

Island A is completely sunk. Note (2,0) was never reached: it touches (1,1) only on a diagonal.

```text
Frame 3  scan moves on: (0,1) (0,2) (0,3) (1,0) (1,1) (1,2)
         are all '0' now -> no new flood
      c0 c1 c2 c3
  r0   x  x  0  0       scan at (1,2)
  r1   0  x  0  1       count: 1
  r2   1  0  0  1
```

The scan passes over (0,1) and (1,1) without counting them. In the brute force, these two cells each re-walked island A.

```text
Frame 4  scan reaches (1,3)='1': count=2, sink, push
         pop (1,3): down (2,3)=1 sink+push
         pop (2,3): nothing new. stack empty
      c0 c1 c2 c3
  r0   x  x  0  0       stack: []
  r1   0  x  0  x       count: 2
  r2   1  0  0  x
```

Island B is found and sunk in one flood.

```text
Frame 5  scan reaches (2,0)='1': count=3, sink, push
         pop (2,0): neighbours water. stack empty
         scan passes (2,1) (2,2) (2,3): all '0'
      c0 c1 c2 c3
  r0   x  x  0  0       stack: []
  r1   0  x  0  x       count: 3
  r2   x  0  0  x       answer: 3
```

A one-cell island is still an island. Scan ends.

Across the frames, the scan pointer only moves forward, and every `'1'` it has passed has been sunk. So whenever it
meets a `'1'`, that cell cannot belong to any island seen before: if it did, the earlier flood would have sunk it.

## Why it is correct

Two facts, each from the previous problem's argument:

1. A flood started at s sinks exactly the island containing s. (It reaches every connected land cell and nothing else.)
2. A sunk cell never starts a flood and is never pushed again.

Now count. Each island I contains at least one cell, so the scan reaches its first cell in row order at some moment. At
that moment, no cell of I is sunk yet: a cell of I could only be sunk by a flood started inside I (floods never cross
water), and no cell of I was scanned earlier. So a flood starts there, count goes up by one, and fact 1 sinks all of I.
Afterwards fact 2 guarantees no other cell of I triggers a count. So each island adds exactly one, and the final count
is the number of islands.

## Cost

- **Time O(m*n).** The scan reads every cell once; every land cell is pushed and popped at most once with four
  neighbour checks.
- **Space O(m*n)** in the worst case for the stack (a grid that is all land). A BFS queue instead of a stack has a
  smaller worst-case peak, O(min(m, n)) for a full grid, but the same O(m*n) bound in general.

If you may not modify the input, copy it or use a `visited` boolean grid; same bounds.

## Variations you will meet

- **Max Area of Island** (next problem). Same scan and floods, but each flood returns the number of cells it sank.
- **Union-find instead of flood.** Treat each land cell as a node, union it with land to its right and below, and count
  roots. Same answer, and it extends to **Number of Islands II**, where land appears one cell at a time and you must
  report the count after each addition. Re-flooding after each addition would be O(m*n) per update; union-find makes
  each update almost O(1).
- **Count distinct island shapes** (LeetCode 694). Record each flood's path relative to its start cell, including
  "backtrack" markers, and put the signatures in a set.
- **Islands that do not touch the border** (Number of Closed Islands, Number of Enclaves). Either check during the
  flood whether it touched the edge, or first sink every island that touches the border and then count. The second
  version is the subject of problem 4.

## What to carry forward

The number of components is the number of floods a full scan has to launch, as long as every flood shares one visited
mark. The next problem keeps the scan and the floods exactly as they are, but makes each flood report how many cells it
swallowed.
