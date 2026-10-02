# Maximum Gap
*LeetCode 164 · Hard · Pattern: Pigeonhole buckets · Reading time ~9 min*

## What the problem is really asking

You get an unsorted array of non-negative integers. Imagine it sorted, and look at the differences between neighbours in that sorted order. Return the largest of those differences. Fewer than two numbers means there are no neighbours, so return 0. The budget is linear time and linear extra space.

The answer is one number: a distance on the number line. What makes it hard is that "neighbours in sorted order" sounds like it needs a sort, and comparison sorting costs O(n log n). The problem is asking whether you can learn one fact about the sorted order (its widest hole) without paying for all of the sorted order.

```text
nums = [1, 9, 2, 5, 18]

number line:
 1 2     5       9                 18
 *-*-----*-------*-----------------*
  1   3      4           9
                      ^ widest hole = 9
```

## Do it by hand first

If you plot these five numbers as dots on a ruler, you do not sort them in your head. Your eye sees *clumps* and *empty stretches*. The 1 and 2 form a clump, then there is empty space, and the long empty stretch between 9 and 18 jumps out immediately. You never compared 1 with 2 to find the answer; you only noticed where dots stop and where they start again.

```text
ruler 1..20, cut into stretches of 4:
stretch:   1..4    5..8    9..12   13..16   17..20
dots:      1 2     5       9       (none)   18
keep:      1/2     5/5     9/9       -      18/18
                           9 ----------------> 18
```

What your eye kept track of was, for each stretch of the ruler, only its leftmost and rightmost dot. Inside a stretch the order did not matter. That "per stretch: min and max" record is the seed of the data structure.

## The first honest attempt

Sort, then take the largest adjacent difference. O(n log n) time, O(1) or O(n) space depending on the sort. It is correct, and you should say it first.

```text
sorted:  1   2   5   9   18
gaps:      1   3   4   9      max = 9
           ^   ^
   these comparisons fixed the exact order of 1,2 and 2,5,
   facts the answer never uses
```

The waste is that sorting determines the complete order of all n elements, roughly n log n bits of information, when we only want one number. In particular it carefully orders values that are very close to each other, like 1 and 2, even though two values that close can never be the widest gap.

There is also a hard wall here. Any algorithm that learns about the data only by comparing two elements needs on the order of n log n comparisons to sort, and it is easy to believe the same wall applies to this problem. The way around it is to stop comparing and start *computing*: turning a value into a bucket number with arithmetic, `(x - lo) // width`, is not a comparison, and it places a value in O(1).

## The turning point

**Claim: if you cut the range [lo, hi] into buckets narrower than the average gap, the maximum gap can never be between two values in the same bucket, so it is always "max of one non-empty bucket to min of the next non-empty bucket".**

Start with pigeonhole. Let `lo` and `hi` be the smallest and largest values. Sorted, the n values have n - 1 gaps, and those gaps add up to exactly `hi - lo` (they tile the segment from `lo` to `hi`). If n - 1 numbers add up to `hi - lo`, the largest of them is at least their average:

```text
max gap  >=  (hi - lo) / (n - 1)  >=  floor((hi - lo) / (n - 1))
                                       = width
```

Here that is `(18 - 1) / 4 = 4.25`, so the maximum gap is at least 4.25, and we choose `width = 4`.

Now cut the line into buckets of that width starting at `lo`: bucket `b` holds values `lo + b*width` up to `lo + b*width + width - 1`, and a value `x` goes to bucket `(x - lo) // width`. Two values in the same bucket differ by at most `width - 1`, which is strictly less than the maximum gap. So the two values forming the maximum gap are in different buckets.

Now take that pair, `a < b`, adjacent in sorted order. Nothing lies strictly between them. So `a` must be the largest value in its bucket (anything bigger in the same bucket would lie between them), and `b` must be the smallest value in its bucket, and every bucket strictly between theirs must be empty. That is exactly the claim: the answer is the largest "next non-empty bucket's min minus previous non-empty bucket's max".

So each bucket needs only two numbers, its min and its max. The order inside a bucket is never needed, which is precisely the order sorting was wasting effort on. The buckets themselves are already in order, because bucket indices are computed from values. With `width = floor((hi - lo)/(n - 1))` there are about n buckets, so one pass fills them and one pass scans them.

Two edge cases make the formula safe. If `hi - lo < n - 1` (many duplicates packed tightly), the floor is 0, so clamp `width` to at least 1. If `hi == lo`, every gap is 0; return early.

## Watch it work

`nums = [1, 9, 2, 5, 18]`, n = 5.

```text
Frame 1   lo = 1, hi = 18, width = max(1, 17 // 4) = 4
          count = 17 // 4 + 1 = 5 buckets
          bucket:   b0     b1     b2     b3      b4
          covers:  1..4   5..8  9..12  13..16  17..20
          min/max:  -/-    -/-    -/-    -/-     -/-
```
Five empty buckets of width 4 tile the range from 1 to 20.

```text
Frame 2   drop 1 -> (1-1)//4 = 0    drop 9 -> (9-1)//4 = 2
          bucket:   b0     b1     b2     b3      b4
          min/max:  1/1    -/-    9/9    -/-     -/-
```
Each value updates only its own bucket's min and max.

```text
Frame 3   drop 2 -> b0   drop 5 -> b1   drop 18 -> b4
          bucket:   b0     b1     b2     b3      b4
          min/max:  1/2    5/5    9/9    -/-    18/18
```
Bucket 0 now holds two values but stores only 1 and 2; b3 stays empty.

```text
Frame 4   scan, prev = lo = 1, best = 0
          b0: gap = min 1 - prev 1 = 0   best 0, prev = 2
          b1: gap = min 5 - prev 2 = 3   best 3, prev = 5
```
Each non-empty bucket is compared against the max of the previous non-empty one.

```text
Frame 5   b2: gap = min 9 - prev 5 = 4   best 4, prev = 9
          b3: empty -> skip, prev stays 9
          b4: gap = min 18 - prev 9 = 9  best 9, prev = 18
          answer = 9
```
The empty bucket is stepped over, so the gap from 9 to 18 spans it.

Through every frame, `prev` was the largest value seen so far in left-to-right bucket order, which is the sorted predecessor of the next bucket's min. The pair 1, 2 was never compared at all.

## Why it is correct

Two facts carry it. First, by pigeonhole the maximum gap is at least `width`, while two values in one bucket differ by at most `width - 1`, so the maximum gap always crosses a bucket boundary. Second, the scan computes, for every pair of consecutive non-empty buckets, `bucket_min[next] - bucket_max[prev]`. Each of these differences is a genuine adjacent gap in sorted order, because no value can lie strictly between the max of one non-empty bucket and the min of the next non-empty bucket (any such value would sit in one of those buckets or in an empty one between). And the maximum gap is one of these differences, by the argument in the turning point. So the largest difference the scan sees is the answer. The first step, `bucket_min[0] - lo`, is always 0, because the bucket of `lo` is bucket 0 and contains `lo`.

## Cost

- **Time O(n):** one pass to find `lo` and `hi`, one pass to drop values into buckets, one pass over at most n buckets.
- **Space O(n):** two arrays of bucket mins and maxes. `count = (hi - lo) // width + 1` is at most about n, because `width` is about `(hi - lo)/(n - 1)`.

Sort-and-scan is O(n log n) time; that is the level to state first, and buckets are the step down to linear.

## Variations you will meet

- **Radix sort.** Sort in O(d * n) with d digit passes (d is about 10 for 32-bit values in base 10), then scan. Linear for bounded integers and a legitimate answer; the bucket method avoids sorting at all.
- **Minimum gap.** The trick fails: the smallest gap can be *inside* a bucket, so you would need the order inside buckets. This asymmetry is worth saying out loud: buckets work because big gaps cannot hide in small buckets.
- **Contains Duplicate III (220).** Buckets again, but with width chosen by the problem (`t + 1`) and maintained over a sliding window. The roles flip: here same bucket means "too close to be the answer", there it means "close enough to be the answer".
- **Floating-point values.** The same pigeonhole works with real-valued width `(hi - lo)/(n - 1)` and bucket `int((x - lo) / width)`, clamping the top value into the last bucket.

## What to carry forward

Make buckets narrower than the answer is guaranteed to be, and the answer must cross a bucket border, so each bucket only needs its min and max. The next problem, Contains Duplicate III, keeps the value buckets but makes them slide: buckets of width t + 1 over the last k elements answer "is anything close in value and close in index?".
