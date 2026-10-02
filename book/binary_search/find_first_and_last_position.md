# Find First and Last Position of Element in Sorted Array

*LeetCode 34 · Medium · Pattern: Binary search for a boundary (lower / upper bound) · Reading time ~7 min*

## What the problem is really asking

The array is sorted but may contain repeats. Given a target, return the index of its first copy and the index of its
last copy, or `[-1, -1]` if it does not appear. O(log n), no matter how many copies there are.

The answer is a pair of indices that bracket a *run*: a flat stretch of equal values.

```text
idx      0   1   2   3   4   5
nums     5   7   7   8   8  10
                     [-----]
target 8 -> [3, 4]
target 6 -> [-1, -1]
```

What makes it hard is that "find the target" is not enough. Finding *some* 8 tells you nothing about how far the run of
8s extends in either direction, and a run can be as long as the whole array.

## Do it by hand first

Draw the sorted array as a staircase. Each distinct value is a step; repeats make a step wider.

```text
value
 10 |                      ___
  8 |              _______
  7 |      _______
  5 |  ___
    +-----------------------------
       0   1   2   3   4   5   idx
```

The run of 8s is a flat tread. Its left edge is where the staircase first reaches height 8. Its right edge is one cell
before the staircase first goes *above* 8. Your eye found both by asking about heights, not by walking along the tread.

So your hand kept track of two borders:

- the first index with value at least 8, which is 3;
- the first index with value greater than 8, which is 5.

The answer is `[3, 5 - 1] = [3, 4]`.

## The first honest attempt

Two common answers come out first.

**Scan once**, remembering the first and last index where the value equals the target. O(n).

**Binary search for any copy, then expand** left and right while the neighbours still equal the target. This feels
logarithmic, and it is when the run is short. But the expansion walks the run one cell at a time:

```text
nums = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]    target 8
binary search lands at idx 4
expand left : 3, 2, 1, 0        4 steps
expand right: 5, 6, 7, 8, 9     5 steps
total ~ n
```

The repeated work is stepping along a run of identical values, where each comparison says "still 8" and learns nothing
new about the border.

## The turning point

**Claim: each end of the run is a border between T's and F's of a monotone question, so each end costs one binary
search, independent of the run's length.**

The two questions are:

```text
nums       5   7   7   8   8  10
x < 8 ?    T   T   T   F   F   F    first F = 3 = lower(8)
x < 9 ?    T   T   T   T   T   F    first F = 5 = lower(9)
```

The first F of `nums[i] < 8` is the first copy of 8. The first F of `nums[i] < 9` is the first value bigger than 8, one
past the last copy. Because values are integers, "first value > 8" is the same as "first value >= 9", so one helper,
`lower(x)`, answers both: `first = lower(target)` and `last = lower(target + 1) - 1`.

The helper uses the half-open template from the background chapter, `hi = n` and `while lo < hi`:

- `nums[mid] < x` (T): mid is before the border. `lo = mid + 1`.
- otherwise (F): mid could be the border. `hi = mid`, keeping mid in the window.

Why half-open here? Because the border can be n. For `lower(11)` on this array every cell is T and the right answer is 6,
one past the end. The half-open window `[lo, hi)` starts as `[0, 6)` and can collapse onto 6 without ever reading
`nums[6]`, because mid is always strictly less than hi.

After the first search, check that the target is actually there: if `first == n` or `nums[first] != target`, the target
is absent. Without this check, target 6 gives `lower(6) = 1` and `lower(7) - 1 = 0`, and you would return the nonsense
pair `[1, 0]`.

## Watch it work

`nums = [5, 7, 7, 8, 8, 10]`, target 8. Two searches; the second row of T/F changes with x. Index 6 is the
past-the-end slot.

```text
Frame 1: lower(8) lo=0 hi=6 mid=3
idx      0   1   2   3   4   5  |6
nums     5   7   7   8   8  10
P8       T   T   T   F   F   F
         L           M           H
```

`nums[3] = 8` is not less than 8 (F). Mid might be the first copy, so `hi = 3`, not 2.

```text
Frame 2: lower(8) lo=0 hi=3 mid=1
idx      0   1   2   3   4   5  |6
nums     5   7   7   8   8  10
P8       T   T   T   F   F   F
         L   M       H
```

7 < 8 (T): the border is right of index 1, `lo = 2`.

```text
Frame 3: lower(8) lo=2 hi=3 mid=2
idx      0   1   2   3   4   5  |6
nums     5   7   7   8   8  10
P8       T   T   T   F   F   F
               L/M   H
```

7 < 8 again: `lo = 3 = hi`. The loop stops, `first = 3`, and `nums[3] == 8` confirms the target exists.

```text
Frame 4: lower(9) lo=0 hi=6 mid=3
idx      0   1   2   3   4   5  |6
nums     5   7   7   8   8  10
P9       T   T   T   T   T   F
         L           M           H
```

Same array, new question. Now `nums[3] = 8 < 9` is T, so `lo = 4`.

```text
Frame 5: lower(9) lo=4 hi=6 mid=5
idx      0   1   2   3   4   5  |6
nums     5   7   7   8   8  10
P9       T   T   T   T   T   F
                         L   M   H
```

10 is not less than 9 (F): `hi = 5`.

```text
Frame 6: lower(9) lo=4 hi=5 mid=4
idx      0   1   2   3   4   5  |6
nums     5   7   7   8   8  10
P9       T   T   T   T   T   F
                       L/M   H
```

8 < 9 (T): `lo = 5 = hi`. `lower(9) = 5`, so `last = 4`. Answer `[3, 4]`.

In both searches every cell left of L was known T and every cell from H on was known F (or past the end). Neither search
ever walked along the run of 8s; with a run of a million 8s, both would still take about 20 probes.

## Why it is correct

On a sorted array, `nums[i] < x` is monotone: true at i implies true at every smaller index. So the row is T...TF...F
with the border somewhere in `0..n`. The helper's invariant is "cells below `lo` are T, cells at or above `hi` are F or
past the end". Each branch preserves it: a T at mid lets `lo` jump past mid; an F at mid lets `hi` drop to mid. The window
shrinks every round because `lo <= mid < hi`. When `lo == hi`, nothing is unknown and `lo` is the first F.

Then `lower(target)` is the first index holding a value at least the target. It holds the target exactly when the target
exists (that is the presence check). `lower(target + 1)` is the first index with a value above the target, so the cell
before it is the last copy.

## Cost

Time O(log n): two binary searches, each about `log2(n + 1)` probes. Space O(1).

## Variations you will meet

- **Count occurrences.** `lower(t + 1) - lower(t)`, or `bisect_right(a, t) - bisect_left(a, t)`. Zero means absent.
- **Non-integer values.** "first value > target" cannot be written as `lower(target + 1)` for floats or strings. Write an
  `upper` helper with the test `nums[mid] <= x` instead, which is `bisect_right`.
- **Range count queries.** How many values lie in `[a, b]`? `bisect_right(b) - bisect_left(a)`. Many later counting
  problems reduce to exactly this.
- **One helper, two predicates.** Some people write a single function with a flag `left=True/False` that switches between
  `<` and `<=`. Same idea; pick whichever you can write without hesitation.

## What to carry forward

A range in sorted data is two borders, and each border is a first F you can find in log n regardless of the run's length:
`[lower(t), lower(t+1) - 1]`. The next problem keeps the plain lookup but hides the sorted array inside a grid, so the
candidates become virtual positions.
