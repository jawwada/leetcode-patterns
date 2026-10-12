# Subarray Sum Equals K (LeetCode 560)

**Area:** arrays & hashing · **Difficulty:** Medium · **Key operations:** running prefix sum, count lookup of prefix - k, record the prefix in the count dict

## Problem

Given an integer array `nums` (negatives and zeros allowed) and an integer `k`, return the number of contiguous subarrays whose elements sum to `k`.

## Example

```
nums = [1, 2, 3, -3, 3]   k = 3
answer = 5
```

The five subarrays: `[1,2]`, `[1,2,3,-3]`, `[3]` at index 2, `[3,-3,3]`, and `[3]` at index 4.

## Brute force

For every start `i`, extend an end `j` to the right while accumulating the running sum, and count each time it equals `k`.

O(n²) time, O(1) space. (Re-summing each subarray from scratch would be O(n³).) The wasted work is the accumulation itself: the sum of `nums[i..j]` is rebuilt for every start `i`, although it equals `prefix[j + 1] - prefix[i]`, two numbers that could have been computed once.

## From brute force to optimal

Rewrite the condition `sum(i..j) == k` as `prefix[j + 1] - prefix[i] == k`, i.e. `prefix[i] == prefix[j + 1] - k`. For a fixed right end the question becomes "how many *earlier* prefix sums equal exactly this value?", and a dict of counts answers that in O(1).

So sweep left to right with a running prefix sum and a dict counting every prefix seen so far, seeded with `{0: 1}` for the empty prefix (the subarray that starts at index 0). At each step add `counts[prefix - k]` to the answer, *then* record the current prefix. A sliding window does not work here because negative numbers break monotonicity; the count dict does not need monotonicity.

## Intuition

Plot the prefix sums as a staircase over positions 0..n. A subarray summing to `k` is a pair of points on the staircase, the right one exactly `k` higher than the left one. Walking right along the staircase, at each point look down by `k` and count how many earlier points sit at that height; each of them is a valid left end. The seed `{0: 1}` is the point at height 0 before the first element. Recording the current point *after* looking is what keeps a zero-length subarray from being counted when `k == 0`.

## Walkthrough

`counts` maps a prefix sum to how many times it has occurred so far.

```
nums   1   2   3  -3   3      k 3          counts {0: 1}

i=0  v= 1   prefix 1    earlier prefixes == 1-3 = -2 : 0   answer 0   counts {0:1, 1:1}
i=1  v= 2   prefix 3    earlier prefixes == 3-3 =  0 : 1   answer 1   counts {0:1, 1:1, 3:1}
i=2  v= 3   prefix 6    earlier prefixes == 6-3 =  3 : 1   answer 2   counts {0:1, 1:1, 3:1, 6:1}
i=3  v=-3   prefix 3    earlier prefixes == 3-3 =  0 : 1   answer 3   counts {0:1, 1:1, 3:2, 6:1}
i=4  v= 3   prefix 6    earlier prefixes == 6-3 =  3 : 2   answer 5   counts {0:1, 1:1, 3:2, 6:2}

return 5
```

At `i=4` the prefix 3 has been seen twice (after index 1 and after index 3), which is why two subarrays end there: `[3,-3,3]` and `[3]`.

## Steps

1. `counts = {0: 1}`, `prefix = 0`, `answer = 0`.
2. For each value `v`: `prefix += v`.
3. `answer += counts.get(prefix - k, 0)`.
4. `counts[prefix] = counts.get(prefix, 0) + 1`.
5. Return `answer`.

## Complexity

O(n) time: one pass with O(1) dict work per element. O(n) space: the dict holds at most n + 1 distinct prefix sums.

## Pitfalls

- **Missing seed.** `counts = {}` never counts subarrays that start at index 0: `[1, 1, 1]` with `k = 2` returns 1 instead of 2.
- **Wrong difference.** `counts.get(k - prefix)` asks for the wrong earlier prefix; the example returns 2 instead of 5. The earlier prefix must be `k` *smaller*: `prefix - k`.
- **Overwriting the count.** `counts[prefix] = 1` counts a repeated prefix sum once; the example (prefix 3 appears twice) returns 4 instead of 5.
- **Recording before looking.** Updating `counts[prefix]` before the lookup counts the empty subarray whenever `k == 0`.
- **Sliding window.** Shrinking the window when the sum exceeds `k` is wrong with negatives, since the sum can come back down.
