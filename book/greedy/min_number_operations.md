# Minimum Number of Increments on Subarrays to Form a Target Array

*LeetCode 1526 · Hard · Pattern: Count only the rises (adjacent-difference greedy) · Reading time ~8 min*

## What the problem is really asking

You start with an array of zeros the same length as `target`. One operation chooses any contiguous stretch and adds 1 to every element in it. What is the fewest operations that turn the zeros into `target`?

The answer is a count. What makes it hard is that operations overlap freely and can be any length, so the space of plans is enormous: you could build `[2, 1, 3]` as three single-cell strokes plus three more, or as one long stroke under everything plus some short ones on top. The question is which plan is cheapest, and how to know it without trying plans.

Draw the target as a skyline. An operation is a horizontal brick of height 1 laid across a run of adjacent columns. You are asked for the fewest bricks that fill the skyline exactly.

```text
target = [2, 1, 3, 3, 1, 2]
height
  3        [#][#]
  2  [#]   [#][#]   [#]
  1  [#][#][#][#][#][#]
     -----------------
 i:   0  1  2  3  4  5
```

The answer for this skyline is 5.

## Do it by hand first

Fill the skyline with horizontal bricks, layer by layer from the bottom. Each brick must be one contiguous run of filled cells in its row.

```text
row 3:          [====]          1 brick  (i=2..3)
row 2:  [=]     [====]    [=]   3 bricks (i=0, 2..3, 5)
row 1:  [================]      1 brick  (i=0..5)
                                total 5
```

Now look at where each brick starts, its left edge. Row 1's brick starts at i=0. Row 2 has bricks starting at 0, 2 and 5. Row 3's brick starts at 2. Count left edges per column:

```text
 i:              0  1  2  3  4  5
target:          2  1  3  3  1  2
bricks start:    2  0  2  0  0  1     sum = 5
rise from left:  2  -  2  -  -  1
                 (0->2)(1->3)    (1->2)
```

The number of bricks starting at column `i` equals how much the skyline rises from column `i-1` to column `i` (treating the space before column 0 as height 0). Where the skyline is flat or falls, no new brick starts. Your hand was keeping track of one number: the previous column's height.

## The first honest attempt

Simulate. While some position is below its target, find the first position still short, extend a stroke right across the whole run of still-short positions, add 1 to that run, and count one operation.

```text
cur after each op (target 2 1 3 3 1 2):
op1: [1 1 1 1 1 1]   stroke i=0..5
op2: [2 1 1 1 1 1]   stroke i=0
op3: [2 1 2 2 1 1]   stroke i=2..3
op4: [2 1 2 2 1 2]   stroke i=5
op5: [2 1 3 3 1 2]   stroke i=2..3
     every op rescans the whole array to find runs
```

This gives the right count, but each operation scans O(n) and there are up to `max(target)` levels of operations, so it is O(n * max). With heights up to 10^5 and length 10^5, that is far too slow. The repeated work is visible: every scan rediscovers the same run boundaries, and those boundaries are fully determined by the target's shape before you do anything.

The tempting wrong shortcut is "one stroke per height level, so the answer is `max(target)`". For this skyline that gives 3, but row 2 is cut into three separate pieces by the dips at i=1 and i=4, and a single stroke cannot skip over a dip without overshooting the low column. The dips are exactly what makes the problem interesting.

## The turning point

**Claim: the minimum number of operations is `target[0]` plus the sum of all positive steps `target[i] - target[i-1]`.**

Move from the array to its differences. Define `d[0] = target[0]` and `d[i] = target[i] - target[i-1]`. The zero array has all differences 0. What does one operation on `[l, r]` do to the differences? Inside the stretch, adjacent cells both go up by 1, so their difference is unchanged. Only the two boundaries change: `d[l]` goes up by 1 (the stretch rises at its left end) and `d[r+1]` goes down by 1 (it falls at its right end, or that falls off the array if `r` is the last index).

```text
op on [l, r]:
 index:   ... l-1  l  ...  r  r+1 ...
 values:  ...  x  x+1 ... y+1  y  ...
 diffs:         +1 at l    -1 at r+1
                (all others unchanged)
```

So each operation adds exactly 1 to exactly one difference, and possibly subtracts 1 from one other. To reach `target` we must raise the total of positive differences from 0 to `P = sum of max(0, d[i])`. One operation can raise that total by at most 1. Therefore at least `P` operations are needed.

And `P` is enough: the layer-by-layer bricks from the hand solution achieve it, because each brick's left edge sits on a rise, and the number of bricks starting at column `i` is exactly the rise there. So the algorithm needs one variable for the previous height and one running total.

## Watch it work

Example: `target = [2, 1, 3, 3, 1, 2]`. The solution returns 5.

Frame 1. Initialise with the first column: two strokes must start at index 0.

```text
target:  2  1  3  3  1  2
         ^ i=0
ops = target[0] = 2
```

Before index 0 the height is 0, so the rise is 2.

Frame 2. i = 1: 1 < 2, a fall. One of the two strokes ends here for free.

```text
target:  2  1  3  3  1  2
            ^ i=1   prev=2
rise = 1-2 < 0 -> add 0     ops = 2
```

Frame 3. i = 2: 3 > 1, a rise of 2. Two new strokes start here.

```text
target:  2  1  3  3  1  2
               ^ i=2   prev=1
rise = 2 -> ops = 4
```

Frame 4. i = 3: 3 = 3, flat. The strokes simply continue.

```text
target:  2  1  3  3  1  2
                  ^ i=3   prev=3
rise = 0 -> ops = 4
```

Frame 5. i = 4: 1 < 3, a fall of 2. Two strokes end, costing nothing.

```text
target:  2  1  3  3  1  2
                     ^ i=4   prev=3
rise < 0 -> ops = 4
```

Frame 6. i = 5: 2 > 1, a rise of 1. One stroke starts. Done.

```text
target:  2  1  3  3  1  2
                        ^ i=5  prev=1
rise = 1 -> ops = 5      answer 5
```

Across the frames, `ops` always equalled the number of strokes needed to build the prefix `target[0..i]` exactly, and the strokes still "open" at column `i` numbered `target[i]`. A rise opens new strokes, a fall closes some for free, flat changes nothing.

## Why it is correct

The invariant: after processing index `i`, `ops` is the minimum number of operations that build `target[0..i]`, and every optimal plan for that prefix has exactly `target[i]` strokes covering column `i`.

The lower bound is the difference argument. The quantity "sum of positive differences" starts at 0, must end at `P`, and one operation raises it by at most 1. No plan can beat `P`. This is the greedy's certificate: we never pay for anything a lower bound did not already force.

The upper bound is the explicit layering plan. For each height `h` from 1 to the maximum, take the cells with `target[i] >= h` and cover each maximal run of them with one stroke. Every cell at height `t` is covered by exactly `t` strokes, so the result is exactly `target`. A run at level `h` starts at index `i` exactly when `target[i] >= h > target[i-1]`, so the number of runs starting at `i` across all levels is `max(0, target[i] - target[i-1])`. Total strokes = `P`.

You can also phrase it as an exchange. Take any optimal plan and look at one boundary, between columns `j-1` and `j`. If some stroke ends at `j-1` and another starts at `j`, splice them into one stroke: the array built is identical and the plan has one fewer operation, contradicting optimality. So at every boundary, strokes either start or end but never both. Since (strokes starting at `j`) minus (strokes ending at `j-1`) must equal `d[j]`, the number of starts is exactly `max(0, d[j])`, and summing starts counts every stroke once.

## Cost

Time O(n): one pass comparing each element with its predecessor.

Space O(1): the running total and the index. Compare with the simulation's O(n * max(target)) time.

## Variations you will meet

- **Decrements allowed too (LeetCode 3229, start from `nums`).** Work on `diff = target - nums`, which can be negative. Positive and negative stretches need separate strokes, so walk the diffs: with the same sign as the previous cell you pay only the growth in absolute value; when the sign flips you pay the full new magnitude.
- **Strokes of fixed length k.** The free choice of length disappears. Sweep left to right with a difference array of "strokes still active", and at each index you are forced to start exactly `target[i] - active` strokes; any negative requirement means impossible.
- **Minimum operations to make array equal using +1 on n-1 elements.** Same lens of "what does an operation do to a summary quantity", here relative to the minimum element.
- **Painting a fence or a skyline with horizontal strokes (Strange Printer style).** When strokes can overwrite with different colours, counting rises is no longer enough and you need interval DP.

## What to carry forward

Turn an array-building question into a difference-array question: an operation that touches a contiguous range only changes the two boundary differences, so count what each boundary must pay. The next problem keeps prefix balances but lets every machine move one item per step simultaneously, and the answer becomes the worst bottleneck among the boundaries.
