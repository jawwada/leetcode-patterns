# Subarray Sum Equals K
*LeetCode 560 · Medium · Pattern: Prefix sum + hash map of counts · Reading time ~7 min*

## The problem

Given an integer array nums (which may contain negatives and zeros) and an integer k, return the number of contiguous
subarrays whose elements sum to k.

```text
Example: nums = [1, 1, 1], k = 2 -> 2 (the subarrays at indices
  0..1 and 1..2).
```

## What the problem is really asking

You get an array of integers (positive, negative, zero, anything) and a target `k`. Count every contiguous stretch of the array whose elements add up to exactly `k`. You are not asked to find one, and not the longest one: you must count all of them. Two stretches are different if they cover different index ranges, even if they hold the same numbers.

The answer is one integer, but it is a count over up to n(n+1)/2 candidate ranges, so listing them all is already quadratic. What makes it hard is that negatives are allowed. If every number were positive, a window's sum would grow when you extend it and shrink when you trim it, and a sliding window would solve it in one pass. A single `-1` breaks that rule: extending can make the sum smaller, so there is no way to decide which end of the window to move.

```text
index:   0   1   2   3   4   5
nums:  [ 1,  2,  1, -1,  2,  1 ]      k = 3

 [0..1]   1 + 2               = 3   yes
 [1..2]       2 + 1           = 3   yes
 [0..3]   1 + 2 + 1 - 1       = 3   yes
 [2..5]           1 - 1 + 2 + 1 = 3 yes
 [4..5]                   2 + 1 = 3 yes
                                 answer = 5
```

Notice `[0..3]` and `[2..5]`: both contain the `-1`, and both are longer than ranges that overshoot. A window that "shrinks when too big" would walk straight past them.

## Do it by hand first

With pen and paper, nobody adds up 21 ranges one by one. You write the running total under the array, starting with 0 before anything has been added. Call these the prefix sums `P`: `P[t]` is the sum of the first `t` elements.

```text
index:        0    1    2    3    4    5
nums:       [ 1,   2,   1,  -1,   2,   1 ]
P:       0    1    3    4    3    5    6
         ^P0  ^P1  ^P2  ^P3  ^P4  ^P5  ^P6

sum(nums[i..j]) = P[j+1] - P[i]
e.g. sum(nums[2..5]) = P6 - P2 = 6 - 3 = 3
```

Now the question changes shape. A range is a pair of marks on the `P` row, a left mark and a right mark, and its sum is the right mark minus the left mark. So you put your finger on each `P` value in turn and ask: how many marks to my left sit exactly 3 below me? At `P6 = 6` you look left for 3s and find two of them (`P2` and `P4`), which are the ranges `[2..5]` and `[4..5]`.

What your hand kept track of was the row of totals written so far. More precisely, it only ever needed to know *how many times each total has appeared*. That tally is the seed of the data structure.

## The first honest attempt

Fix a start `i`, extend an end `j` to the right while keeping a running sum, and bump the answer whenever the running sum equals `k`. That is O(n^2) time and O(1) space, and it is the right first thing to say out loud.

Now look at what the running sums actually are for each start:

```text
start 0:  1  3  4  3  5  6     (= P1..P6 - P0)
start 1:     2  3  2  4  5     (= P2..P6 - P1)
start 2:        1  0  2  3     (= P3..P6 - P2)
start 3:          -1  1  2     (= P4..P6 - P3)
start 4:              2  3     (= P5..P6 - P4)
start 5:                 1     (= P6    - P5)
every row is the same P row, shifted down by P[i]
```

Every row is the tail of one single row, `P`, minus a constant. The brute force recomputes that row n times, once per start. The repeated work is the accumulation itself: the information in all six rows is already in the seven numbers of `P`.

## The turning point

**Claim: the number of subarrays that end at index `j` and sum to `k` equals the number of earlier prefix sums whose value is exactly `P[j+1] - k`.**

The justification is one line of algebra. A range `i..j` sums to `k` exactly when `P[j+1] - P[i] = k`, which rearranges to `P[i] = P[j+1] - k`. For a fixed right end, the right-hand side is a single known number, and the valid left ends are exactly the earlier positions whose prefix sum equals it. Different `i` give different ranges, so we want the *count* of such positions, not just whether one exists.

This is Two Sum again, with two twists. Two Sum asked "have I seen `target - x`?"; here we ask "how many times have I seen `P - k`?". And the pairs are ordered: the left mark must come earlier. Both twists are handled by the same structure, a hash map from prefix-sum value to how many times it has appeared so far, filled as we sweep left to right.

Three details make it exact rather than approximately right:

- **Counts, not a set.** With zeros and negatives the same prefix value repeats (`P2 = P4 = 3` above). Each occurrence is a different start position, so each must be counted.
- **Seed `{0: 1}`.** The empty prefix `P0 = 0` exists before any element. Without it, every range starting at index 0 is missed, such as `[0..1]` and `[0..3]` above.
- **Query before insert.** At step `j` we must look only at `P0..Pj`, never at `P[j+1]` itself. Pairing a prefix with itself would be the empty range, which has sum 0 and would be wrongly counted when `k == 0`.

The order of operations is the whole invariant, so here it is as code:

```python
for v in nums:
    prefix += v
    answer += counts.get(prefix - k, 0)   # earlier marks only
    counts[prefix] = counts.get(prefix, 0) + 1
```

There is no monotonicity anywhere in this argument. That is exactly why it survives negatives where a sliding window does not.

## Watch it work

`nums = [1, 2, 1, -1, 2, 1]`, `k = 3`. The map is shown after the step.

```text
Frame 1   v=1   prefix=1   look for 1-3=-2   found 0
          answer=0      counts {0:1, 1:1}
```
Nothing at -2. Record prefix 1.

```text
Frame 2   v=2   prefix=3   look for 3-3=0    found 1
          answer=1      counts {0:1, 1:1, 3:1}
```
The seeded 0 matches: range `[0..1]`.

```text
Frame 3   v=1   prefix=4   look for 4-3=1    found 1
          answer=2      counts {0:1, 1:1, 3:1, 4:1}
```
`P1 = 1` matches: range `[1..2]`.

```text
Frame 4   v=-1  prefix=3   look for 3-3=0    found 1
          answer=3      counts {0:1, 1:1, 3:2, 4:1}
```
The prefix fell back to 3; the seed matches again, giving `[0..3]`. Now 3 has been seen twice.

```text
Frame 5   v=2   prefix=5   look for 5-3=2    found 0
          answer=3      counts {0:1,1:1,3:2,4:1,5:1}
```
No earlier prefix equals 2.

```text
Frame 6   v=1   prefix=6   look for 6-3=3    found 2
          answer=5      counts {0:1,1:1,3:2,4:1,5:1,6:1}
```
Both earlier 3s match: `[2..5]` and `[4..5]`. Final answer 5.

Across every frame the map held exactly the prefix sums strictly before the current one, with multiplicity. Frame 6 is where counting (not mere membership) paid off: one lookup accounted for two ranges at once.

## Why it is correct

The invariant: just before processing index `j`, `counts` is the multiset `{P0, P1, ..., Pj}`. It holds initially because of the seed `{0: 1}`, and each step restores it by inserting `P[j+1]` after the query.

Given the invariant, the query at step `j` returns the number of `i` in `0..j` with `P[i] = P[j+1] - k`, which by the algebra above is exactly the number of ranges ending at `j` with sum `k`. Every range has exactly one right end, so summing the per-step counts counts every qualifying range exactly once. No range is empty, because `i <= j` means the range `i..j` has at least one element.

## Cost

- **Time O(n):** one pass, each step a constant number of expected-O(1) dictionary operations.
- **Space O(n):** the map holds at most n + 1 distinct prefix sums.

The brute force is O(n^2) time and O(1) space; the trade is linear memory for a linear factor of time.

## Variations you will meet

- **Longest subarray with sum k (LeetCode 325).** Store the *first index* where each prefix appeared instead of a count; the length is `j + 1 - first[P - k]`. Never overwrite an earlier index, since earliest means longest.
- **Subarray sums divisible by K (974) and Continuous Subarray Sum (523).** Two prefixes give a range divisible by `k` when they are equal modulo `k`, so key the map by `prefix % k`. Python's `%` is never negative for positive `k`, which saves a bug other languages have.
- **Count nice subarrays (1248) and binary-array variants.** Map each element to 0 or 1 first (odd -> 1), then it is this exact problem with `k` = the required count.
- **Number of submatrices that sum to target (1074).** Fix a pair of rows, collapse the columns between them into one array of column sums, and run this algorithm on it. O(rows^2 * cols).

## What to carry forward

A range sum is the difference of two prefix sums, so counting ranges is counting earlier prefixes at the right height, and a frequency map does that in one pass. The next problem leaves arithmetic behind but keeps the spirit of writing a number down *in front* so the reader never has to search: encode a list of strings by prefixing each with its length.
