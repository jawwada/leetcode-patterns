# Number of Islands II
*LeetCode 305 · Hard · Pattern: Union-Find (disjoint set union) · Reading time ~13 min*

## What the problem is really asking

You have an `m x n` board that starts as all water. You get a list of operations. Each one
turns a cell `(r, c)` into land. After **every** operation, report how many islands there
are. An island is a group of land cells joined up, down, left or right. A cell may be named
twice, and turning land into land changes nothing.

The answer is a list with one count per operation. Number of Islands answered this once, for
a finished board, with a flood fill. Here the board changes `k` times and you need `k`
answers. The difficulty is that one new cell can do three different things. It can start a
new island. It can extend one existing island. Or it can **weld several islands into one**,
and then the count can go *down* by more than one.

```text
  m = n = 3, positions = (0,0) (0,1) (1,2) (2,1) (1,1) (1,1)

  after op:  1    2    3    4    5    6
           X..  XX.  XX.  XX.  XX.  XX.
           ...  ...  ..X  ..X  .XX  .XX
           ...  ...  ...  .X.  .X.  .X.
  count:     1    1    2    3    1    1
                                ^ one cell welds 3 islands
                                       ^ repeat: no change
```

## Do it by hand first

Keep a running tally and update it after each drop. Do not recount the board. For each new
tile, look only at its four neighbours.

```text
  drop   touches which islands?        tally
  (0,0)  none                          0 + 1     = 1
  (0,1)  {A} (the (0,0) island)        1 + 1 - 1 = 1
  (1,2)  none                          1 + 1     = 2
  (2,1)  none                          2 + 1     = 3
  (1,1)  {A}, {B=(1,2)}, {C=(2,1)}     3 + 1 - 3 = 1
  (1,1)  already land                  1
```

The rule your hand followed is this. A new tile adds one island, and then subtracts one for
every **distinct** island it touches. Your hand also kept track of *which island each land
cell belongs to*, so it could tell "distinct" from "the same island seen through two
neighbours." That label, which only ever merges, is union-find again. This time the nodes
appear one by one.

## The first honest attempt

Keep a set of land cells. After every operation, flood-fill all the land from scratch and
count the floods.

```text
  op 4: flood finds {(0,0),(0,1)} {(1,2)} {(2,1)}  -> 3
  op 5: flood finds {(0,0),(0,1),(1,1),(1,2),(2,1)} -> 1
        ^ re-walks (0,0),(0,1),(1,2),(2,1) again,
          though only (1,1) changed
```

Each recount costs `O(m * n)`, or `O(land)` if you only store land. Over `k` operations that
is `O(k * m * n)`. With `m = n = 10^4` and `k = 10^4`, that is hopeless. The repeated work is
rediscovering the islands of the previous step, which have not changed at all except near
the one new tile.

## The turning point

**Claim: adding land at `x` changes the island count by exactly `1 - d`, where `d` is the
number of distinct islands among `x`'s land neighbours.**

The justification: islands only ever merge, and nothing is ever removed. Before the drop
there are `count` islands. The new cell is, on its own, a new island, so the count goes up
by one. It is adjacent to some set of existing islands, and all of those, plus `x`, become
one island. The other islands are untouched because `x` is not adjacent to them. So `d + 1`
islands become 1, and the count changes by `1 - d`. Everything is local to four
neighbours.

Turning this into code takes three small decisions.

**Keys.** A cell `(r, c)` becomes the integer `r * n + c`, which is row-major numbering. On
a 3-wide board, `(1,1)` is 4 and `(2,1)` is 7.

**Storage.** `parent` is a **dict** holding land cells only. "Is this neighbour land?" is
the same question as "is its key in `parent`?" It also means memory grows with `k`, not
with `m * n`, which matters when the board is huge and the operation list is short.

**Counting distinct islands without a set.** Do not collect the neighbours' roots and then
count them. Union one neighbour at a time instead. Before each union, compare the *current*
root of `x` with the neighbour's root. After the first merge, `x`'s root may already equal
another neighbour's root. In that case skip it, because that island has already been
counted. Each union that actually happens subtracts one.

```text
  2x2 board, positions (0,0) (1,1) (0,1) (1,0)
  before op 4:       op 4 drops (1,0) = key 2
     X X             nb (0,0): root 1 != root 2 -> union, -1
     . X             nb (1,1): find(3)=1 == find(2)=1 -> skip
  count 1            count: 1 + 1 - 1 = 1   (not 0!)
```

A version that subtracts one per land neighbour would report 0 islands there. Comparing
roots, not cells, is the fix.

**Duplicates.** If the key is already in `parent`, append the current count and move on.
Re-initialising the cell would detach it from its island and break the forest.

Union by rank and path halving are the same as in Number of Connected Components. The
`rank` dict sits next to `parent`.

## Watch it work

`m = n = 3`, `positions = [(0,0),(0,1),(1,2),(2,1),(1,1),(1,1)]`. Neighbours are checked in
the order down, up, right, left. On a rank tie, the new cell's root stays on top.

```text
Frame 1  drop (0,0) key 0; no land neighbours
  board  X . .      parent {0:0}        0
         . . .      rank   {0:0}
         . . .      count 0+1 = 1       out [1]
```
A brand-new singleton island.

```text
Frame 2  drop (0,1) key 1; count -> 2
  left nb key 0: find(1)=1, find(0)=0, tie -> 0 under 1
  board  X X .      parent {0:1, 1:1}   1
         . . .      rank   {0:0, 1:1}   |
         . . .      count 2-1 = 1       0     out [1,1]
```
The new tile touched one island. One union, so the count goes up one and down one.

```text
Frame 3  drop (1,2) key 5; neighbours (0,2),(2,2) water
  board  X X .      parent {0:1,1:1,5:5}    1    5
         . . X      count 1+1 = 2           |
         . . .                              0
                                         out [1,1,2]
```
The tile is diagonal to `(0,1)`, and diagonals do not count, so it is a new island.

```text
Frame 4  drop (2,1) key 7; up nb (1,1) is water
  board  X X .      parent {0:1,1:1,5:5,7:7}  1   5   7
         . . X      count 2+1 = 3             |
         . X .                                0
                                       out [1,1,2,3]
```
This is a third separate island. Three roots, so the count is 3.

```text
Frame 5  drop (1,1) key 4; count 3+1 = 4, then:
  down  key 7: roots 4,7, tie      -> 7 under 4, rank4=1, 3
  up    key 1: roots 4,1, tie 1=1  -> 1 under 4, rank4=2, 2
  right key 5: roots 4,5, 2 > 0    -> 5 under 4,          1
  left  key 3: water
  board  X X .      parent {0:1,1:4,4:4,5:4,7:4}
         . X X                 4
         . X .               / | \
                            7  1  5
                               |
                               0         out [...,3,1]
```
One tile, three successful unions, a net change of `1 - 3 = -2`. Node 0 still points to 1.
Its depth grew to 2, but rank kept the tree shallow.

```text
Frame 6  drop (1,1) again: key 4 already in parent
  parent, rank unchanged     count 1
                             out [1,1,2,3,1,1]
```
The duplicate is a no-op. We report the current count and do not touch the forest.

What stayed invariant: `parent` held exactly the land cells. Two land cells shared a root
exactly when they were on the same island. `count` equalled the number of roots in
`parent`.

## Why it is correct

Invariant before each operation: the trees in `parent` are exactly the islands of the
current board, and `count` is the number of trees. Initially the board is empty, there are
no trees, and `count` is 0.

For a duplicate, the board does not change, and we change nothing, so the invariant holds.
For a new cell `x`, we add a singleton tree and add 1 to the count, which is correct for the
board where `x` has no neighbours yet. Then we process `x`'s land neighbours one at a time.
For each neighbour `y`, if `find(x) != find(y)`, then `y`'s island is not yet merged with
`x`'s growing island. It must be, since `x` and `y` touch, so we union them and subtract
one, because two trees became one. If the roots are equal, the island is already merged,
and subtracting would double-count it. After all four neighbours, `x`'s tree contains
exactly `x` plus every island adjacent to it, which matches the new board. Every other
island is unchanged. So the invariant holds and `count` is the true island count.

The appended value is therefore correct after every operation.

## Cost

- Time `O(k * alpha(k))`. Each operation does at most four neighbour checks, each with two
  finds and maybe one union. That is effectively `O(k)`.
- Space `O(k)`. The `parent` and `rank` dicts hold one entry per distinct land cell. If you
  use flat arrays of size `m * n` instead, space is `O(m * n)` but there is no hashing,
  which is faster when the board is small.
- The flood-fill recount is `O(k * m * n)` time and `O(m * n)` space.

## Variations you will meet

- **Online connectivity in general.** Any time items arrive and you are asked about groups
  after each arrival, think "insert as a singleton, union with neighbours, track count."
  This covers streams of friendships, of pixels turning on, and of edges in a network.
- **Deletions instead of insertions.** Union-find cannot split a set. The standard trick is
  to **reverse time**. Start from the final state and add things back in reverse order,
  recording answers backwards. Bricks Falling When Hit (803) is exactly this.
- **Track island sizes or perimeters too.** Keep `size[root]` and add on union. Making a
  Large Island (827) asks for the best single flip, which is the same "what does this one
  cell weld together?" question asked for every water cell.
- **Make the count query cheap but not every step.** If answers are only needed at a few
  checkpoints, batch the unions in between. The cost stays the same, since union-find is
  already incremental.

## What to carry forward

When cells arrive one at a time, each one is `+1`, then `-1` for every **distinct** root
among its neighbours. Compare roots, never cells, and keep only land in the dict. The next
problem, Minimize Malware Spread, keeps union-find's components but asks about their sizes:
`size[root]` and a count of infected nodes per component decide which node to remove.
