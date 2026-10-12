# Find Median from Data Stream

*LeetCode 295 · Hard · Pattern: Two heaps (balanced max-heap / min-heap) · Reading time ~10 min*

## The problem

Design a class with addNum(num) and findMedian(). findMedian returns the median of all numbers added so far: the
middle value for an odd count, the mean of the two middle values for an even count.

```text
Example: add(1), add(2) -> findMedian()=1.5; add(3) ->
  findMedian()=2.0.
```

## What the problem is really asking

Numbers arrive one at a time through `addNum`. At any moment, `findMedian` must return the median of everything seen so far: the middle value if the count is odd, the average of the two middle values if it is even. Calls can be interleaved freely, for example tens of thousands of adds with a median query after each one.

The answer is one number, but it depends on the sorted position of the data, and the data keeps changing. Sorting on every query is too slow. Keeping everything fully sorted is wasteful, because a median only ever looks at one or two positions in the middle.

```text
after adding 5, 15, 1, 3, 8:

sorted:   1   3   5   8   15
                  ^
               median = 5

after adding 5, 15, 1, 3:
sorted:   1   3 | 5   15
              ^   ^
          median = (3 + 5) / 2 = 4
```

## Do it by hand first

Imagine numbers written on cards arriving one by one, and someone asking for the median after every card. You would not re-sort the whole pile each time. You would keep two piles: a **left pile** of the smaller cards and a **right pile** of the larger cards, kept about equal in size. Then the median is whatever sits at the boundary: the biggest card on the left, or the average of that and the smallest card on the right.

When a new card arrives, you check which side of the boundary it belongs on and drop it there. If one pile gets two cards ahead of the other, you move the boundary card across.

```text
          left pile        |        right pile
     (smaller half)        |     (larger half)
      1    3    [5]        |     [8]    15
                 ^         |      ^
             biggest left  |  smallest right
                     the seam = median
```

What did your hand track? Only two values ever mattered, the biggest card on the left and the smallest card on the right. You never cared how the left pile was ordered inside. "Always show me the max of this pile" is a max-heap, and "always show me the min of that pile" is a min-heap.

## The first honest attempt

**Append and sort on query.** `addNum` appends in O(1). `findMedian` sorts in O(n log n) and reads the middle. With a query after every add, the total is O(n^2 log n).

**Keep it sorted with binary insertion.** Use `bisect.insort` to put each number in place. The median read is O(1), but each insert shifts up to `n` elements, so the total is O(n^2).

Here is what both of them pay for:

```text
sorted list after 5 adds:   1   3   5   8   15
                            \___/       \___/
                        order inside these halves
                        is maintained but never read
```

Every comparison spent ordering 1 against 3, or 8 against 15, is wasted. The median does not care whether the left half is `[1, 3]` or `[3, 1]`.

## The turning point

**Claim: the median is determined entirely by the largest element of the lower half and the smallest element of the upper half, so it is enough to keep each half in a heap that exposes exactly that element.**

Split the numbers into `small` (the lower half) and `large` (the upper half) with two rules:

1. **Order rule:** every element of `small` is `<=` every element of `large`.
2. **Size rule:** `len(small)` equals `len(large)` or `len(large) + 1`.

If both rules hold, then `max(small)` is the middle element when the count is odd (small has the extra one), and `(max(small) + min(large)) / 2` is the median when the count is even. Store `small` as a max-heap (in Python, a min-heap of negated values) and `large` as a min-heap. Both seam values are at index 0 and can be read in O(1).

Inserting while keeping both rules uses a neat trick that needs no comparison against the seam:

1. Push the new number onto `small`.
2. Pop `small`'s max and push it onto `large`. The element that crosses is the largest of the old lower half plus the newcomer. Everything left in `small` is at most that element, and at most the old lower half's max, which was already `<=` all of `large`. So the order rule holds again with no comparison written by you.
3. If `large` is now bigger than `small`, pop `large`'s min and push it onto `small`. This restores the size rule, and moving the smallest of `large` to `small` keeps the order rule.

The point of step 2 is that you do not have to decide which side the newcomer belongs on. Routing every number through `small` and then across hands the decision to the heaps.

## Watch it work

Add 5, 15, 1, 3, 8. `small` is drawn by its true values (internally stored negated). Each frame shows the state after one full `addNum`.

Frame 1: add 5. Push to small, its max 5 crosses to large, large is bigger, so 5 comes back.

```text
 small (max-heap)          large (min-heap)
        5                       (empty)
 array: [5]                array: [ ]
 sizes 1 / 0   odd  -> median = 5
```

The first number always ends up in `small`.

Frame 2: add 15. Push to small (`[15, 5]`), its max 15 crosses to large. Sizes are 1 and 1, so no rebalance is needed.

```text
 small                     large
        5                       15
 array: [5]                array: [15]
 sizes 1 / 1   even -> (5 + 15) / 2 = 10
```

15 never had to be compared with 5 by our code. The max-heap did it.

Frame 3: add 1. Push to small (`[5, 1]`), max 5 crosses (large `[5, 15]`), large is bigger, so its min 5 comes back.

```text
 small                     large
        5                       15
       /
      1
 array: [5, 1]             array: [15]
 sizes 2 / 1   odd  -> median = 5
```

5 went across and came straight back. That round trip is the price of not comparing.

Frame 4: add 3. Push to small (`[5, 1, 3]`), max 5 crosses to large. Sizes are 2 and 2.

```text
 small                     large
        3                       5
       /                       /
      1                      15
 array: [3, 1]             array: [5, 15]
 sizes 2 / 2   even -> (3 + 5) / 2 = 4
```

The seam moved: 5 is now the smallest of the upper half.

Frame 5: add 8. Push to small (`[8, 1, 3]`), max 8 crosses (large `[5, 15, 8]`), large is bigger, so its min 5 crosses back.

```text
 small                     large
        5                       8
       / \                     /
      1   3                  15
 array: [5, 1, 3]          array: [8, 15]
 sizes 3 / 2   odd  -> median = 5
```

The newcomer 8 belonged on the right, and it ended up there even though it first went into `small`.

```text
the seam across all frames:
   frame:   1     2     3     4     5
   small  [5]   [5]  [5,1] [3,1] [5,1,3]
   large   -   [15]  [15]  [5,15] [8,15]
   median   5    10     5     4     5
```

In every frame both rules held: every value on the left was `<=` every value on the right, and the left had the same number of elements as the right or one more. So the median was always readable from the two roots.

## Why it is correct

**Invariant.** Between calls: (O) `max(small) <= min(large)`, and (S) `len(small) - len(large)` is 0 or 1. Together they say `small` is exactly the lowest `ceil(n/2)` numbers and `large` is the rest, which is the definition of the median split.

**addNum preserves (O).** Let `small` and `large` satisfy (O), call the old lower max `s`, and push `x` into `small`. Step 2 pops `m = max(s, x)` and pushes it to `large`. What remains in `small` is the old lower half, possibly with `x` added and `s` removed. Every remaining element is `<= m`, because `m` was the max. Every remaining element is also `<= s` or equal to `x <= s`, and `s <= min(old large)` by (O). So every remaining element is `<=` every element of the new `large`, which is the old `large` plus `m`. Step 3 moves `min(large)` to `small`. That element is `>=` everything already in `small`, so it becomes `small`'s max and is still `<=` everything left in `large`.

**addNum preserves (S).** Before the call the size difference is 0 or 1. Step 1 adds one to `small`, step 2 moves one to `large`, so the difference is now `-1` or `0`. If it is `-1`, step 3 moves one back, making it `+1`. Either way it ends at 0 or 1.

**findMedian is correct** given (O) and (S): odd count means `small` has the extra element, which is the middle one. Even count means the two middle elements are the two roots. Divide with `/`, not `//`, so `(5 + 15) / 2` gives `10.0` and `(3 + 4) / 2` gives `3.5`.

## Cost

- **addNum: O(log n).** At most three heap operations (push, pop+push, pop+push), each O(log n).
- **findMedian: O(1).** It reads two roots.
- **Space: O(n).** Every number lives in exactly one heap.

Compared with the brute forces: sort-on-query is O(n log n) per query, and sorted insertion is O(n) per add. The heaps make both operations logarithmic or better.

A slightly faster `addNum` compares `x` with `-small[0]` first and pushes to the correct side, then rebalances. It does fewer heap operations, but you must handle the empty-heap case. The "always through `small`" version trades one extra push and pop for zero special cases.

## Variations you will meet

- **Sliding Window Median (LeetCode 480).** Numbers also leave, when they slide out of the window. Heaps cannot delete arbitrary elements cheaply, so you use lazy deletion: keep a "to delete" counter, and pop stale roots when they surface. You must also track each heap's logical size separately from its array length.
- **Values in a small range (for example 0 to 100).** Use a counting array instead and walk it to the middle. That is O(100) per query, O(1) per add.
- **"99% of values are in [0, 100]".** Use counting for the common range, and keep two counters (or small heaps) for the outliers below and above.
- **Any percentile, not the median.** Change the size rule to `len(small) = ceil(p * n)`. The two-heap seam still works for one fixed percentile.

## What to carry forward

Two heaps facing each other across a seam give you a running order statistic. The max-heap holds the lower part, the min-heap holds the upper part, sizes are pinned, and the answer is read at the roots. Routing every insert through one heap and across settles the order without any comparison of your own.

The next problem, IPO, also uses a heap whose contents change as an outside quantity grows. Your capital acts as a sweep line that unlocks projects into a max-heap, and you greedily take the most profitable project unlocked so far.
