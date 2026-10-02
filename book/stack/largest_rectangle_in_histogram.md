# Largest Rectangle in Histogram

*LeetCode 84 · Hard · Pattern: Monotonic stack · Reading time ~11 min*

## What the problem is really asking

You get a row of bars, each one unit wide, with given heights. Find the largest axis-aligned rectangle that fits entirely inside the bars, and return its area.

The answer is a single number, but behind it is a pair of walls and a height. Any rectangle inside a histogram has a height equal to the shortest bar it covers, otherwise it would poke out above that bar. So every candidate rectangle is "pinned" by one bar that is its shortest, and it extends sideways until it would have to cover something even shorter.

```text
heights = [2, 1, 5, 6, 2, 3]

6 |       #
5 |     R R
4 |     R R
3 |     R R   #
2 | #   R R # #
1 | # # R R # #
   -------------
 i: 0 1 2 3 4 5

R = best rectangle: height 5, bars 2..3, area 10
```

What makes it hard is that there are O(n^2) ranges of bars to consider, and each range's minimum seems to need its own scan.

## Do it by hand first

Pick a bar and ask: if this bar is the shortest one in my rectangle, how wide can the rectangle be? Walk left until you hit a shorter bar, walk right until you hit a shorter bar. The rectangle lives strictly between those two shorter bars.

```text
bar 2 (h=5): left: bar 1 is 1 < 5, stop
             right: bar 3 is 6 >= 5, go on
                    bar 4 is 2 < 5, stop
             walls at 1 and 4 -> width 4-1-1 = 2
             area 5*2 = 10
bar 4 (h=2): left: 6, 5 ok; 1 < 2 stop at 1
             right: 3 ok; edge at 6
             width 6-1-1 = 4, area 8
```

Your hand computed, for each bar, two things: its **nearest shorter bar on the left** and its **nearest shorter bar on the right**. Everything else follows from those two walls. The right wall is a "next smaller element", the mirror image of Daily Temperatures' "next greater". The left wall is a "previous smaller element". One stack will deliver both.

## The first honest attempt

For each bar `i`, expand left while neighbours are at least `h[i]`, expand right likewise, and take `h[i] * width`. That is O(n^2) time, O(1) space. (Trying every pair of walls with a running minimum is also O(n^2).)

```text
heights: 1 2 3 4 5   (rising)

bar 0 expands right over: 1 2 3 4 5
bar 1 expands right over:   2 3 4 5
bar 2 expands right over:     3 4 5
                              ~~~~~
the same tall bars are walked again
from every shorter bar to their left
```

The waste: each expansion rediscovers boundaries that are implied by work already done. If bar 3 is taller than bar 2, then bar 2's right wall is also beyond bar 3, and the walk from bar 2 crosses ground that bar 3's walk will cross again.

## The turning point

**Claim: if we keep a stack of bar indices with non-decreasing heights, then the moment a shorter bar `i` arrives, the top bar's right wall is `i` and its left wall is the bar directly beneath it on the stack.**

Justify both walls.

*Right wall.* The top bar `t` is popped by the first bar to its right that is shorter than it. Every bar between `t` and `i` was pushed on top of `t` and was at least as tall (otherwise it would have popped `t`). So `i` is the nearest shorter bar on the right. This is exactly Daily Temperatures with the comparison flipped.

*Left wall.* Let `l` be the index beneath `t` on the stack (or -1 if none). When `t` was pushed, it had just popped every bar taller than itself, so `l` is the nearest bar on its left that is not taller: `h[l] <= h[t]`. Every bar strictly between `l` and `t` is gone from the stack, and each one was popped by a shorter bar to its right; that popper was either `t` itself or was popped in turn by an even shorter bar further right, and the chain ends at `t`. So every bar between `l` and `t` is taller than `h[t]`. The rectangle of height `h[t]` therefore spans exactly the open interval `(l, i)`.

So each pop computes one bar's best rectangle:

```text
top = pop();  left = stack top or -1
area = h[top] * (i - left - 1)
```

The width `i - left - 1` counts the bars strictly between the two walls. Append a height-0 sentinel at the end so that every bar still on the stack is popped (a height-0 bar is shorter than everything), and we never need a separate cleanup loop.

Picture: the stack is a rising staircase standing on the left edge. A shorter bar arrives and cuts the staircase at its own height; each step above the cut is closed off, and its rectangle runs from just after the step below it to just before the newcomer.

## Watch it work

`heights = [2, 1, 5, 6, 2, 3]`, plus sentinel 0 at index 6. Left: the histogram (`#` = on the stack, `:` = already popped and settled, `.` = not yet read). Right of the `|`: the stack staircase, its bars drawn bottom to top left to right, with the indices beneath.

Frame 1 — `i = 0`: push.

```text
6 |       .         |
5 |     . .         |
4 |     . .         |
3 |     . .   .     |
2 | #   . . . .     | #
1 | # . . . . .     | #
   -------------    | --
 i: 0 1 2 3 4 5     | 0
    ^               | stack
```

Frame 2 — `i = 1` (h=1) is shorter than bar 0 (h=2): pop 0.

```text
6 |       .         |
5 |     . .         |
4 |     . .         |
3 |     . .   .     |
2 | :   . . . .     |
1 | : # . . . .     | #
   -------------    | --
 i: 0 1 2 3 4 5     | 1
      ^             | stack
pop 0: left = -1, width 1-(-1)-1 = 1, area 2
best = 2
```

Bar 0's answer is final: it cannot extend right past bar 1.

Frame 3 — `i = 2, 3` are taller than the top: push both.

```text
6 |       #         |     #
5 |     # #         |   # #
4 |     # #         |   # #
3 |     # #   .     |   # #
2 | :   # # . .     |   # #
1 | : # # # . .     | # # #
   -------------    | ------
 i: 0 1 2 3 4 5     | 1 2 3
          ^         | stack
```

A rising staircase: nobody's right wall is known yet.

Frame 4 — `i = 4` (h=2) cuts the staircase.

```text
6 |       :         |
5 |     : :         |
4 |     : :         |
3 |     : :   .     |
2 | :   : : # .     |   #
1 | : # : : # .     | # #
   -------------    | ----
 i: 0 1 2 3 4 5     | 1 4
            ^       | stack
pop 3 (h=6): left = 2, width 4-2-1 = 1, area 6
pop 2 (h=5): left = 1, width 4-1-1 = 2, area 10
stop at 1 (h=1 <= 2); push 4.   best = 10
```

Two steps closed. Bar 2's rectangle spans bars 2..3: the best answer appears here.

Frame 5 — `i = 5` (h=3) is taller than the top: push.

```text
6 |       :         |
5 |     : :         |
4 |     : :         |
3 |     : :   #     |     #
2 | :   : : # #     |   # #
1 | : # : : # #     | # # #
   -------------    | ------
 i: 0 1 2 3 4 5     | 1 4 5
              ^     | stack
```

Frame 6 — `i = 6`, sentinel height 0, flushes the stack.

```text
6 |       :         |
5 |     : :         |
4 |     : :         |
3 |     : :   :     |
2 | :   : : : :     |
1 | : : : : : :     |
   -------------    | --
 i: 0 1 2 3 4 5 6   | 6  (h=0)
                ^   | stack
pop 5 (h=3): left = 4, width 1, area 3
pop 4 (h=2): left = 1, width 4, area 8
pop 1 (h=1): left = -1, width 6, area 6
best = 10
```

Running the solution confirms the result 10. In every frame the stack heights rose from bottom to top, each bar was settled exactly once, at its pop, and its area used the step below as the left wall and the current index as the right wall.

## Why it is correct

**Invariant.** Before processing index `i`, the stack holds indices in increasing order with non-decreasing heights, and for each stacked index `s`, the entry beneath it (or -1) is the nearest index left of `s` whose height is not greater than `h[s]`; every bar between the two is taller than `h[s]`.

Pushing preserves it: we push `i` only after popping every bar taller than `h[i]`, so what remains beneath `i` is the nearest bar on its left that is not taller, the bars in between were all popped by shorter bars chaining to `i` (as argued in the turning point), and the heights stay non-decreasing. Popping removes the top and leaves the rest untouched.

**The popped element's answer is fixed at pop time.** When `t` is popped by `i`, with `l` beneath it:

- Every bar in `(t, i)` was pushed above `t` and did not pop it, so each is at least `h[t]`, while `h[i] < h[t]`. So `i` is `t`'s right wall, and no later bar can move it.
- Every bar in `(l, t)` is taller than `h[t]` by the invariant, and `h[l] <= h[t]`. The left wall was settled when `t` was pushed.
- So the rectangle of height `h[t]` through bar `t` spans `(l, i)`, area `h[t] * (i - l - 1)`. Both walls are permanent, so this number is final the moment it is computed.

Ties: if `h[l] == h[t]`, the left wall stops one bar early and this pop undercounts. That is harmless, because bar `l` has the same height, sits on the same stretch, and will be popped later with a left wall at least as far out; its pop reports the full width. Every maximal rectangle is reported exactly by the leftmost of its shortest bars.

Finally, the optimal rectangle has some shortest bar `t`, and its walls are `t`'s nearest strictly shorter neighbours. So it is one of the areas computed at a pop, and the maximum over pops is the answer. The sentinel guarantees every bar is popped.

## Cost

Time O(n): each index is pushed once and popped once; the inner loop's total work across the whole run is at most `n + 1` pops.

Space O(n): an increasing histogram keeps every index on the stack until the sentinel.

The brute force is O(n^2) time, O(1) space. A divide-and-conquer split at the minimum is O(n log n) on average, O(n^2) on sorted input.

## Variations you will meet

- **Two arrays instead of one pass.** Compute `left_smaller[]` with one stack pass from the left and `right_smaller[]` with one from the right, then `max(h[i] * (R[i] - L[i] - 1))`. Easier to explain, same O(n), twice the passes.
- **Maximal Rectangle in a binary matrix** (LeetCode 85, next). Turn each row into a histogram of "consecutive 1s above" and run this algorithm per row.
- **Sum of subarray minimums** (LeetCode 907). Each element is the minimum of `(t - l) * (r - t)` subarrays; the same walls appear, but now you sum contributions instead of maximising areas. Ties must be broken with `<` on one side and `<=` on the other to avoid double counting.
- **Trapping Rain Water with a stack.** A decreasing stack; when a taller bar arrives, the popped bar is the floor of a pool whose walls are the new top and the newcomer.

## What to carry forward

Every rectangle is pinned by its shortest bar, and a rising stack hands each bar both walls the instant a shorter bar arrives: the newcomer on the right, the step beneath it on the left.

The next problem lifts this into two dimensions: each row of a binary matrix becomes a histogram, and this exact routine runs once per row.
