# Design Skiplist

*LeetCode 1206 · Hard · Pattern: Multi-level sorted linked list with randomised express lanes · Reading time ~14 min*

## What the problem is really asking

Build a sorted multiset from scratch, without any library ordered structure, supporting:

- `search(target)`: is target present?
- `add(num)`: insert num (duplicates allowed).
- `erase(num)`: remove one copy of num; return False if there is none.

Each operation should take O(log n) expected time. The answer objects are booleans; what you are really building is an
ordered container, the job a balanced binary search tree does. The difficulty is that balanced trees are painful to
write under pressure (rotations, colours, heights), and a plain sorted list or linked list is O(n) per operation. The
problem asks for a structure that is ordered, fast, and simple enough to write in twenty minutes.

```text
add 1, 2, 3; search(0) -> False
add 4; search(1) -> True
erase(0) -> False; erase(1) -> True; search(1) -> False

contents as a sorted line:
  before erase:  1  2  3  4
  after  erase:     2  3  4
```

## Do it by hand first

Picture a single road with exits numbered in increasing order. To reach exit 37 you drive past 1, 2, 3, ... one at a
time. Now add a highway that only stops at every fourth exit, and above it an express route that stops at every
sixteenth. To reach 37: take the express route as far as you can without passing 37 (stop at 32), drop to the
highway (36), drop to the local road (37).

```text
express:  0 ------------------------------> 32 -------> 48
highway:  0 ----> 4 ----> 8 ... 28 ------> 32 -> 36 -> 40
local:    0 -> 1 -> 2 -> 3 ... 32 -> 33 ... 36 -> 37

route to 37:  express to 32, highway to 36, local to 37
              ^ drop when the next stop would overshoot
```

What you did by hand: on each road, move right while the next stop is still smaller than the target, then drop one
road down. You visited only a few stops per road, and there were only a few roads. That is the whole search.

## The first honest attempt

Keep a sorted Python list. `search` can binary search, O(log n), but `add` and `erase` shift the tail, O(n). Or keep a
sorted linked list: insertion is an O(1) pointer splice once you are at the right place, but getting there is a linear
walk, O(n), because a linked list cannot jump into the middle.

```text
sorted linked list, search(6):

H -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
     ^    ^    ^    ^    ^    ^
     every node visited to reach 6
```

The repeated work is walking past nodes one at a time when the target is far away. A linked list's only weakness is
that it cannot skip; the splice itself is already cheap.

## The turning point

**Claim: if every node independently joins row i with probability 1/2^i, then row i holds about n/2^i nodes, there
are about log2 n rows, and a search that drops down a row whenever it cannot move right takes O(1) expected steps per
row, so O(log n) in total.**

This is the express-lane picture made precise. A skiplist is a stack of sorted linked lists:

- Row 0 is the full sorted list: every node is in it.
- Row 1 contains a subset of the nodes, row 2 a subset of row 1, and so on.
- A head sentinel (value smaller than everything) sits at the left of every row.
- A node of height h is in rows 0..h-1, and owns an array `forward[0..h-1]` where `forward[i]` is the next node on row i.

```text
the picture (an ideal skiplist of 1..8)

row 3: H ---------------------------------> 8
row 2: H -------------> 4 ----------------> 8
row 1: H -----> 2 ----> 4 -----> 6 -------> 8
row 0: H -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8

how it is stored: one node per value, a tower
of forward pointers

  node 4: val 4, forward[0]->5
                 forward[1]->6
                 forward[2]->8
  node 5: val 5, forward[0]->6
```

The ideal picture puts every second node in row 1, every fourth in row 2, and so on. Maintaining that exactly under
inserts would need rebalancing. The randomised trick: when a node is created, flip a coin until it comes up tails;
the number of heads plus one is its height. Height 1 with probability 1/2, height 2 with 1/4, height 3 with 1/8. On
average the rows thin out by half each level, without any global bookkeeping.

**Search.** Start at the head on the top row in use. On each row, move right while the next node's value is smaller
than the target; when you cannot, drop one row. After row 0, the next node on row 0 is the first node with value at
least the target. Found iff it equals the target.

Why O(1) expected steps per row? Walk the path backwards: from where the search ends on row 0, retrace it. At each
node, the step back was either "up" (if the node also exists one row higher, probability 1/2) or "left". So the
expected number of left steps before going up is about 1, per row. With about log2 n rows, the search is O(log n)
expected.

**The update array.** During the descent, record `update[i]` = the last node visited on row i, the node where we
dropped down. It is exactly the node after which a new value must be spliced on row i, and the node before the value to
erase.

**Add.** Run the descent for num, get `update`. Pick a random height h. On each row i below h, splice:
`node.forward[i] = update[i].forward[i]; update[i].forward[i] = node`. If h exceeds the current number of rows,
the new rows start at the head, which is why `update` is initialised with the head everywhere.

**Erase.** Run the descent, look at `update[0].forward[0]`. If it is not num, return False. Otherwise, on each row
the node lives in, `update[i].forward[i] = node.forward[i]`, which unlinks it. If the top rows became empty, lower the
level.

A subtle point with duplicates: the descent uses strictly `<`, so it stops before the first copy of num on every row.
That guarantees the node found on row 0 is the first copy, and that on every row it occupies, it is exactly
`update[i].forward[i]`, so the unlink is correct on all rows. Mixing `<` and `<=` breaks this.

## Watch it work

Operations: add 1, 2, 3, 4, search(0), add 6, add 5, search(5), erase(1). The heights below are the ones the seeded
generator in the solution produces: 4, 1, 3, 1, 1, 3.

Frame 1: `add(1)`, height 4.

```text
level 4
row 3: H -> 1
row 2: H -> 1
row 1: H -> 1
row 0: H -> 1
update[] = [H, H, H, H]  (empty list)
```

The first node is tall by luck; every row starts at the head, so `update` is the head on all rows.

Frame 2: add 2 (h=1), 3 (h=3), 4 (h=1).

```text
level 4
row 3: H -> 1
row 2: H -> 1 ------> 3
row 1: H -> 1 ------> 3
row 0: H -> 1 -> 2 -> 3 -> 4
```

Node 3 joined rows 0, 1, 2; nodes 2 and 4 live only on row 0.

Frame 3: `search(0)`.

```text
row 3: at H, next 1 < 0? no  -> down
row 2: at H, next 1 < 0? no  -> down
row 1: at H, next 1 < 0? no  -> down
row 0: at H, next 1 < 0? no  -> stop
candidate = H.forward[0] = 1 != 0 -> False
```

The descent never moves right; the first node at least 0 is 1, which is not 0.

Frame 4: `add(6)` h=1, then `add(5)` h=3, with its update array.

```text
before 5:
row 3: H -> 1
row 2: H -> 1 ------> 3
row 1: H -> 1 ------> 3
row 0: H -> 1 -> 2 -> 3 -> 4 -> 6
descent for 5:
  row 3: H->1, next None   update[3] = 1
  row 2: 1->3, next None   update[2] = 3
  row 1: at 3, next None   update[1] = 3
  row 0: 3->4, next 6 > 5  update[0] = 4
height 3: splice after 4 (row 0), 3 (rows 1, 2)
```

The update array names the exact splice point on each row the new node joins.

Frame 5: after `add(5)`, `search(5)`.

```text
row 3: H -> 1
row 2: H -> 1 ------> 3 ------> 5
row 1: H -> 1 ------> 3 ------> 5
row 0: H -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
path: row3 H->1 | row2 1->3 | row1 stay 3
      | row0 3->4, next 5 not < 5 -> stop
candidate = 4.forward[0] = 5 -> True
```

Three right moves across four rows reach 5; node 2 is never visited because row 2 jumped over it.

Frame 6: `erase(1)`.

```text
descent for 1: nothing < 1, update = [H, H, H, H]
node 1 has height 4: unlink on rows 0..3
row 3 now empty -> level 4 -> 3
row 2: H -> 3 -> 5
row 1: H -> 3 -> 5
row 0: H -> 2 -> 3 -> 4 -> 5 -> 6
```

Node 1 is removed from every row it was on, and the empty top row is retired.

Across all frames, every row was sorted, every row was a subset of the row below it, and each node appeared on rows
0..h-1 for its own height h. The descent always stopped on each row at the last node smaller than the target.

## Why it is correct

Invariant: each row i is a sorted linked list starting at the head, and it contains exactly the nodes whose height is
greater than i. Row 0 therefore contains every stored value in sorted order.

Search: on each row the walk stops at the last node with value smaller than the target (moving right only past
smaller values, stopping before the first value that is at least the target). Because row i+1 is a subset of row i, the node
where row i+1 stopped is also on row i and is smaller than the target, so starting row i from there skips only nodes
that are even smaller; nothing the target could equal is jumped over. At row 0, `update[0]` is the last node smaller than target, so `update[0].forward[0]` is the
first node at least target, and target is present iff that node equals it.

Add: `update[i]` is the last node smaller than num on row i, so splicing the new node right after it keeps row i
sorted. It is spliced exactly into rows 0..h-1, preserving "row i holds the nodes with height above i".

Erase: the found node is the first node with value num on row 0. On any row i it occupies, every node between
`update[i]` and it would have a value smaller than num (impossible, `update[i]` is the last such) or at least num and
before it on row 0 (impossible, it is the first). So it is exactly `update[i].forward[i]`, and bypassing it removes it
from that row while keeping the row sorted.

## Cost

- `search`, `add`, `erase`: O(log n) expected, from about log2 n rows and O(1) expected right moves per row.
- Worst case O(n) if the coin flips are very unlucky, which happens with vanishing probability.
- Space: O(n) expected; the expected height of a node is 2, so about 2n forward pointers.

Compare with the sorted linked list (O(n) per op) and the sorted Python list (O(log n) search, O(n) insert). A
balanced BST gives O(log n) worst case but with rotations; the skiplist trades a probabilistic guarantee for code
with only pointer splices.

## Variations you will meet

- **Probability p other than 1/2.** With p = 1/4 there are fewer pointers (about 4n/3) but more steps per row.
  Redis uses p = 1/4 in its sorted sets, which are skiplists.
- **Indexable skiplist.** Store on each forward pointer the number of row-0 nodes it skips. Then "k-th smallest" and
  "rank of x" are O(log n): sum the widths as you descend. This is the skiplist answer to "order statistics", and the
  basis of rolling medians in some libraries.
- **Range queries.** Search for the left end, then walk row 0 to the right end: O(log n + k).
- **Concurrent skiplists.** Because updates touch only a few local pointers and need no rebalancing, skiplists are
  the usual choice for lock-free ordered maps (Java's `ConcurrentSkipListMap`).

## What to carry forward

A skiplist is a sorted linked list with randomly assigned express lanes: ride the highest lane that does not
overshoot, drop a lane, repeat, and splice new nodes in at the drop points you recorded. This closes the chapter: every
tracker you built here, from a moving-average window to sorted boundaries, Fenwick blocks and version-stamped heaps,
came from the same move of asking which work repeats and choosing the structure that keeps the answer ready instead of
recomputing it.
