# Koko Eating Bananas

*LeetCode 875 · Medium · Pattern: Binary search on the answer · Reading time ~8 min*

## The problem

piles[i] bananas sit in pile i. Each hour Koko chooses a pile and eats up to k bananas from it; if the pile has fewer
than k she finishes it and waits. Return the minimum integer speed k that lets her finish every pile within h hours.

```text
Example: piles = [3,6,7,11], h = 8 returns 4 (hours at k = 4: 1
  + 2 + 2 + 3 = 8).
```

## What the problem is really asking

Koko has piles of bananas and a deadline of `h` hours. She picks a fixed eating speed `k`. Each hour she sits at one pile and eats up to `k` bananas from it. If the pile has fewer than `k` left she finishes it and wastes the rest of the hour; she never moves to a second pile in the same hour. We want the slowest speed that still clears every pile by the deadline.

So the answer is one integer, a speed. It is not a position in the input, and nothing in the input is sorted. That is what makes it feel unlike the eight problems before it. Up to now we searched an array for an index. Here there is no array to search, only a number we have to choose.

Because Koko never shares an hour between piles, a pile of `p` bananas costs `ceil(p / k)` hours, and the total time at speed `k` is the sum of those ceilings.

```text
piles = [3, 6, 7, 11], h = 8

speed k = 4, one box = one hour at one pile

pile  3: [3]            -> 1 hour
pile  6: [4][2]         -> 2 hours
pile  7: [4][3]         -> 2 hours
pile 11: [4][4][3]      -> 3 hours
                           -------
                           8 hours <= h = 8   -> OK
```

The answer here is 4. At speed 3 the same piles take 1 + 2 + 3 + 4 = 10 hours, which is too many.

## Do it by hand first

With pen and paper, most people try a speed, add up the hours, and adjust. Try `k = 1` and Koko needs 27 hours, far too many. Try 11, the biggest pile, and every pile takes one hour, so 4 hours total. That is plenty. The answer is somewhere between those two, so try something in the middle.

```text
k :   1   2   3   4   5   6   7   8   9  10  11
hrs: 27  15  10   8   8   6   5   5   5   5   4
ok?   F   F   F   T   T   T   T   T   T   T   T
                  ^
          first T = answer 4
```

What your hand kept track of was not a pile or a sum, it was a single question: "at this speed, does she make it?" You also noticed, without saying so, that the answers line up as a run of F followed by a run of T. You never saw a T and then an F later on. That one-way shape is the seed of the whole solution.

## The first honest attempt

A strong candidate says: "Start at `k = 1`. Compute total hours. If it fits in `h`, return `k`. Otherwise try `k + 1`." It is correct, since the first speed that fits is the answer by definition.

The cost is the problem. The largest pile can be 10^9 and there can be 10^4 piles. In the worst case the scan walks through up to `max(piles)` speeds, each costing a pass over all `n` piles: O(n · max(piles)), around 10^13 operations.

```text
check k=1  : scan all piles -> F
check k=2  : scan all piles -> F
check k=3  : scan all piles -> F
   ...
every check re-reads every pile, and each F
tells us only "not this one" -- one speed ruled
out per full pass
```

The waste is that each failed check rules out a single speed. A failure at `k = 3` actually tells us much more than that: if Koko cannot finish at speed 3, she cannot finish at 2 or 1 either. The linear scan throws that information away.

## The turning point

**Claim: the predicate `fits(k) = (hours(k) <= h)` is monotone. Once it is true for some speed, it stays true for every faster speed.**

Justification: each pile's cost `ceil(p / k)` can only stay the same or go down when `k` grows. Eating faster never makes a pile take longer. A sum of terms that never grow never grows either, so `hours(k)` is non-increasing in `k`. If `hours(k) <= h`, then `hours(k + 1) <= hours(k) <= h`.

So over the range of possible speeds, `fits` looks like `F F ... F T T ... T`, and a boolean sequence with that shape is sorted. Everything this chapter has done so far applies to it. We binary search for the **first T**, and the "array" we search is the range of candidate answers rather than the input. Each probe is a feasibility check instead of a comparison with a stored value.

This is the move the rest of the chapter is built on, so name its three parts:

1. **The answer range.** The slowest sensible speed is 1, since speed 0 never finishes. The fastest speed we need is `max(piles)`, because at that speed every pile takes exactly one hour, and we know `h >= len(piles)` from the constraints. Going faster than that changes nothing.
2. **The predicate.** `fits(k)`: does the sum of `ceil(p / k)` come to at most `h`? It costs one O(n) pass.
3. **The direction.** We want the smallest `k` where `fits` is true. If `fits(mid)` holds, the answer is `mid` or something slower, so set `hi = mid`. If it fails, the answer is strictly faster, so set `lo = mid + 1`.

```text
answer range on a line, predicate painted above:

  F F F T T T T T T T T
  1 2 3 4 5 6 7 8 9 . 11
  lo                  hi
        |<-- the F|T edge is the answer
```

This uses the `lo < hi`, `hi = mid` template from search insert position (problem 2): both look for the first index where a condition turns true.

## Watch it work

`piles = [3, 6, 7, 11]`, `h = 8`. The search range starts at `[1, 11]`.

```text
Frame 1   lo=1  hi=11  mid=6
  hours per pile at 6: [1,1,2,2] = 6 <= 8   fits -> T
  1 2 3 4 5 6 7 8 9 10 11
  L         M           H
```
Speed 6 is fast enough, so the answer is 6 or slower: `hi = 6`.

```text
Frame 2   lo=1  hi=6  mid=3
  hours per pile at 3: [1,2,3,4] = 10 > 8   fits -> F
  1 2 3 4 5 6
  L   M     H
```
Speed 3 is too slow, and so is every slower speed: `lo = 4`.

```text
Frame 3   lo=4  hi=6  mid=5
  hours per pile at 5: [1,2,2,3] = 8 <= 8   fits -> T
  4 5 6
  L M H
```
Speed 5 works, so the answer is at most 5: `hi = 5`.

```text
Frame 4   lo=4  hi=5  mid=4
  hours per pile at 4: [1,2,2,3] = 8 <= 8   fits -> T
  4 5
  L H
  M
```
Speed 4 also works: `hi = 4`. Now `lo == hi == 4`, the loop stops, and the answer is 4.

Throughout, every speed below `lo` was known to fail and every speed at or above `hi` was known to fit. The window `[lo, hi]` always held the first T, and it shrank by about half each probe. Four checks replaced up to eleven.

## Why it is correct

The invariant is: **`fits(lo - 1)` is false (or `lo = 1`), and `fits(hi)` is true.** At the start it holds because `fits(max(piles))` is true and nothing sits below 1. If `fits(mid)` is true, setting `hi = mid` keeps `fits(hi)` true. If it is false, then by monotonicity every speed up to `mid` fails, so setting `lo = mid + 1` keeps "everything below `lo` fails" true. Each step strictly shrinks `hi - lo`, because `mid < hi` whenever `lo < hi`. When `lo == hi`, that single speed fits and the speed just below it does not, so it is the smallest speed that fits.

Monotonicity is doing all the work here. Without it, an F at `mid` would say nothing about the speeds below `mid`, and discarding them would be a guess.

## Cost

- **Time: O(n log M)**, where M = `max(piles)`. There are about log₂ M probes, each summing `n` ceilings.
- **Space: O(1).** Only `lo`, `hi`, `mid`, and a running sum.

For M = 10^9 that is about 30 passes over the piles, compared with up to a billion for the linear scan.

## Variations you will meet

- **Capacity to Ship Packages Within D Days (LeetCode 1011).** The answer is a ship capacity and the check greedily packs packages into days. It is the same first-T search, but the lower bound becomes `max(weights)` because one package cannot be split. That is a preview of problem 11.
- **Minimum Number of Days to Make m Bouquets (LeetCode 1482).** The answer is a day, and the check counts runs of bloomed flowers. Once again it is monotone, since waiting longer never un-blooms a flower.
- **Real-valued speed.** If `k` could be fractional, the loop would run until `hi - lo < eps` instead of `lo < hi`. Problem 15 does exactly this.
- **Maximise instead of minimise.** If the predicate looked like `T ... T F ... F` and we wanted the last T, the template would flip. Problem 10 is the first time that happens.

## What to carry forward

When the answer is a number and you can cheaply check "is this number good enough?", and good enough stays good enough as the number moves one way, binary search the answer and put the check inside the loop.

The next problem asks for the largest value that still works instead of the smallest, so the predicate becomes `T ... T F ... F` and we hunt for the last T.
