# Range Module

*LeetCode 715 · Hard · Pattern: Sorted disjoint intervals with bisect · Reading time ~12 min*

## What the problem is really asking

You own a number line. Three operations arrive in any order:

- `addRange(l, r)` paints the half-open stretch `[l, r)` black.
- `removeRange(l, r)` paints `[l, r)` white.
- `queryRange(l, r)` asks: is every point of `[l, r)` black right now?

The answer to a query is a boolean, but the thing you must maintain is the whole painting: the set of tracked points,
which is always a union of disjoint stretches. Half-open matters. `[10, 20)` contains 10 and 19.999 but not 20, so
`[10,20)` and `[20,25)` touch and should merge into `[10,25)`, and removing `[14,16)` leaves 16 tracked.

```text
addRange(10,20); removeRange(14,16)

  10    12    14    16    18    20
   |#####|#####|     |#####|#####|
   [==========)      [==========)
   tracked     hole   tracked

queryRange(10,14) -> True   (inside the left block)
queryRange(13,15) -> False  (14 and 15 are white)
queryRange(16,17) -> True   (16 is tracked again)
```

What makes it hard: coordinates go up to 10^9, so you cannot store points; a single add can swallow dozens of
existing blocks; a single remove can split one block into two. The previous problem only ever added one point. Here
both endpoints of an operation can land anywhere, inside a block or in a gap, and the bookkeeping must not drown in
cases.

## Do it by hand first

Draw the line, then apply `addRange(10,20)`, `addRange(30,40)`, `removeRange(14,16)`, `addRange(15,32)`.

```text
after add(10,20), add(30,40):
  [10------20)        [30------40)

remove(14,16): cut a hole inside the first block
  [10--14)  [16--20)  [30------40)

add(15,32): paint from 15 to 32
  [10--14)  [16--20)  [30------40)
       ####################
          15              32
  15 sits in the hole -> new block edge at 15
  32 sits inside [30,40) -> no edge at 32
  every edge between 15 and 32 (16,20,30) is erased
  [10--14) [15-------------------40)
```

Look at what you actually wrote down. Not points, and not even "blocks" really: you wrote **edges**. 10, 14, 16, 20,
30, 40. A block opens at one edge and closes at the next. The add operation erased the edges inside `[15, 32]` and then
decided, for each end, whether that end becomes a new edge. That decision depended on one thing: was the end in a white
gap or inside a black block?

That is the seed: a sorted list of edges, and a way to tell inside from outside.

## The first honest attempt

Store every tracked integer in a set. `addRange` inserts `l..r-1`, `removeRange` deletes them, `queryRange` checks
each. Correct, and O(r - l) per operation. With coordinates up to 10^9 a single `addRange(0, 10**9)` never finishes.

The second honest attempt keeps a sorted list of `[start, end)` pairs and merges by hand: find overlapping pairs, take
min start and max end, splice. That works for add, but remove needs its own case analysis (the range may trim the
left of a block, the right, the middle, or cover it entirely) and query needs another. The code balloons and the bugs
hide in the edge cases where an end equals a boundary.

The waste in the point set is easy to draw:

```text
addRange(10,20) stores:
  10 11 12 13 14 15 16 17 18 19
  ^                          ^
  only these two facts matter: "opens at 10", "closes at 20"
  the 8 points in between carry no information
```

A contiguous block is described by its two boundaries. Everything between them is redundant.

## The turning point

**Claim: the tracked set is fully described by its sorted list of boundaries `[l0, r0, l1, r1, ...]`, and the parity of
a position in that list tells you whether a point is inside or outside.**

Lay the boundaries out as one flat list `ends`. Even indices open a block, odd indices close one. Now ask, for any
coordinate x, "how many boundaries are at or before x?" That count is the position where x would be inserted. If it is
odd, x is past an opener but not past its closer: x is inside a block. If it is even, x is in a gap.

```text
ends:   [ 10, 14, 16, 20, 30, 40 ]
index:     0   1   2   3   4   5
role:     op  cl  op  cl  op  cl

x =  12 -> insert pos 1 (odd)  -> inside [10,14)
x =  15 -> insert pos 2 (even) -> gap
x =  35 -> insert pos 5 (odd)  -> inside [30,40)
x =  50 -> insert pos 6 (even) -> gap
```

With parity in hand, every operation becomes the same three steps.

**addRange(l, r).** Find the slice of boundaries that lie inside `[l, r]`: `i = bisect_left(ends, l)`,
`j = bisect_right(ends, r)`. Everything in `ends[i:j]` is swallowed by the new paint, so delete it. Then decide the ends.
If i is even, l was in a gap, so l becomes a new opener. If j is even, r was in a gap, so r becomes a new closer. If i is
odd, l was inside a block, and that block's opener (left of i) stays as the opener of the merged block; similarly for
odd j. Replace `ends[i:j]` with whichever of `[l]`, `[r]` survived.

The choice of `bisect_left` for l and `bisect_right` for r is what makes touching blocks merge. If `l == 20` and 20 is
an existing closer, `bisect_left` places i at that closer (odd), so the closer gets deleted and the blocks join. If
`r == 30` and 30 is an existing opener, `bisect_right` places j after it (odd), so that opener is deleted too.

**removeRange(l, r).** The mirror image. Same two bisects, same slice delete. Now l becomes a boundary if it was
*inside* a block (odd i): the block that covered l must now close at l. And r becomes a boundary if it was inside a block
(odd j): the remainder of that block reopens at r.

**queryRange(l, r).** `[l, r)` is fully tracked iff l and r both sit inside the same block. Use
`i = bisect_right(ends, l)` and `j = bisect_left(ends, r)`. They must be equal (no boundary strictly between them) and
odd (that common position is inside a block). Here the sides flip: `bisect_right` for l so that l equal to an opener
counts as inside, and `bisect_left` for r so that a block closing exactly at r still covers `[l, r)`.

The whole data structure is one sorted list plus that rule:

```text
new boundaries for [l, r):
             add          remove
  l kept if  i even       i odd
  r kept if  j even       j odd
  then       ends[i:j] = kept
```

## Watch it work

Operations: add(10,20), add(30,40), remove(14,16), query(10,14), query(13,15), add(15,32), query(12,38).

Frame 1: add(10,20) on an empty list.

```text
ends []          i = bisect_left(10) = 0  (even)
                 j = bisect_right(20) = 0 (even)
keep l and r ->  ends[0:0] = [10, 20]
ends [10, 20]
```

Both ends in the gap, both become boundaries.

Frame 2: add(30,40).

```text
ends [10, 20]    i = 2 (even), j = 2 (even)
ends[2:2] = [30, 40]
ends [10, 20, 30, 40]
       op  cl  op  cl
```

A second, separate block.

Frame 3: remove(14,16).

```text
ends [10, 20, 30, 40]
          ^ 14 and 16 both insert at 1
i = bisect_left(14) = 1  (odd: 14 inside [10,20))
j = bisect_right(16) = 1 (odd: 16 inside [10,20))
keep both -> ends[1:1] = [14, 16]
ends [10, 14, 16, 20, 30, 40]
```

Nothing is deleted; the slice is empty. Two boundaries are inserted, splitting the block.

Frame 4: two queries.

```text
ends [10, 14, 16, 20, 30, 40]
idx    0   1   2   3   4   5
query(10,14): i = bisect_right(10) = 1
              j = bisect_left(14)  = 1  equal, odd -> True
query(13,15): i = bisect_right(13) = 1
              j = bisect_left(15)  = 2  differ      -> False
```

In the first query 14 is the closer itself, and `bisect_left` keeps j at 1, so a block ending exactly at r counts.

Frame 5: add(15,32).

```text
ends [10, 14, 16, 20, 30, 40]
               |--slice--|
i = bisect_left(15)  = 2 (even: 15 in the gap)  keep 15
j = bisect_right(32) = 5 (odd: 32 inside)       drop 32
ends[2:5] = [15]   deletes 16, 20, 30
ends [10, 14, 15, 40]
```

Three boundaries vanish at once, one is added, and the gap between `[16,20)` and `[30,40)` is painted over.

Frame 6: query(12,38).

```text
ends [10, 14, 15, 40]
i = bisect_right(12) = 1
j = bisect_left(38)  = 3   differ -> False
```

The point 14 is still white, and the boundaries 14 and 15 between the query's ends say so.

In every frame `ends` stayed strictly increasing with even length, so even positions are openers and odd positions are
closers. Each operation touched only one contiguous slice of the list.

## Why it is correct

The invariant: `ends` is strictly increasing, has even length, and the tracked set is exactly the union of
`[ends[2k], ends[2k+1])`. Strictly increasing also means no empty blocks and no touching blocks, since a touch would
appear as a closer equal to the next opener.

Take `addRange(l, r)`. After the operation, the tracked set should be the old set union `[l, r)`. Outside `[l, r]`
nothing changes, and the boundaries outside the slice are untouched. Inside, the new set is all black, so it must have
no boundaries strictly inside, which is why the slice is deleted. At l, the line goes from "whatever was left of l" to
black. If l was in a gap (even i), that is a white-to-black change, so l must be an opener. If l was inside a block
(odd i), the line was already black left of l, so no boundary belongs there; the existing opener at index i - 1
continues the block. The same logic at r gives "keep r iff j is even". The parity of the new list stays consistent:
the kept boundary at l lands at an even index exactly when i was even.

The bisect sides handle equality. A closer equal to l means the old block ends exactly where the new one begins; the
blocks touch, so that closer must go, and `bisect_left` includes it in the slice. An opener equal to r is symmetric
with `bisect_right`.

`removeRange` is the same argument with black and white swapped. `queryRange` asks whether `[l, r)` contains no
white point. Every boundary strictly between l and r would mark a colour change, so there must be none (`i == j`),
and the colour there must be black (odd).

## Cost

- Each operation: two binary searches, O(log n), plus one slice assignment, O(n) worst case in a Python list because
  the tail shifts, where n is the number of boundaries.
- Amortised, the boundaries an add deletes were each inserted once, so the deletions are paid for in advance.
- Space: O(n) boundaries, at most two per operation ever performed.

A balanced tree (TreeMap in Java) brings the splice to O(log n + deleted). A segment tree over compressed or dynamic
coordinates gives O(log C) per operation when coordinates are known in advance.

## Variations you will meet

- **Data Stream as Disjoint Intervals (the previous problem).** Points instead of ranges, closed intervals, merging on
  adjacency. With boundaries in half-open form, adding v is simply `addRange(v, v + 1)`, and the touching rule does the
  merging for you.
- **My Calendar I / II / III.** Calendar I asks whether a new booking overlaps anything: a query with "all white"
  instead of "all black". Calendar III counts maximum overlap, where boundaries need counts, not just parity: a sweep
  over a sorted map of `+1` at start and `-1` at end.
- **Count tracked length.** Sum `ends[2k+1] - ends[2k]`. To keep it live, subtract the lengths in the deleted slice
  and add the new ones.
- **Segment tree with lazy assignment.** When an interviewer wants guaranteed O(log C) per operation, build a dynamic
  segment tree whose nodes store "fully tracked / fully untracked / mixed", with lazy set-to-black and set-to-white.

## What to carry forward

A union of disjoint intervals is an alternating list of boundaries; parity of a bisect position tells inside from
outside, and any range edit is "delete the slice, re-insert at most two ends". The next problem, Range Sum Query 2D
Mutable, keeps the theme of answering range questions under updates but swaps "is it covered?" for "what is the sum?",
and introduces the Fenwick tree.
