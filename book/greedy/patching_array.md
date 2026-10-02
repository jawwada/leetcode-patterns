# Patching Array

*LeetCode 330 · Hard · Pattern: Greedy reach (furthest reachable index) · Reading time ~9 min*

## What the problem is really asking

You get a sorted array of positive integers `nums` and a target `n`. A value is "buildable" if it is the sum of some subset of the array. Add as few new integers ("patches") as possible so that every value from 1 to `n` is buildable.

The answer is a count. What makes it hard is that subset sums explode: `k` numbers have up to `2^k` subsets, and `n` can be as large as `2^31 - 1`. You cannot list the sums, and you cannot try candidate patches one by one. You need a summary of "what is buildable" that is tiny and updates cheaply.

```text
nums = [1, 5, 10], n = 20

buildable from nums alone:
  1  5  6  10  11  15  16
values 1..20:
  1 2 3 4 5 6 7 8 9 10 ... 20
  # . . . # # . . . #  ...
  holes start at 2 -> patch needed

with patches 2 and 4:  every 1..20 buildable
answer 2
```

## Do it by hand first

Walk up from 1 and ask, "can I make this value yet?" Keep only the largest value up to which everything is makeable. Call it `reach`.

```text
have {}          makeable 1..0    reach 0
take 1:          makeable 1..1    reach 1
next is 5, but 2 is missing:
  nothing later can make 2 (every later number >= 5)
  patch 2:  old sums {0,1} + 2 -> {2,3}
                 makeable 1..3    reach 3
next is 5, but 4 is missing:
  patch 4:       makeable 1..7    reach 7
take 5:  old 0..7 shifted by 5 -> 5..12
                 makeable 1..12   reach 12
take 10: 10..22 joins 1..12 ->    reach 22 >= 20
```

Your hand did not track the set of sums. It tracked one integer, the end of a solid prefix `[1, reach]`. That is the seed: coverage is always a contiguous bar starting at 1, and you only need to know where the bar ends.

## The first honest attempt

Build the full set of subset sums, find the smallest missing value in `[1, n]`, patch it, rebuild, repeat.

```text
round 1: sums of [1,5,10]        -> missing 2, patch
round 2: sums of [1,5,10,2]      -> missing 4, patch
round 3: sums of [1,5,10,2,4]    -> none missing
         ^ each round recomputes every subset sum,
           including all those already known
```

Each round costs time proportional to the number of distinct sums, which is up to `n` and up to `2^k`. For `n` near `2^31` this is hopeless. The repeated work is recomputing a set that changes in a perfectly predictable way: once you know `[1, reach]` is solid, adding `x` makes `[x, reach + x]` solid as well, and nothing else about the set matters.

The tempting wrong greedy goes like this: "subset sums are like binary digits, so make sure every power of two up to `n` is present." Patch whatever of 1, 2, 4, 8, 16 is missing.

```text
nums = [1, 5, 10], n = 20
powers needed: 1 2 4 8 16
present:       1 . . . .
power-of-two greedy patches: 2, 4, 8, 16   -> 4
true answer:                 2, 4          -> 2
```

It ignores what the existing numbers already contribute. Once the bar reaches 7, the 5 and the 10 extend it to 22 for free.

## The turning point

**Claim: if every value in `[1, reach]` is buildable and the next number `x` satisfies `x <= reach + 1`, then adding `x` makes `[1, reach + x]` buildable; and if `x > reach + 1`, the best patch is exactly `reach + 1`, which grows the bar to `[1, 2 * reach + 1]`.**

First half. Every value `v` in `[1, reach]` is already buildable without `x`. Every value `v` in `[x, reach + x]` is `x` plus a value in `[0, reach]`, all buildable (0 is the empty subset). The two ranges overlap or touch exactly when `x <= reach + 1`. So the bar extends by `x` with no hole.

```text
old bar:   [1 ............ reach]
shifted:          [x ............ reach+x]
need x <= reach+1 so no gap between them
```

Second half. If the next array value is larger than `reach + 1`, then `reach + 1` can never be built from the array: all smaller numbers are already used to make at most `reach`, and every remaining number is too big on its own. So some patch `p` is forced, and to be useful at all it must satisfy `p <= reach + 1`, or it leaves the same hole. Among those, `p = reach + 1` makes the longest bar: `[1, reach + p]` is longest when `p` is largest.

This also explains where the power-of-two intuition came from, and why it is only half right. With an empty array, the greedy patches 1, then 2 (bar 3), then 4 (bar 7), then 8 (bar 15): exactly the powers of two, because each patch is `reach + 1` and `reach` is always one less than a power of two. Array elements break that rhythm. They lengthen the bar by arbitrary amounts, and the next patch, if one is needed, is whatever `reach + 1` happens to be at that moment, not the next power of two. On `nums = [1, 2, 31, 33]` with `n = 2^31 - 1`, the answer is 28 patches, and many of them are not powers of two at all.

So the algorithm keeps one integer and a pointer into `nums`. Each step either consumes an array element (bar grows by that element) or patches (bar more than doubles). The structure is "greedy reach", the same furthest-reachable idea as Jump Game, but here reach grows by addition instead of by jumping.

## Watch it work

Example: `nums = [1, 5, 10]`, `n = 20`. The solution returns 2.

Frame 1. Start: nothing is buildable.

```text
nums: [1, 5, 10]      i -> 1
bar:  (empty)          reach 0, patches 0
next = 1 <= reach+1 = 1 -> take it
```

Frame 2. Took 1: the bar is `[1, 1]`.

```text
nums: [1, 5, 10]         i -> 5
bar:  [#]                reach 1
      1
next = 5 > reach+1 = 2 -> hole at 2, patch 2
```

Frame 3. Patched 2: the bar is `[1, 3]`.

```text
bar:  [###]              reach 3, patches 1
      1 2 3
next = 5 > reach+1 = 4 -> hole at 4, patch 4
```

Frame 4. Patched 4: the bar is `[1, 7]`.

```text
bar:  [#######]          reach 7, patches 2
      1     7
next = 5 <= 8 -> take 5
```

Frame 5. Took 5: the bar is `[1, 12]`.

```text
bar:  [############]     reach 12, patches 2
      1          12      i -> 10
next = 10 <= 13 -> take 10
```

Frame 6. Took 10: the bar is `[1, 22]`, past `n = 20`. Stop.

```text
bar:  [######################]   reach 22 >= 20
      1                    22
answer: patches = 2  (values 2 and 4)
```

The invariant across every frame: every value in `[1, reach]` is buildable from the elements consumed so far plus the patches, and `reach + 1` is not. Every step lengthened the bar; a patch step at least doubled it.

## Why it is correct

The invariant above gives validity: when the loop ends, `reach >= n`, so every value in `[1, n]` is buildable.

For minimality, use an exchange argument backed by one monotonicity fact.

**Monotonicity.** If two runs are at the same array position, one with bar `reach` and the other with bar `reach' >= reach`, the second will never need more future patches than the first. A longer bar accepts every array element the shorter one accepts (the test `x <= reach + 1` only gets easier), and each acceptance or patch keeps it at least as long.

**Exchange.** Take any optimal set of patches and look at the first moment the greedy patches, with bar `reach` and next array value larger than `reach + 1`. The optimal solution must also contain some patch `p <= reach + 1` at or before this point, because otherwise `reach + 1` is unbuildable for it too. Replace that `p` with `reach + 1`. The new bar `2 * reach + 1` is at least `reach + p`, so by monotonicity the modified solution still covers `[1, n]` with the same number of patches. Repeat at the next greedy patch. After all exchanges the optimal solution's patches are exactly the greedy's, so the greedy count equals the optimum.

Intuitively: a patch is only ever forced at the hole `reach + 1`, and the hole itself is the largest patch that fills it, so it buys the most future coverage for the same price.

## Cost

Time O(len(nums) + log n). Each loop step either consumes an array element or patches; a patch takes `reach` to `2 * reach + 1`, so there are at most about `log2(n)` patches.

Space O(1): `reach`, `patches`, and the index. Use 64-bit thinking in other languages: `reach` can exceed `n` by up to a factor of 2.

## Variations you will meet

- **Smallest value that cannot be built (no patches).** Run the same loop and stop at the first `x > reach + 1`; the answer is `reach + 1`. It needs the array sorted, so sort first if it is not.
- **Maximum Number of Consecutive Values You Can Make (LeetCode 1798).** Exactly that variant: sort coins, grow `reach`, stop at the first gap, return `reach + 1`.
- **Minimum Number of Coins to be Added (LeetCode 2952).** Same problem with unsorted coins; sort first and the greedy is unchanged.
- **Each value may be used more than once.** Coverage is no longer a single prefix in general; the reasoning becomes coin-change DP or number theory (Frobenius numbers) instead of a reach bar.

## What to carry forward

Summarise an exploding set by the length of its solid prefix, extend the prefix with whatever fits, and when a hole is forced, fill it with the hole itself because that buys the most. The next problem also places points as far right as possible to serve future demands, but now each interval demands two points instead of one.
