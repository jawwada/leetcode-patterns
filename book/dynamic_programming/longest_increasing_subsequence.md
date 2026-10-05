# Longest Increasing Subsequence

*LeetCode 300 · Medium · Pattern: Patience sorting (tails array + binary search) · Reading time ~7 min*

## The problem

Given an integer array nums, return the length of the longest strictly increasing subsequence, where a subsequence
keeps the original order but may skip elements.

```text
Example: [10,9,2,5,3,7,101,18] -> 4 (for instance 2, 3, 7, 101);
  [7,7,7] -> 1.
```

## What the problem is really asking

Given an array, pick elements in their original order so that each picked element is strictly larger than the previous one. Return the most elements you can pick. Gaps are allowed; equal values do not count as increasing.

The answer is a length. What makes it hard: `2^n` subsequences, and early choices that look good (a long run starting at 10) can be beaten by starting later from a smaller value.

```text
 index:   0    1    2    3    4    5    6     7
 nums:   10    9    2    5    3    7   101   18
                    *         *    *    *          2,3,7,101
                    *    *         *         *     2,5,7,18
                                         length 4
```

## Do it by hand first

Go left to right and, under each number, write the length of the longest increasing run that *ends at* that number. For each new number, look back at every smaller number to its left and extend the best of them by one.

```text
 nums:      10    9    2    5    3    7   101   18
 ends here:  1    1    1    2    2    3    4     4
                                      ^
       7: smaller ones to its left are 2 (1), 5 (2), 3 (2)
          best is 2, so 7 ends a run of length 3
```

Your hand kept one number per element and, to fill it, scanned everything before it. The answer is the largest number written. That is the classic O(n^2) DP. Keep watching your hand though: most of that scanning is wasted, and that waste is this problem's real lesson.

## The first honest attempt

The brute force recurses on `(i, prev)`: at index `i`, skip `nums[i]`, or take it if it is larger than the last taken value. That enumerates all `2^n` subsequences, and the best continuation from `(i, prev)` is recomputed for every path that arrives there.

Memoise it, or rather tabulate the hand method:

- **State:** `dp[i]` = length of the longest increasing subsequence ending exactly at `nums[i]`.
- **Recurrence:** `dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])`, or 1 if no such `j`.
- **Order:** left to right; **answer:** `max(dp)`.

This is correct and costs O(n^2): each element rescans all earlier ones.

```text
 computing dp[6] for 101: scan j = 0..5
   10   9   2   5   3   7
   1    1   1   2   2   3     max = 3 -> dp[6] = 4
   ^---^---^---^---^---^  every one inspected again
 computing dp[7] for 18: scan the same six plus 101
```

The repeated work is the scan. For every new `x` we ask the same kind of question, "what is the best run ending on something smaller than `x`?", and answer it by brute force over the whole prefix.

## The turning point

**Claim: for each length `L`, you only need to remember the smallest value that can end an increasing subsequence of length `L`; any run with a larger tail is never more useful.**

Compare two runs of length 3, one ending at 7 and one ending at 9. Anything that can extend the 9-run (a value above 9) can also extend the 7-run, but not vice versa. So the 7-run dominates, and the 9-run can be forgotten. Keep `tails[L-1]` = smallest known tail of an increasing run of length `L`.

Two facts make this a structure, not just a table:

1. **`tails` is strictly increasing.** A run of length `L+1` contains a run of length `L` ending at a smaller value, so the smallest tail for `L` is below the smallest tail for `L+1`.
2. **A new `x` changes exactly one entry.** Find the first tail `>= x` (binary search, because the array is sorted). Every run whose tail is below `x` can be extended by `x`; the longest of them has length `i`, so `x` ends a run of length `i+1`, and `x <= tails[i]` makes it the new smallest tail for that length. If no tail is `>= x`, `x` extends the longest run: append.

That is exactly the card game patience. Deal the numbers as cards left to right; put each card on the leftmost pile whose top is `>= ` it, or start a new pile on the right. Pile tops are `tails`. The number of piles is the LIS length.

```text
 piles (top of each pile at the bottom of the column):

   pile 1   pile 2   pile 3   pile 4
    10
     9
     2        5
              3        7       101
                                18
   tops: 2    3        7        18    = tails
```

Note what is lost: `tails` is not itself an increasing subsequence of the input. In the end `tails = [2, 3, 7, 18]` happens to be one, but in general (for example `[3, 4, 1]` ends with `tails = [1, 4]`, and 1 comes after 4) it is not. Only its length is meaningful. To recover an actual subsequence, store for each card a pointer to the top of the pile to its left at the time it was placed, and follow pointers back from the last pile.

## Watch it work

`nums = [10, 9, 2, 5, 3, 7, 101, 18]`. Each frame shows `tails` after the step and where `bisect_left` landed.

**Frame 1.** `10`: empty, append. `9`: first tail `>= 9` is index 0, replace. `2`: index 0 again, replace.

```text
 tails: [ 2 ]
          ^ 10 -> 9 -> 2 overwrote slot 0
```

Three cards, one pile; the best length-1 tail kept dropping.

**Frame 2.** `5`: nothing `>= 5`, append at index 1.

```text
 tails: [ 2 | 5 ]
              ^ new pile, length 2 (2, 5)
```

**Frame 3.** `3`: first tail `>= 3` is 5 at index 1, replace.

```text
 tails: [ 2 | 3 ]
              ^ 5 -> 3: a length-2 run can now end lower
```

No length changed, but the future got easier.

**Frame 4.** `7`: append at index 2. `101`: append at index 3.

```text
 tails: [ 2 | 3 | 7 | 101 ]
                  ^    ^ two new piles
```

**Frame 5.** `18`: first tail `>= 18` is 101 at index 3, replace.

```text
 tails: [ 2 | 3 | 7 | 18 ]   len = 4 -> answer
                       ^ 101 -> 18
```

Invariant across frames: `tails` stayed strictly increasing, its length equalled the longest run seen so far, and each entry was the smallest possible tail for its length.

## Why it is correct

Two inequalities. **At least:** each card placed on pile `k > 1` sits on top of a smaller card on pile `k-1` at that moment (the pile to the left had a top `< x`, or the search would have stopped there), so following those links back gives an increasing subsequence with one card per pile: length = number of piles. **At most:** within one pile, cards are placed in time order with non-increasing values (each new card is `<=` the top it covers), so an increasing subsequence can use at most one card from each pile. Hence LIS = number of piles = `len(tails)`.

`bisect_left` (first tail `>= x`) is what makes it strictly increasing: an equal value replaces, it does not extend. `bisect_right` would compute the longest non-decreasing subsequence instead.

## Cost

- **Brute force:** O(2^n) time, O(n) stack.
- **Classic DP:** O(n^2) time, O(n) space.
- **Patience sorting:** O(n log n) time (one binary search per element), O(n) space for `tails`.

## Variations you will meet

- **Number of Longest Increasing Subsequences (LC 673):** counts are needed, so go back to the O(n^2) DP with a count per index (or a Fenwick tree for O(n log n)).
- **Russian Doll Envelopes (LC 354):** sort by width ascending and height descending, then LIS on heights; the descending tie-break stops equal widths from nesting.
- **Longest non-decreasing subsequence:** switch to `bisect_right`.
- **Minimum deletions to make the array sorted:** `n - LIS`.

## What to carry forward

Keep only the smallest tail for each length; the tails stay sorted, so each new element is one binary search. This closes the chapter, and the book, with a lesson worth keeping: a correct DP is a starting point, not the finish line. The O(n^2) table asked "best run ending below `x`?" by scanning; patience sorting noticed that only the smallest tail per length matters, that those tails are sorted, and that a sorted array answers the question in log time. When your DP's transition is a scan over earlier states, ask whether a dominance rule plus the right structure (a sorted array, a heap, a monotonic stack, a tree) can answer it faster.
