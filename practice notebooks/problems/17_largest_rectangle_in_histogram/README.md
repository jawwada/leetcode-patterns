# Largest Rectangle in Histogram (LeetCode 84)

**Area:** monotonic stack · **Difficulty:** Medium-Hard · **Key operations:** push index, pop while top is taller, width from the new top, sentinel 0 flushes the stack

## Problem

You are given the heights of a histogram's bars; every bar has width 1. Return the area of the largest rectangle that fits entirely inside the histogram.

## Example

```
heights = [2, 1, 5, 6, 2, 3]   ->   10

        6
      5 #
      # #   3
  2   # # 2 #
  # 1 # # # #
  0 1 2 3 4 5
```

The best rectangle has height 5 and spans bars 2 and 3 (heights 5 and 6): area 5 * 2 = 10.

## Brute force

Take each bar `i` as the height of the rectangle. Walk left while the neighbour is at least as tall, walk right the same way, and multiply the height by the width found. Keep the maximum.

O(n²) time, O(1) extra space. The wasted work: every bar of a plateau rediscovers the same two walls, and a tall bar's long walk is repeated by all the bars of the same height around it. The walls are "nearest shorter bar on each side", and the brute force finds them by walking from scratch each time.

## From brute force to optimal

A bar's rectangle is bounded by the nearest shorter bar on its left and the nearest shorter bar on its right. Instead of walking to find them, let the bars discover their walls as the scan moves.

Keep a stack of bar indices whose heights increase from bottom to top. When bar `i` arrives and is shorter than the top of the stack, bar `i` is the top's right wall. The top's left wall is the bar beneath it in the stack, because everything between them was taller (it was pushed after and already popped). So pop the top, compute `height * (i - left - 1)`, and keep popping while the top is taller than `h`. Then push `i`.

To close the bars still on the stack at the end, process one extra bar of height 0: a sentinel shorter than everything. Each index is pushed once and popped once, so the pass is O(n).

## Intuition

Sweep a vertical line across the histogram from left to right. The stack holds a rising staircase of "open" bars, each one still hoping to extend further right. When the sweep meets a bar lower than the top step, the taller steps must close one by one: each closed step's rectangle reaches from just after the step below it to just before the sweep line, at the step's own height. The step below is the left wall precisely because the stack is increasing. The sentinel 0 at the end is the sweep line leaving the histogram, which closes every remaining step.

## Walkthrough

`bars = [2, 1, 5, 6, 2, 3, 0]` (sentinel appended). Stack shown top first as (index, height). Walls are exclusive, width = `i - left - 1`.

```
i=0 h=2   stack []              push 0          stack [(0,2)]
i=1 h=1   top 2 > 1  pop 0      left -1  width 1-(-1)-1 = 1  area 2*1 = 2   best 2
          push 1                                stack [(1,1)]
i=2 h=5   top 1 not > 5         push 2          stack [(2,5),(1,1)]
i=3 h=6   top 5 not > 6         push 3          stack [(3,6),(2,5),(1,1)]
i=4 h=2   top 6 > 2  pop 3      left 2   width 4-2-1 = 1      area 6*1 = 6   best 6
          top 5 > 2  pop 2      left 1   width 4-1-1 = 2      area 5*2 = 10  best 10
          top 1 not > 2         push 4          stack [(4,2),(1,1)]
i=5 h=3   top 2 not > 3         push 5          stack [(5,3),(4,2),(1,1)]
i=6 h=0   top 3 > 0  pop 5      left 4   width 6-4-1 = 1      area 3*1 = 3   best 10
          top 2 > 0  pop 4      left 1   width 6-1-1 = 4      area 2*4 = 8   best 10
          top 1 > 0  pop 1      left -1  width 6-(-1)-1 = 6   area 1*6 = 6   best 10
          push 6 (sentinel)                     stack [(6,0)]
answer 10
```

When bar 2 (height 5) is popped at `i=4`, the bar below it on the stack is bar 1 (height 1): the nearest shorter bar to its left. Bar 3 (height 6) sat between them and was popped a moment earlier.

## Steps

1. Append a sentinel 0 to the heights; `best = 0`, `stack = []` (indices, heights increasing bottom to top).
2. For each bar `i` with height `h`:
3. While the stack is non-empty and the top's height is **greater** than `h`: pop `top`; `left = stack[-1]` if the stack is non-empty else -1; `best = max(best, heights[top] * (i - left - 1))`.
4. Push `i`.
5. Return `best`.

## Complexity

O(n) time: each index is pushed once and popped once. O(n) space for the stack in the worst case (an increasing histogram).

## Pitfalls

- **Width off by one.** Both walls are exclusive: width is `i - left - 1`, not `i - left`. On the example that reports 15.
- **Wrong left wall for an empty stack.** No shorter bar on the left means the rectangle starts at index 0, so the exclusive wall is -1. Using 0 loses a column: `[2, 2, 2]` gives 4 instead of 6.
- **Forgetting the sentinel.** Without a final height 0, an increasing run is never popped and `[1, 2, 3, 4, 5]` returns 0. A final flush loop works too, but the sentinel is shorter.
- **`>=` instead of `>`.** Popping equal bars early still gives the right area (the last bar of a plateau sees the full width), so both are accepted; the strict `>` keeps the stack reasoning simplest.
- **Storing heights instead of indices.** The width needs indices; the height is a lookup away.
