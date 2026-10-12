---
rank: 28
slug: kadane
---

Given a non-empty array of integers, find the contiguous subarray with the largest sum and report that sum with the subarray's first and last index. In `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` the answer is `6`, from `[4, -1, 2, 1]` at indices `3` to `6`.

The brute force tries every subarray, and even with a running total per start that is `O(n²)` work. Kadane's insight is to ask a smaller question at each index: what is the best sum of a subarray that ends exactly here? That subarray either extends the best one ending one step earlier or starts fresh at the current number, so `ending_here = max(x, ending_here + x)`. Extending loses exactly when the run behind is negative, because a negative prefix can only drag `x` down, so the choice is a sign test: restart when `ending_here < 0`, extend otherwise. The answer is the best `ending_here` seen anywhere, and one pass carries just two numbers, the run that ends at the pointer and the best run so far.

Picture the prefix sums as a mountain profile, point `k` standing at the sum of the first `k` numbers; the sum of `nums[i..j]` is then the climb from point `i` to point `j + 1`. The run turns negative exactly when the profile dips to a new low, so every restart moves the base camp to the lowest point so far, and the best subarray is the biggest climb from a low to a later peak: the stock problem of #29 run on prefix sums, except that a trade is compulsory, because the subarray cannot be empty. The bounds come almost free. `start` jumps to `i` on every restart, and whenever `best` improves, the current `start` and `i` are copied into `best_start` and `best_end`.

```text
  i    x    extend or restart    ending_here   start   best   best bounds
  0   -2    first element             -2          0      -2      [0, 0]
  1    1    restart: -2 < 0            1          1       1      [1, 1]
  2   -3    extend                    -2          1       1      [1, 1]
  3    4    restart: -2 < 0            4          3       4      [3, 3]
  4   -1    extend                     3          3       4      [3, 3]
  5    2    extend                     5          3       5      [3, 5]
  6    1    extend                     6          3       6      [3, 6]
  7   -5    extend                     1          3       6      [3, 6]
  8    4    extend                     5          3       6      [3, 6]

  prefix sums   0  -2  -1  -4   0  -1   1   2  -3   1
                            ▲ new low       ▲ peak: 2 - (-4) = 6
```

```pseudo
FUNCTION MaxSubarray(nums)
    ending_here ← nums[0]                  // best sum of a subarray ending at i
    start ← 0                              // where that subarray begins
    best ← nums[0]                         // not 0: all may be negative
    best_start ← 0
    best_end ← 0
    FOR i FROM 1 TO len(nums) - 1
        IF ending_here < 0                 // a negative run only drags x down
            ending_here ← nums[i]          // restart at x
            start ← i
        ELSE
            ending_here ← ending_here + nums[i]        // extend the run
        IF ending_here > best              // improved: copy the bounds
            best ← ending_here
            best_start ← start
            best_end ← i
    RETURN (best, best_start, best_end)
```

One pass with constant work per element gives `O(n)` time and `O(1)` space. Reach for Kadane when a problem asks for the best contiguous stretch, a largest sum or gain over consecutive elements, and the best stretch ending at `i` can be built from the best one ending at `i - 1`. The variants change what is carried. A circular array (LC 918) takes the larger of the plain answer and the total minus the minimum subarray sum, unless every number is negative; a product (LC 152) carries both the largest and the smallest product ending here, because a negative factor swaps them; the largest absolute sum (LC 1749) is the larger of the maximum sum and the negated minimum sum. The classic mistake is starting `best` at `0`, which answers `0` for `[-3, -1, -2]` instead of `-1`: the empty subarray is not a choice.

*Practice:* LC 53 Maximum Subarray · LC 918 Maximum Sum Circular Subarray · LC 152 Maximum Product Subarray · LC 1749 Maximum Absolute Sum of Any Subarray
