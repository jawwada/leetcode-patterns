# Number of Digit One

*LeetCode 233 · Hard · Pattern: Digit counting by position (high / current / low split) · Reading time ~8 min*

## What the problem is really asking

Write down every integer from `0` to `n`. Count how many times the character `1` appears in total. `n` goes up to about `2 * 10^9`.

The answer is a single count. A number like `11` contributes two, `101` contributes two, `7` contributes zero. What makes it hard is that `n` is far too large to visit each number, so the count must come from the *structure* of decimal notation itself.

```text
 n = 13
   0 1 2 3 4 5 6 7 8 9 10 11 12 13
     ^                 ^  ^^  ^  ^
     1                 1  2   1  1     total = 6
```

## Do it by hand first

Take `n = 213`. Counting number by number is miserable. So turn the paper sideways: write the numbers in a column, right-aligned, and look *down one digit position at a time*.

```text
  numbers 000..213 as three-digit rows
         H T U        H = hundreds, T = tens, U = units
   000   0 0 0
   001   0 0 1  <- U shows 1
   ...
   010   0 1 0  <- T shows 1 for 010..019
   ...
   100   1 0 0  <- H shows 1 for 100..199
   ...
   213   2 1 3
```

Look at the units column alone. Reading down, it cycles `0,1,2,...,9,0,1,...` with period 10, and in each period it shows `1` exactly once. The tens column cycles with period 100: ten `0`s, ten `1`s, ..., ten `9`s; in each period it shows `1` ten times in a row. The hundreds column: period 1000, a run of one hundred `1`s.

So for each column you ask: how many complete periods fit in `0..n`, and how far into the last, partial period does `n` reach? What your hand kept track of is the *column*, not the number. That is the seed: count per position.

## The first honest attempt

For each `i` in `0..n`, convert to a string and count `'1'`. That is `O(n log n)` character work and `O(1)` space. At `n = 2 * 10^9`, roughly twenty billion character checks: far too slow.

Where is the repeated work? The units digit's rhythm (one `1` per ten numbers) is a fact about the number system. The brute force rediscovers it two hundred million times. Same for the tens rhythm, the hundreds rhythm, and so on.

```text
 units column, rows 0..39
   0123456789 0123456789 0123456789 0123456789
    ^          ^          ^          ^
 four periods, four 1s: the brute force checks all 40 rows
 to learn "one per period"
```

## The turning point

**Claim: for a position with weight `p` (1, 10, 100, ...), split `n` as `n = high * 10p + cur * p + low`. Then that position shows `1` exactly `high * p` times in the complete periods, plus `p` more if `cur > 1`, plus `low + 1` more if `cur == 1`, plus nothing if `cur == 0`.**

The three pieces have concrete meanings.

```text
 n = 213, position p = 10 (tens)
     2  |  1  |  3
   high   cur   low
   high = 213 // 100     = 2   complete periods above
   cur  = (213 // 10) % 10 = 1 the digit at this position
   low  = 213 % 10       = 3   what sits below it
```

Justify each term.

**Complete periods.** The digit at weight `p` cycles through `0..9`, each value held for `p` consecutive numbers, for a period of `10p`. Numbers `0 .. high * 10p - 1` consist of exactly `high` complete periods. In each, the position shows `1` for exactly `p` numbers. That is `high * p`.

**The partial period.** The remaining numbers are `high * 10p .. n`. In this stretch the higher digits are fixed at `high`, and our position climbs from `0` up to `cur`.

- If `cur == 0`, our position never reached `1` in this stretch: add nothing.
- If `cur > 1`, it passed through its entire run of `1`s, which lasted `p` numbers: add `p`.
- If `cur == 1`, it is in the middle of the run. The run started at `high * 10p + 1 * p` (low part `00..0`) and has reached `n` (low part `low`). That is `low + 1` numbers: add `low + 1`.

```text
 the partial period at position p, by value of cur
  digit at p:  0000  1111  2222  ...  9999   (each run = p)
  cur = 0:     ..^                           -> +0
  cur = 1:           ..^  (low+1 into the run) -> +low+1
  cur = 2:                 ..^  (run passed) -> +p
```

The whole count is a sum of those terms over positions `p = 1, 10, 100, ...` while `p <= n`. Positions above `n`'s top digit show only leading zeros, never `1`, so they contribute nothing and the loop can stop.

Why is this the right decomposition? Because the count of `1`s over all numbers equals the sum, over positions, of the count of numbers showing `1` at that position. Swapping the order of summation — numbers-then-positions to positions-then-numbers — is the entire trick. Columns have rhythm; rows do not.

## Watch it work

Example: `n = 213`. Expected total `146` (checked by brute force).

Frame 1 — setup. `total = 0`, `p = 1`.

```text
 n = 213     total = 0     p = 1
 positions to visit: units (p=1), tens (10), hundreds (100)
```

Frame 2 — units, `p = 1`: `high = 21`, `cur = 3`, `low = 0`. `21` complete periods give `21`; `cur = 3 > 1` adds a full run of `1`.

```text
  2 1 | 3 |      high=21  cur=3  low=0
        ^p=1     periods 0..209: 21 ones (1, 11, ..., 201)
                 partial 210..213 passed 211: +1
 total = 0 + 21 + 1 = 22
```

Frame 3 — tens, `p = 10`: `high = 2`, `cur = 1`, `low = 3`. Two periods of 100 give `2 * 10`; `cur = 1` adds `low + 1 = 4` (210, 211, 212, 213).

```text
  2 | 1 | 3      high=2   cur=1  low=3
      ^p=10      periods 0..199: 10..19, 110..119 -> 20
                 partial 200..213: 210..213 -> 3 + 1 = 4
 total = 22 + 20 + 4 = 46
```

Frame 4 — hundreds, `p = 100`: `high = 0`, `cur = 2`, `low = 13`. No complete period; `cur = 2 > 1` adds the full run `100..199`.

```text
 | 2 | 1 3       high=0   cur=2  low=13
   ^p=100        partial 0..213 passed 100..199: +100
 total = 46 + 0 + 100 = 146
```

Frame 5 — `p = 1000 > 213`: stop. Answer `146`.

```text
 p = 1000 > n: no digit here, loop ends
 answer 146   (brute force over 0..213 agrees)
```

What stayed invariant: after processing position `p`, `total` equals the number of `1`s appearing in positions below `10p` across all of `0..n`. Each frame added one column's contribution, computed in `O(1)` from three integers, and no column was counted twice.

## Why it is correct

Let `C(p)` be the number of integers `x` in `[0, n]` whose digit at weight `p` is `1`. The answer is the sum of `C(p)` over all positions, because each `1` character belongs to exactly one number and exactly one position.

Fix `p`. The digit of `x` at weight `p` is `(x // p) % 10`. Write `x = h * 10p + d * p + l` with `0 <= d <= 9`, `0 <= l < p`. Then the digit is `d`, and `x <= n` iff `(h, d, l)` is lexicographically at most `(high, cur, low)`. Count triples with `d = 1`:

- `h < high`: any `l`, so `high * p` triples.
- `h = high`: need `1 <= cur` and, if `cur == 1`, `l <= low`. That gives `p` if `cur > 1`, `low + 1` if `cur == 1`, `0` if `cur == 0`.

That is exactly the formula. For `p > n`, `high = cur = 0`, so `C(p) = 0` and stopping at `p > n` loses nothing. Note the loop condition is `p <= n`, not `p < n`: at `n = 1000`, the position `p = 1000` holds the leading `1` and must be counted.

## Cost

- **Time:** `O(log10 n)` — one constant-time step per decimal position, about ten for `n <= 2 * 10^9`.
- **Space:** `O(1)` — a few integers.

The brute force was `O(n log n)`. The gain comes entirely from counting columns instead of rows.

## Variations you will meet

- **Count digit `d` for `d` in `2..9` (Digit Count in Range, LeetCode 1067).** Same split; the partial period adds `p` if `cur > d`, `low + 1` if `cur == d`. For `d = 0` there is a twist: leading zeros are not written, so the `h = 0` period does not count. A position contributes only when `high > 0`, and then it is `(high - 1) * p` plus `p` if `cur > 0`, or `low + 1` if `cur == 0` (counting `1..n`). A range `[lo, hi]` is `count(hi) - count(lo - 1)`.
- **Factorial Trailing Zeroes (LeetCode 172).** Also "count by position instead of by item": count multiples of 5, 25, 125, ... instead of examining each factor.
- **Count numbers with a property spanning several digits** (no repeated digits, digit sum equals `s`, at most `k` nonzero digits). Per-position counting breaks because positions interact; use digit DP with state `(position, tight, extra state)`. The `high / cur / low` split is the closed-form special case of digit DP with no extra state.
- **Sum of all digits from `0` to `n`.** For each position, complete periods contribute `high * p * 45`, the partial one contributes `p * (0+1+...+(cur-1)) + cur * (low + 1)`.

## What to carry forward

When counting a digit over a range of numbers, sum over positions instead: each position has a periodic rhythm, and `n` cuts its last period at a place described by `cur` and `low`.

The next problem, Poor Pigs, also counts with positional numerals, but uses them the other way round: instead of reading a number's digits, it asks how many digits (pigs) are needed to name one of `N` buckets.
