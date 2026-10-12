---
rank: 44
slug: largest_rectangle_histogram
---

Given the heights of a histogram whose bars all have width 1, return the area of the largest rectangle that fits inside it. For `[2, 1, 5, 6, 2, 3]` the answer is 10: the bars 5 and 6 together hold a rectangle of height 5 and width 2.

The brute force tries every pair of left and right edges while carrying the minimum height between them, `O(n²)`. Look at it per bar instead. The widest rectangle at exactly one bar's height spreads left and right until it meets a lower bar on each side, so every bar needs its nearest lower neighbor on both sides, and the monotonic stack of #17 finds both in a single pass. Keep a stack of indices whose heights never fall from bottom to top. When bar `i` arrives lower than the top, the top's rectangle stops at `i - 1`, since every bar between them is at least as tall or it would have popped the top sooner. Pop it and measure. Its left edge sits just right of the new top, because every bar between those two was popped earlier, and only by a lower bar, so all of them are taller than the bar being measured. The area is the height times `i - left`, and the best area wins.

Two details complete the loop. A 0 appended to the heights is lower than every bar of positive height, so at the end it pops each of them still on the stack and measures it against the right edge of the histogram. When a pop empties the stack, nothing lower lies to the left, and the rectangle reaches index 0. Equal heights may stand side by side; the leftmost of them is popped last and measures the full width.

```text
 6           #               # = bar, ● = the largest rectangle,
 5        ●  ●               height 5 × width 2 = 10
 4        ●  ●
 3        ●  ●     #
 2  #     ●  ●  #  #
 1  #  #  ●  ●  #  #
    2  1  5  6  2  3   + sentinel 0 at index 6

 i  bar   pops: height × width               stack after (index:height)
 0   2    -                                  0:2
 1   1    2 × 1 = 2                          1:1
 2   5    -                                  1:1  2:5
 3   6    -                                  1:1  2:5  3:6
 4   2    6 × 1 = 6, 5 × 2 = 10              1:1  4:2
 5   3    -                                  1:1  4:2  5:3
 6   0    3 × 1 = 3, 2 × 4 = 8, 1 × 6 = 6    6:0
```

```pseudo
FUNCTION LargestRectangleArea(heights)
    bars ← heights + [0]                // the 0 sentinel flushes the stack
    stack ← empty stack                 // indices; heights never fall
    best ← 0
    FOR i FROM 0 TO len(bars) - 1
        WHILE len(stack) > 0 AND bars[stack.top()] > bars[i]
            height ← bars[stack.pop()]          // its rectangle ends at i - 1
            IF len(stack) > 0
                left ← stack.top() + 1          // just right of the new top
            ELSE
                left ← 0                        // empty stack: reaches index 0
            width ← i - left
            best ← max(best, height * width)
        stack.push(i)
    RETURN best
```

Each index is pushed once and popped at most once, so the run is `O(n)` time with `O(n)` space for the stack. The signal is a largest rectangle, or any "minimum times width" score, over contiguous bars or subarrays. Maximal Rectangle in a binary matrix reduces to this: treat each row as the floor of a histogram whose heights count the consecutive 1s running up from it, and run this loop once per row, `O(rows × cols)` in all. Maximum Score of a Good Subarray is the same rectangle with the extra rule that it must cover index `k`. The classic mistakes are measuring the width as `i - j` from the popped index `j` instead of from the new top, which ignores the taller bars popped earlier on the left and returns 3 instead of 4 for `[1, 3, 2]`, and forgetting the sentinel, which leaves a rising histogram such as `[1, 2, 3]` unmeasured on the stack and returns 0 instead of 4.

*Practice:* LC 84 Largest Rectangle in Histogram · LC 85 Maximal Rectangle · LC 1793 Maximum Score of a Good Subarray
