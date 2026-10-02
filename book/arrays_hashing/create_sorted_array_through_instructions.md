# Create Sorted Array through Instructions
*LeetCode 1649 · Hard · Pattern: Fenwick tree over values (order-statistics counting) · Reading time ~11 min*

## What the problem is really asking

You build a sorted container by inserting the numbers of `instructions` one at a time, in the given order. Inserting `x` has a cost: look at what is already in the container, count the elements strictly smaller than `x` and the elements strictly larger than `x`, and pay the smaller of the two counts. Equal elements are free: they count as neither. Return the total cost modulo 1e9+7.

The answer is one number, a sum of n small costs. What makes it hard is that each cost is a question about the *current* contents, which change after every step. Merge sort answered "how many smaller" for everyone at once, offline. Here the questions arrive online, interleaved with insertions, and n can be 10^5, so anything quadratic is too slow.

```text
instructions = [4, 8, 1, 6, 5, 2]

insert  container before   smaller  larger  cost
  4     {}                    0       0      0
  8     {4}                   1       0      0
  1     {4,8}                 0       2      0
  6     {1,4,8}               2       1      1
  5     {1,4,6,8}             2       2      2
  2     {1,4,5,6,8}           1       4      1
                                     total = 4
```

## Do it by hand first

With pen and paper you would not keep a sorted list and shuffle it. You would draw a number line from 1 to 8 and put a tick mark above a value each time it is inserted. To price an insertion of `x`, count the ticks strictly left of `x` and the ticks strictly right of `x`.

```text
after inserting 4, 8, 1, 6:
ticks:    |           |       |       |
value:    1   2   3   4   5   6   7   8
inserting 5:
          <- left of 5: 2 ->  <- right: 2 ->
          cost = min(2, 2) = 2
```

What your hand kept track of was a *histogram over values*: `cnt[v]` = how many times `v` has been inserted. "Smaller than `x`" is the sum `cnt[1] + ... + cnt[x-1]`, a prefix sum. "Larger than `x`" is everything inserted so far minus the prefix sum up to `x`. That histogram is the seed of the data structure; the rest of this problem is about making its prefix sums fast.

## The first honest attempt

Keep a real sorted Python list. For each `x`, `bisect_left` gives the number of smaller elements, `len(arr) - bisect_right` gives the number of larger elements, and `insort` puts `x` in place.

```text
arr = [1, 4, 6, 8]       insert 5
bisect: O(log n) to find the slot between 4 and 6
insort: [1, 4, _, 6, 8]  <- 6 and 8 shift right
                            to open the slot
n inserts x O(n) shifting = O(n^2) in the worst case
```

The searches are cheap. The insertion is not: it physically moves every element after the slot, just to keep an *order*. But we never use the order. We only ever ask "how many are below `x`", a count. The histogram view drops the order entirely. Then the plain histogram has its own problem: incrementing `cnt[x]` is O(1), but each prefix sum walks O(V) cells. And a precomputed prefix-sum array flips it: queries O(1), but one insertion changes O(V) prefix entries.

```text
                     update      prefix query
plain cnt[] array     O(1)          O(V)
prefix-sum array      O(V)          O(1)
want                  O(log V)      O(log V)
```

## The turning point

**Claim: if each cell `tree[i]` stores the sum of `cnt` over a block of length `lowbit(i)` ending at `i`, then every prefix sum is a sum of at most log V blocks, and every update touches at most log V blocks.**

This structure is the Fenwick tree, or Binary Indexed Tree. Let us build it from zero.

**lowbit.** For a positive integer `i`, `lowbit(i)` is the value of its lowest set bit: `lowbit(6) = 2` because 6 is `110` in binary, `lowbit(8) = 8`, `lowbit(odd) = 1`. In Python it is `i & -i`: negating a number in two's complement flips every bit and adds one, which leaves the lowest set bit as the only bit the two have in common.

```text
 i   binary   lowbit   tree[i] covers values
 1   0001       1      [1..1]
 2   0010       2      [1..2]
 3   0011       1      [3..3]
 4   0100       4      [1..4]
 5   0101       1      [5..5]
 6   0110       2      [5..6]
 7   0111       1      [7..7]
 8   1000       8      [1..8]

  6 = 0110,  -6 = ...1010,  6 & -6 = 0010 = 2
```

**The blocks, drawn.** Cell `i` covers `(i - lowbit(i), i]`. Drawn over the number line, the blocks form a layered ruler: odd cells cover themselves, cells divisible by 2 but not 4 cover pairs, and so on. This is the memory layout: one flat array `tree[1..V]`, index 0 unused.

```text
value:   1   2   3   4   5   6   7   8
t[8]    [-----------------------------]
t[4]    [-------------]
t[2]    [-----]
t[6]                    [-----]
t[1]    [-]
t[3]            [-]
t[5]                    [-]
t[7]                            [-]
```

**Prefix query: walk down by stripping the low bit.** To sum `cnt[1..i]`, take `tree[i]`, which covers `(i - lowbit(i), i]`, then continue from `i - lowbit(i)`, until you reach 0. Each step removes one set bit from `i`, so there are at most log V steps, and the blocks tile `[1..i]` without overlap.

```text
prefix(7):  7 = 111 -> t[7] covers [7..7]
            6 = 110 -> t[6] covers [5..6]
            4 = 100 -> t[4] covers [1..4]
            0       -> stop      [1..4]+[5..6]+[7] = [1..7]
```

**Update: walk up by adding the low bit.** Inserting `x` adds 1 to `cnt[x]`, so every block containing `x` must be incremented. Those are exactly `x, x + lowbit(x), ...` up to V. Adding the low bit carries into a higher bit, landing on the next, larger block that still reaches back over `x`. The low bit at least doubles each step, so again at most log V steps.

```text
add(5):     5 = 0101 -> t[5] [5..5]
            6 = 0110 -> t[6] [5..6]
            8 = 1000 -> t[8] [1..8]
           16 > V    -> stop
blocks t[1],t[2],t[3],t[4],t[7] do not contain 5: untouched
```

Both walks are two-line loops, and the indexing must start at 1: `lowbit(0) = 0`, so a walk that reaches index 0 by adding would never move again.

With the tree, each instruction `x` (with `inserted` values already present) costs:

```python
less    = prefix(x - 1)               # strictly below x
greater = inserted - prefix(x)        # strictly above x
cost   += min(less, greater)
add(x)
```

Using `x - 1` on one side and `x` on the other is what keeps equal values out of both counts.

## Watch it work

`instructions = [4, 8, 1, 6, 5, 2]`, V = 8. `tree` is shown as `t[1..8]` after the insertion.

```text
Frame 1   x=4  inserted=0
          less    = prefix(3) = t3+t2       = 0
          greater = 0 - prefix(4) = 0 - t4  = 0
          cost += 0   (total 0);  add 4 -> t4, t8
          t[1..8] = [0 0 0 1 0 0 0 1]
```
The first insertion is free and marks blocks 4 and 8.

```text
Frame 2   x=8  inserted=1
          less    = prefix(7) = t7+t6+t4    = 1
          greater = 1 - prefix(8) = 1 - t8  = 0
          cost += 0   (total 0);  add 8 -> t8
          t[1..8] = [0 0 0 1 0 0 0 2]
```
`prefix(7)` found the 4 through block `t4`; nothing is above 8.

```text
Frame 3   x=1  inserted=2
          less    = prefix(0)               = 0
          greater = 2 - prefix(1) = 2 - t1  = 2
          cost += 0   (total 0);  add 1 -> t1, t2, t4, t8
          t[1..8] = [1 1 0 2 0 0 0 3]
```
Value 1 sits in four blocks, so the upward walk touches four cells.

```text
Frame 4   x=6  inserted=3
          less    = prefix(5) = t5+t4       = 0+2 = 2
          greater = 3 - prefix(6) = 3-(t6+t4) = 1
          cost += 1   (total 1);  add 6 -> t6, t8
          t[1..8] = [1 1 0 2 0 1 0 4]
```
Two values (1 and 4) lie below 6, one (8) above; we pay 1.

```text
Frame 5   x=5  inserted=4
          less    = prefix(4) = t4          = 2
          greater = 4 - prefix(5) = 4-(t5+t4) = 2
          cost += 2   (total 3);  add 5 -> t5, t6, t8
          t[1..8] = [1 1 0 2 1 2 0 5]
```
A balanced insertion: two below, two above.

```text
Frame 6   x=2  inserted=5
          less    = prefix(1) = t1          = 1
          greater = 5 - prefix(2) = 5 - t2  = 4
          cost += 1   (total 4);  add 2 -> t2, t4, t8
          t[1..8] = [1 2 0 3 1 2 0 6]
          answer = 4 % (1e9+7) = 4
```
The final total matches the table at the top.

Across every frame, `t[i]` equalled the number of inserted values inside its block, for example `t[6] = 2` in Frame 5 because 5 and 6 had been inserted, and `t[8]` always equalled the number of insertions so far.

## Why it is correct

The Fenwick invariant: after any sequence of insertions, `tree[i]` equals the number of inserted values in `(i - lowbit(i), i]`.

- **add keeps it.** The blocks containing `x` are exactly the indices on the walk `x, x + lowbit(x), ...`. A block `(j - lowbit(j), j]` contains `x` when `j >= x` and `j` with its lowest set bit cleared is below `x`. Starting at `x` and repeatedly adding the low bit produces precisely such `j`s in increasing order, and skips every index whose block ends before reaching back to `x`. Each of them gains 1; no other block changes.
- **prefix reads it.** Stripping low bits from `i` yields blocks `(i - lowbit(i), i]`, then `(i' - lowbit(i'), i']` with `i' = i - lowbit(i)`, and so on down to 0. These intervals are adjacent and disjoint and cover `[1..i]`, so the sum of their cells is the number of inserted values `<= i`.

Given both, `prefix(x - 1)` is the number of present values strictly below `x` and `inserted - prefix(x)` the number strictly above, which is the definition of the cost. Summing and reducing modulo 1e9+7 gives the answer.

## Cost

- **Time O(n log V):** each instruction does two prefix walks and one update walk, each at most log V steps. V is at most 10^5 here, so log V is about 17.
- **Space O(V):** the tree has one cell per possible value.

Brute force with `insort` is O(n^2) in the worst case. If values were huge (say up to 10^9), first coordinate-compress: sort the distinct values and map each to its rank 1..m, making it O(n log n) time and O(n) space.

## Variations you will meet

- **Count of Smaller Numbers After Self (315), again.** Scan from right to left; before adding `nums[i]`, answer `prefix(nums[i] - 1)` over compressed values. Same O(n log n) as merge sort, online, and no index bookkeeping.
- **Reverse Pairs (493), again.** Scan left to right; before adding `x`, count inserted values greater than `2x`: `inserted - prefix(rank(2x))`, with `nums` and `2 * nums` compressed together into one rank table.
- **Range Sum Query - Mutable (307).** The same tree with arbitrary deltas instead of `+1`: point update, range sum as `prefix(r) - prefix(l - 1)`. Range Sum Query 2D - Mutable (308) nests the walks, one per dimension.
- **k-th smallest inserted value.** Descend the tree from the highest power of two, greedily taking blocks while their total is below k: an order-statistics query in O(log V). A segment tree does the same with more code but supports range updates too.

## What to carry forward

When every question is "how many values are below x" and values are bounded, index a tree by value: each cell covers the block its low bit names, queries strip low bits and updates add them. That closes the chapter's arc, which grew from a hash map that remembers what was seen (Two Sum) through prefix-sum counting, buckets that approximate order, and merge sort that counts while it orders, to a Fenwick tree that keeps counts by value under live insertions, the last tool you need for rank questions over an array.
