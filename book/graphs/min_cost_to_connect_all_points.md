# Min Cost to Connect All Points
*LeetCode 1584 · Medium · Pattern: Minimum spanning tree (Prim's with heap) · Reading time ~9 min*

## The problem

Given n points on a plane, connecting two points costs their Manhattan distance |x1-x2| + |y1-y2|. Return the minimum
total cost to connect all points so that there is a path between every pair, i.e. the weight of a minimum spanning
tree of the complete graph.

```text
Example: [[0,0],[2,2],[3,10],[5,2],[7,0]] -> 20.
```

## What the problem is really asking

You get `n` points on a grid. Linking two points costs their Manhattan distance
`|x1-x2| + |y1-y2|`. Pick links so that every point can reach every other (directly or
through others), paying as little as possible in total.

Any cheapest answer has no cycle (drop one cycle link and everything stays connected, for
less), so it is a tree touching all `n` points: `n - 1` links. This object is a **minimum
spanning tree** (MST). The graph is complete: every pair is a candidate link.

```text
  points                         chosen links (total 20)
  y                              P0-P1  4
  10 .  .  .  P2 .  .  .  .      P1-P3  3
     :                           P3-P4  4
   2 .  .  P1 .  .  P3 .  .      P1-P2  9
   0 P0 .  .  .  .  .  .  P4
     0  1  2  3  4  5  6  7  x

  stored as a distance table (complete graph):
        P0  P1  P2  P3  P4
    P0   0   4  13   7   7
    P1   4   0   9   3   7
    P2  13   9   0  10  14
    P3   7   3  10   0   4
    P4   7   7  14   4   0
```

What makes it hard: the number of spanning trees is astronomical, and a cheap-looking local
choice (link each point to its nearest neighbour) can leave the set in separate clumps.

## Do it by hand first

Start with one point, say `P0`, and call it "the blob". Repeatedly draw the shortest line
from any blob point to any non-blob point, and absorb that point.

```text
  blob {P0}           shortest out: P0-P1 4
  blob {P0,P1}        shortest out: P1-P3 3
  blob {P0,P1,P3}     shortest out: P3-P4 4
  blob {P0,P1,P3,P4}  shortest out: P1-P2 9
  all in, total 4+3+4+9 = 20
```

Your hand kept **which points are in the blob** and **a list of candidate lines leaving the
blob**, choosing the shortest each time. That is a visited array and a min-heap.

## The first honest attempt

List all `n(n-1)/2` links, sort them, and walk the list: accept a link if its endpoints are
not already connected through accepted links, checked by a DFS over the accepted links.

```text
  sorted: 3 P1P3, 4 P0P1, 4 P3P4, 7 P0P3, 7 P0P4, 7 P1P4, 9 P1P2
  7 P0P3: DFS from P0 over accepted links -> reaches P3, reject
  7 P0P4: DFS from P0 again              -> reaches P4, reject
  7 P1P4: DFS from P1 again              -> reaches P4, reject
          the same component re-walked for every candidate
```

Sorting is `O(n^2 log n)` and each of `O(n^2)` checks can cost `O(n)`: `O(n^3)`. The waste
is rediscovering connectivity by traversal. Union-find answers "same component?" in near
`O(1)`, and that version is Kruskal's algorithm. But is greedy even right?

## The turning point

**Claim (the cut property): split the points into any two non-empty groups; the cheapest
link crossing between the groups belongs to some minimum spanning tree.**

```text
     blob S              outside
   +--------+          +--------+
   |   P0   |  ======  |   P2   |
   |   P1   |   cut    |   P3   |
   +--------+  ======  |   P4   |
                       +--------+
   links crossing the cut, cheapest first:
     P1-P3 3  <- e, safe
     P0-P3 7, P0-P4 7, P1-P4 7, P1-P2 9, P0-P2 13
   (P0-P1 lies inside S, so it does not cross)
```

Why: take any MST `T` that does not use `e`. Adding `e` to `T` creates a cycle, and that
cycle crosses the cut once via `e`, so it must cross back via some other link `f`. Remove
`f`. Still spanning, still a tree, and the weight changed by `w(e) - w(f) <= 0`. So a tree
using `e` is at least as cheap: `e` is safe.

Both classic algorithms are this claim with a different choice of cut.

- **Prim** cuts between the blob and the rest, every step. The heap holds `(cost, point)`
  for links from blob members to outside points; pop the cheapest whose point is still
  outside. When a point joins, push its distance to every outside point. A popped point
  that is already in the blob is a stale entry: skip it.
- **Kruskal** sorts all links; a link joining two different union-find components is the
  cheapest link crossing the cut around either component, so it is safe.

On a complete graph Prim is the natural fit: it never builds the sorted list of all
`n(n-1)/2` links up front.

## Watch it work

Prim from `P0`. The heap is shown sorted as `cost:point`.

```text
Frame 1  pop 0:P0  (seed)    blob {P0}  total 0
  push 4:P1 7:P3 7:P4 13:P2
  heap [4:P1 7:P3 7:P4 13:P2]
```
The seed costs 0; its four distances become the first candidates.

```text
Frame 2  pop 4:P1            blob {P0,P1}  total 4
  push 3:P3 7:P4 9:P2
  heap [3:P3 7:P3 7:P4 7:P4 9:P2 13:P2]
```
P1 offers a cheaper route to P3 (3 beats 7); both entries sit in the heap.

```text
Frame 3  pop 3:P3            blob {P0,P1,P3}  total 7
  push 4:P4 10:P2
  heap [4:P4 7:P3 7:P4 7:P4 9:P2 10:P2 13:P2]
```
The cheapest crossing link wins even though it starts from P1, not the newest member.

```text
Frame 4  pop 4:P4            blob {P0,P1,P3,P4}  total 11
  push 14:P2
  heap [7:P3 7:P4 7:P4 9:P2 10:P2 13:P2 14:P2]
```
Only P2 is left outside; the 7s on top are all stale.

```text
Frame 5  pop 7:P3 skip, 7:P4 skip, 7:P4 skip
         pop 9:P2            blob = all  total 20
  heap [10:P2 13:P2 14:P2]   stop: n points added
```
Stale entries are skipped without adding cost; the answer is 20.

Invariant across frames: the accepted links always formed one tree over the blob, and that
tree is contained in some MST.

## Why it is correct

Induction on the blob. Initially the empty set of links is contained in every MST. At each
step the heap's top valid entry is the cheapest link from the blob to outside: every
blob member pushed its distance to every outside point when it joined, so all crossing
links are present. By the cut property, with the cut "blob versus rest", adding that link
keeps the accepted set inside some MST. After `n - 1` additions the accepted set is a
spanning tree contained in an MST, so it is one.

## Cost

- **Prim with a heap:** `O(n^2 log n)` time (each of `n` joins pushes up to `n` entries),
  `O(n^2)` space for the heap.
- **Prim with an array:** keep `best[j]`, the cheapest link from the blob to `j`, and scan
  it for the minimum each step: `O(n^2)` time, `O(n)` space, optimal for a complete graph.
- **Kruskal:** `O(n^2 log n)` time for the sort, `O(n^2)` space for the edge list.

## Variations you will meet

- **Sparse graph given as an edge list** (Connecting Cities With Minimum Cost, LeetCode
  1135). Kruskal with union-find is simplest; return `-1` if fewer than `n - 1` links join.
- **Optimize Water Distribution (LeetCode 1168).** A well at a house is a link to a virtual
  node 0; then plain MST.
- **Maximum spanning tree or bottleneck path.** Same algorithms with the order reversed;
  the MST also contains the minimax path between any two points (Swim in Rising Water).

## What to carry forward

The cheapest link across any cut is safe; Prim grows one blob with a heap of crossing
links, Kruskal merges components with sorted links and union-find. The next problem runs
Kruskal many times, excluding or forcing one edge each run, to decide which edges every
MST needs and which only some MSTs use.
