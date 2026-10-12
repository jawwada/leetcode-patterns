# Maximum Average Subarray II

*LeetCode 644 · Hard · Pattern: Binary search on the answer · Reading time ~11 min*

## The problem

Given an integer array nums and an integer k, find a contiguous subarray of length at least k with the maximum average
and return that average; any answer within 1e-5 of the true value is accepted.

```text
Example: nums = [1,12,-5,-6,50,3], k = 4 returns 12.75, the
  average of [12,-5,-6,50].
```

## What the problem is really asking

Among all contiguous subarrays whose length is **at least** `k`, find the largest average and return it (to within `1e-5`).

The answer is a real number, not an integer, and that is new for this chapter. The "at least `k`" makes the problem hard. With exactly `k` a sliding window would finish it in one pass (that is part I of this problem). With "at least `k`", a longer subarray might win by swallowing a big value even though it also swallows some negatives. Averages do not add up nicely, so the best subarray cannot be built from best pieces.

```text
nums = [1, 12, -5, -6, 50, 3], k = 4

index:   0   1   2   3   4   5
value:   1  12  -5  -6  50   3
             [-------------]       length 4
             12-5-6+50 = 51  -> 51/4 = 12.75   best

         [------------------]      length 5
         1+12-5-6+50 = 52    -> 10.4
             [------------------]  length 5: 54/5 = 10.8
```

The answer is 12.75. Adding the 3 at the end, or the 1 at the front, pulls the average down.

## Do it by hand first

Most people pick a target and test it. "Is there a long-enough stretch averaging at least 10?" Subtract 10 from every number and ask whether some stretch of length at least 4 now sums to zero or more.

```text
value    :   1  12  -5  -6  50   3
minus 10 :  -9   2 -15 -16  40  -7
stretch [1..4]: 2-15-16+40 = 11 >= 0   -> YES, 10 reachable

minus 13 : -12  -1 -18 -19  37 -10
stretch [1..4]: -1-18-19+37 = -1 <  0
(no other length>=4 stretch does better) -> NO
```

So the answer lies between 10 and 13. Your hand kept **a target `x`**, and the trick that made each test easy was **shifting every value by `-x`**, which turns an average question into a sum question. Sums are what prefix sums and running minima handle well.

## The first honest attempt

"For every start `i`, extend `j` rightward with a running sum, and whenever the length is at least `k` compare `sum / length` with the best so far." That is O(n²) time and O(1) space. With `n = 10^4` it is 5 · 10^7 steps, which is borderline in compiled code and too slow in Python.

```text
start 0: len4 [1 12 -5 -6]  len5 [.. 50]  len6 [.. 3]
start 1: len4 [12 -5 -6 50] len5 [.. 3]
start 2: len4 [-5 -6 50 3]
  every subarray is evaluated, and the averages of
  overlapping stretches are recomputed from scratch
  as separate ratios -- nothing carries over
```

The waste is that we compute an exact average for Θ(n²) subarrays, when for any single target the question "does any subarray reach it?" has a linear-time answer.

## The turning point

**Claim: the predicate `can(x)` = "some subarray of length >= k has average >= x" is monotone in `x`, and after shifting every element by `-x` it is decided in O(n) by a prefix-minimum scan.**

*Monotone.* If some subarray averages at least `x`, the same subarray averages at least any `x' < x`. So `can` is true for every target up to the true answer and false above it. Over the real line from `min(nums)` to `max(nums)` (an average always lies between the smallest and largest element), `can` reads `T ... T F ... F`, and we want the boundary, the **last T**.

```text
x   :  -6     8    11.5  12.75  13.25   15     22      50
can :   T     T     T      T      F      F      F       F
                           ^
                 last T = answer
```

*The shift.* For a subarray of length `L > 0`, `sum / L >= x` exactly when `sum - x·L >= 0`, which is the same as `sum(v - x for v in it) >= 0`. So subtract `x` from every element and the question becomes whether some subarray of length at least `k` has a non-negative sum.

*Prefix sums.* Let `P[0] = 0` and `P[j] = P[j-1] + nums[j-1] - x`. The subarray `[i, j)` has shifted sum `P[j] - P[i]` and length `j - i`. We need some `j` with `P[j] - P[i] >= 0` for some `i <= j - k`, which is the same as `P[j] >= min(P[0..j-k])`. Sweep `j` from `k` to `n`, folding `P[j-k]` into a running minimum before each comparison. One pass.

```text
the lag is the whole constraint:
  P:  P0  P1  P2  P3  P4  P5  P6
                      ^j=4: may pair with P0 only
                          ^j=5: P0..P1
                              ^j=6: P0..P2
  running min admits P[j-k] just as j reaches it
```

Drawn as a curve, the prefix sums of the shifted values rise and fall. `can(x)` asks whether some point of the curve sits at or above some earlier point that is at least `k` steps to its left. Raising `x` tilts the whole curve downward, which is why the answer flips exactly once.

Why does the shift help so much? An average is a ratio, and ratios do not compose: knowing the best average of the left half and of the right half tells you little about the best average overall, so no Kadane-style recurrence works on averages directly. Once `x` is fixed and subtracted, the quantity becomes a plain sum, and sums compose perfectly, which is why prefix sums apply. Binary search buys us the right to fix `x`. This is the general lesson of the whole "search the answer" family: guessing the answer turns an awkward objective into a simple yes/no question about sums, counts, or placements.

Notice also that `P[0] = 0` is part of the running minimum from the first comparison. It stands for "start the subarray at index 0". Forgetting it silently drops every subarray that begins at the front.

*Real-valued search.* There is no "first integer" here. We keep `lo` known-T and `hi` known-F and halve until `hi - lo <= 1e-6`. On T set `lo = mid`, on F set `hi = mid`, with no `+1` and no `-1`. The interval starts at width `max - min` and halves each probe, so about `log₂((max - min) / 1e-6)` probes are needed, around 26 for this example and about 35 at the problem's limits.

## Watch it work

`nums = [1, 12, -5, -6, 50, 3]`, `k = 4`. Start with `lo = -6`, `hi = 50`.

```text
Frame 1   lo=-6  hi=50  mid=22
  P = [0, -21, -31, -58, -86, -58, -77]
  j=4: -86 vs min(P0)=0        no
  j=5: -58 vs min(P0..1)=-21   no
  j=6: -77 vs min(P0..2)=-31   no      -> F
```
No subarray reaches 22: `hi = 22`.

```text
Frame 2   lo=-6  hi=22  mid=8
  P = [0, -7, -3, -16, -30, 12, 7]
  j=4: -30 vs 0                no
  j=5:  12 vs min(0,-7)=-7     yes     -> T
        (subarray [1..4], 12 -5 -6 50)
```
Some subarray beats 8: `lo = 8`.

```text
Frame 3   lo=8  hi=22  mid=15
  P = [0, -14, -17, -37, -58, -23, -35]
  j=4: -58 vs 0   j=5: -23 vs -14   j=6: -35 vs -17
  all below                            -> F
```
Nobody reaches 15: `hi = 15`.

```text
Frame 4   lo=8  hi=15  mid=11.5
  P = [0, -10.5, -10, -26.5, -44, -5.5, -14]
  j=4: -44 vs 0                no
  j=5: -5.5 vs -10.5           yes     -> T
```
11.5 is reachable: `lo = 11.5`.

```text
Frame 5   lo=11.5  hi=15  mid=13.25
  P = [0, -12.25, -13.5, -31.75, -51, -14.25, -24.5]
  j=5: -14.25 vs -12.25  no   j=6: -24.5 vs -13.5  no
                                       -> F
```
13.25 is out of reach: `hi = 13.25`. The answer is now pinned in `[11.5, 13.25]`.

```text
Frame 6   after 26 probes: hi - lo < 1e-6
  lo = 12.7499994...      return lo
  check x=12.75: j=5: P5=-11.75 vs min(0,-11.75)
                 -11.75 - (-11.75) = 0 >= 0  -> T
```
The interval collapses onto 12.75. At exactly 12.75 the best subarray has shifted sum zero, which is the boundary itself.

Across all frames `can(lo)` stayed true and `can(hi)` stayed false. Each probe was a single forward pass carrying one running minimum, and the minimum always lagged `j` by exactly `k`.

## Why it is correct

**Invariant: the true answer `A` satisfies `lo <= A <= hi`.** At the start, `A` is an average of some elements, so it lies in `[min, max]`. If `can(mid)` holds, some subarray reaches `mid`, so `A >= mid` and `lo = mid` keeps `A` inside. If not, no subarray reaches `mid`, so `A < mid` and `hi = mid` keeps it inside. Each step halves `hi - lo`. When the width falls below `1e-6`, `lo` is within `1e-6` of `A`, well inside the `1e-5` tolerance.

The probe itself is exact. Every subarray of length at least `k` ending at `j` starts at some `i <= j - k`, and its shifted sum is `P[j] - P[i]`, which is at most `P[j] - min(P[0..j-k])`. So the scan finds a non-negative sum if one exists. The floating-point rounding in `P` is far below the tolerance.

## Cost

- **Brute force:** O(n²) time, O(1) space.
- **Binary search on the average:** O(n · log(R / ε)) time, where R = `max - min` and ε = `1e-6`, about 35 passes at the limits. **O(n)** space for the prefix array (O(1) if you fold it into the sweep).

There is also an O(n) convex-hull solution that treats prefix sums as points and looks for the steepest slope, but it is much harder to get right in an interview.

## Variations you will meet

- **Maximum Average Subarray I (LeetCode 643).** With exactly length `k`, a fixed window is enough and no search is needed.
- **Fractional programming in general.** Maximising a ratio `sum(a) / sum(b)` over some family of choices: binary search `x` and ask whether `sum(a - x·b) >= 0` is achievable. Examples include the best ratio cycle and the best density subgraph. It is the same shift.
- **Minimum average, length at least k.** Negate the array, or flip the predicate and track a running maximum.
- **Return the subarray.** At the final `lo`, rerun the check and remember the `(i, j)` that succeeded.

## What to carry forward

To optimise an average (or any ratio), guess the answer `x`, subtract it from every element, and ask whether some valid choice has a non-negative sum. When the answer is real-valued, search with `lo = mid` / `hi = mid` until the interval is narrower than the tolerance.

The last problem leaves "search the answer" for a different space: the position of a cut through two sorted arrays, where the check compares four boundary values instead of scanning anything.
