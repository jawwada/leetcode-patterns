# Reverse Pairs
*LeetCode 493 · Hard · Pattern: Merge sort counting · Reading time ~10 min*

## What the problem is really asking

Count the index pairs `i < j` where the earlier value is more than twice the later one: `nums[i] > 2 * nums[j]`. Return one number, the count.

This is the inversion-counting question with a twist. An inversion is "earlier and bigger"; a reverse pair is "earlier and more than *double*". The answer is a single integer over up to n^2/2 pairs, and what makes it hard is the same tension as the previous problem: one condition is about index order (`i < j`), the other about values (`nums[i] > 2 * nums[j]`), and no single sort of the data respects both. Values can be negative, so "twice as big" does not simply mean "bigger".

```text
idx:    0   1   2   3   4
nums: [ 2,  4,  3,  5,  1 ]

pairs i<j with nums[i] > 2*nums[j]:
  (1,4)  4 > 2*1 = 2   yes
  (2,4)  3 > 2*1 = 2   yes
  (3,4)  5 > 2*1 = 2   yes
  (0,4)  2 > 2         no  (strict)
  (3,0)  5 > 2*2 = 4, but index 3 is after index 0: no
answer = 3
```

## Do it by hand first

By hand you would fix the right element of the pair and look left for anything more than double it. Or, more cleverly, you would split the list in two, count pairs inside each part separately, and then count pairs that straddle the cut. For the straddling pairs, the "earlier" condition is automatic: everything in the left part is earlier than everything in the right part. So you can rearrange each part however you like, for example sort it, without breaking the question.

```text
         left part      |   right part
nums:    2   4          |   3   5   1
sorted:  2   4          |   1   3   5
straddling pairs: which left x has x > 2r for which right r?
   x=2: 2 > 2*1? no                       -> 0
   x=4: 4 > 2*1? yes  4 > 2*3? no         -> 1
```

What your hand kept track of, for each left value, was *how far along the sorted right part* the condition stays true. That moving finger is the seed of the algorithm.

## The first honest attempt

Check every pair: for each `i`, for each `j > i`, test `nums[i] > 2 * nums[j]`. O(n^2) time, O(1) space.

```text
i=0 (2):  vs  4  3  5  1    -> 0
i=1 (4):  vs     3  5  1    -> 1
i=2 (3):  vs        5  1    -> 1
i=3 (5):  vs           1    -> 1
the 1 at the end is tested against every element, and each
test ignores everything learned from the previous rows
```

For a fixed `i`, the question "how many later `r` have `2r < nums[i]`" is a rank query: if the later elements were sorted, the answer would be one prefix of them. The brute force answers it by touching every later element instead of using any order.

## The turning point

**Merge sort in one picture.** Split in half, sort both halves recursively, then merge two sorted lists by repeatedly taking the smaller head:

```text
         [2 4 3 5 1]
         /          \
      [2 4]       [3 5 1]
      /   \       /     \
    [2]   [4]   [3]    [5 1]
                       /   \
                     [5]   [1]
merge = zip two sorted rails, taking the smaller head:
   rail A: 2 4        rail B: 1 3 5      -> 1 2 3 4 5
```

The property that matters, as in the previous problem: at every merge, every left element is earlier in the original array than every right element. So at that moment `i < j` holds for every cross pair, and only the value condition remains.

It is worth pausing on why sorting the halves is allowed at all, since sorting is what normally destroys index information. The number of cross pairs depends only on *which* values sit in the left half and *which* sit in the right half, not on their order inside each half. Sorting a half shuffles its elements but never moves one across the cut, so the cross count is unchanged, and we are free to arrange each half in whatever order makes counting cheap.

**Claim: with both halves sorted, the right elements `r` with `2r < x` form a prefix of the right half, and that prefix only grows as `x` walks up the sorted left half, so all cross pairs are counted with one forward-moving pointer.**

Why a prefix: the right half is sorted, so `2r` increases along it; once `2r < x` fails, it fails for every later `r`. Why it only grows: the left half is sorted too, so the next `x` is at least as big; anything with `2r < x` still satisfies `2r < x'`. So a pointer `j` on the right half never moves backwards. Each left element adds `j` (the length of the prefix) to the count. The pointer moves at most `len(right)` times in total, and the left loop is `len(left)` steps, so the cross count is linear.

```text
left (sorted):  x1 <= x2 <= x3 ...
right (sorted): r1 <= r2 <= r3 <= r4 ...
                |-- 2r < x1 --|
                |---- 2r < x2 ----|
                |------ 2r < x3 ------|
the boundary j is a staircase that only steps right
```

**Why not count during the merge, as in the previous problem?** There, the merge's comparison (`r < x`) was the pair's comparison, so `j - mid` at emission time was the count. Here the pair test is `x > 2r` while the merge still has to compare `x` against `r` to produce a sorted list. The two comparisons disagree: take left `[4]`, right `[3]`. The merge emits 3 first (3 < 4), but `4 > 2*3 = 6` is false. So we run *two* linear passes per level: first the counting staircase, then the ordinary merge. The core is four lines:

```python
j = 0
for x in left:                      # x increases
    while j < len(right) and 2 * right[j] < x:
        j += 1                      # never moves back
    count += j
```

Negative numbers need no special case. The condition is written as `2 * r < x`, which is monotone in `r` whatever the signs, and the right half is sorted by `r`, so the staircase argument holds. (In Python, ints do not overflow; in Java or C++, `2 * r` needs a 64-bit type.)

## Watch it work

`nums = [2, 4, 3, 5, 1]`. The split is `[2 4] | [3 5 1]`, then `[3] | [5 1]`, then `[5] | [1]`.

```text
Frame 1   merge [2] | [4]
          x=2: 2*4=8 < 2? no      j=0   +0
          cross = 0      sorted -> [2 4]     subtotal 0
```
No pair inside `[2 4]`.

```text
Frame 2   merge [5] | [1]
          x=5: 2*1=2 < 5? yes j=1  (end)  +1   pair (5,1)
          cross = 1      sorted -> [1 5]     subtotal 1
```
The pair at indices (3, 4) is found where 5 and 1 are separated.

```text
Frame 3   merge [3] | [1 5]
          x=3: 2*1=2 < 3? yes j=1
               2*5=10 < 3? no      stop   +1   pair (3,1)
          cross = 1      sorted -> [1 3 5]   subtotal 1+1 = 2
```
3 dominates the 1 but not the 5; the right half `[3 5 1]` holds 2 pairs in total.

```text
Frame 4   merge [2 4] | [1 3 5]
          x=2: 2*1=2 < 2? no       j=0   +0
                    ^ strict: 2 is not > 2
```
The smallest left value dominates nothing; `j` stays at 0.

```text
Frame 5   x=4: 2*1=2 < 4? yes j=1
               2*3=6 < 4? no      stop   +1   pair (4,1)
          cross = 1
          j only moved right: 0 -> 1
```
The pointer resumes from where `x=2` left it, never restarting.

```text
Frame 6   total = left 0 + right 2 + cross 1 = 3
          merge -> [1 2 3 4 5]
```
The three pairs (4,1), (3,1), (5,1) were each counted at the merge that separated them.

Across the frames, every count happened at the moment both halves were sorted and their index relation was fixed, and within one merge the pointer `j` only moved forward.

## Why it is correct

Recursive invariant: `sort(arr)` returns `arr` sorted together with the number of reverse pairs inside `arr`. A singleton has none. For a longer array, every pair `i < j` is of exactly one kind: both in the left half (counted by the left call), both in the right half (counted by the right call), or `i` left and `j` right. Sorting a half does not change which elements it contains, so the cross pairs are exactly the pairs `(x, r)` with `x` in the left half, `r` in the right half, and `x > 2r`, regardless of order inside the halves. The staircase counts, for each `x`, the length of the prefix of sorted `right` with `2r < x`, which is the number of such `r` by the prefix argument. Adding the three parts gives the count for `arr`, and merging returns it sorted, as the invariant requires.

## Cost

- **Time O(n log n):** about log n levels; each level does a linear counting pass and a linear merge.
- **Space O(n):** the halves and merged lists at each level (this implementation slices), plus O(log n) recursion depth.

Brute force is O(n^2) time and O(1) space.

## Variations you will meet

- **Different factor or function.** "`nums[i] > c * nums[j]`", or any condition `x > f(r)` with `f` increasing, uses the same staircase. Only the comparison inside the `while` changes.
- **Count of Range Sum (327).** Merge sort over prefix sums; for each left prefix `p`, count right prefixes with `lower <= q - p <= upper`. Two staircase pointers (one for each bound) in the counting pass, then merge.
- **Fenwick tree version.** Scan left to right; before inserting `x`, ask how many inserted values are greater than `2x`. Needs coordinate compression of both `nums` and `2 * nums` into one sorted list of keys. The next problem builds that tree.
- **Global and Local Inversions (775).** Plain inversion counting with the merge comparison doubling as the pair comparison; or a one-pass observation specific to permutations.

## What to carry forward

Merge sort gives you a moment where both halves are sorted and every left element is known to be earlier: any monotone pair condition becomes a staircase walk, counted in its own pass before the merge. The last problem, Create Sorted Array through Instructions, asks "how many smaller, how many larger" *online*, one insertion at a time, so instead of sorting everything at once we build a Fenwick tree over values.
