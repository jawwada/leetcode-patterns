---
rank: 64
slug: sliding_window_maximum
---

Given an array and a window size `k`, return the maximum of every window of `k` consecutive values as the window slides one step at a time from left to right. For `[9, 7, 8, 3, 2, 5, 1]` and `k = 3` the windows are `[9, 7, 8]`, `[7, 8, 3]`, `[8, 3, 2]`, `[3, 2, 5]` and `[2, 5, 1]`, so the answer is `[9, 8, 8, 5, 5]`.

The brute force rescans every window, `O(n · k)`, and a max-heap that lazily discards expired indices still pays `O(n log n)`. The linear solution rests on one observation: when a new value arrives, every older value in the window that it matches or beats is never needed again, because the newcomer is at least as large and stays in the window longer. Throw those losers away and the survivors, read from oldest to newest, form a strictly decreasing staircase of candidates. Keep their indices in a deque. The newcomer enters at the back after popping every value at the back that is no larger than itself. The oldest survivor sits at the front and is the largest, so it is the window's maximum, unless its index has slid out of the window, in which case it leaves through the front.

Each index is pushed once and popped at most once, from one end or the other, so the total work is `O(n)` even though a single step may pop several values. The deque stores indices rather than values because the index is what tells the front that it has expired.

```text
k = 3; the deque holds index:value, front on the left
  i   nums[i]   popped from back   popped from front   deque after     max
  0      9                                             [0:9]
  1      7                                             [0:9 1:7]
  2      8      1:7                                    [0:9 2:8]        9
  3      3                         0:9 (expired)       [2:8 3:3]        8
  4      2                                             [2:8 3:3 4:2]    8
  5      5      4:2 3:3            2:8 (expired)       [5:5]            5
  6      1                                             [5:5 6:1]        5
```

```pseudo
FUNCTION MaxSlidingWindow(nums, k)
    window ← empty deque                 // indices of the candidates
    result ← empty list
    FOR i FROM 0 TO len(nums) - 1
        WHILE len(window) > 0 AND nums[window.back()] ≤ nums[i]
            window.pop_back()            // older and no larger: never needed
        window.push_back(i)
        IF window.front() ≤ i - k
            window.pop_front()           // the front slid out of the window
        IF i ≥ k - 1
            result.append(nums[window.front()])   // front is the window max
    RETURN result
```

The cost is `O(n)` time and `O(k)` space for the deque, plus the output. The signals are a window that slides while its maximum or minimum is needed, and dynamic programming whose next state takes the best of the last `k` states, as in Jump Game VI; for a minimum, flip the comparison so the staircase climbs instead. It is the monotonic stack of #23 with a second exit at the front. The classic mistakes are storing values instead of indices, which leaves the front no way to know that it has expired, and popping the back with `IF` instead of `WHILE`: a large newcomer must clear every smaller value, or on `[3, 1, 2, 5]` with `k = 4` the `3` stays in front of the larger `5` and is reported instead of it.

*Practice:* LC 239 Sliding Window Maximum · LC 1438 Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit · LC 862 Shortest Subarray with Sum at Least K · LC 1696 Jump Game VI
