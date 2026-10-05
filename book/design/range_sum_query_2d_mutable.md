# Range Sum Query 2D - Mutable

*LeetCode 308 · Hard · Pattern: 2D Fenwick tree (binary indexed tree) + inclusion-exclusion · Reading time ~14 min*

## The problem

Design NumMatrix(matrix) with update(row, col, val), which sets one cell, and sumRegion(row1, col1, row2, col2), which
returns the sum of that inclusive rectangle. Updates and queries are interleaved, many of each.

```text
Example: matrix
  [[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]:
  sumRegion(2,1,4,3) -> 8; update(3,2,2); sumRegion(2,1,4,3) ->
  10.
```

## What the problem is really asking

You are handed a grid of integers. Two operations then interleave, many times each:

- `update(row, col, val)` overwrites one cell.
- `sumRegion(r1, c1, r2, c2)` returns the sum of the inclusive rectangle with those corners.

The answer to a query is a single integer. The difficulty is that neither operation is allowed to be slow. Make
updates trivial and queries walk the whole rectangle; make queries trivial with a precomputed table and every update
has to rewrite a big part of the table. You need a structure where both meet in the middle.

```text
matrix (0-indexed), query sumRegion(2,1,4,3)

        c0 c1 c2 c3 c4
  r0  [  3  0  1  4  2 ]
  r1  [  5  6  3  2  1 ]
  r2  [  1 |2  0  1| 5 ]
  r3  [  4 |1  0  1| 7 ]
  r4  [  1 |0  3  0| 5 ]
            +------+
  2+0+1 + 1+0+1 + 0+3+0 = 8

update(3,2,2): r3c2 goes 0 -> 2, same query -> 10
```

## Do it by hand first

If you had to answer many rectangle queries on paper with no updates, you would build a table of prefix sums once:
`P[r][c]` = sum of everything above and left of `(r, c)`. Then any rectangle is four lookups.

```text
rectangle = big - top strip - left strip + overlap

   +-----------+------+
   |  overlap  | top  |      want = P(bottom-right)
   +-----------+------+             - P(top band)
   |   left    | WANT |             - P(left band)
   +-----------+------+             + P(overlap, removed twice)
```

That is inclusion-exclusion, and it is half the answer. Now add one update: change `r3c2` from 0 to 2. Every prefix
sum whose rectangle contains `r3c2` is now wrong, which is every `P[r][c]` with `r >= 3` and `c >= 2`. On a 5 x 5
grid that is 6 entries; on a 200 x 200 grid it can be 40,000.

Your hand kept track of prefix sums. The seed is right: prefix sums plus inclusion-exclusion. What breaks is that a
prefix sum is one giant block, and one cell belongs to too many giant blocks.

## The first honest attempt

Two brute forces, opposite failures.

- Plain matrix: update is O(1), `sumRegion` loops over the rectangle, O(m n).
- 2D prefix table: `sumRegion` is O(1), update rewrites up to O(m n) entries.

The repeated work in the first is re-adding the same interior cells on every query. The repeated work in the second is
re-adding the same delta into thousands of table cells. Draw the second:

```text
update r3c2 by +2, prefix table P (1-indexed):
       c1 c2 c3 c4 c5
  r1   .  .  .  .  .
  r2   .  .  .  .  .
  r3   .  .  .  .  .
  r4   .  .  +  +  +     every entry right of and
  r5   .  .  +  +  +     below the cell changes
```

What we want is blocks of **varied** sizes: small enough that one cell is in only a few of them, but arranged so that
any prefix is the union of only a few of them. That is precisely a Fenwick tree.

## The turning point

**Claim: if block i covers the index range `(i - lowbit(i), i]`, where `lowbit(i)` is the value of the lowest set bit of
i, then every prefix `[1, k]` is the disjoint union of at most log2(k) + 1 blocks, and every index lies in at most
log2(n) + 1 blocks.**

Let us build this in one dimension first, from nothing.

**Lowbit.** Write an index in binary and keep only its lowest 1 bit. In two's complement, `i & -i` does exactly that.

```text
 i   binary   lowbit   block (i - lowbit, i]
 1   0001     1        [1]
 2   0010     2        [1..2]
 3   0011     1        [3]
 4   0100     4        [1..4]
 5   0101     1        [5]
 6   0110     2        [5..6]
 7   0111     1        [7]
 8   1000     8        [1..8]
```

Draw the blocks as bars over the array. Each bar ends at its own index and reaches back lowbit(i) cells.

```text
index:    1   2   3   4   5   6   7   8
a:        5   2   9   1   6   3   8   4

t[8]    [==============================]  38
t[4]    [==============]                  17
t[2]    [======]                           7
t[6]                    [======]           9
t[1]    [==]                               5
t[3]            [==]                       9
t[5]                    [==]               6
t[7]                            [==]       8
```

The array `t` stores, at index i, the sum of a over that bar. For this array:
`t = [_, 5, 7, 9, 17, 6, 9, 8, 38]`.

**Prefix sums as a binary decomposition.** Write k in binary, say k = 7 = 4 + 2 + 1. Read the bits from the low end:
the bar ending at 7 has length 1, covering [7]. Strip that bit: 6. The bar ending at 6 has length 2, covering [5..6].
Strip that bit: 4. The bar ending at 4 has length 4, covering [1..4]. Strip it: 0, done.

```text
prefix(7):  7 = 0111
  i = 7  (0111)  t[7] covers [7]       +8
  i = 6  (0110)  t[6] covers [5..6]    +9
  i = 4  (0100)  t[4] covers [1..4]    +17
  i = 0  stop                     sum = 34

  [1  2  3  4][5  6][7]
  |--- t4 ---|-t6--|t7|  tiles [1..7] exactly
```

Each step `i -= i & -i` removes the lowest set bit, so there is one step per 1 bit of k: at most log2(k) + 1 steps.
And the bars tile `[1, k]` with no overlap, because each bar starts exactly where the previous (higher) chunk of
bits leaves off. That is the binary representation of k, read as lengths.

**Point updates go the other way.** If a[3] changes by delta, which bars contain index 3? Bar 3 itself. Then the next
bar that reaches back over 3: add the lowbit, `3 + 1 = 4`, and bar 4 covers [1..4]. Again: `4 + 4 = 8`, bar 8 covers
[1..8]. Then 16, past the end.

```text
update index 3:  i = 3 -> 4 -> 8 -> (16 > n, stop)
  t[3] [3]         contains 3
  t[4] [1..4]      contains 3
  t[8] [1..8]      contains 3
  (t[5], t[6], t[7] start after 3: untouched)
```

Each `i += i & -i` pushes the lowest set bit upward, so i's lowbit at least doubles each step: at most log2(n) + 1
steps. Bars that contain index 3 are exactly the ones on this chain, because a bar ending at j > 3 reaches back to 3
only if its lowbit is large enough, which is the condition this walk follows.

So in 1D, both update and prefix are O(log n), and a range `[l, r]` is `prefix(r) - prefix(l-1)`.

**Two dimensions.** Apply the same trick independently on each axis. Node `tree[i][j]` stores the sum over rows
`(i - lowbit(i), i]` crossed with columns `(j - lowbit(j), j]`: a rectangular block. A prefix rectangle `P(r, c)` (the
first r rows and first c columns) decomposes rows into O(log m) row-bars, and inside each, columns into O(log n)
column-bars. So prefix is a nested loop: outer `i -= lowbit`, inner `j -= lowbit`. Update is the nested loop with `+=`.

```text
P(r, c) = sum over i on r's down-chain,
              sum over j on c's down-chain, tree[i][j]
```

Then `sumRegion` is inclusion-exclusion on four prefixes. With 0-indexed inputs and P counting rows and columns,
the rectangle `r1..r2, c1..c2` is `P(r2+1, c2+1) - P(r1, c2+1) - P(r2+1, c1) + P(r1, c1)`.

One more detail: Fenwick trees store sums, so they accept **deltas**, not new values. `update(row, col, val)` must add
`val - old`, which means you keep a plain copy of the matrix to know `old`.

## Watch it work

Same 5 x 5 matrix, 1-indexed in the tree. The built tree (row 0 and column 0 unused):

```text
tree   j=1  j=2  j=3  j=4  j=5
i=1      3    3    1    8    2
i=2      8   14    4   24    3
i=3      1    3    0    4    5
i=4     13   22    4   34   15
i=5      1    1    3    4    5
```

Frame 1: split the query `sumRegion(2,1,4,3)` into four prefixes.

```text
rows 2..4, cols 1..3 (0-indexed)
= P(5,4) - P(2,4) - P(5,1) + P(2,1)
   all     rows      cols    corner
          r0..r1    c0       r0..r1,c0
```

P counts rows and columns from the top-left corner, so P(5,4) is the first 5 rows and first 4 columns.

Frame 2: compute P(5,4).

```text
i chain: 5 -> 4 -> 0      j chain: 4 -> 0
tree[5][4] = 4    rows (4,5] x cols (0,4]
tree[4][4] = 34   rows (0,4] x cols (0,4]
P(5,4) = 38
```

Two row-bars (row 5 alone, rows 1..4) times one column-bar (cols 1..4): two nodes.

Frame 3: the other three prefixes.

```text
P(2,4): i 2->0, j 4->0   tree[2][4]          = 24
P(5,1): i 5->4->0, j 1   tree[5][1]+tree[4][1]
                         = 1 + 13            = 14
P(2,1): i 2, j 1         tree[2][1]          =  8
answer = 38 - 24 - 14 + 8 = 8
```

Six node reads in total answer a query that the brute force would sum cell by cell.

Frame 4: `update(3,2,2)`. Old value 0, delta +2. Tree index (4,3).

```text
i chain up: 4 -> 8 (>5 stop)
j chain up: 3 -> 4 -> 8 (>5 stop)
touch tree[4][3]: 4 -> 6
      tree[4][4]: 34 -> 36
```

Only two nodes contain cell (4,3): the block rows 1..4 x col 3, and rows 1..4 x cols 1..4.

Frame 5: re-run the query.

```text
P(5,4) = tree[5][4] + tree[4][4] = 4 + 36 = 40
P(2,4) = 24,  P(5,1) = 14,  P(2,1) = 8   (unchanged)
answer = 40 - 24 - 14 + 8 = 10
```

Only the prefix whose blocks included the updated cell moved, and by exactly the delta.

Throughout, every `tree[i][j]` equalled the sum of the matrix over its block, rows `(i - lowbit(i), i]` by columns
`(j - lowbit(j), j]`. Updates kept that true by adding the delta to every block containing the cell; queries relied on
it by tiling a prefix with blocks.

## Why it is correct

Invariant: `tree[i][j] = sum of vals[x][y]` for x in `(i - lowbit(i), i]` and y in `(j - lowbit(j), j]` (1-indexed),
and `vals` is the current matrix.

Prefix: the down-chain of r visits row-bars that tile `[1, r]` exactly once each (the binary decomposition of r).
The same holds for c. The cross product of the two tilings tiles the rectangle `[1, r] x [1, c]` exactly once, so the
nested sum equals P(r, c).

Update: a block contains cell (x, y) iff its row-bar contains x and its column-bar contains y. The up-chain from x
visits exactly the row-bars containing x, and likewise for y. So the nested walk adds the delta to exactly the blocks
containing the cell, preserving the invariant. Storing `vals` makes the delta correct.

Inclusion-exclusion: subtracting the top band and the left band removes the overlap twice, adding it back once
restores it, leaving exactly the rectangle.

## Cost

- Build: O(m n log m log n) by repeated updates as in the solution file (an O(m n) build exists but is rarely needed).
- `update`: O(log m · log n), one node per pair of steps on the two chains.
- `sumRegion`: four prefixes, each O(log m · log n).
- Space: O(m n) for the tree plus O(m n) for the value copy.

Compare: the plain matrix is O(1) update and O(m n) query; the prefix table is O(m n) update and O(1) query.

## Variations you will meet

- **Range Sum Query - Mutable (1D, LeetCode 307).** Drop the inner loop. This is the classic place to first meet a
  Fenwick tree, and a segment tree solves it equally well.
- **Count of Smaller Numbers After Self, Create Sorted Array through Instructions.** The Fenwick tree indexes values,
  not positions: "how many earlier elements are smaller than x" is `prefix(x - 1)` over a frequency array.
  Coordinate-compress first when values are large.
- **Range update, point query.** Store differences instead of values: add delta at l and subtract at r + 1, and a
  prefix sum recovers the point value. Range update with range query uses two Fenwick trees.
- **Row-wise 1D trees.** A simpler alternative keeps one 1D Fenwick tree per row: update O(log n), query O(m log n).
  Fine when rectangles are short.

## What to carry forward

A Fenwick tree tiles any prefix with one block per set bit and puts each point in one block per level, so `i -= i & -i`
walks a prefix down and `i += i & -i` walks an update up; do it on both axes and finish with inclusion-exclusion. The
next problem, Online Majority Element in Subarray, also answers questions about arbitrary subarrays under many queries,
but trades sums for counts and builds its index around each value's sorted positions.
