---
rank: 58
slug: longest_increasing_subsequence
---

Given an array of integers, return the length of its longest strictly increasing subsequence: values kept in their original order, but not necessarily adjacent. In `[10, 9, 2, 5, 3, 7, 101, 18]` the answer is `4`, for example `2, 3, 7, 18`.

The quadratic method gives each index the length of the longest increasing subsequence ending there, one more than the best over earlier smaller values, `O(n²)`. The fast method keeps only the best way to reach each length. Let `tails[k]` be the smallest value that ends an increasing subsequence of length `k + 1` so far; a smaller tail is the better state, since whatever extends a larger tail extends a smaller one too. The tails increase strictly, because cutting the last value off a subsequence of length `k + 2` leaves one of length `k + 1` that ends lower. So a new value `x` binary searches them with the lower bound of #14. The tails below `x` are lengths it can extend, and the first tail at least `x`, at index `i`, is where it stops: `x` ends a subsequence of length `i + 1` and is no larger than the old tail, so it takes that slot. If no tail is at least `x`, then `x` extends the longest subsequence and `tails` grows.

This is patience sorting: deal the values like cards, each onto the leftmost pile whose top is at least the card, or onto a new pile at the right. The pile tops are `tails`, and the number of piles is the answer. The tops are not themselves a subsequence: on `[4, 5, 6, 1]` they end as `[1, 5, 6]`, out of order in the array, yet the length 3 is right, because each slot only records the best tail for its length. To rebuild a real subsequence, keep indices in `tails`, link each value to the index in the slot to its left when it arrived, and follow the links back from the last slot.

```text
   x    first tail ≥ x         tails after
  10    none: append           [10]
   9    10 at 0: replace       [9]
   2    9 at 0: replace        [2]
   5    none: append           [2, 5]
   3    5 at 1: replace        [2, 3]
   7    none: append           [2, 3, 7]
 101    none: append           [2, 3, 7, 101]
  18    101 at 3: replace      [2, 3, 7, 18]
answer = len(tails) = 4

piles      10    5    7  101     each card lands on the leftmost pile
            9    3        18     whose top is ≥ it; the four tops
            2                    2, 3, 7, 18 are the tails
```

```pseudo
FUNCTION LowerBound(values, target)     // first i with values[i] ≥ target
    lo ← 0
    hi ← len(values)                    // half-open [lo, hi)
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF values[mid] < target
            lo ← mid + 1
        ELSE
            hi ← mid
    RETURN lo

FUNCTION LengthOfLIS(nums)
    tails ← empty list              // tails[k]: smallest tail of length k + 1
    FOR EACH x IN nums
        i ← LowerBound(tails, x)        // how many tails are smaller than x
        IF i = len(tails)
            tails.append(x)             // x extends the longest subsequence
        ELSE
            tails[i] ← x                // a smaller tail for length i + 1
    RETURN len(tails)
```

Each value costs one binary search over at most `n` tails, so the method runs in `O(n log n)` time and `O(n)` space. The signals are "longest increasing", "longest chain" and "fits inside", including two-dimensional orders that a sort reduces to one. Russian Doll Envelopes sorts by width ascending and, for equal widths, by height descending, then runs this on the heights; the descending tie-break keeps two envelopes of the same width out of one chain, since their heights now appear in decreasing order. Find the Longest Valid Obstacle Course at Each Position wants non-decreasing courses, so it searches for the first tail greater than `x` and reports `i + 1` at every position. That swap is the classic mistake here: with the first tail greater than `x`, an equal value extends its twin, and `[7, 7, 7, 7]` reports 4 instead of 1.

*Practice:* LC 300 Longest Increasing Subsequence · LC 354 Russian Doll Envelopes · LC 1964 Find the Longest Valid Obstacle Course at Each Position
