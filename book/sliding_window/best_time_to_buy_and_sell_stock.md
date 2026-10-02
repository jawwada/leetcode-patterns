# Best Time to Buy and Sell Stock
*LeetCode 121 · Easy · Pattern: Running minimum sweep · Reading time ~5 min*

## What the problem is really asking

You are given a list of daily prices. You may buy once and sell once, and the sale must happen on a later day than the purchase. Return the largest profit you can make, or 0 if every possible trade loses money.

Strip the story and it is: find two positions `i < j` that maximise `prices[j] - prices[i]`. The answer is a single number, not the pair of days. What makes it slightly tricky is the ordering constraint. The biggest price minus the smallest price is not the answer when the smallest comes after the biggest.

```text
day:     0   1   2   3   4   5
price:   7   1   5   3   6   4

 7 *
 6 |                 *
 5 |         *
 4 |                     *
 3 |             *
 1 |     *
   +---------------------------
       buy at 1 (day 1), sell at 6 (day 4): profit 5
```

## Do it by hand first

Walk the days with a finger. On each day, ask: "if I sold today, what is the cheapest day before today I could have bought on?" You do not need to remember every earlier price for that, only the lowest one so far.

```text
day   price   lowest before today   sell-today profit
 0      7            -                    -
 1      1            7                   -6
 2      5            1                    4
 3      3            1                    2
 4      6            1                    5   <- best
 5      4            1                    3
```

Your hand kept track of exactly one thing: the lowest price seen so far. That single number is the seed of the algorithm.

## The first honest attempt

Try every buy day `i` and every later sell day `j`, compute `prices[j] - prices[i]`, keep the maximum. That is n(n-1)/2 pairs, so O(n^2) time and O(1) space. With n = 10^5 that is billions of pairs.

Where is the waste? Look at it from the sell day's side. For sell day 4 the brute force scans days 0 through 3 to find the cheapest buy. For sell day 5 it scans days 0 through 4, re-reading days 0 through 3 that it just read.

```text
sell day 4 scans:  [7  1  5  3]  -> min 1
sell day 5 scans:  [7  1  5  3  6] -> min 1
                    ^^^^^^^^^^
                    same four cells read again
```

The minimum of a prefix changes by at most one element when the prefix grows by one element. Rescanning it is pure repetition.

## The turning point

**Claim: the best purchase for a sale on day `j` is always the minimum of `prices[0..j-1]`, and that minimum can be carried forward in O(1) per day.**

Justification: for a fixed sell price, profit is `sell - buy`, which is largest when `buy` is smallest. So the inner loop of the brute force was only ever computing a prefix minimum. And `min(prefix + one more element) = min(old min, new element)`, so you never need to look back.

Seen as a window, the left edge `L` sits on the cheapest day so far and the right edge `R` is today. `R` moves one step each day. `L` only moves when today is a new low, and then it jumps straight to today. Both move only rightwards, so the whole thing is one pass. The state is two scalars: `min_price` and `best`.

The order of the two updates matters. On each day, first compute the profit of selling today against the old minimum, then lower the minimum if today is cheaper. Reversing them means buying and selling on the same day: harmless here, a real bug in variants.

## Watch it work

Example: `prices = [7, 1, 5, 3, 6, 4]`. `min` is the cheapest price before or on today after the update; `best` is the best profit so far.

Frame 1

```text
 7  1  5  3  6  4
 R                    min=7  best=0
 L
```

Day 0: nothing to sell against yet; `min` becomes 7.

Frame 2

```text
 7  1  5  3  6  4
    R                 1-7=-6  best=0  min=1
    L
```

Day 1: selling loses money; 1 is a new low, so `L` jumps to day 1.

Frame 3

```text
 7  1  5  3  6  4
    L  R              5-1=4   best=4  min=1
```

Day 2: profit 4 against the valley at 1 becomes the best.

Frame 4

```text
 7  1  5  3  6  4
    L     R           3-1=2   best=4  min=1
```

Day 3: profit 2 is worse; 3 is not below 1, so `L` stays.

Frame 5

```text
 7  1  5  3  6  4
    L        R        6-1=5   best=5  min=1
```

Day 4: profit 5 is the new best.

Frame 6

```text
 7  1  5  3  6  4
    L           R     4-1=3   best=5  min=1
```

Day 5: profit 3, no change. The answer is 5.

Throughout, `L` pointed at the lowest price in days `0..R`, and `best` was the best trade selling by day `R`.

## Why it is correct

Invariant at the end of iteration `R`: `min_price = min(prices[0..R])` and `best = max over all i < j <= R of prices[j] - prices[i]` (or 0). It holds trivially before the loop. In iteration `R`, every new pair has sell day exactly `R`, and the best of those uses the cheapest buy among days `0..R-1`, which is the old `min_price`. So `best = max(best, prices[R] - min_price)` accounts for every new pair. Then `min_price` absorbs `prices[R]` so the invariant holds for the next day. After the last day the invariant covers every pair.

## Cost

- Time O(n): one pass, constant work per day.
- Space O(1): two scalars, regardless of n.

## Variations you will meet

- **Stock II (unlimited trades, LeetCode 122).** No window at all: add every positive day-to-day rise. The thinking changes from "one valley, one peak" to "collect every upslope".
- **Stock with cooldown or fee (309, 714).** Several states per day (holding, not holding, cooling down); this becomes a small DP where `min_price` generalises to "best cash if I am holding".
- **At most k trades (123, 188).** DP over trades; the running-minimum idea reappears inside each layer.

## What to carry forward

Memory hook: when the inner loop only computes a prefix minimum (or maximum, or sum), replace it with a running value carried across the sweep.

Next, Minimum Size Subarray Sum gives the left edge real work to do: instead of jumping to a new low, `L` creeps forward step by step to shrink a window whose sum must stay at least a target.
