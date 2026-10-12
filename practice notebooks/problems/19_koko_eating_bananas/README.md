# Koko Eating Bananas (LeetCode 875)

**Area:** binary search · **Difficulty:** Medium · **Key operations:** hours(speed) by ceiling division, binary search on the answer, hi = mid when feasible, lo = mid + 1 when not

## Problem

There are `n` piles of bananas; pile `i` has `piles[i]` bananas. The guards return in `h` hours. Each hour Koko picks one pile and eats up to `k` bananas from it; if the pile has fewer than `k` she finishes it and does nothing else that hour. Return the minimum integer speed `k` at which she can eat all the bananas within `h` hours. (`h >= n`, so a solution always exists.)

## Example

```
piles = [3, 6, 7, 11], h = 8   ->   4

speed 4: ceil(3/4) + ceil(6/4) + ceil(7/4) + ceil(11/4) = 1 + 2 + 2 + 3 = 8 hours  (fits)
speed 3: 1 + 2 + 3 + 4 = 10 hours                                                 (too slow)
```

## Brute force

Try `k = 1, 2, 3, ...`. For each speed compute the total hours `sum(ceil(p / k))` and return the first speed whose total is at most `h`.

O(n * max(piles)) time, O(1) space. The wasted work: once a speed works, every faster speed works too, and once a speed fails every slower speed fails. The scan checks each speed in turn although the pattern of answers is a solid block of "no" followed by a solid block of "yes", and a block boundary can be found by halving.

## From brute force to optimal

Define `feasible(k) = hours(k) <= h`. Eating faster never takes more hours, so `feasible` is monotone: `F F F ... F T T ... T` over `k = 1 .. max(piles)`. A monotone boolean sequence is "sorted", and the first `T` can be found by binary search on the *answer* rather than on the data.

Bounds: `k = 1` is the slowest sensible speed; `k = max(piles)` always works (one hour per pile), so nothing faster needs testing. Each probe costs one O(n) pass, and there are O(log max(piles)) probes.

## Intuition

Do not search the piles; search the speeds. Draw the speeds `1 .. max(piles)` on a line and above each write F or T for "finishes in time". The picture is a wall of F's and then a wall of T's. `lo` and `hi` squeeze onto the boundary: when `mid` is T, the answer is `mid` or something slower, so `hi = mid` keeps it in play; when `mid` is F, the answer is strictly faster, so `lo = mid + 1`. The loop stops when `lo == hi`, standing on the first T.

## Walkthrough

`piles = [3, 6, 7, 11]`, `h = 8`. Carets mark `lo`, `mid`, `hi` on the speed line. Each probe shows the hours per pile.

```
speed   1  2  3  4  5  6  7  8  9 10 11
        ^              ^              ^     lo=1 mid=6 hi=11
speed 6: [1, 1, 2, 2] -> 6 hours <= 8   feasible   hi = 6

speed   1  2  3  4  5  6  7  8  9 10 11
        ^     ^        ^                    lo=1 mid=3 hi=6
speed 3: [1, 2, 3, 4] -> 10 hours > 8   too slow   lo = 4

speed   1  2  3  4  5  6  7  8  9 10 11
                 ^  ^  ^                    lo=4 mid=5 hi=6
speed 5: [1, 2, 2, 3] -> 8 hours <= 8   feasible   hi = 5

speed   1  2  3  4  5  6  7  8  9 10 11
                 ^  ^                       lo=4 mid=4 hi=5
speed 4: [1, 2, 2, 3] -> 8 hours <= 8   feasible   hi = 4

lo == hi == 4 -> answer 4
```

The F/T line for this input is `F F F T T T T T T T T`; the search landed on the first T.

## Steps

1. `lo = 1`, `hi = max(piles)`.
2. `hours(k) = sum((p + k - 1) // k for p in piles)` (ceiling division without floats).
3. While `lo < hi`: `mid = (lo + hi) // 2`.
4. If `hours(mid) <= h`: `hi = mid` (feasible, try slower). Else `lo = mid + 1` (too slow).
5. Return `lo`.

## Complexity

O(n log M) time with `M = max(piles)`: about log M probes, each an O(n) sum. O(1) extra space.

## Pitfalls

- **`<` instead of `<=`.** Using exactly `h` hours is allowed. With `<` the speed that needs exactly `h` hours is rejected and the answer is one too fast (5 instead of 4 on the example).
- **`hi = mid - 1` on a feasible mid.** A feasible `mid` may be the answer; throwing it away can make `lo` end on an infeasible speed. Use `hi = mid` with `while lo < hi`.
- **`lo = mid` on an infeasible mid.** When `hi == lo + 1`, `mid == lo` and the loop never moves: an infinite loop. Exclude the failed speed with `lo = mid + 1`.
- **Floor instead of ceiling.** `p // k` undercounts hours; use `(p + k - 1) // k` or `-(-p // k)`.
- **`lo = 0`.** Speed 0 divides by zero. The slowest sensible speed is 1.
