# Sliding Window Maximum

*LeetCode 239 · Hard · Pattern: Monotonic deque · Reading time ~11 min*

## What the problem is really asking

You have an array `nums` and a window width `k`. Slide a window of exactly `k` elements from the left end to the right end, one step at a time, and report the largest value in the window at every position. With `n` elements there are `n - k + 1` windows, so the answer is a list of that many numbers.

```text
nums = [5, 3, 4, 1, 2, 6]    k = 3
        0  1  2  3  4  5

window [0..2]  5 3 4      max 5
window [1..3]    3 4 1    max 4
window [2..4]      4 1 2  max 4
window [3..5]        1 2 6  max 6

answer: [5, 4, 4, 6]
```

The window itself is the easiest kind in the chapter, rigid like Permutation in String. What changes is what we must know about it. Until now every window carried a **summary that can be updated by adding and subtracting**: a sum, a histogram, a count of distinct keys. The maximum is not like that. When an element leaves, you cannot "subtract" it from a max. If the leaving element was the max, the new max is some element you have not been watching, and finding it seems to require a rescan.

So the hard part is not the window. It is the summary.

## Do it by hand first

Picture the numbers as bars and stand at the right end of the current window looking left. Which bars could ever be the answer for this window or a later one?

```text
window [1..3], standing at index 3

  5 |  #
  4 |  #     #
  3 |  #  #  #
  2 |  #  #  #
  1 |  #  #  #  #
    +--------------
       0  1  2  3      index
          [-------]    window

bar 1 (value 3): bar 2 (value 4) is newer AND taller
                 -> bar 1 can never be a max again
bar 2 (value 4): tallest in window      -> current max
bar 3 (value 1): might matter later, once 4 leaves
```

A person doing this would naturally cross out any bar that has a taller bar to its right inside the window. A taller, newer bar will stay in every future window at least as long as the shorter, older one, so the older one is dead. What is left is a **staircase that goes down from left to right**. Its first step is the max. Your hand kept track of that staircase.

## The first honest attempt

For each window, call `max(nums[i : i+k])`. That is `n - k + 1` windows times `k` work, so `O(n · k)`. With `n = 10^5` and `k = 5·10^4` that is billions of comparisons.

The repeated work: neighbouring windows share `k - 1` elements, and we compare all of them again. Worse, most of those comparisons involve elements that could never win.

```text
nums:  5  3  4  1  2  6
win 0 [5  3  4]           compare 5,3,4
win 1    [3  4  1]        compare 3,4,1   <- 3 again,
win 2       [4  1  2]     compare 4,1,2      already beaten
                                             by 4
```

A natural next idea is a heap: push every element, read the top, and lazily discard tops that have slid out. That works in `O(n log n)` and is a fine answer. But the hand picture suggests something better, because the staircase never needs reordering: new elements always arrive at the right end.

## The turning point

**Claim: if `j < i` and `nums[j] <= nums[i]`, then `nums[j]` is never again the maximum of any window that contains `i`, so it can be thrown away the moment `i` arrives.**

Justification: any future window that contains `j` also contains `i`, because windows are contiguous and `i` is to the right of `j` while the windows only move right. In that window, `nums[i]` is at least as large as `nums[j]`. So `nums[j]` either loses or ties with an element that is still present. Either way, reporting `nums[i]` is correct, and `j` contributes nothing.

Throwing away every dominated element leaves the survivors in a very particular order: going left to right, their values **strictly decrease**. (If two survivors had the left one smaller or equal, the left one would be dominated.) This is the staircase from the hand trace.

Now look at how the staircase changes.

- **A new element arrives at the right.** It dominates every survivor at the right end that is less than or equal to it. Because the survivors decrease, those are exactly a run at the back. Pop from the back while the back is `<=` the newcomer, then append the newcomer.
- **The window's left edge passes an index.** If that index is still a survivor, it must be the oldest one, which is at the front. Pop from the front.
- **The maximum** is the largest survivor, which is the front.

Operations at both ends, in order: that is a `collections.deque`. And we store **indices**, not values, because the expiry test ("has this survivor slid out?") is about position: the front expires when its index is `<= i - k`.

```text
deque (indices), values strictly decreasing front -> back

front                             back
 [ i0 ]  [ i1 ]  [ i2 ] ... [ im ]
  big     ...            small
  ^ max; pops when i0 <= i-k
                            ^ pops when newcomer >= it
```

## Watch it work

`nums = [5, 3, 4, 1, 2, 6]`, `k = 3`. The deque is written as `index:value`.

Frame 1: filling, i = 0 and i = 1.

```text
idx:  0  1  2  3  4  5
nums: 5  3  4  1  2  6
     [5  3]
dq: [0:5, 1:3]                  no output yet
```

`3` is smaller than `5`, so it waits behind it; the deque is a two-step staircase.

Frame 2: i = 2, the newcomer kills a step.

```text
nums: 5  3  4  1  2  6
     [5  3  4]
4 >= 3 -> pop 1:3 from back; 4 < 5 -> stop
dq: [0:5, 2:4]                  output 5
```

`3` is dominated by the newer, taller `4` and is gone for good; the front `5` is the first window's max.

Frame 3: i = 3, the front expires.

```text
nums: 5  3  4  1  2  6
        [3  4  1]
push 3:1 -> [0:5, 2:4, 3:1]
front index 0 <= 3 - 3 -> popleft
dq: [2:4, 3:1]                  output 4
```

The old max `5` slid out of the window, and the next step of the staircase, `4`, was already waiting at the front.

Frame 4: i = 4, a small newcomer pops a smaller one.

```text
nums: 5  3  4  1  2  6
           [4  1  2]
2 >= 1 -> pop 3:1; 2 < 4 -> stop
dq: [2:4, 4:2]                  output 4
```

`1` can never be a max while `2` is around; the front index 2 is still inside the window, so `4` stays the answer.

Frame 5: i = 5, a giant clears the deque.

```text
nums: 5  3  4  1  2  6
              [1  2  6]
6 >= 2 -> pop 4:2; 6 >= 4 -> pop 2:4
dq: [5:6]                       output 6
```

`6` dominated every survivor, so the deque collapsed to one element, and the final answer is `[5, 4, 4, 6]`.

In every frame the deque held exactly the indices in the window that have no taller-or-equal element to their right inside the window, in increasing index order and strictly decreasing value order, and the front was the window maximum.

## Why it is correct

The invariant after processing index `i`: the deque contains, in increasing order of index, exactly those indices `j` in the window `[i - k + 1, i]` such that `nums[j] > nums[t]` for every `t` with `j < t <= i`. Call these the *leaders* of the window.

It holds after each step. The newcomer `i` is always a leader (nothing is to its right). An old leader `j` stops being a leader exactly when `nums[i] >= nums[j]`, and since leader values decrease toward the back, those are precisely the ones popped from the back before the stop. Old leaders that remain are still leaders, because the only new element is `i` and it is smaller than them. Finally, the only index that can leave the window at step `i` is `i - k`; if it is a leader it is the oldest, so the front check removes it. One check suffices because only one index leaves per step.

The maximum of the window is a leader (nothing to its right is larger or equal, if we take its rightmost copy), and leaders decrease left to right, so the maximum is the first leader: the front.

## Cost

- Time `O(n)`: each index is appended once and popped at most once (from one end or the other), so the total work in all the `while` loops is at most `n`.
- Space `O(k)`: the deque only holds indices inside the current window.

The brute force is `O(n · k)`; a heap with lazy deletion is `O(n log n)`.

## Variations you will meet

- **Sliding window minimum.** Flip every comparison: keep values strictly increasing from front to back.
- **Longest subarray where max - min <= limit (LeetCode 1438).** Run two deques at once, one for max and one for min, inside a variable window: grow the right edge, and while `front of max-deque - front of min-deque > limit`, advance the left edge and expire fronts whose index fell behind it.
- **Jump Game VI / Constrained Subsequence Sum.** A DP where `dp[i] = nums[i] + max(dp[i-k .. i-1])`. The "max over the last `k` values" is this problem, run over the DP array as it is being filled.
- **Ties.** Popping with `<=` keeps the deque strictly decreasing and smaller. Popping only with `<` also gives correct maxima but keeps equal values around for no benefit.

## What to carry forward

When a window's summary cannot be subtracted, keep only the candidates that are not dominated by a newer, better element; they form a monotone deque, the front is the answer, and every element enters and leaves once. The next problem applies the same dominance pruning to prefix sums, which is how we get a window back when negative numbers break the usual "shrink while too big" rule.
