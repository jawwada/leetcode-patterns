# Sliding Window Maximum (LeetCode 239)

**Area:** sliding window · **Difficulty:** Medium-Hard · **Key operations:** pop back while smaller or equal, push index, pop front when it leaves the window, read the max at the front

## Problem

Given an array `nums` and a window size `k`, return the maximum of every contiguous window of `k` elements, from left to right.

## Example

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

[1  3  -1] -3  5  3  6  7   -> 3
 1 [3  -1  -3] 5  3  6  7   -> 3
 1  3 [-1  -3  5] 3  6  7   -> 5
 1  3  -1 [-3  5  3] 6  7   -> 5
 1  3  -1  -3 [5  3  6] 7   -> 6
 1  3  -1  -3  5 [3  6  7]  -> 7

answer = [3, 3, 5, 5, 6, 7]
```

## Brute force

For each of the `n - k + 1` windows, take `max(nums[i:i+k])`.

O(n·k) time, O(1) extra space. The wasted work: neighbouring windows share `k - 1` elements that get rescanned, and most of them are dominated by a newer, larger element and could never be a maximum again.

## From brute force to optimal

If `nums[j] <= nums[i]` with `j < i`, then `j` leaves every future window before `i` does and is never larger, so `j` is useless from now on. Keep only the useful indices in a deque whose values strictly decrease from front to back. The front is the current window's maximum. When a new element arrives, pop smaller-or-equal values off the back (they are dominated), then push its index. Pop the front when its index slides out of the window. Each index is pushed once and popped at most once, so the pass is O(n).

## Intuition

Stand at the newest bar and look left: the only bars that can still matter are the ones visible as a descending staircase, each taller than everything newer. The deque *is* that staircase. A new bar hides every older bar that is not taller, so those drop off the back. The tallest step at the front is the window maximum, and it crumbles only when the window edge passes it.

## Walkthrough

The deque holds `(index, value)` pairs, front first. `i - k` is the index that has just left the window.

```
i=0 x= 1                                push 0    deque [(0,1)]                  window [0..0]
i=1 x= 3  pop back 0 (1 <= 3)           push 1    deque [(1,3)]                  window [0..1]
i=2 x=-1                                push 2    deque [(1,3) (2,-1)]           window [0..2]  out [3]
i=3 x=-3                                push 3    deque [(1,3) (2,-1) (3,-3)]    window [1..3]  out [3, 3]
          front 1 <= 3-3=0? no, still inside
i=4 x= 5  pop back 3 (-3 <= 5)
          pop back 2 (-1 <= 5)
          pop back 1 ( 3 <= 5)          push 4    deque [(4,5)]                  window [2..4]  out [3, 3, 5]
i=5 x= 3                                push 5    deque [(4,5) (5,3)]            window [3..5]  out [3, 3, 5, 5]
i=6 x= 6  pop back 5 (3 <= 6)
          pop back 4 (5 <= 6)           push 6    deque [(6,6)]                  window [4..6]  out [3, 3, 5, 5, 6]
i=7 x= 7  pop back 6 (6 <= 7)           push 7    deque [(7,7)]                  window [5..7]  out [3, 3, 5, 5, 6, 7]
```

The front never expired in this example because every maximum was evicted by a larger newcomer first. On `[9, 8, 7, 6]` with `k = 2` the opposite happens: nothing is ever popped from the back, and the front is popped every step as it leaves the window.

## Steps

1. `dq = deque()` of indices, `out = []`.
2. For each `i`: while the deque is non-empty and `nums[dq[-1]] <= nums[i]`, pop the back. Push `i`.
3. If `dq[0] <= i - k`, pop the front: it has left the window.
4. If `i >= k - 1`, append `nums[dq[0]]` to `out`.
5. Return `out`.

## Complexity

O(n) time: each index is pushed once and popped at most once (from either end). O(k) space: the deque never holds more than one window's worth of indices.

## Pitfalls

- **`dq[0] < i - k` for the expiry check.** Index `i - k` is already outside `[i-k+1..i]`; the stale front lingers one step and `[5, 1, 1, 1]`, `k = 2` reports `5` for the second window.
- **`i >= k` for the first output.** The first full window ends at `k - 1`; starting at `k` drops the first answer and the output is one short.
- **Reading the back instead of the front.** `dq[-1]` is the newest survivor, the smallest candidate; `[1, 3, -1]` with `k = 3` would report `-1`.
- **Storing values instead of indices.** You cannot tell when a value leaves the window without its index.
- **Evicting with `<` instead of `<=`.** Still correct, but equal values pile up in the deque and it can grow to O(n) instead of O(k).
