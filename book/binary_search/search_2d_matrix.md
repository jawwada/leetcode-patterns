# Search a 2D Matrix

*LeetCode 74 · Medium · Pattern: Binary search on a sorted array · Reading time ~6 min*

## What the problem is really asking

You get an m x n grid of integers with two promises: each row is sorted left to right, and the first number of each row
is bigger than the last number of the row above. Is the target somewhere in the grid? The answer is a yes or no.

```text
         c0  c1  c2  c3
row 0 [   1,  3,  5,  7 ]
row 1 [  10, 11, 16, 20 ]
row 2 [  23, 30, 34, 60 ]
target 3  -> True
target 13 -> False
```

What looks hard is the second dimension. A grid has no single "middle", and comparing with one cell seems to leave an
awkward L-shaped region alive. The real question is whether the grid is secretly one-dimensional.

## Do it by hand first

Read the grid the way you read a page: row 0 left to right, then row 1, then row 2.

```text
1  3  5  7 | 10 11 16 20 | 23 30 34 60
  row 0    |   row 1     |   row 2
```

Because each row is sorted and each row starts above where the previous one ended, the reading order is one sorted list
of 12 numbers. Looking for 13 by hand, you would check the row ends: 7 is too small, 20 is big enough, so 13 must be in
row 1. Then scan row 1: 10, 11, 16 — no 13.

What your hand kept track of was a position along that reading order. The grid was a way of printing a sorted list on
several lines, nothing more.

## The first honest attempt

Check every cell: O(m * n). It ignores both promises.

A better candidate answer is "walk from the top-right corner" (go left if too big, down if too small). That is O(m + n)
and works on a weaker kind of grid, but here it still wastes the second promise: it eliminates one row or one column per
step, while the rows in reading order form a single sorted list where one comparison could eliminate half the cells.

```text
corner walk for 13, from top-right:
  7 < 13 -> down      20 > 13 -> left
 16 > 13 -> left      11 < 13 -> down
 30 > 13 -> left      23 > 13 -> left ... off the grid
6 probes, each killing one row or one column
```

## The turning point

**Claim: a flat position k in the reading order corresponds to cell `(k // n, k % n)`, so you can binary search the
grid as if it were a sorted array of length m * n, without building that array.**

The mapping comes from how reading order counts. Each row holds n cells, so position k has passed `k // n` full rows and
then sits `k % n` cells into the next one. With n = 4:

```text
k :  0  1  2  3 |  4  5  6  7 |  8  9 10 11
r :  0  0  0  0 |  1  1  1  1 |  2  2  2  2   r = k // 4
c :  0  1  2  3 |  0  1  2  3 |  0  1  2  3   c = k % 4
```

So the algorithm is the closed-window exact lookup from the first problem, over positions `0 .. m*n - 1`. The only change
is that "read `nums[mid]`" becomes `r, c = divmod(mid, n)` and then `matrix[r][c]`. Nothing is copied; the flattening is
virtual.

The thing to get right is the divisor. You divide by the row *length* n (number of columns), not the number of rows m. On
a square grid the bug is invisible; on a 3 x 4 grid it reads the wrong cells or runs off the end.

## Watch it work

The 3 x 4 grid above, target 13 (absent). The strip is the reading order; P is "value < 13".

```text
Frame 1: lo=0 hi=11 mid=5 -> (r,c)=(1,1)
k        0   1   2   3   4   5   6   7   8   9  10  11
val      1   3   5   7  10  11  16  20  23  30  34  60
P        T   T   T   T   T   T   F   F   F   F   F   F
         L                   M                       H
```

`matrix[1][1] = 11 < 13`, so positions 0..5 are dead and `lo = 6`.

```text
Frame 2: lo=6 hi=11 mid=8 -> (r,c)=(2,0)
k        0   1   2   3   4   5   6   7   8   9  10  11
val      1   3   5   7  10  11  16  20  23  30  34  60
P        T   T   T   T   T   T   F   F   F   F   F   F
                                 L       M           H
```

`matrix[2][0] = 23 > 13`: the whole of row 2 is gone in one probe, `hi = 7`.

```text
Frame 3: lo=6 hi=7 mid=6 -> (r,c)=(1,2)
k        0   1   2   3   4   5   6   7   8   9  10  11
val      1   3   5   7  10  11  16  20  23  30  34  60
P        T   T   T   T   T   T   F   F   F   F   F   F
                               L/M   H
```

`matrix[1][2] = 16 > 13`: `hi = 5`.

```text
Frame 4: lo=6 hi=5 -> window empty, return False
k        0   1   2   3   4   5   6   7   8   9  10  11
P        T   T   T   T   T   T   F   F   F   F   F   F
                             H   L
in the grid: between (1,1)=11 and (1,2)=16
```

The window is empty. The border sits between 11 and 16, which is exactly where 13 would have been.

At every frame, the target, if present, would lie among the positions in `[lo, hi]`. The windows crossed rows freely
(frame 1 straddled all three rows) because the search never thinks about rows; it only folds a position back into the
grid when it needs a value.

## Why it is correct

The two promises make the reading-order sequence sorted: within a row by the first promise, across a row boundary by the
second. The `divmod` map is a bijection between positions `0 .. m*n - 1` and cells, and it preserves that order. So the
search is ordinary binary search on a sorted sequence, and the invariant from problem 1 carries over: if the target
exists, its position is in `[lo, hi]`. Every update discards only positions whose values are on the wrong side of the
target.

## Cost

Time O(log(m * n)) = O(log m + log n): one binary search over m * n positions, each probe O(1) with `divmod`. Space O(1);
the flat array is never built.

The two-step version (binary search the column of first elements to pick a row, then binary search that row) has the same
O(log m + log n) bound and twice as much code.

## Variations you will meet

- **Search a 2D Matrix II (LeetCode 240).** Rows sorted and columns sorted, but rows do *not* continue each other, so the
  reading order is not sorted and the flattening trick fails. Use the top-right corner walk, O(m + n). Rows and columns
  alone are not enough for a global order.
- **Kth smallest in a sorted matrix / multiplication table.** The grid is sorted along rows and columns but not globally.
  Instead of searching positions, binary search on the *value* and count how many cells are at most the guess. That is
  problem 13 in this chapter.
- **Return the position.** Return `divmod(mid, n)` instead of `True`.
- **Lower bound in the grid.** Use the half-open boundary template over `[0, m*n)`; the result position may be `m*n`
  (larger than everything).

## What to carry forward

If a structure can be read in an order that is sorted, binary search over positions in that order and convert a position
to a real address only when you need a value. The next problem breaks sortedness on purpose, with a rotation, and the
predicate changes from "smaller than target" to "on the high side of the cliff".
