# Minimum Moves to Move a Box to Their Target Location
*LeetCode 1263 · Hard · Pattern: 0-1 BFS (deque shortest path) · Reading time ~11 min*

## The problem

A grid holds walls '#', floor '.', the player 'S', a box 'B' and a target 'T'. The player walks 4-directionally for
free; walking into the box pushes it one cell if the cell beyond is floor. Return the minimum number of pushes to get
the box onto the target, or -1.

```text
Example: in
  ["######","#T####","#..B.#","#.##.#","#...S#","######"] the
  answer is 3 (push left twice, walk round below the box, push
  up).
```

## What the problem is really asking

This is Sokoban with one box. The grid has walls `#`, floor `.`, the player `S`, the box
`B` and the target `T`. The player walks in four directions over floor. If the player is
next to the box and walks into it, the box slides one cell in that direction, provided the
cell beyond the box is floor; the player moves into the box's old cell. Return the minimum
number of **pushes** to get the box onto the target, or -1. Walking without pushing is
free.

The answer counts pushes, not steps. That single sentence decides everything: it makes the
graph weighted (walks cost 0, pushes cost 1), and it means that two very different player
routes are equally good if they lead to the same push.

```text
  c     0 1 2 3 4 5
  r0    # # # # # #
  r1    # T # # # #       box   B = (2,3)
  r2    # . . B . #       player S = (4,4)
  r3    # . # # . #       target T = (1,1)
  r4    # . . . S #
  r5    # # # # # #

  plan: walk up to (2,4), push left twice  -> box (2,1)
        walk round the bottom to (3,1), push up -> box (1,1)
  answer: 3 pushes (10 free walking steps)
```

What makes it hard is that two things move. The box decides whether we are done, but the
player decides what pushes are possible, because a push needs the player standing on the
opposite side of the box, and the box itself can block the player's way around.

## Do it by hand first

Look at the box at (2,3). It can only move left or right: above and below it are walls. To
push it left the player must stand on its right, at (2,4). Can the player get there? From
(4,4) go up through (3,4) to (2,4). Yes. Push: box to (2,2), player to (2,3). Push again:
box to (2,1), player to (2,2).

Now the box is in column 1, directly below the target. To push it up, the player must stand
*below* it, at (3,1). The box blocks the short way, so the player walks right along row 2,
down column 4, left along row 4, and up to (3,1). Push up. Three pushes.

```text
  after 2 pushes            the long walk round
  # # # # # #               # # # # # #
  # T # # # #               # T # # # #
  # B P . . #     P=(2,2)   # B P > v #     player route:
  # . # # . #               # ^ # # v #     (2,2) -> (2,4)
  # . . . . #               # ^ < < < #     -> (4,4) -> (4,1)
  # # # # # #               # # # # # #     -> (3,1), push up
```

What did your hand keep track of? **Where the box is, and where the player is** (or more
precisely, which side of the box the player can get to). And you counted only the pushes;
the walking you did freely, as much as needed. That gives both halves of the solution: the
state is (box, player), and walking edges cost nothing.

## The first honest attempt

A strong candidate sees the state immediately: (box row, box col, player row, player col).
From a state, the player tries four directions. If the next cell is the box (and the cell
beyond is free), that is a push: the box and player both advance, cost 1. Otherwise it is a
walk, cost 0. Shortest path in a graph with weights 0 and 1: "Dijkstra with a heap."

That is correct. With a 20 x 20 grid there are up to 400 x 400 = 160,000 states, and
Dijkstra costs O(S log S). Where is the waste? Look at the heap while it runs:

```text
  heap contents at some moment (key = pushes so far)

             1
          /     \
         1       2          every key is D or D+1
        / \     / \
       2   1   2   2        each heappush / heappop:
                            O(log S) sift through a tree
  as array: [1, 1, 2, 2, 1, 2, 2]   that only ever holds
                                    two distinct values
```

The heap keeps a full ordering among keys that only take two values at any time. It pays a
logarithmic factor per operation to sort what is essentially two buckets.

There is a second common attempt that wastes differently: BFS on box positions only,
counting pushes, and for each candidate push run a fresh BFS to check whether the player
can reach the cell behind the box. Every box state re-floods the same open region from
scratch:

```text
  box at (2,3): flood player region  -> 10 cells
     push left?  BFS from player to (2,4) .....
     push right? BFS from player to (2,2) .....
  box at (2,2): flood again           -> 10 cells
  box at (2,1): flood again           -> 9 cells
  the region barely changes; it is recomputed every time
```

## The turning point

**Claim: when every edge weighs 0 or 1, a deque can replace the priority queue: push a
0-edge's target to the front, a 1-edge's target to the back, and the deque stays sorted by
distance.**

Why it stays sorted. Suppose the front of the deque has distance D. Everything in it is D
or D + 1, with all the D's before all the D + 1's. Pop the front (distance D). A walk edge
leads to a state at distance D: put it at the front, next to the other D's. A push edge
leads to D + 1: put it at the back, after the other D + 1's. Both moves keep the shape
"D's, then D + 1's". So the deque pops states in non-decreasing distance, which is all
Dijkstra needs, at O(1) per operation. This is **0-1 BFS**.

The deque, drawn as memory:

```text
  front                                  back
  +-------+-------+-------+-------+-------+
  | (s,0) | (s,0) | (s,0) | (s,1) | (s,1) |
  +-------+-------+-------+-------+-------+
    ^ appendleft here           append here ^
      for a walk (cost 0)         for a push (cost 1)

  invariant: front block all = D, back block all = D+1
```

Now draw the state space the way the chapter keeps asking: the graph is not the grid, the
graph is the state. Group states by box position. Each box position is a **room**; inside
it, the player roams freely over the floor not covered by the box (thin, cost-0 edges). A
push is a thick, cost-1 arrow from one room to another:

```text
  room box=(2,3)        room box=(2,2)       room box=(2,1)
  player can be at      player can be at     player can be at
  any of 10 cells       any of 10 cells      any of 9 cells
       |   \                  |                    |
  push |    \ push       push |               push |
  left |     \ right     left |                 up |
       v      v               v                    v
  box=(2,2)  box=(2,4)    box=(2,1)            box=(1,1) = T
             dead end
             (box against
              the wall)
```

0-1 BFS floods a whole room (front pushes) before it takes any thick arrow (back pushes),
so it naturally does "walk anywhere for free, then push". It also fixes the second
attempt's waste: the player's reachable region is not recomputed separately for each
push question; it is part of the one search.

Two more details. The rule "the player must stand behind the box" needs no special code:
the only way to push is to step *into* the box, and stepping into it from the left moves
it right. And a state may be added to the deque twice (once at the back with a push, later
at the front with a cheaper walk), so we keep a `dist` map and only relax when the new
distance is strictly smaller.

## Watch it work

States are `box | player`, with their push count. The deque is shown front to back.

```text
Frame 1  room box=(2,3), d=0
  pop (2,3)|(4,4) and flood the room with 0-edges
  player reaches: (4,3) (4,2) (4,1) (3,1) (2,1)
                  (2,2) (1,1) (3,4) (2,4)
```

Walking is free, so the whole room is popped at distance 0 before anything else.

```text
Frame 2  two pushes found while flooding
  player (2,2) steps right into box -> (2,4)|(2,3) d=1
  player (2,4) steps left  into box -> (2,2)|(2,3) d=1
  deque: [ (2,4)|(2,3):1 , (2,2)|(2,3):1 ]   (back)
```

Both pushes went to the back. Once the 0s are exhausted, the deque holds only 1s.

```text
Frame 3  room box=(2,4), d=1
  player floods 10 cells around it
  push right: (2,5) is a wall      no
  push up: (1,4) is a wall          no
  push down: player would stand
             on (1,4), a wall      no
  deque: [ (2,2)|(2,3):1 ]
```

The box against the right wall is stuck; its room produces no push. 0-1 BFS still pays
for exploring it, once.

```text
Frame 4  room box=(2,2), d=1
  pop (2,2)|(2,3): step left into box
       -> (2,1)|(2,2) d=2   append to back
  flood the rest of the room at d=1
  player (2,1) pushing right -> (2,3)|(2,2),
       d=2, but dist is already 0: no relax
```

Pushing the box back to where it started is useless; the `dist` check discards it.

```text
Frame 5  room box=(2,1), d=2
  player walks (2,2) (2,3) (2,4) (3,4) (4,4)
               (4,3) (4,2) (4,1) (3,1)
  player (3,1) steps up into box
       -> (1,1)|(2,1) d=3   append to back
  deque: [ (1,1)|(2,1):3 ]
```

The long walk round the bottom costs nothing; the push up costs one.

```text
Frame 6  pop (1,1)|(2,1), d=3
  box on target -> return 3
```

The first state with the box on the target is popped at distance 3. 40 states were
popped in total.

Across every frame the deque held at most two distance values, the smaller ones in front,
and each room was fully explored at one push count before any room at the next count was
entered.

## Why it is correct

The state graph has a node per (box, player) position pair and edges of weight 0 (walk) or
1 (push). Any legal sequence of player moves maps to a path in this graph, and the weight
of the path is its number of pushes. So the answer is the shortest weighted distance from
the start state to any state whose box is on the target.

Dijkstra's argument says: if states are removed in non-decreasing order of tentative
distance and edges are non-negative, then each state's distance is final when it is
removed. 0-1 BFS satisfies the ordering condition by the deque invariant ("all D's, then
all D + 1's"), proved in the turning point: popping takes from the D block, a 0-edge adds to
the D block, a 1-edge adds to the D + 1 block, and when the D block empties the old D + 1
block becomes the new front block. So the first popped state with the box on the target has
the minimum number of pushes. A stale duplicate popped later only re-relaxes with an
already-final distance and changes nothing. If the deque empties, no state with the box on
the target is reachable, and -1 is right.

## Cost

- **Time O((R x C)^2)**: at most R x C box positions times R x C player positions, each
  state relaxing four moves in O(1). Duplicates are bounded by the number of edges.
- **Space O((R x C)^2)** for the `dist` map and deque. In practice far fewer states are
  reachable, since the player is confined to floor and to one side of the box.
- Dijkstra with a heap over the same states costs an extra log factor.

## Variations you will meet

- **Count all player steps instead of pushes.** Every edge weighs 1, so plain BFS over the
  same (box, player) states.
- **Minimum Cost to Make at Least One Valid Path in a Grid.** Following a cell's arrow costs
  0, changing it costs 1: the same 0-1 BFS on plain cells. It comes later in the chapter.
- **BFS on (box, side of box) with an inner reachability check.** A smaller outer state
  (box plus which of four sides the player is on) with a BFS or union-find query for "can
  the player get from here to there without passing the box". Fewer states, more work per
  state.
- **Several boxes.** The state includes every box position, and the state space explodes;
  real Sokoban solvers add heuristics (A*) and deadlock detection (a box in a corner is a
  dead end, like the box at (2,4) above).

## What to carry forward

When two kinds of moves cost 0 and 1, use a deque: free moves go to the front, paid moves to
the back, and you get Dijkstra's answer at BFS speed; and when two agents interact, the
state is both of them. The next problem, Find the Town Judge, starts a new part of the
chapter: instead of searching a graph, it reads in-degrees and out-degrees, the counting
that drives topological sort.
