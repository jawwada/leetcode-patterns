# Shortest Path to Get All Keys
*LeetCode 864 · Hard · Pattern: BFS over augmented states (position + bitmask/budget) · Reading time ~10 min*

## The problem

A grid has '.' empty cells, '#' walls, '@' the start, lowercase keys and matching uppercase locks (at most 6 pairs).
You walk 4-directionally, pick up keys automatically, and can pass a lock only while holding its key. Return the
fewest moves to collect every key, or -1.

```text
Example: ["@.a..","###.#","b.A.B"] -> 8 (fetch a, go down the
  gap, pass A, reach b); ["@Aa"] -> -1.
```

## What the problem is really asking

A grid contains `.` floor, `#` walls, one `@` start, some lowercase keys `a`..`f`, and the
matching uppercase locks `A`..`F`. You move one cell per step in four directions. Walking
onto a key picks it up automatically. You can walk onto a lock only if you already hold its
key. Return the fewest steps to hold **every** key in the grid, or -1. There are at most
six keys, and each key has exactly one matching lock.

The answer is again a shortest-path length. What makes it hard is that the grid's walls
change as you play: a lock is a wall before you have its key and floor after. And unlike
the previous problem, the optimal walk often goes back over cells it has already visited,
carrying something new.

```text
  grid                     c0 c1 c2 c3 c4
                     r0     @  .  a  .  .
                     r1     #  #  #  .  #
                     r2     b  .  A  .  B

  keys a, b    locks A, B
  route: right to a (2), right 1, down 2, left through A
         to b (3)      -> 2 + 1 + 2 + 3 = 8 steps
  B at (2,4) is never opened and never needed
```

The answer is any walk that ends the moment the last key is picked up; you do not have to
return anywhere.

## Do it by hand first

Before the 2D grid, look at the smallest case that shows the trouble: one row.

```text
  col    0  1  2  3  4  5  6
         a  .  @  .  A  .  b

  try right first: 3 -> 4 is the lock A, no key. Stuck.
  so: left 2 to a, then right 6 to b, passing @ again
      2 + 6 = 8 steps
```

To get `b` you must first walk *away* from it, grab `a`, and then walk back over cells 1,
2 and 3, which you have already stood on. A normal BFS would refuse to revisit them.

What did your hand keep track of? Your position, of course, and **the keys in your
pocket**. Standing on cell 3 with no keys and standing on cell 3 holding `a` are completely
different situations: one is a dead end, the other leads straight to the answer. The
pocket is the seed of the solution.

## The first honest attempt

There are at most six keys, so a strong candidate says: "Try every order to collect them.
For each order, BFS from the start to the first key, then from there to the second key
(now allowed through the first key's lock), and so on. Sum the legs and keep the best
order."

```text
  orders for keys {a, b, c}:   abc acb bac bca cab cba

  abc :  [@ -> a]  [a -> b | held a]    [b -> c | held a,b]
  acb :  [@ -> a]  [a -> c | held a]    [c -> b | held a,c]
              ^ same leg, BFS'd again
  with 6 keys: 720 orders, ~6 BFS legs each, and the leg
  "a -> b holding {a}" is recomputed in all 24 orders that
  start with a, b
```

That is O(k! x k x R x C) and correct, because between pickups the shortest leg is indeed
a shortest BFS path. The waste is clear: the same leg from the same position with the same
pocket is searched again and again, once per order that shares that prefix. The search
does not realise that "standing on key b, holding {a, b}" is one situation, regardless of
the route that led there.

There is also a subtle trap in the "obvious" fix of running one BFS on the grid and just
remembering keys as you go. With a visited set on cells, the one-row example fails: cells
1, 2, 3 are marked when you first spread out with no keys, so after picking up `a` you
cannot walk back, and the answer comes out as -1.

## The turning point

**Claim: the whole situation is (row, column, keys held), and the keys held is a subset of
at most six letters, so it fits in a 6-bit mask. One BFS over these states finds the
answer.**

Nothing else about the past matters. Which order you collected the keys in, how you got
here, how many times you crossed a cell: none of it changes what you can do next. Only
where you stand and which locks you can open.

So the graph is the grid copied 2^k times, once per possible pocket. With six keys that is
64 copies:

```text
  the thing: 2^k stacked copies of the grid (k = 2 here)

    mask 00  @ . a . .      walking: stay in the same copy
             # # # . #
             b . A . B      A, B are walls in this copy
                 |
                 | step onto a: jump to mask 01
                 v
    mask 01  @ . a . .      A is floor here, B still a wall
             # # # . #
             b . A . B
                 |
                 | step onto b: jump to mask 11
                 v
    mask 11  any cell here = all keys = done

  how it is stored: queue of (r, c, mask)
                    seen = set of (r, c, mask)
```

Each step is still one move. Moving onto a key cell sets that key's bit (`mask | 1 << i`)
and the move lands in a different copy. Moving onto a lock cell is allowed only if the
matching bit is already set. Everything else is an ordinary grid step inside one copy.

Because every edge has length 1, plain BFS works, and the first popped state whose mask
equals `full` (every key that exists in this grid) gives the answer. `full` is computed by
scanning the grid, since a grid may have fewer than six keys.

The `seen` set is on the full triple. That is precisely what allows walking back: (0, 1)
with mask `00` and (0, 1) with mask `01` are different nodes, so revisiting a cell with a
new pocket is a new state. It is also what keeps the search finite: re-entering the same
cell with the *same* pocket is pointless and is cut.

This is the previous problem's idea with a set instead of a counter. There, a cell carried
"how many smashes left"; here it carries "which keys". The graph is not the grid; the graph
is the state.

## Watch it work

Keys `a` = bit 0, `b` = bit 1, so `full = 11` (binary). States are written `(r,c)mask`.
Each frame shows the copy the wave is in; numbers are BFS depths.

```text
Frame 1  depths 0-1, copy mask 00
    r0   0 1 a . .
    r1   # # # . #
    r2   b . A . B
  queue after: [(0,2)01]
```

Without keys the wave can only reach (0,1); its one new neighbour is the key `a`, which
pushes a state into copy 01 instead.

```text
Frame 2  depth 2, copy mask 01
    r0   . . 2 . .
    r1   # # # . #
    r2   b . A . B
  queue: [(0,2)01]          seen: 3 states
```

The key is picked up on arrival. The same cell (0,2) now lives in copy 01.

```text
Frame 3  depths 3-4, copy mask 01
    r0   4 3 2 3 4
    r1   # # # 4 #
    r2   b . A . B
  queue: [(1,3)01, (0,4)01, (0,0)01]
```

The wave spreads both ways. (0,1) and (0,0) are revisited: they were seen with mask 00,
but in copy 01 they are new states.

```text
Frame 4  depths 5-6, copy mask 01
    r0   4 3 2 3 4
    r1   # # # 4 #
    r2   b . 6 5 B
  queue: [(2,2)01]
```

Through the gap to (2,3) at depth 5. From there, B at (2,4) is still a wall in this copy,
but A at (2,2) is floor, so the wave enters it at depth 6.

```text
Frame 5  depths 7-8
    copy 01:  r2   b 7 6 5 B
    copy 11:  r2   8 . . . .     (2,0) reached with mask 11
  pop (2,0)11 at depth 8: mask == full -> return 8
```

Stepping onto `b` sets bit 1 and lands in copy 11. When that state is popped, the mask is
full, so the answer is 8. Only 12 states were ever created out of 4 x 15 = 60 possible.

The invariants on display: every state's depth is the number of steps taken; a cell can
appear in several copies but never twice in the same copy; and the wave only ever moves to
a copy with more bits set, never fewer, because keys are never lost.

## Why it is correct

Model the game as a graph whose nodes are (r, c, mask) and whose edges are single legal
moves, with the mask updated on key cells. A real walk in the grid corresponds to exactly
one path in this graph, with the same number of steps, because the mask at each point is
determined by which key cells the walk has stepped on so far. A lock check is a check on
the mask, so legal walks map to paths and paths map back to legal walks.

The goal is reached precisely when the walk's mask equals `full`, so the answer is the
distance from (start, 0) to the nearest node with mask `full`. BFS on a unit-weight graph
discovers nodes in order of distance, and the depth at which a node is first pushed is its
true distance (anything closer would have been found from an earlier layer). Hence the first
popped node with a full mask is a nearest one. If the queue empties, no full-mask node is
reachable, and -1 is correct.

Keys picked up never need to be "dropped", and there are no costs other than steps, so no
information beyond position and mask could change the future. That is what justifies
collapsing all histories with the same triple into a single node.

## Cost

- **Time O(R x C x 2^k)**: at most 2^k copies of R x C cells, each state popped once and
  checking four neighbours. With R, C <= 30 and k <= 6, that is at most 57,600 states.
- **Space O(R x C x 2^k)** for `seen` and the queue. A 3D boolean array
  `seen[r][c][mask]` is a constant-factor faster alternative to a set of tuples.
- The permutation brute force is O(k! x k x R x C).

## Variations you will meet

- **Keys can be used up (each key opens one lock).** Then the pocket is a multiset or the
  locks opened also join the state; the state space grows, but the method is the same.
- **More than ~15 keys.** 2^k explodes; you would need to compress the grid to a graph on
  key positions (BFS between them) and then do a bitmask DP over that smaller graph, which is
  the shape of the next problem.
- **Return to the start after collecting.** Add "and at the start cell" to the goal test.
  Nothing else changes.
- **Weighted moves (doors that take time to open).** Edge weights differ, so Dijkstra over
  the same (cell, mask) states; if the weights are only 0 and 1, use 0-1 BFS.

## What to carry forward

If the rules of the walk depend on a small set of things you have collected, the set
becomes part of the node, as a bitmask, and a cell visited with a new set is a new place.
The next problem, Shortest Path Visiting All Nodes, keeps the bitmask but drops the grid:
the set to collect is every node of a graph, and the walk may start anywhere.
