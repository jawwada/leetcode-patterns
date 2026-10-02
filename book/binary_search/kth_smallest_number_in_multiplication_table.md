# Kth Smallest Number in Multiplication Table

*LeetCode 668 · Hard · Pattern: Binary search on the answer · Reading time ~10 min*

## What the problem is really asking

Picture the `m x n` multiplication table from primary school, where cell `(i, j)` holds `i · j` with rows and columns numbered from 1. Pour every cell's value into one bag, duplicates included, sort the bag, and read off the `k`-th value.

The answer is a single value from the table. What makes it hard is size: `m` and `n` can each be 30,000, so the table holds up to 9 · 10^8 numbers. We cannot write them down, let alone sort them. We need the k-th smallest of a multiset we are not allowed to build.

```text
m = 3, n = 3, k = 5

        j=1  j=2  j=3
  i=1    1    2    3
  i=2    2    4    6
  i=3    3    6    9

sorted bag: 1 2 2 3 3 4 6 6 9
            1 2 3 4 5 6 7 8 9   <- rank
                    ^
              k=5  -> answer 3
```

## Do it by hand first

Asked for the 5th smallest, most people don't sort. They ask "how many cells are 3 or less?" and count. Row 1 has 1, 2, 3, so 3 cells. Row 2 has just the 2, so 1 cell. Row 3 has just the 3, so 1 cell. That's 5 in total, so the 5th smallest is at most 3. "How many are 2 or less?" Row 1 has 2, row 2 has 1, row 3 has 0, so 3 in total, which is fewer than 5. So the 5th smallest is more than 2, and therefore exactly 3.

```text
cells <= 3            cells <= 2
  [1][2][3]             [1][2] 3
  [2] 4  6              [2] 4  6
  [3] 6  9               3  6  9
count = 3+1+1 = 5     count = 2+1+0 = 3
```

Your hand kept **a threshold and a count of cells at or below it**, and it counted each row without reading every cell: row `i` is `i, 2i, 3i, ...`, so the cells at or below `v` are the first `v // i` of them, capped at `n`. That one division per row is the seed of the algorithm.

## The first honest attempt

"Generate all `m · n` products, sort, return index `k - 1`." That is O(mn log mn) time and O(mn) space, which is 9 · 10^8 numbers in the worst case. Too much memory and far too slow.

A smarter candidate says: "Each row is sorted, so merge the `m` rows with a min-heap and pop `k` times." That is O(k log m), but `k` can be as large as `mn`, so it does not help in the worst case.

```text
heap merge, popping k=5 times:
  pop 1 (row1)  push 2 (row1)
  pop 2 (row1)  push 3 (row1)
  pop 2 (row2)  push 4 (row2)
  pop 3 (row1)  -- row1 done
  pop 3 (row3)  -> 5th = 3
every pop handles ONE cell; for k near mn we
touch nearly every cell anyway
```

The waste in both is that we materialise individual cells to find a rank, when the table's structure (every row is an arithmetic progression) lets us count whole runs of cells at once.

## The turning point

**Claim: `count(v)`, the number of cells `<= v`, can be computed in O(m) without looking at any cell, and the answer is the smallest `v` with `count(v) >= k`.**

*Counting.* Row `i` contains `i, 2i, ..., n·i`. The entries at or below `v` are `i · 1, ..., i · j` for every `j <= v / i`, so there are `min(n, v // i)` of them. Summing over the rows:

```text
count(v) = sum over i = 1..m of  min(n, v // i)
```

Geometrically, the cells at or below `v` form a staircase hugging the top-left corner: the region under the hyperbola `i · j = v`. Each row's step is shorter than the one above it.

```text
v = 5, 3x3 table        row count
  [1][2][3]             min(3, 5//1) = 3
  [2][4] 6              min(3, 5//2) = 2
  [3] 6  9              min(3, 5//3) = 1
                        count(5)     = 6
staircase edge follows i*j = 5
```

*The predicate* is `enough(v) = count(v) >= k`: are there at least `k` cells at or below `v`?

*Monotone.* Raising `v` can only add cells to the staircase, never remove one, so `count` is non-decreasing and `enough` reads `F ... F T ... T` over `v`. We binary search for the **first T** on `[1, m · n]`, where 1 is the smallest cell and `m · n` the largest.

*Why the first T is the k-th smallest.* Let `x` be the true k-th smallest value. At least `k` cells are `<= x` (the first `k` in sorted order), so `enough(x)` is true. At most `k - 1` cells are `<= x - 1`, because the k-th one is `x` itself, so `enough(x - 1)` is false. So `x` is exactly the F|T boundary.

```text
v      :  1  2  3  4  5  6  7  8  9
count  :  1  3  5  6  6  8  8  8  9
enough :  F  F  T  T  T  T  T  T  T     (k = 5)
                ^
          first T = 3
```

*A subtle point.* The search probes values that are not in the table at all, such as 5 or 7 here. That is fine. The first T is always a real table value, because `count` jumps from below `k` to at least `k` exactly there, and `count` only jumps at values that occur in the table. Values like 5 sit in the flat stretches where nothing new is added.

Compare this with the first eight problems. There we searched over *positions* in a sorted array, and the array told us its value at each position. Here the sorted array (the bag) exists only in our heads, so we cannot ask "what value sits at rank `k`?". We can ask the reverse question, "what rank does value `v` reach?", and that is enough. The binary search runs over values, and `count` converts each value into a rank. Any time you can cheaply turn a value into a rank, the k-th smallest is a first-T search.

One practical refinement: loop over the shorter dimension. Swap `m` and `n` if needed so that each count is O(min(m, n)).

## Watch it work

`m = 3`, `n = 3`, `k = 5`. The search range is `[1, 9]`.

```text
Frame 1   lo=1  hi=9
  answer line: 1 2 3 4 5 6 7 8 9
               L               H
```
The range covers every value the table can hold.

```text
Frame 2   lo=1  hi=9  mid=5
  [1][2][3]   3
  [2][4] 6    2
  [3] 6  9    1     count=6 >= 5  T
```
At least five cells are at or below 5, so the answer is at most 5: `hi = 5`. Note that 5 itself is not in the table.

```text
Frame 3   lo=1  hi=5  mid=3
  [1][2][3]   3
  [2] 4  6    1
  [3] 6  9    1     count=5 >= 5  T
```
Exactly five cells are at or below 3, so still enough: `hi = 3`.

```text
Frame 4   lo=1  hi=3  mid=2
  [1][2] 3    2
  [2] 4  6    1
   3  6  9    0     count=3 <  5  F
```
Only three cells are at or below 2, so the k-th is bigger than 2: `lo = 3`.

```text
Frame 5   lo=3  hi=3   stop, answer 3
  sorted bag: 1 2 2 | 3 3 | 4 6 6 9
              <=2: 3  ^ the 4th and 5th are 3
```
`lo == hi == 3`. The count jumped from 3 (at `v=2`) to 5 (at `v=3`), so 3 occupies ranks 4 and 5, and rank 5 is the one we want.

The staircase only ever grew or shrank as `mid` moved, and every value below `lo` was known to have too few cells under it. We never listed a cell; each frame was three divisions.

## Why it is correct

**Invariant: `enough(hi)` is true and `enough(lo - 1)` is false (or `lo = 1`).** It holds at the start because `count(m·n) = m·n >= k`. On T, `hi = mid` keeps `enough(hi)`. On F, monotonicity makes everything at or below `mid` false, so `lo = mid + 1` keeps the left side false. The window shrinks every step because `mid < hi`. At termination `lo` is the first value with `count >= k`, which by the argument above is the k-th smallest. It is guaranteed to be a table value because `count(lo) > count(lo - 1)` means at least one cell equals `lo`.

## Cost

- **Sort everything:** O(mn log mn) time, O(mn) space.
- **Heap merge:** O(k log m) time, O(m) space.
- **Binary search on value:** O(min(m, n) · log(mn)) time. There are about 30 probes for `mn = 9 · 10^8`, each summing one division per row. **O(1)** space.

## Variations you will meet

- **Kth Smallest Element in a Sorted Matrix (LeetCode 378).** The rows and columns are sorted but arbitrary, so there is no formula per row. Count with a staircase walk from the bottom-left corner in O(m + n) per probe. The search range is `[matrix[0][0], matrix[-1][-1]]`.
- **K-th smallest prime fraction (LeetCode 786).** The answer is a real number. Binary search on `x` in `(0, 1)` and count fractions `<= x` with two pointers, remembering the largest fraction under `x` to recover the exact answer.
- **Count of cells strictly less than v.** Use `(v - 1) // i`. Mixing up `<` and `<=` shifts the answer by one rank.
- **Find the k-th largest.** Use the (`mn - k + 1`)-th smallest and do not change the machinery.

## What to carry forward

To find the k-th smallest of a huge implicit set, binary search on the value and count how many elements are at or below it. The answer is the first value whose count reaches `k`, and it always lies in the set.

The next problem uses the same "count at or below `d`" search, but the counting is done by a two-pointer window over a sorted array instead of a division per row.
