# Find K-th Smallest Pair Distance

*LeetCode 719 · Hard · Pattern: Binary search on the answer · Reading time ~10 min*

## The problem

The distance of a pair (i, j) with i < j is |nums[i] - nums[j]|. Return the k-th smallest distance among all n(n-1)/2
pairs.

```text
Example: nums = [1,3,1], k = 1 returns 0 (distances 2, 0, 2;
  sorted 0, 2, 2). Example: nums = [1,6,1], k = 3 returns 5.
```

## What the problem is really asking

Take every pair of positions `i < j` in the array and compute `|nums[i] - nums[j]|`. That gives `n(n-1)/2` distances. Sort them and return the `k`-th smallest.

The answer is one distance value. The difficulty is the same as in the multiplication table. The multiset is quadratic in size (about 5 · 10^7 pairs when `n = 10^4`), so listing it is out, and we need its k-th element without ever building it.

```text
nums = [1, 3, 4, 8], k = 4

pairs and distances:
  (1,3)=2  (1,4)=3  (1,8)=7
  (3,4)=1  (3,8)=5  (4,8)=4

sorted: 1 2 3 4 5 7
        1 2 3 4 5 6   <- rank
              ^
        k=4 -> answer 4
```

## Do it by hand first

Put the numbers on a number line. Distances are gaps between dots, and every pair's distance is the length of the stretch between its two dots.

```text
  1     3  4           8
  o-----o--o-----------o
   <-2-> <1>  <---4--->
```

Asked "how many pairs are within 4 of each other?", your hand does not list pairs. It slides a ruler of length 4 along the line. With its right end at 3, the dot 1 is within reach: 1 pair. Right end at 4, dots 1 and 3 are within reach: 2 pairs. Right end at 8, only 4 is within reach (8 - 3 = 5 is too far): 1 pair. That makes 4 pairs in total, and since `k = 4`, the 4th smallest distance is at most 4. Repeating with a ruler of length 3 gives 3 pairs, so the 4th distance is more than 3. The answer is 4.

What your hand tracked: **a sorted line, a ruler length `d`, and a left edge that only ever slid right as the right edge moved right.** That is a sliding window, and it counts pairs without naming them.

## The first honest attempt

"Two nested loops produce every distance; sort them; index `k - 1`." That is O(n² log n) time and O(n²) space. A heap of size `k` saves memory but still touches every pair: O(n² log k).

```text
r\l   1   3   4
 3    2
 4    3   1
 8    7   5   4
every cell computed and stored, then sorted --
yet all we need is how many cells are <= some d
```

The waste is that we materialise and order all `n²/2` distances when, for any threshold, how many are at or below it is a single number that a linear scan can produce.

## The turning point

**Claim: after sorting `nums`, `count(d)`, the number of pairs with distance `<= d`, takes O(n) with two pointers, and the k-th smallest distance is the smallest `d` with `count(d) >= k`.**

*Sorting makes the pairs local.* Once the array is sorted, the pairs ending at index `r` with distance `<= d` are exactly the indices `l, l+1, ..., r-1` for the smallest `l` with `nums[r] - nums[l] <= d`. They form a contiguous block, because values further left are smaller and therefore further away. So for each `r` we add `r - l`.

*Sorting is allowed.* The problem talks about index pairs `i < j`, which can make sorting look like cheating. But a distance `|a - b|` does not care which element came first, and sorting only relabels positions. Every unordered pair of elements is still exactly one pair after the shuffle, so the multiset of distances is unchanged. That is the first thing to check whenever you want to sort an input whose answer seems tied to positions.

*The window only moves forward.* When `r` steps right, `nums[r]` grows, so the smallest valid `l` can only stay or move right. Each pointer travels the array once, so one count is O(n) in total.

```text
count(4) on sorted [1, 3, 4, 8]
  r=0 (1): l=0              adds 0
  r=1 (3): l=0  [1 3]       adds 1
  r=2 (4): l=0  [1 3 4]     adds 2
  r=3 (8): l: 0->1->2 [4 8] adds 1
                     total = 4
```

*The predicate* is `enough(d) = count(d) >= k`. *Monotone*: a larger `d` keeps every pair already counted and possibly adds more, so `count` never decreases, and `enough` reads `F ... F T ... T`.

*The answer is the first T*, by the same rank argument as the last problem. If `x` is the true k-th distance, at least `k` pairs are `<= x` and fewer than `k` are `<= x - 1`. And since `count` only jumps at real distances, the first T is a real distance.

*Range*: `[0, max - min]`. Zero must be allowed, because duplicate values give distance 0. The largest possible distance is the span of the array.

```text
d      : 0  1  2  3  4  5  6  7
count  : 0  1  2  3  4  5  5  6
enough : F  F  F  F  T  T  T  T     (k = 4)
                     ^
              first T = 4
```

Why not a heap? A min-heap seeded with each adjacent pair `(i, i+1)`, popping the smallest and pushing `(i, j+1)`, does produce distances in order. But it pops `k` times, and `k` can be close to `n²/2`. The binary search's cost does not depend on `k` at all. It depends only on how many values the answer could take, and each probe is a fixed-cost linear pass. That trade, paying log(range) linear scans instead of `k` heap operations, is the reason this pattern beats the obvious structure whenever `k` can be large.

The structure is identical to the multiplication table. Binary search over values, convert each value into a rank with a fast count, stop at the first value whose rank reaches `k`. The only new piece is the counting engine: a sliding window over sorted data instead of a formula per row.

## Watch it work

`nums = [1, 3, 4, 8]` (already sorted), `k = 4`. The range is `[0, 7]`.

```text
Frame 1   lo=0  hi=7
  line:  1     3  4           8
  d   :  0 1 2 3 4 5 6 7
         L             H
```
The search covers every distance the array could produce.

```text
Frame 2   lo=0  hi=7  mid=3
  r=1: [1 3] +1   r=2: [1 3 4] +2
  r=3: l slides to 3, window [8] +0
  count=3 < 4  F
```
Only three pairs are within 3, so the answer is above 3: `lo = 4`.

```text
Frame 3   lo=4  hi=7  mid=5
  r=1: +1   r=2: +2
  r=3: l slides to 1, window [3 4 8] +2
  count=5 >= 4  T
```
Five pairs are within 5. 8 - 3 = 5 now counts, so the answer is at most 5: `hi = 5`.

```text
Frame 4   lo=4  hi=5  mid=4
  r=1: +1   r=2: +2
  r=3: l slides to 2, window [4 8] +1
  count=4 >= 4  T
```
Exactly four pairs are within 4: `hi = 4`.

```text
Frame 5   lo=4  hi=4   stop, answer 4
  sorted distances: 1 2 3 | 4 | 5 7
                    <=3: 3  ^ rank 4
```
`lo == hi == 4`. The count jumped from 3 to 4 at `d = 4`, so the 4th smallest distance is 4.

In every probe the left pointer only moved right, and every `d` below `lo` was known to have fewer than `k` pairs under it. No distance was ever stored.

## Why it is correct

**Invariant: `enough(hi)` is true and `enough(lo - 1)` is false (or `lo = 0`).** At the start, `count(max - min)` counts every pair, `n(n-1)/2 >= k`, so `enough(hi)` holds. On T, `hi = mid` preserves it. On F, monotonicity makes every `d <= mid` false, so `lo = mid + 1` preserves the other side. The window shrinks every step because `mid < hi`. At the end `lo` is the smallest `d` with at least `k` pairs within `d`, which is exactly the k-th smallest distance.

Each count is right because, in a sorted array, the set of valid partners of `r` is a suffix of `[0, r)`, and that suffix's left boundary is non-decreasing in `r`. So a single forward-only `l` finds every boundary.

## Cost

- **Enumerate and sort:** O(n² log n) time, O(n²) space.
- **Binary search plus sliding count:** O(n log n) to sort, then O(n log R) for about log₂ R probes, where R = `max - min` (up to 10^6, so about 20 probes). **O(1)** extra space if you sort in place.

## Variations you will meet

- **Count pairs with distance strictly less than `d`.** Change the window condition from `> d` to `>= d`. A slip between them shifts the answer by one rank, which is the most common bug here.
- **K-th smallest pair sum from two sorted arrays (LeetCode 373 asks for the first k pairs).** For just the k-th sum, binary search the sum and count pairs `<= s` with two pointers moving in opposite directions.
- **K-th smallest subarray sum (LeetCode 1918).** With positive numbers, count subarrays with sum `<= s` using a sliding window. Same skeleton, different window rule.
- **Huge `k` relative to the pair count.** Nothing changes. The search does not care about `k`, only about `count`.

## What to carry forward

Sort first so that "close in value" means "close in index". Then a two-pointer window counts the pairs within `d` in one pass, and binary search over `d` finds the first value whose count reaches `k`.

The next problem moves the answer off the integers: the target is a real-valued average, so the loop runs until the interval is narrower than `1e-5`, and the check needs a clever algebraic shift.
