# Sliding Puzzle
*LeetCode 773 · Hard · Pattern: BFS on implicit graph (board-state strings) · Reading time ~11 min*

## The problem

A 2x3 board holds tiles 1..5 and one blank 0. A move swaps the blank with a 4-directionally adjacent tile. Return the
minimum number of moves to reach [[1,2,3],[4,5,0]], or -1 if it is unsolvable.

```text
Example: [[1,2,3],[4,0,5]] -> 1; [[4,1,2],[5,0,3]] -> 5;
  [[1,2,3],[5,4,0]] -> -1.
```

## What the problem is really asking

A 2-by-3 tray holds tiles `1` to `5` and one empty slot, written `0`. A move slides a tile that
is next to the empty slot (up, down, left or right) into it; equivalently, it swaps `0` with an
adjacent tile. What is the fewest moves to reach

```text
  goal          [ 1 2 3 ]
                [ 4 5 0 ]
```

and if the goal is unreachable, return `-1`.

The answer is a shortest distance, but not on the tray. The tray is just six cells. The graph
lives one level up: **each node is a whole arrangement of the tray**, and each edge is one
move. Starting from one arrangement, we want the BFS distance to another.

```text
  a node                          its edges (blank at
  [ 4 1 2 ]                       the centre bottom):
  [ 5 0 3 ]
                  /                 |                \
     [ 4 0 2 ]           [ 4 1 2 ]           [ 4 1 2 ]
     [ 5 1 3 ]           [ 0 5 3 ]           [ 5 3 0 ]
     (1 slid down)       (5 slid right)      (3 slid left)
```

What makes this hard: there is no adjacency list anywhere, the nodes are not integers or
grid cells, and you must decide what a node **is** in code (something hashable and cheap),
how to list a node's neighbours, and how big the graph is. Those three decisions are the
whole problem; once they are made, BFS is the same loop as Word Ladder.

## Do it by hand first

Take `[[4,1,2],[5,0,3]]`. Try to solve it with your fingers. The `1`, `2`, `3` are each one
step from home, and the blank is in the middle of the bottom row. One natural plan: slide the
`5` right, then the `4` down, then move `1`, `2`, `3` round in turn.

```text
  start      5 right    4 down     1 left     2 left     3 up
  4 1 2      4 1 2      0 1 2      1 0 2      1 2 0      1 2 3
  5 0 3      0 5 3      4 5 3      4 5 3      4 5 3      4 5 0
             move 1     move 2     move 3     move 4     move 5
```

Five moves. But why is five the minimum? Your hand cannot prove that; it found **a** path. To
be sure, you would have to try every sequence of one move, then every sequence of two, and so
on, and avoid re-trying arrangements you have already seen. Your hand was implicitly
remembering **which arrangements it had already been in**, and that is what the algorithm
must remember explicitly: a set of seen boards, plus a queue of boards to expand, one ring
of distance at a time.

## The first honest attempt

There are only `6! = 720` arrangements of `0..5`. A tempting first program lists all 720
boards and runs BFS where, to find the neighbours of a board, it compares it against **every**
arrangement, keeping those that differ by one legal swap of the blank.

```text
  expanding "412503" (blank at index 4):
    vs "012345": 4 positions differ    no
    vs "012354": 4 differ              no
    vs "012435": 4 differ              no
    ... 716 more comparisons ...
    real neighbours: "402513" "412053" "412530"

  719 comparisons to find at most 3 neighbours,
  repeated for every board the BFS expands
```

That is `O(S^2 * 6)` with `S = 720`. It runs, but the waste is plain: the blank's position
already tells you every legal move. A move swaps the blank with one of its 2 or 3 grid
neighbours, so the neighbours can be **generated**, not searched for.

## The turning point

**Claim: flatten the board into a 6-character string, and the neighbours of a state are
exactly the strings obtained by swapping `'0'` with each index listed in a fixed 6-entry
adjacency table.**

Three decisions make it work.

**1. State encoding.** Read the tray row by row into a string: `[[4,1,2],[5,0,3]]` becomes
`"412503"`. A string is hashable, so it can go into a set; a list of lists cannot. Equal boards
give equal strings, different boards give different strings.

**2. Neighbour function.** In the flattened string, which indices touch which? Draw it:

```text
  tray positions        flattened index adjacency
  [ 0  1  2 ]           0: 1 3        3: 0 4
  [ 3  4  5 ]           1: 0 2 4      4: 1 3 5
                        2: 1 5        5: 2 4
  2 and 3 are NOT adjacent: they are
  consecutive in the string but on
  different rows (end of row 0, start of row 1)
```

Index `i` touches `i - 1` and `i + 1` only within the same row, and `i +- 3` across rows. The
table is computed once by hand and never changes. For any state, find `i = s.index('0')`;
for each `j` in the table at `i`, swap characters `i` and `j` to get a neighbour. Two or three
neighbours, each built in `O(6)`.

**3. Size.** At most 720 strings. That bound is what tells you exhaustive BFS is fine. In
fact only half of them, 360, are reachable from any given start, a parity fact we come back to
below.

Then the BFS is the familiar loop: queue of `(state, moves)` seeded with `(start, 0)`, a `seen`
set marked on push, return `moves` when the goal string `"123450"` is popped, `-1` if the
queue empties.

## Watch it work

Start `"412503"`. Each frame shows the layer just completed: the queue holds exactly the
boards at that distance. `seen` counts every string ever pushed.

```text
Frame 1   setup, layer 0
  q    = [ 412503 ]           4 1 2
  seen = 1                    5 0 3
                              blank at index 4 -> 1 3 5
```
One board, distance 0, already in `seen`.

```text
Frame 2   layer 1 (3 boards)
  pop 412503: swap 4<->1, 4<->3, 4<->5
  q    = [ 402513  412053  412530 ]
  seen = 4
```
The centre-bottom blank has three neighbours, so the first ring has three boards.

```text
Frame 3   layer 2 (4 boards)
  402513 -> 042513 420513   (412503 seen)
  412053 -> 012453          (412503 seen)
  412530 -> 410532          (412503 seen)
  q    = [ 042513 420513 012453 410532 ]
  seen = 8
```
Every board's move back to the start is already in `seen`, so it is not pushed.

```text
Frame 4   layer 3 (4 boards)
  042513 -> 542013     420513 -> 423510
  012453 -> 102453     410532 -> 401532
  q    = [ 542013 423510 102453 401532 ]
  seen = 12
```
Each board has only one new neighbour here; the other move undoes the last one.

```text
Frame 5   layer 4 (6 boards)
  542013 -> 542103     423510 -> 423501
  102453 -> 120453 152403
  401532 -> 041532 431502
  q    = [ 542103 423501 120453 152403
           041532 431502 ]
  seen = 18
```
`102453` (blank in the top-middle) has three neighbours, two new, so the ring widens.

```text
Frame 6   layer 5: goal pushed, then popped
  542103 -> 502143 542130
  423501 -> 403521 423051
  120453 -> 123450   <- goal enters the queue
  ... the rest of layer 4 adds 5 more
  pop 502143 542130 403521 423051 (6 pushes)
  pop 123450: == "123450" -> return 5
```
The goal is first pushed by `120453`, a layer-4 board, so it sits in layer 5; when it is popped
the answer is 5, after `seen` reached 34 boards.

Following the parent of each board back from the goal gives
`412503 -> 412053 -> 012453 -> 102453 -> 120453 -> 123450`, exactly the hand solution above.
Invariant across frames: the queue held boards of one or two consecutive distances, and every
board entered it at most once.

## Why it is correct

The state graph is unweighted (every move costs one) and undirected (every move can be
undone). BFS's **layer property** holds: when a board is first pushed with `moves = d`, `d` is
the true minimum number of moves to reach it. Seed: the start, `d = 0`. Step: boards are popped
in non-decreasing `d`, so a board's first discovery comes from a parent at the smallest possible
distance, plus one; the `seen` set ensures no later, longer discovery replaces it. The neighbour
table lists exactly the legal moves, so the BFS walks exactly the real graph. When the goal is
popped, its `d` is the minimum.

**Why `-1` happens, and why the queue really empties.** The graph has at most 720 nodes, so the
BFS always finishes. Read the five tiles in row order, ignoring `0`, and count inversions
(pairs out of order). A horizontal move does not change that reading at all. A vertical move
lifts one tile past exactly two others in the reading, changing the inversion count by `-2`,
`0` or `+2`. So **inversion parity never changes**. The goal `12345` has zero inversions (even).
`[[1,2,3],[5,4,0]]` reads `12354`, one inversion (odd), so it lies in the other half of the 720
boards and can never reach the goal; its BFS visits all 360 boards of its half and returns `-1`.
Our start `41253` has four inversions, even, consistent with reaching the goal.

## Cost

- **Brute force neighbour search**: `O(S^2 * 6)` with `S = 720`.
- **Generated neighbours**: each of at most `S` boards is popped once, makes at most 3
  neighbours, each a 6-character string: `O(S * 6)` time, `O(S)` space for `seen` and the
  queue.

For an `m x n` tray the state count is `(mn)!`, so this approach is exactly as good as the
state space is small. At 3x3 (`9!/2 = 181440` reachable) BFS is still fine; at 4x4 it is
not, and you need A* with a heuristic such as total Manhattan distance.

## Variations you will meet

- **8-puzzle (3x3) or other tray shapes.** Same string encoding; rebuild the neighbour table
  for the new shape (index `i` touches `i +- 1` within a row, `i +- n` across rows).
- **Open the Lock (LeetCode 752).** States are 4-digit strings, a move turns one wheel up or
  down, some states are forbidden. The same three decisions: string state, generated
  neighbours, `seen` set; the deadends go into `seen` before the BFS starts.
- **Minimum Genetic Mutation / Word Ladder.** A string state where only dictionary strings are
  legal nodes.
- **Return the moves, not just the count.** Store `parent[state]` when pushing, then walk back
  from the goal, as in the path traced above.

## What to carry forward

A puzzle is a graph whose nodes are whole configurations: pick a hashable encoding, generate
neighbours from the rules rather than searching for them, check that the state count is small,
then BFS. The next problem, Bus Routes, is also a BFS on an implicit graph, but the clever part
is choosing what a node is: a whole bus route rather than a single stop.
