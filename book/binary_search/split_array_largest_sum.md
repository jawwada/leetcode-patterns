# Split Array Largest Sum

*LeetCode 410 · Hard · Pattern: Binary search on the answer · Reading time ~10 min*

## What the problem is really asking

We have an array of non-negative integers and must cut it into exactly `k` contiguous, non-empty pieces. Each piece has a sum. Among the `k` sums one is the largest, and we want to choose the cuts so that this largest sum is as small as possible.

Think of it as dividing a row of jobs among `k` workers in order, where each worker takes a contiguous stretch, and we want the busiest worker to be as lightly loaded as possible. The answer is a single number, a load. It is "minimise the maximum", the mirror image of the last problem's "maximise the minimum".

```text
nums = [7, 2, 5, 10, 8], k = 2

  [ 7  2  5 | 10  8 ]
    -------   -----
     14        18          largest = 18

  [ 7  2  5  10 | 8 ]
    ------------  -
         24       8        largest = 24  (worse)
```

The best split is `[7,2,5] | [10,8]` with a largest sum of 18. What makes this hard is that a cut affects two pieces at once, so moving one cut to help one piece hurts its neighbour, and with `k` cuts these effects chain across the whole array.

## Do it by hand first

Most people do this by guessing a budget. "Could each piece stay under 15?" Walk from the left with a running total. 7, then 9, then 14. Adding 10 would give 24, which is over 15, so cut. Start again with 10, and adding 8 would give 18, so cut again. Then 8 alone. That makes three pieces, but we only get two, so 15 is too tight. "Under 20?" 7, 9, 14, then 10 would give 24, so cut. 10, 18. That makes two pieces, so 20 works.

```text
budget 15:  7 2 5 | 10 | 8        -> 3 pieces  (too many)
            -----   --   -
             14     10   8
budget 20:  7 2 5 | 10 8          -> 2 pieces  (fits)
            -----   ----
             14      18
```

Your hand kept two numbers: **the running sum of the current piece** and **how many pieces you have opened**. You also cut only when forced, filling each piece as full as the budget allowed. That greedy habit, together with the guessed budget, is the whole algorithm.

## The first honest attempt

"Try every placement of the `k - 1` cuts among the `n - 1` gaps between elements. For each placement, sum the pieces and take the max. Keep the smallest max." There are C(n-1, k-1) placements, which is exponential when `k` is around `n/2`. Each one costs O(n).

```text
cuts after index:   piece sums        max
  (1)               7 | 25            25
  (2)               9 | 23            23
  (3)              14 | 18            18   <- best
  (4)              24 | 8             24
with k=3 the same prefixes recur:
  (1,2)  7 | 2 | 23   (1,3)  7 | 7 | 18   (1,4) 7 | 17 | 8
   ^^^^ every placement starting with cut 1 re-sums [7]
```

The repeated work shows up in two places. Placements that share a prefix of cuts re-sum the same pieces again and again, and most placements are hopeless from the start: any placement whose first piece exceeds the best answer so far is evaluated in full anyway.

A dynamic program fixes the first kind of waste. Let `dp[j][i]` be the best largest-sum when the first `i` elements are split into `j` pieces. That gives O(k · n²): polynomial, but about 5·10^7 steps at n = 1000 and k = 50, which is slow in Python, and it is a lot of machinery. There is a much simpler route.

## The turning point

**Claim: the predicate `fits(cap)` = "the array can be cut into at most `k` pieces, each with sum <= cap" is monotone in `cap`, and a left-to-right greedy decides it in O(n).**

*Monotone.* If every piece sum is at most `cap`, every piece sum is also at most `cap + 1`, so the same cuts still work. Raising the budget can never make a split invalid. Over the budget range, `fits` reads `F ... F T ... T`, and the answer is the **first T**: the smallest budget under which `k` pieces suffice.

*The greedy is right.* Fill the current piece while adding the next element keeps it at or below `cap`, and cut only when the next element would overflow. This uses the fewest pieces possible for that cap. Here is why. Compare the greedy's cuts with those of any valid split. The greedy's first piece ends at least as far right as the other split's first piece, because the greedy extends as far as the cap allows. If the greedy's j-th piece ends at or beyond the other split's j-th piece, the greedy's (j+1)-th piece starts no later than the other's, and since sums of non-negative numbers only grow as a stretch gets longer, it can extend at least as far. So the greedy is never behind, and it finishes in no more pieces.

*Why "at most k", not "exactly k".* If the greedy uses fewer than `k` pieces, we can split any piece with two or more elements further without raising any sum (the numbers are non-negative), until we have exactly `k`. Since `n >= k`, there are always enough elements to do this. So "at most `k` pieces fit under `cap`" is the same as "exactly `k` pieces fit under `cap`".

*The answer range.* The cap can never be below `max(nums)`, because the largest element sits in some piece by itself or with others. It never needs to exceed `sum(nums)`, which is one piece holding everything. So we search `[max(nums), sum(nums)]` with the first-T template from Koko: `hi = mid` on T, `lo = mid + 1` on F.

```text
cap   : 10 .. 13 | 14 .. 17 | 18 ........ 31 | 32
pieces:     4    |     3    |        2       |  1
fits  :  F .. F  |  F .. F  |  T ........ T  |  T
(k=2)                          ^
                       first T = answer 18
```

The lower bound matters more than it looks. If you start at `lo = 0`, the greedy meets an element bigger than `cap`, cuts before it, and then adds it to an empty piece anyway, making a piece that breaks the cap while the count says "fits".

## Watch it work

`nums = [7, 2, 5, 10, 8]`, `k = 2`. The range is `[10, 32]`.

```text
Frame 1   lo=10  hi=32
  answer line: 10 ............................ 32
               L                                H
```
The range is set up: no cap below 10 can hold the element 10, and 32 is the whole array.

```text
Frame 2   lo=10  hi=32  mid=21
  7+2+5=14, then +10 would be 24 > 21 -> cut before 10
  [7 2 5] [10 8]      sums 14, 18     pieces=2  T
```
Two pieces fit under 21, so the answer is 21 or less: `hi = 21`.

```text
Frame 3   lo=10  hi=21  mid=15
  [7 2 5] [10] [8]    sums 14, 10, 8  pieces=3  F
           ^ 10+8=18 > 15 forces a third piece
```
Cap 15 needs three pieces, so every cap at or below 15 fails: `lo = 16`.

```text
Frame 4   lo=16  hi=21  mid=18
  [7 2 5] [10 8]      sums 14, 18     pieces=2  T
```
18 fits: `hi = 18`.

```text
Frame 5   lo=16  hi=18  mid=17
  [7 2 5] [10] [8]    sums 14, 10, 8  pieces=3  F
           ^ 10+8=18 > 17 by one
```
17 is one short: `lo = 18`. Now `lo == hi == 18`, so the answer is 18.

Across the frames, every cap below `lo` was known to fail and the cap at `hi` was known to fit. The greedy in each frame only ever held a running sum and a piece count. Four O(n) passes replaced the search over cut placements.

## Why it is correct

**Invariant: `fits(hi)` is true and `fits(lo - 1)` is false (or `lo = max(nums)`, below which nothing can fit).** At the start, `fits(sum(nums))` is true because one piece does it. On T we set `hi = mid`, which preserves `fits(hi)`. On F, monotonicity says every cap at or below `mid` fails, so `lo = mid + 1` preserves the other half. The gap `hi - lo` shrinks each round because `mid < hi`. When the two meet, the cap at `lo` fits and the one just below it does not, so `lo` is the smallest feasible cap. By the greedy-optimality argument, "feasible" here means that some split into `k` pieces achieves it, and by the definition of the problem that smallest feasible cap is exactly the minimised largest sum.

One more check: the answer is always a value some real split achieves, not just a bound. At the first T, the greedy split at that cap has some piece sum equal to the cap. Otherwise every piece would be at most `cap - 1`, and `cap - 1` would also fit, which contradicts "first".

## Cost

- **Brute force: O(C(n-1, k-1) · n)** time. Exponential.
- **DP: O(k · n²)** time, O(k · n) space.
- **Binary search on the answer: O(n log S)** time, where S = `sum(nums)`. There are about log₂(S - max) probes, each one greedy pass. **O(1)** space.

With S up to 10^9 that is about 30 passes of 1000 elements.

## Variations you will meet

- **Capacity to Ship Packages Within D Days (LeetCode 1011).** This is the same problem with days in place of pieces and weights in place of numbers. Copy the solution line for line.
- **Painter's partition / book allocation.** Classic textbook names for this problem. Sometimes time per unit is multiplied in, which scales the range but not the idea.
- **Minimise the largest sum with negative numbers allowed.** The greedy argument breaks, because extending a piece can lower its sum, so the "never behind" proof fails. You fall back to DP.
- **Return the cuts.** Run the greedy once more at the final cap. If it uses fewer than `k` pieces, split the longest pieces until there are `k`.

## What to carry forward

"Minimise the maximum" becomes "can everything fit under a cap?", answered by packing greedily and cutting only when forced, then binary searching for the smallest cap that fits. The lower bound is the largest single item, never zero.

The next problem keeps the "can it fit?" check but swaps the greedy for a counting argument: each battery's contribution is clamped to the candidate answer, and one inequality decides feasibility.
