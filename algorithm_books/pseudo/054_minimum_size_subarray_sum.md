---
rank: 54
slug: minimum_size_subarray_sum
---

Given an array of positive integers and a positive target, return the length of the shortest contiguous subarray whose sum is at least the target, or `0` if no subarray gets there. In `[2, 3, 1, 2, 4, 3]` with target `7` the answer is `2`, the subarray `[4, 3]`.

The brute force sums forward from every start until it reaches the target, `O(n²)` in the worst case. The insight is that positive values make the window sum move in a known direction: pushing the right edge forward can only raise it, and pushing the left edge forward can only lower it. So one window slides with two edges. `right` takes one more value per step; whenever the sum is enough, record the window's length and drop `nums[left]` to try a shorter one, and keep dropping while the sum stays enough. The first drop that leaves the sum short hands control back to `right`. This is the expand-right, shrink-left loop of Minimum Window Substring (#13), with a running sum in place of character counts.

Positivity is also what makes it safe to drop a left index for good. When `left` leaves, `nums[left..right]` is the first window starting at `left` that reaches the target: one step earlier, a window that started at or before `left` and ended at `right - 1` fell short, and a window inside it sums to no more. So it is the shortest valid window starting at `left`, and later right ends only make it longer. A negative value breaks this. On `[3, -2, 4]` with target `4` the window reaches sum `5`, records length 3, drops the `3`, sees `2` and stops, never learning that dropping the `-2` too climbs back to `4` with the single value `[4]`.

```text
index          0  1  2  3  4  5      target = 7
nums           2  3  1  2  4  3
right 0..2     sums 2, 5, 6: below 7, keep expanding
right 3        └────────┘          sum  8 ≥ 7   len 4   drop 2 → sum 6
right 4           └────────┘       sum 10 ≥ 7   len 4   drop 3 → sum 7
                     └─────┘       sum  7 ≥ 7   len 3   drop 1 → sum 6
right 5                 └─────┘    sum  9 ≥ 7   len 3   drop 2 → sum 7
                           └──┘    sum  7 ≥ 7   len 2   drop 4 → sum 3
best = 2: the window [4, 3]
```

```pseudo
FUNCTION MinSubarrayLen(nums, target)
    left ← 0
    window_sum ← 0                          // sum of nums[left..right]
    best ← len(nums) + 1                    // longer than any real window
    FOR right FROM 0 TO len(nums) - 1
        window_sum ← window_sum + nums[right]   // expand: take one more value
        WHILE window_sum ≥ target               // enough: record, then shrink
            best ← min(best, right - left + 1)
            window_sum ← window_sum - nums[left]
            left ← left + 1
    IF best > len(nums)
        RETURN 0                            // no window ever reached the target
    RETURN best
```

Each index enters and leaves the window at most once, so the scan is `O(n)` time even when one step drops several values, with `O(1)` extra space. Reach for it when a problem asks for the shortest or longest stretch under a condition that moves one way as the window grows, such as a sum or product of positive numbers. Subarray Product Less Than K counts instead: shrink while the product is at least `k`, and then all `right - left + 1` windows that end at `right` qualify. With negatives, as in Shortest Subarray with Sum at Least K, keep the prefix sums of #2 in an increasing monotonic deque (#64): a new prefix pops the front while it beats it by at least `k`, recording lengths, and pops the back while the back is no smaller before joining. The classic mistake is shrinking with `IF` instead of `WHILE`: the window then gives up one value per step, so on `[1, 1, 1, 1, 7]` with target `7` it records length 5 and never shrinks to the single `7`.

*Practice:* LC 209 Minimum Size Subarray Sum · LC 713 Subarray Product Less Than K · LC 862 Shortest Subarray with Sum at Least K
