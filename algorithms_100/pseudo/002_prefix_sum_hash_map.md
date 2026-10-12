---
rank: 2
slug: prefix_sum_hash_map
---

Given an array of integers, negatives allowed, and a target `k`, count the contiguous subarrays whose sum is exactly `k`. In `[2, -1, 1, 2]` with `k = 2` the answer is `4`: `[2]`, `[2, -1, 1]`, `[-1, 1, 2]` and the final `[2]`.

The brute force fixes every start, extends every end with a running sum and pays `O(n²)`. The insight is that every subarray sum is a difference of two prefix sums. If `prefix` is the sum of everything up to the current index and some earlier prefix equals `prefix - k`, the stretch between them sums to exactly `k`. The question at each index becomes Two Sum (#1) looking backward: how many earlier prefixes equal `prefix - k`? A map from prefix sum to the number of times it has occurred answers it in one lookup. The map is seeded with `0 → 1`, the empty prefix before index 0, so that a subarray starting at index 0 has a partner to find.

Picture the prefix sums as a walk of heights, `0, 2, 1, 2, 4` here. Every subarray is a step from an earlier height to a later one, and the algorithm counts the steps that climb exactly `k`. The map stores counts, not indices, because a height can come back: `2` occurs twice, and both visits pair with the final `4`. That return is why a sliding window fails. With only positive numbers the walk climbs strictly, so each right end has at most one matching left end, and a window that shrinks whenever its sum passes `k` finds it. A negative number lets the walk fall back, the window sum stops being monotone, and the window cannot tell which end to move; on this array it finds only 3 of the 4.

```text
k = 2; prefix_count starts as {0: 1} for the empty prefix
  x   prefix   prefix - k   found   total   prefix_count after
  2      2          0         1       1     {0: 1, 2: 1}
 -1      1         -1         0       1     {0: 1, 2: 1, 1: 1}
  1      2          0         1       2     {0: 1, 2: 2, 1: 1}
  2      4          2         2       4     {0: 1, 2: 2, 1: 1, 4: 1}
the four subarrays:  [2]   [2, -1, 1]   [-1, 1, 2]   [2]
```

```pseudo
FUNCTION SubarraySum(nums, k)
    prefix_count ← empty map               // prefix sum → how many times seen
    prefix_count[0] ← 1                    // the empty prefix, before index 0
    prefix ← 0
    total ← 0
    FOR EACH x IN nums
        prefix ← prefix + x                // sum of nums up to and including x
        // each earlier prefix equal to prefix - k starts one subarray of sum k
        total ← total + prefix_count.get(prefix - k, 0)
        prefix_count[prefix] ← prefix_count.get(prefix, 0) + 1   // record last
    RETURN total
```

One pass with constant-time map operations gives `O(n)` time, and the map costs `O(n)` space. Reach for this pattern whenever a problem asks about subarrays with an exact sum, especially when negative numbers rule out a window. Key the map by `prefix mod k` to count sums divisible by `k`, or store each prefix's first index instead of a count to find the longest such subarray, as in Contiguous Array with every `0` read as `-1`. The classic mistakes are forgetting the seed, which misses every subarray that starts at index 0 (2 of the 4 here), and recording the current prefix before counting, which pairs a prefix with itself when `k = 0`: on `[0, 0, 0]` that reports 9 subarrays instead of 6.

*Practice:* LC 560 Subarray Sum Equals K · LC 974 Subarray Sums Divisible by K · LC 523 Continuous Subarray Sum · LC 525 Contiguous Array
