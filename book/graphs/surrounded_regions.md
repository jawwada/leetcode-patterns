# Surrounded Regions

*LeetCode 130 · Medium · Pattern: Multi-source reverse BFS/DFS from the boundary · Reading time ~6 min*

## The problem

Given an m x n board of 'X' and 'O', flip to 'X' every region of 'O' cells that is completely surrounded, i.e. that
does not touch the border. Modify the board in place.

```text
Example:
  [["X","X","X","X"],
   ["X","O","O","X"],
   ["X","X","O","X"],
   ["X","O","X","X"]]
  becomes all 'X' except the bottom-row 'O', which touches the
  border and survives.
```

## What the problem is really asking

A board holds `'X'` and `'O'`. Groups of `'O'` connected up/down/left/right form regions. A region is **captured** if
none of its cells lies on the border of the board; capturing flips all its cells to `'X'`. Modify the board in place.

So the output is the same board with some `'O'` regions erased. Which ones? Exactly the regions that do not touch the
edge.

```text
  before                     after
      c0 c1 c2 c3 c4             c0 c1 c2 c3 c4
  r0   X  X  X  X  X         r0   X  X  X  X  X
  r1   X  O  O  X  X         r1   X  X  X  X  X
  r2   X  X  O  X  O         r2   X  X  X  X  O
  r3   X  O  X  O  O         r3   X  X  X  O  O
  r4   X  X  X  X  X         r4   X  X  X  X  X

  region {(1,1),(1,2),(2,2)}: no border cell -> captured
  region {(3,1)}:             no border cell -> captured
  region {(2,4),(3,4),(3,3)}: (2,4) on border -> survives
```

This is the previous problem with a twist: you must not destroy the escaping cells, because they stay `'O'` in the
answer. You also cannot flip captured cells while you are still deciding, because the deciding walks through `'O'`s.

## Do it by hand first

On paper you would do what you did for enclaves: walk the rim, and wherever the rim has an `'O'`, put a tick on that
whole region ("safe"). Then sweep the board: every `'O'` without a tick becomes `'X'`, and ticks are erased.

```text
  rim scan finds O at (2,4) and (3,4): tick them
  spread ticks through connected O: (3,3) gets a tick
      X X X X X
      X O O X X        unticked O: (1,1) (1,2) (2,2) (3,1)
      X X O X O'       -> flip to X
      X O X O' O'      ticked O' -> stay O
      X X X X X
```

The tick is a third state, neither `'X'` nor plain `'O'`. Your hand needed three colours, not two. That is the seed of
the sentinel letter.

## The first honest attempt

For each `'O'`, flood its region with a private visited set, check whether any cell is on the border, and flip the
region if not.

```text
  captured region {(1,1),(1,2),(2,2)}
  from (1,1): flood 3 cells, no border -> flip all 3
  (1,2), (2,2) are X now: skipped. fine.

  surviving region {(3,3),(2,4),(3,4)} is never flipped
  from (2,4): flood 3 cells, border -> keep
  from (3,3): flood the same 3 cells again -> keep
  from (3,4): flood the same 3 cells again -> keep
              3 cells x 3 floods = 9 steps for 3 cells
```

Captured regions are flooded once and then disappear, but a safe region of k cells stays `'O'` and is flooded from
every one of its cells: k^2. A board that is nearly all `'O'` and touches the border costs O((m*n)^2). The waste is
deciding "is this region safe?" again for every cell of a region whose answer never changes.

## The turning point

**Claim: an `'O'` survives exactly when it is connected to a border `'O'`, so one flood started from all border `'O'`s
at once finds every survivor, and everything else is captured.**

As with enclaves, connectivity is symmetric: "my region contains a border cell" is the same as "a border `'O'` can reach
me". Do not look for what is surrounded; look for what is not.

The new difficulty is marking. The flood needs a visited mark, and it must be different from both letters:

- If you mark survivors as `'X'`, you lose them; they must come back as `'O'`.
- If you leave them as `'O'`, you cannot tell them apart from captured cells at the end, and the flood revisits them.

So mark survivors with a temporary third letter, `'S'`. The flood then only enters cells that are still `'O'`, so `'S'`
doubles as the visited mark. After the flood, one sweep resolves all three states:

```text
  'S' -> 'O'    survivor, restore
  'O' -> 'X'    never reached by the border: captured
  'X' -> 'X'    unchanged
```

The solution uses BFS (a deque) for the flood. DFS would mark the same cells; BFS is used simply because the order does
not matter and a queue keeps the frontier small on wide boards. All border `'O'`s are marked and enqueued before the
loop starts: that is the multi-source seed.

## Watch it work

Board as above. Queue front on the left. Neighbour order: down, up, right, left.

```text
Frame 1  seed: border cells that are O -> mark S, enqueue
      c0 c1 c2 c3 c4
  r0   X  X  X  X  X
  r1   X  O  O  X  X     queue: [(2,4), (3,4)]
  r2   X  X  O  X  S
  r3   X  O  X  O  S
  r4   X  X  X  X  X
```

Only column 4 has border `'O'`s. The inner region and (3,1) are not seeds.

```text
Frame 2  pop (2,4): down (3,4) is S, up X, right OOB,
         left (2,3) X -> nothing new
      c0 c1 c2 c3 c4
  r0   X  X  X  X  X
  r1   X  O  O  X  X     queue: [(3,4)]
  r2   X  X  O  X  S
  r3   X  O  X  O  S
  r4   X  X  X  X  X
```

(3,4) is already `'S'`, so it is not enqueued twice.

```text
Frame 3  pop (3,4): left (3,3) is O -> mark S, enqueue
      c0 c1 c2 c3 c4
  r0   X  X  X  X  X
  r1   X  O  O  X  X     queue: [(3,3)]
  r2   X  X  O  X  S
  r3   X  O  X  S  S
  r4   X  X  X  X  X
```

The safe region grows inward by one cell.

```text
Frame 4  pop (3,3): down X, up (2,3) X, right S,
         left (3,2) X -> nothing. queue empty
      c0 c1 c2 c3 c4
  r0   X  X  X  X  X
  r1   X  O  O  X  X     queue: []
  r2   X  X  O  X  S     remaining O: never reached
  r3   X  O  X  S  S
  r4   X  X  X  X  X
```

The flood is done. Every `'O'` left is unreachable from the border.

```text
Frame 5  final sweep: O -> X, S -> O
      c0 c1 c2 c3 c4
  r0   X  X  X  X  X
  r1   X  X  X  X  X
  r2   X  X  X  X  O
  r3   X  X  X  O  O
  r4   X  X  X  X  X
```

Captured regions are flipped and survivors restored, in one pass.

Throughout the flood, `'S'` cells are exactly the cells known to be connected to the border, and the queue holds `'S'`
cells whose neighbours have not been examined yet.

## Why it is correct

*Every `'S'` survives*: seeds are border `'O'`s. A cell becomes `'S'` only as an `'O'` neighbour of an `'S'` cell. By
induction each `'S'` cell is joined to a border `'O'` by `'O'` cells, so its region touches the border.

*Every survivor becomes `'S'`*: take an `'O'` whose region touches the border at b. b was seeded. Along a path of `'O'`
cells from b to it, each cell is a neighbour of the previous one; when the previous one was popped, this one was still
`'O'` (then marked) or already `'S'`. So the whole path, including our cell, ends as `'S'`.

So after the flood, `'S'` is exactly the set of survivors, and the sweep turns survivors back into `'O'` and every
other `'O'` into `'X'`. That is the definition of the answer.

## Cost

- **Time O(m*n).** The seed scan and the final sweep read every cell once; each cell is enqueued at most once.
- **Space O(m*n)** for the queue in the worst case (a board of all `'O'`); the sentinel itself is free because it lives
  in the board.

## Variations you will meet

- **Union-find version.** Create one extra node "border". Union every border `'O'` with it, and every `'O'` with its
  `'O'` neighbours. An `'O'` is captured iff `find(cell) != find(border)`. Same answer; the extra node is the
  union-find form of the multi-source seed.
- **Not allowed to modify cells until the end** (e.g. immutable input). Use a separate `safe` boolean grid instead of
  `'S'`; same algorithm.
- **Number of Enclaves** (previous problem) is the counting version; **Number of Closed Islands** counts captured
  regions rather than flipping them.
- **Recursive DFS from each border cell.** Works, but on a 200 x 200 board of `'O'` the recursion depth reaches 40,000.
  Use an explicit stack or the queue.

## What to carry forward

When the result must keep the reachable cells, mark them with a temporary third value during the flood and resolve all
three states in a final sweep. The next problem runs two such border floods, one per ocean, with a direction rule (you
may only climb), and keeps the cells both floods reach.
