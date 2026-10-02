# Count of Smaller Numbers After Self
*LeetCode 315 · Hard · Pattern: Merge sort counting · Reading time ~10 min*

## What the problem is really asking

For every position `i` in `nums`, count how many elements to its *right* are *strictly smaller* than `nums[i]`. Return those n counts as a list.

The answer is an array of n numbers, one per position. What makes it hard is that each count mixes two different orders. "To the right" is about index order. "Smaller" is about value order. Any one of these questions alone is easy: sorting answers value questions, a single scan answers index questions. Here every answer needs both at the same time, for every element.

```text
idx:     0   1   2   3
nums:  [ 5,  2,  6,  1 ]

5: right of it  2 6 1  -> smaller: 2, 1   -> 2
2: right of it  6 1    -> smaller: 1      -> 1
6: right of it  1      -> smaller: 1      -> 1
1: right of it  (none)                    -> 0
counts = [2, 1, 1, 0]
```

## Do it by hand first

The natural way by hand is to go from right to left, keeping a *sorted* pile of everything you have already passed. Each new element's answer is its rank in that pile: how many cards in the pile are below it. Then you slide it into the pile.

```text
read 1:  pile []          rank of 1 = 0   pile [1]
read 6:  pile [1]         rank of 6 = 1   pile [1 6]
read 2:  pile [1 6]       rank of 2 = 1   pile [1 2 6]
read 5:  pile [1 2 6]     rank of 5 = 2   pile [1 2 5 6]
counts (left to right) = [2, 1, 1, 0]
```

What your hand kept was *the suffix to the right, in sorted order*. That is the seed. With a sorted Python list and `bisect`, the rank is O(log n), but inserting into the middle of a list shifts everything after it, O(n) per insert, O(n^2) total. We need a way to build sorted suffixes that does not pay for one insertion at a time.

## The first honest attempt

For each `i`, scan every `j > i` and count `nums[j] < nums[i]`. O(n^2) time, O(1) extra space.

```text
i=0 (5):  compare with  2  6  1     3 comparisons
i=1 (2):  compare with     6  1     2 comparisons
i=2 (6):  compare with        1     1 comparison
          the suffix [6, 1] is re-examined for i=0 and i=1,
          the suffix [1] for i=0, i=1 and i=2
```

The waste: the suffix to the right of `i` is mostly the same suffix that was examined for `i - 1`, but its order is rediscovered from scratch, one comparison at a time. Every pair of elements is compared individually; nothing learned about the relative order of 6 and 1 is reused.

## The turning point

We need to learn a little about merge sort first, because it is the tool that builds sorted runs cheaply, and it has a property that is exactly what this problem needs.

**Merge sort in one picture.** Split the array in half, sort each half recursively, then *merge* the two sorted halves. A single element is already sorted. Merging two sorted lists is a zip: keep a pointer at the head of each, repeatedly take the smaller head, advance that pointer.

```text
split:          [5 2 6 1]
               /         \
          [5 2]           [6 1]
          /   \           /   \
        [5]   [2]       [6]   [1]

merge:  [5]+[2] -> [2 5]     [6]+[1] -> [1 6]
        [2 5] + [1 6]:
          left  2 5      right  1 6
                ^i              ^j
          take 1 (right head smaller), then 2, 5, then 6
        -> [1 2 5 6]
```

Each level of the tree touches every element once during merging, and there are about log n levels, so merge sort is O(n log n).

**The property we need.** Look at any merge. The left half came from positions `lo..mid-1` of the original array and the right half from `mid..hi-1`. So *every element of the right half was originally to the right of every element of the left half*. Inside a single merge, "to the right of" is a fact you get for free. The only thing left to decide is "smaller", and the merge is deciding exactly that.

**Claim: when the merge emits a left element `x`, the number of right-half elements already emitted, `j - mid`, is exactly the number of elements in that right half that are smaller than `x` and to its right.**

Justify it. A right element is emitted before `x` only if it was strictly smaller than the left head at that moment, and the left heads only grow, so it was strictly smaller than `x` too. A right element not yet emitted is at least `x` (the right half is sorted, and the current right head was not strictly smaller than `x`, otherwise it would have gone first). So the emitted ones are precisely the smaller ones.

Now sum over all levels. Take any pair `p < q` in the original array. They start in the same half and are split apart at exactly one merge, the one where `p` falls in the left half and `q` in the right. At that merge and only there, `q` is in the right half of a merge where `p` is on the left. So every "smaller and to the right" pair is counted exactly once, at the level where the two elements are separated.

Two implementation details turn this into code:

- **Sort indices, not values.** Merging moves elements around, so we must remember which original position each one came from, otherwise we do not know whose count to increase. Keep an array `idx` of positions and sort it by `nums[idx]`; add to `counts[idx[i]]`.
- **Ties go left first.** Emit the right head only if it is *strictly* smaller. On equality emit the left element first, so an equal right element is not counted as smaller.

The heart of the merge, as code:

```python
if nums[idx[j]] < nums[idx[i]]:   # strictly smaller: right
    merged.append(idx[j]); j += 1
else:                             # left goes, stamp count
    counts[idx[i]] += j - mid
    merged.append(idx[i]); i += 1
```

When the right half runs out first, the remaining left elements still each get `+ (j - mid)`: all of the right half was smaller than them.

## Watch it work

`nums = [5, 2, 6, 1]`. Elements are written as value(original index).

```text
Frame 1   split to singletons
          [5(0)] [2(1)] | [6(2)] [1(3)]
          counts = [0, 0, 0, 0]
```
Singletons are sorted; no counting yet.

```text
Frame 2   merge [5(0)] + [2(1)]       mid boundary: |
          left 5   right 2:  2 < 5  -> emit 2, j-mid = 1
          right empty: flush 5, counts[0] += 1
          -> [2(1) 5(0)]        counts = [1, 0, 0, 0]
```
5 learns that one smaller element (the 2) is to its right.

```text
Frame 3   merge [6(2)] + [1(3)]
          left 6   right 1:  1 < 6  -> emit 1, j-mid = 1
          right empty: flush 6, counts[2] += 1
          -> [1(3) 6(2)]        counts = [1, 0, 1, 0]
```
Same story for 6 and 1. Its count is now final.

```text
Frame 4   merge [2(1) 5(0)] + [1(3) 6(2)]
          left  2 5     right 1 6
                ^i            ^j
          1 < 2 -> emit 1(3), j-mid = 1
          out: [1(3)]
```
The right element 1 is smaller than the left head, so it goes first.

```text
Frame 5   left  2 5     right 1 6
                ^i              ^j
          6 < 2? no -> emit 2(1), counts[1] += 1
          6 < 5? no -> emit 5(0), counts[0] += 1
          out: [1(3) 2(1) 5(0)]   counts = [2, 1, 1, 0]
```
Both left elements see one emitted right element (the 1) and stamp it on their counts.

```text
Frame 6   left exhausted, append rest of right: 6(2)
          idx = [3, 1, 0, 2]    (values 1 2 5 6)
          counts = [2, 1, 1, 0]
```
The array is sorted and every count is complete.

Across all frames, inside each merge the right half was always "later in the original array", and `j - mid` was always the number of right elements already passed, all strictly smaller than the current left head. The 5 collected its total in two installments: 1 from its own pair merge and 1 from the top merge.

## Why it is correct

Invariant for one merge: when the left element `x` is emitted, the emitted right elements are exactly the right-half elements strictly smaller than `x`. Shown above: emitted right elements were strictly smaller than some left head that is no larger than `x`; unemitted ones are at least the current right head, which is at least `x`.

Invariant across levels: after `sort(lo, hi)` returns, `idx[lo:hi]` is sorted by value, and for every position `p` in that range, `counts[p]` has been increased by the number of `q` with `p < q < hi`, `q` in `lo..hi-1`, and `nums[q] < nums[p]`. Proof by induction: the two recursive calls handle pairs inside each half; the merge handles pairs with one in each half, exactly once each. At the top level, `lo..hi` is the whole array, so `counts[p]` is the full answer.

## Cost

- **Time O(n log n):** about log n levels of recursion, each level's merges touching every element once.
- **Space O(n):** the `idx` and `counts` arrays, the merge buffer, plus O(log n) recursion depth.

Brute force is O(n^2) time and O(1) space; the sorted pile with `bisect.insort` is O(n^2) in the worst case because of list shifting.

## Variations you will meet

- **Count of inversions.** The total number of pairs `p < q` with `nums[p] > nums[q]` is the sum of these counts. Same merge, one running total instead of per-element counts, and no need for `idx`.
- **Count larger numbers before self.** Mirror image: when a *right* element is emitted, the left elements not yet emitted are larger and earlier, so add `mid - i` to it.
- **Fenwick tree instead of merge sort.** Scan from right to left and keep a count per (compressed) value; each answer is "how many inserted values are below `nums[i]`", a prefix sum. That is the hand method with a better pile. The last problem of this chapter builds that tree from scratch.
- **Count of Range Sum (327).** Merge sort over prefix sums, but the condition is a window `lower <= P[q] - P[p] <= upper`, counted with two pointers in a separate pass before merging. That separate pass is exactly the shape of the next problem.

## What to carry forward

Inside a merge, every right element is later in the original array than every left element, so "later and smaller" becomes "already emitted from the right", and `j - mid` counts it. The next problem, Reverse Pairs, keeps the same merge skeleton but changes the comparison to `x > 2r`, which no longer matches the merge's own comparison, so counting has to move into its own pass.
