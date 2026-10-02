# Binary Search

*LeetCode 704 · Easy · Pattern: Binary search on a sorted array · Reading time ~5 min*

## What the problem is really asking

You get a sorted list of distinct integers and a target. Say where the target sits, or say -1 if it is not there. The
answer is one index. The only hard part is the demand for O(log n): you are not allowed to look at most of the array.

```text
idx      0   1   2   3   4   5
nums    -1   0   3   5   9  12
target = 9   -> answer 4
target = 2   -> answer -1 (2 would sit between 0 and 3)
```

## Do it by hand first

Think of a dictionary. You open it in the middle, land on "M" while you want "D", and the whole back half stops
existing for you. Then you open the middle of what is left.

Do that with target 2. Open the middle, index 2: the value is 3. Three is bigger than two, and everything after index 2
is bigger still, so indices 2..5 are dead. Open the middle of 0..1, index 0: the value is -1, too small, and so is
everything before it. Only index 1 is left; it holds 0, also too small. Nothing is left. Answer -1.

What your hand tracked was a pair of fingers, a left edge and a right edge, holding the part of the book where the target
could still be. That pair, `lo` and `hi`, is the whole data structure.

## The first honest attempt

Walk left to right and return the first index whose value equals the target. It is O(n) and obviously correct.

The waste is in what each comparison buys you. When you see `nums[0] = -1 < 2` you learn one fact: index 0 is not the
answer. But sortedness says much more: if the value at some index is too small, every value to its left is too small too.
A scan uses each comparison to kill one cell when it could kill a whole side.

```text
linear scan, target 2:
idx      0   1   2
         ^ too small: kills 1 cell
             ^ too small: kills 1 cell
                 ^ too big: kills 1 cell ... and stops
the comparison at idx 2 also proved idx 3, 4, 5 are too big
```

## The turning point

**Claim: one comparison against the middle of the live range can rule out half the range, not one cell.**

Write a T or F under each cell for the question "is this value smaller than the target?" Because the array is sorted, the
row is all T's then all F's. The target, if it exists, is the first F. Probing the middle tells you which side of that
switch you stand on.

- `nums[mid] == target`: done.
- `nums[mid] < target`: mid and everything left of it is T. Move `lo = mid + 1`.
- `nums[mid] > target`: mid and everything right of it is F and not equal to the target. Move `hi = mid - 1`.

This solution uses the closed window `[lo, hi]`: both ends are live cells. The loop runs while the window is non-empty,
`lo <= hi`. Both updates move a bound strictly past mid, so the window loses at least one cell per round and the loop
must stop. When it stops without finding the target, the window is empty and the target is absent.

## Watch it work

`nums = [-1, 0, 3, 5, 9, 12]`, target = 2. Row P is "nums[i] < 2". L, M, H mark lo, mid, hi.

```text
Frame 1: lo=0 hi=5 mid=2 nums[mid]=3
idx      0   1   2   3   4   5
nums    -1   0   3   5   9  12
P        T   T   F   F   F   F
         L       M           H
```

3 is bigger than 2, so indices 2 to 5 are dead and `hi` becomes 1.

```text
Frame 2: lo=0 hi=1 mid=0 nums[mid]=-1
idx      0   1   2   3   4   5
nums    -1   0   3   5   9  12
P        T   T   F   F   F   F
       L/M   H
```

-1 is smaller than 2, so index 0 is dead and `lo` becomes 1.

```text
Frame 3: lo=1 hi=1 mid=1 nums[mid]=0
idx      0   1   2   3   4   5
nums    -1   0   3   5   9  12
P        T   T   F   F   F   F
         L/M/H
```

One live cell; it holds 0, too small, so `lo` becomes 2.

```text
Frame 4: lo=2 hi=1  -> window empty, return -1
idx      0   1   2   3   4   5
P        T   T   F   F   F   F
             H   L
```

The bounds crossed exactly at the T|F switch: `lo` now points at the first F, where 2 would be inserted.

Across every frame, any cell outside `[lo, hi]` was provably not the target. With target 9 the same loop finds index 4 on
the second probe (mid = 2, then mid = 4).

## Why it is correct

The invariant is: if the target is anywhere in `nums`, it is inside `[lo, hi]`. It holds at the start because the window
is the whole array. Each update only removes cells on the wrong side of a comparison, and sortedness guarantees those
cells are all strictly smaller (or strictly larger) than the target. So the invariant survives every step. If the loop
returns at `nums[mid] == target`, the answer is right. If the window becomes empty, the invariant says the target was
nowhere, so -1 is right.

## Cost

Time O(log n): the window goes n, n/2, n/4, ..., 1, 0, about `log2(n) + 1` probes. Space O(1): two integers.

## Variations you will meet

- **Not present: where would it go?** At the moment the loop ends, `lo` is the insert position. That is the next problem.
- **Duplicates allowed, find the first copy.** Stopping at the first equal value returns an arbitrary copy. You need a
  boundary search instead (problem 3).
- **Unknown length (search in a sorted array of unknown size).** Double `hi` (1, 2, 4, 8, ...) until the value there
  exceeds the target, then search inside. Still O(log n).
- **Java / C++.** `(lo + hi) / 2` can overflow; write `lo + (hi - lo) / 2`.

## What to carry forward

A sorted array turns every comparison into a verdict on a whole side; keep the target trapped between two fingers and
halve the gap. The next problem asks what to return when the target is missing, and the answer is the place where the
fingers crossed.
