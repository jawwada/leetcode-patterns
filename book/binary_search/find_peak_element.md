# Find Peak Element

*LeetCode 162 · Medium · Pattern: Binary search on a monotone predicate · Reading time ~7 min*

## What the problem is really asking

An array where no two neighbours are equal. Pretend there is a value of minus infinity just outside each end. A *peak*
is an index whose value is bigger than both neighbours. Return the index of any peak, in O(log n).

```text
          -inf  1   2   1   3   5   6   4  -inf
idx              0   1   2   3   4   5   6
                     ^                   ^
                   peak                peak
answer: 1 or 5 (either is accepted)
```

Two things are unusual. The array is not sorted, so the usual reason for binary search is missing. And the answer is not
unique: you are asked for *a* peak, not the highest one. That freedom is what makes O(log n) possible. Finding the global
maximum of an unsorted array needs O(n); finding some local maximum does not.

## Do it by hand first

Picture the values as a mountain range, with cliffs dropping to minus infinity at both ends.

```text
value
  6 |                *
  5 |             *
  4 |                   *
  3 |          *
  2 |    *
  1 | *     *
    +------------------------
      0  1  2  3  4  5  6     idx
 -inf                          -inf
```

You are dropped somewhere in the fog and can only see the ground right next to you. Strategy: walk uphill. If you keep
going uphill you must eventually stop, because the range ends in a cliff. The place you stop is a peak.

Your hand kept track of one thing at each spot: **which way is uphill**. That is a single comparison with a neighbour.

## The first honest attempt

Walk from the left and return the first i with `nums[i] > nums[i+1]` (or the last index if that never happens). That
first i is a peak: you climbed into it (or it is index 0, next to minus infinity) and it drops after it. O(n).

The waste: the walk confirms "still climbing" one step at a time.

```text
walk from 0:  up? 1<2 yes  -> 2>1 stop: peak at 1
on [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
  up, up, up, up, up, up, up, up, stop -> 9 steps
  the first "up" at idx 0 already proved a peak lies right;
  the walk did not need to see every step of the climb
```

## The turning point

**Claim: if the ground rises to the right of mid (`nums[mid] < nums[mid+1]`), a peak exists strictly right of mid;
otherwise a peak exists at mid or to its left.**

Justify the first half. From mid+1 keep walking right while it goes up. You cannot go up forever, because the array ends
and beyond it is minus infinity. The spot where you stop going up is a peak, and it is right of mid.

The second half is the mirror image. If `nums[mid] > nums[mid+1]`, then mid is higher than its right neighbour. Walk left
from mid while the ground rises to the left. You stop at a peak, which may be mid itself, and in any case is at mid or
left of it, because the left end is a cliff too.

So the test "is it uphill to the right?" plays the role of P:

- T (`nums[mid] < nums[mid+1]`): `lo = mid + 1`.
- F: `hi = mid`, keeping mid, because mid itself may be the peak.

This is the background template exactly. Two details follow from it. First, `while lo < hi` guarantees `mid < hi <= n-1`,
so `nums[mid + 1]` always exists and you never need to fake the minus-infinity on the right. Second, `hi = mid - 1` would
be a bug: when mid is the peak, it throws the peak away.

But look at the T/F row for the example: it is **not** monotone.

```text
nums     1   2   1   3   5   6   4
up?      T   F   T   T   T   F   F
             ^               ^
          T->F             T->F
```

Every T followed by an F is a peak. The search does not find "the" border, because there are several. What it protects
is a weaker promise: **the cell just left of `lo` is T (or lo is 0), and the cell at `hi` is F.** Any row that starts
with T and ends with F has a T-to-F switch somewhere in between, and that switch is a peak. Halving keeps the promise, so
the window always contains a peak. It is the same reason bisection finds a root of a continuous function that changes
sign: you do not need monotonicity, only opposite signs at the two ends.

## Watch it work

`nums = [1, 2, 1, 3, 5, 6, 4]`. Row `up?` is `nums[i] < nums[i+1]`, with minus infinity after index 6 making the last cell
F.

```text
Frame 1: lo=0 hi=6 mid=3
idx      0   1   2   3   4   5   6
nums     1   2   1   3   5   6   4
up?      T   F   T   T   T   F   F
         L           M           H
nums[mid]=3 vs nums[mid+1]=5
```

Uphill to the right of index 3, so a peak waits on the right: `lo = 4`. The peak at index 1 is abandoned; that is fine,
any peak will do.

```text
Frame 2: lo=4 hi=6 mid=5
idx      0   1   2   3   4   5   6
nums     1   2   1   3   5   6   4
up?      T   F   T   T   T   F   F
                         L   M   H
nums[mid]=6 vs nums[mid+1]=4
```

Downhill after index 5: a peak is at 5 or left of it. Keep mid: `hi = 5`.

```text
Frame 3: lo=4 hi=5 mid=4
idx      0   1   2   3   4   5   6
nums     1   2   1   3   5   6   4
up?      T   F   T   T   T   F   F
                       L/M   H
nums[mid]=5 vs nums[mid+1]=6
```

Uphill again: `lo = 5`.

```text
Frame 4: lo=5 hi=5
idx      0   1   2   3   4   5   6
nums     1   2   1   3   5   6   4
up?      T   F   T   T   T   F   F
                           L/H
```

One cell left. Index 5 (value 6) is bigger than 5 on its left and 4 on its right. Return 5.

In every frame the cell left of L was a T (index 3, then index 4) and the cell under H was an F. A T-to-F switch, and so
a peak, was always trapped in the window.

## Why it is correct

Invariant: either `lo == 0` or `nums[lo-1] < nums[lo]`; and either `hi == n-1` or `nums[hi] > nums[hi+1]`. In words, the
ground rises into the window at its left edge and falls out of it at its right edge (the minus infinities make this true
at the start). Any window with that property contains a peak: walk right from lo while rising; you must stop at or before
hi, and where you stop is a peak.

Each branch keeps the invariant. If `nums[mid] < nums[mid+1]`, the new lo is mid+1, and the ground rises into it from mid.
If `nums[mid] > nums[mid+1]`, the new hi is mid, and the ground falls out of it to mid+1. The window shrinks each round
because `lo <= mid < hi`. When `lo == hi`, the one-cell window rises in and falls out: it is a peak.

## Cost

Time O(log n): the window halves per comparison. Space O(1).

## Variations you will meet

- **Peak in a mountain array (LeetCode 852).** Exactly one peak, so the row `up?` really is T...TF...F and the same code
  finds the summit. That is the first step of the next problem.
- **Find a peak in a 2D grid (LeetCode 1901).** Binary search on columns: take the middle column, find its maximum, and
  move toward the larger horizontal neighbour. O(m log n). Same uphill argument, one dimension up.
- **Local minimum.** Flip the comparison and walk downhill.
- **Equal neighbours allowed.** The argument breaks: on a plateau you cannot tell which way is up, and the problem can need
  O(n) in the worst case.

## What to carry forward

Binary search needs a T on the left end and an F on the right end of the window, not a sorted array; for peaks the
question is "is it uphill to the right?" and you always step toward higher ground. The next problem uses this to find the
summit of a mountain, then searches both slopes as two sorted arrays, under a strict budget of reads.
