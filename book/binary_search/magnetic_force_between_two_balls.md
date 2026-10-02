# Magnetic Force Between Two Balls

*LeetCode 1552 · Medium · Pattern: Binary search on the answer · Reading time ~8 min*

## What the problem is really asking

There are baskets at distinct integer positions along a line. We drop `m` balls into `m` different baskets. Among all pairs of balls, look at the closest pair and call its distance the **minimum gap**. We want to place the balls so that this minimum gap is as large as possible, and return it.

This is a "maximise the minimum" problem. The answer is one integer, a distance. The hard part is that the number of placements is enormous, C(n, m), and the quantity we optimise (the smallest gap) depends on the whole placement at once.

```text
position = [1, 2, 3, 4, 7], m = 3

    1   2   3   4           7
    o   .   .   o   .   .   o      o = ball, . = empty
    |<--- 3 --->|<---- 3 -->|
                                   min gap = 3
```

Balls at 1, 4 and 7 give gaps 3 and 3, so the minimum gap is 3. No placement does better, so the answer is 3.

## Do it by hand first

Sort the positions first, because only order along the line matters. Then try a target. "Can I keep every gap at least 4?" Put the first ball at 1, since the leftmost basket costs nothing. The next ball must be at 5 or beyond, and the first basket that far out is 7. Now there is nowhere left for a third ball, so the answer is no. "At least 3?" Ball at 1, next at 4 or beyond, which is basket 4. Then 7 or beyond, which is basket 7. Three balls placed, so the answer is yes.

```text
target gap d = 4:   1 . . . . . 7    -> 2 balls  (need 3)  NO
                    o           o
target gap d = 3:   1 . . 4 . . 7    -> 3 balls            YES
                    o     o     o
```

Your hand kept track of two things: **where the last ball went** and **how many balls you had placed**. That is the whole state of the check. You also probably noticed that if 3 works, 2 and 1 obviously work too.

## The first honest attempt

"For every gap `d` from 1 up to `max - min`, run the greedy placement and keep the largest `d` that fits all `m` balls." It is correct, but positions go up to 10^9, so the range of `d` can be a billion values. Each check is an O(n) scan, which gives O(n · R) where R = `max - min`.

```text
d = 1: place greedily over all baskets -> fits
d = 2: place greedily over all baskets -> fits
d = 3: place greedily over all baskets -> fits
d = 4: place greedily over all baskets -> fails
d = 5: ... fails     d = 6: ... fails
          ^ once d=4 failed, every bigger d must fail;
            those scans re-learn what we already knew
```

The repeated work is a full scan per candidate gap, even though each answer is implied by its neighbours.

## The turning point

**Claim: the predicate `fits(d)` = "the greedy places at least `m` balls with every gap >= d" is monotone. It is true up to some value and false from then on.**

Two facts back this up.

*The greedy check is right.* For a fixed `d`, put the first ball in the leftmost basket and each later ball in the first basket at least `d` past the previous ball. Why is "as early as possible" safe? Take any valid placement and compare it with the greedy one, ball by ball. The greedy's first ball is no further right than the other placement's first ball. If the greedy's k-th ball is no further right than the other's, then the other placement's (k+1)-th ball is a legal next choice for the greedy too, and the greedy picks the earliest legal choice, so its (k+1)-th ball is no further right either. By induction the greedy never falls behind, so it places at least as many balls as any valid placement.

*Monotonicity.* If every gap in some placement is at least `d`, those same gaps are at least `d - 1`. The same placement works for any smaller target, so `fits(d)` true implies `fits(d - 1)` true.

Over the answer range the picture is `T T ... T F F ... F`. In Koko we wanted the first T. Here we want the **last T**, the largest gap that still fits.

```text
d    :  1  2  3  4  5  6
balls:  5  3  3  2  2  2      (greedy count, need m=3)
fits :  T  T  T  F  F  F
                 ^
           last T = answer 3
```

The solution uses the closed-interval template with a remembered best, which is easy to reason about for "last T":

- `lo = 1` (any two distinct integer positions are at least 1 apart), `hi = pos[-1] - pos[0]` (no gap can exceed the full span), `ans = 1`.
- While `lo <= hi`: if `fits(mid)`, record `ans = mid` and try bigger with `lo = mid + 1`; else try smaller with `hi = mid - 1`.

Problem 12 uses the other way to search for a last T, `lo < hi` with a rounded-up `mid`. Both are fine as long as you stick to one.

## Watch it work

Sorted `pos = [1, 2, 3, 4, 7]`, `m = 3`. The range is `[1, 6]`, with `ans = 1`.

```text
Frame 1   lo=1 hi=6 mid=3        ans=1
  baskets: 1  2  3  4  .  .  7
  greedy : o        o        o   -> 3 balls  T
```
Gap 3 fits, so record `ans = 3` and look higher: `lo = 4`.

```text
Frame 2   lo=4 hi=6 mid=5        ans=3
  baskets: 1  2  3  4  .  .  7
  greedy : o                 o   -> 2 balls  F
```
From 1 the next ball must be at 6 or beyond, which is basket 7, and then nothing is left. Gap 5 is too greedy: `hi = 4`.

```text
Frame 3   lo=4 hi=4 mid=4        ans=3
  baskets: 1  2  3  4  .  .  7
  greedy : o                 o   -> 2 balls  F
```
Gap 4 fails too: `hi = 3`. Now `lo = 4 > hi = 3`, so the loop ends and we return `ans = 3`.

At every moment `ans` held a gap known to fit, everything above `hi` was known to fail, and the true answer lay in `{ans} ∪ [lo, hi]`. The greedy inside each frame only needed "last placed position" and "count".

## Why it is correct

The loop keeps this invariant: **every `d < lo` fits, every `d > hi` fails, and `ans` is the largest `d` known to fit.** It starts true because `d = 1` always fits when `m <= n`, and nothing is known about the rest yet. If `fits(mid)` is true, monotonicity says everything below `mid` fits too, so moving `lo` past `mid` loses nothing, and `ans = mid` records the best value so far. If it is false, everything above `mid` fails, so `hi = mid - 1` loses nothing. When `lo > hi`, every value has been sorted into "fits" (at most `ans`) or "fails" (above `ans`), so `ans` is the largest fitting gap. The greedy argument above guarantees that each `fits(mid)` is the true answer to "can `m` balls be placed with gap at least `mid`?", not just what one particular strategy managed.

## Cost

- **Time: O(n log n + n log R)**. Sorting once, then about log₂ R greedy passes, with R = `max - min`.
- **Space: O(n)** for the sorted copy (O(1) extra if you sort in place).

With R up to 10^9 that is about 30 passes.

## Variations you will meet

- **Aggressive Cows (classic SPOJ).** This is the same problem under another name: stalls and cows instead of baskets and balls.
- **Minimise the maximum distance to a gas station (LeetCode 774).** It flips to "minimise the maximum", so the predicate becomes F...FT...T. The answer is real-valued, so you loop on `hi - lo > eps`, and the check counts how many stations each gap needs.
- **Placements on a circle.** The gap that wraps from the last basket to the first also counts. A common trick is to fix the first ball and run the greedy on the unrolled line, checking the wrap gap at the end.
- **Return the placement, not just the gap.** Rerun the greedy at the final `ans` and record where the balls went.

## What to carry forward

For "maximise the minimum", ask "can I keep every gap at least `d`?" Answer it greedily, placing each item as early as allowed, and binary search for the last `d` that still works.

The next problem flips to "minimise the maximum": we choose where to cut an array so the largest piece is small, and the greedy check packs pieces under a cap instead of spacing balls apart.
