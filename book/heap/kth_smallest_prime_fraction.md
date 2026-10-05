# K-th Smallest Prime Fraction

*LeetCode 786 · Hard · Pattern: k-way merge with a heap (merge k sorted feeds) · Reading time ~9 min*

## The problem

arr is sorted and contains 1 and distinct primes. Consider every fraction arr[i] / arr[j] with i < j and return the
k-th smallest as [arr[i], arr[j]].

```text
Example: arr=[1,2,3,5], k=3 -> [2,5] (the fractions in order are
  1/5, 1/3, 2/5, 1/2, 3/5, 2/3).
```

## What the problem is really asking

You get a sorted array `arr` that starts with 1 and then holds distinct primes, for example `[1, 2, 3, 5]`. Form every fraction `arr[i] / arr[j]` with `i < j`, so the numerator is always the smaller number and every fraction is below 1. Return the `k`-th smallest of these fractions as the pair `[numerator, denominator]`.

The answer is one pair of indices out of `n(n-1)/2` candidates. What makes it hard is that the candidates are never given to you as a list. They exist only implicitly, as a triangle of pairs, and you do not want to build all of them when `k` is small.

```text
arr = [1, 2, 3, 5]   k = 3

all fractions, sorted:
  1/5  1/3  2/5  1/2  3/5  2/3
  .20  .33  .40  .50  .60  .67
             ^
          3rd smallest  -> [2, 5]
```

## Do it by hand first

Write the fractions as a grid. The row is the numerator and the column is the denominator. Only cells to the right of the diagonal exist, because the numerator must come earlier in the array.

```text
            den:  2      3      5
num 1   |       1/2    1/3    1/5
num 2   |        -     2/3    2/5
num 3   |        -      -     3/5

  along a row, moving right: bigger denominator,
  smaller value  ->  each row is sorted RIGHT to LEFT
```

Asked to find the smallest fractions by hand, nobody scans the whole grid. You notice that the rightmost column (denominator 5, the largest) holds each row's smallest entry. The smallest of those, 1/5, is the overall smallest. Then you ask: what comes next? It is either another entry of that last column (2/5, 3/5), or the next cell leftward in row 1 (1/3). You keep, per row, a finger on "the smallest entry of this row I have not taken yet", and you take the smallest finger.

That is exactly the frontier from Merge k Sorted Lists. Each row is a sorted list (read right to left), and the fingers are the list heads.

## The first honest attempt

Build all `n(n-1)/2` fractions, sort them, return entry `k - 1`. That costs O(n^2 log n) time and O(n^2) space. With `n = 1000` that is about half a million fractions, sorted just to read one of them.

The waste comes in two forms. First, the sort spends effort ordering fractions near the top of the list, such as `997/1000` against `991/1000`, when only the bottom `k` can matter. Second, it re-derives orderings that are already known for free. Within row `i`, `arr[i]/arr[j]` decreases as `j` grows, so the sort is comparing pairs whose order is obvious:

```text
row 1:  1/2 > 1/3 > 1/5      known without comparing
row 2:        2/3 > 2/5      known without comparing
sort still does:  1/2 ? 1/3,  1/3 ? 1/5,  2/3 ? 2/5 ...
```

## The turning point

**Claim: the grid is `n - 1` sorted lists, one per numerator, so the `k`-th smallest fraction is the `k`-th item of their k-way merge, and you can stop merging after `k` steps.**

Each row `i` read from right to left (`j = n-1, n-2, ..., i+1`) is sorted ascending, because the numerator is fixed and the denominator shrinks. Any sorted feed can go into a k-way merge. The merge produces items in globally sorted order, one per pop, so the `k`-th pop is the answer. You never have to finish the merge.

Turning the claim into an algorithm uses the same tuple shape as the linked-list merge, with indices in place of node pointers:

- Seed: for every row `i < n - 1`, push `(arr[i] / arr[n-1], i, n-1)`. That is the rightmost column, each row's smallest entry.
- Pop `k - 1` times. After popping `(value, i, j)`, if `j - 1 > i`, push row `i`'s next entry `(arr[i] / arr[j-1], i, j-1)`. The condition keeps you to the right of the diagonal.
- The heap root is now the `k`-th smallest. Read `[arr[i], arr[j]]` from it.

The direction is the main trap. Rows are sorted toward the left, so the refill step goes to `j - 1`, not `j + 1`. Push `j + 1` and you will walk off the grid or produce fractions in the wrong order.

Floating-point values are safe as keys here. The values are at most 30,000 and all distinct primes, so two different fractions never collide as doubles. If you prefer exact arithmetic, compare `a/b < c/d` as `a*d < c*b`.

## Watch it work

`arr = [1, 2, 3, 5]`, `k = 3`. Heap entries are drawn as the fraction itself. In the grid, `[ ]` marks cells currently in the heap and `x` marks cells already popped.

Frame 1: seed the heap with the last column.

```text
         2     3     5
  1 |   1/2   1/3  [1/5]          1/5
  2 |    -    2/3  [2/5]         /   \
  3 |    -     -   [3/5]       2/5   3/5

array: [1/5, 2/5, 3/5]      pops done: 0
```

Every row has its finger on its smallest entry, and the root is the global minimum.

Frame 2: pop 1/5 (row 1, col 5). Its row moves one cell left: push 1/3.

```text
         2     3     5
  1 |   1/2  [1/3]   x            1/3
  2 |    -    2/3  [2/5]         /   \
  3 |    -     -   [3/5]       3/5   2/5

array: [1/3, 3/5, 2/5]      pops done: 1  (1st = 1/5)
```

`1/3` was pushed at the bottom and sifted up past `2/5`, the old root's replacement.

Frame 3: pop 1/3 (row 1, col 3). Push row 1's next cell, 1/2.

```text
         2     3     5
  1 |  [1/2]   x     x            2/5
  2 |    -    2/3  [2/5]         /   \
  3 |    -     -   [3/5]       3/5   1/2

array: [2/5, 3/5, 1/2]      pops done: 2  (2nd = 1/3)
```

`k - 1 = 2` pops are done, so the loop stops.

Frame 4: read the root.

```text
root = 2/5  at (i=1, j=3)  ->  [arr[1], arr[3]] = [2, 5]

visited cells form a staircase from the right edge:
         2     3     5
  1 |    o     x     x
  2 |    -     .     o       x popped   o in heap
  3 |    -     -     o       . never touched
```

Only 5 of the 6 cells were touched. For large `n` and small `k`, almost all of the grid is never touched.

Frame 5 (what more pops would do, if `k` were 6):

```text
pop 2/5 -> push 2/3   array [1/2, 3/5, 2/3]
pop 1/2 -> row 1 done array [3/5, 2/3]
pop 3/5 -> row 3 done array [2/3]
root 2/3 = 6th smallest, the largest fraction
```

Throughout, the heap held exactly one cell per row that still had untaken cells, namely that row's smallest untaken cell. The popped cells, in order, were the sorted fractions.

## Why it is correct

**Invariant.** After `t` pops: (a) the popped fractions are the `t` smallest, in increasing order; (b) for every row with untaken cells, the heap holds its smallest untaken cell, which is the leftmost-popped position's left neighbour, or the rightmost cell if nothing has been taken from the row.

Every untaken cell in row `i` is at least row `i`'s heap entry, because the row increases leftward from the finger. So the heap root is the smallest untaken fraction overall. Popping it extends (a) by one. Pushing its left neighbour (if the neighbour is right of the diagonal) restores (b) for that row, and other rows are unaffected. After `k - 1` pops, (a) says the `k - 1` smallest are gone, and the root, the smallest of the rest, is the `k`-th smallest.

Distinct primes matter in one small way: all fractions are distinct, so "the `k`-th smallest" is unambiguous.

## Cost

- **Heap merge: O(n + k log n) time, O(n) space.** Heapify of `n - 1` seeds is O(n). Each of the `k - 1` steps is one pop and at most one push on a heap of at most `n - 1` entries.
- **Brute force: O(n^2 log n) time, O(n^2) space.**
- **When `k` is close to `n^2`**, the heap degrades to O(n^2 log n) as well. The alternative is binary search on the value. Guess `m` in `(0, 1)`. Count fractions below `m` with a two-pointer sweep over the grid in O(n), and remember the largest fraction found below `m`. If the count is less than `k`, raise `m`. If it is more, lower it. Once the count equals `k`, the largest fraction below `m` is the answer. Each guess is O(n), and the number of guesses depends on precision (about 60 for doubles), so the total is independent of `k`.

## Variations you will meet

- **Kth Smallest Element in a Sorted Matrix (LeetCode 378).** Rows and columns both sorted. The same heap works (seed with column 0, refill with `col + 1`). Binary search on the value with a staircase count is the alternative, exactly as here.
- **Find K Pairs with Smallest Sums (LeetCode 373).** The implicit grid is `nums1[i] + nums2[j]`. Rows are sorted left to right, so seed column 0 for each `i` and refill with `j + 1`.
- **K-th Smallest Number in Multiplication Table (LeetCode 668).** Here `m * n` can be about `9 * 10^8`, far too many for any heap. Only the binary search on the value survives. This is the case that shows why the second level in Cost exists.
- **Return all fractions up to the k-th.** Collect the `k` pops in order instead of discarding them. The cost is unchanged.

## What to carry forward

When the input is a set of pairs, look for an implicit grid whose rows are sorted. If you find one, the k-th smallest is a k-way merge stopped after `k` pops, with `(value, row, col)` tuples and the refill going in the row's sorted direction.

The next problem, Smallest Range Covering Elements from K Lists, runs the same merge over real lists but asks a different question at each pop. Besides the minimum it tracks the running maximum, and the window between the two is what gets scored.
