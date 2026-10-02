# Subarrays with K Different Integers

*LeetCode 992 · Hard · Pattern: Exactly-K = atMost(K) - atMost(K-1) · Reading time ~11 min*

## What the problem is really asking

Given an integer array `nums` and an integer `k`, count how many contiguous subarrays contain exactly `k` distinct values. Not the longest one, not the shortest one: *how many*. Two subarrays with the same contents at different positions count separately.

The answer is a single integer, but it summarises up to `n(n+1)/2` subarrays, so we cannot afford to look at them one by one. The previous problems in this chapter each produced one window per right end (the longest valid, or the shortest covering). Counting asks about *all* valid windows per right end, and the condition "exactly `k`" is awkward in a way we will see shortly.

```text
nums = [1, 2, 1, 2, 3]     k = 2
        0  1  2  3  4

exactly 2 distinct:
  [1,2]      [2,1]     [1,2]     [2,3]
  [1,2,1]    [2,1,2]
  [1,2,1,2]
answer: 7
```

What makes it hard: a sliding window works by keeping, for each right end, one boundary on the left. "Exactly `k`" does not have one boundary. It has two.

## Do it by hand first

Fix the right end and ask "which starts work?". That is how you would count by hand without missing anything: column by column.

```text
right end r = 3 (value 2):  windows ending at index 3

start 0: [1 2 1 2]   distinct {1,2}    2  yes
start 1:   [2 1 2]   distinct {1,2}    2  yes
start 2:     [1 2]   distinct {1,2}    2  yes
start 3:       [2]   distinct {2}      1  no
```

Now do `r = 4` (value 3):

```text
start 0: [1 2 1 2 3]   3 distinct   no (too many)
start 1:   [2 1 2 3]   3            no
start 2:     [1 2 3]   3            no
start 3:       [2 3]   2            yes
start 4:         [3]   1            no (too few)
```

Look at the pattern of yes/no as the start moves right. Too many, too many, too many, *yes*, too few. The valid starts form a contiguous band, but it is bounded on **both** sides: on the left by "too many distinct", on the right by "too few". Your hand kept track of two edges, not one. That is the seed of the trick.

## The first honest attempt

For each start `i`, extend `j` to the right, adding `nums[j]` to a set. Whenever the set has size `k`, add one to the answer; once it exceeds `k`, stop, since longer windows only have more values. That is `O(n²)` time in the worst case (think of an array where `k` is large and the set grows slowly), with `O(k)` space.

The repeated work: start `i + 1` rebuilds the set of nearly the same elements that start `i` just processed.

```text
nums:     1  2  1  2  3
start 0: {1}{1,2}{1,2}{1,2}  stop at 3
start 1:    {2}{1,2}{1,2}    stop at 3   rebuilt
start 2:       {1}{1,2}      stop at 3   rebuilt
```

The natural fix is a sliding window: keep one set of counts and move two pointers. But try it and it breaks. With a single left edge, what rule moves it? If the window has more than `k` distinct values, shrink. Fine. But if it has exactly `k`, should the left edge stay, or move to count the shorter windows that also have exactly `k`? Each choice misses windows the other choice would find.

## The turning point

**Claim: the number of subarrays with exactly `k` distinct values equals the number with at most `k` minus the number with at most `k - 1`.**

The justification is set arithmetic. Every subarray with at most `k` distinct values has either exactly `k`, or at most `k - 1`. Those two groups do not overlap. So

```text
atMost(k)  =  exactly(k)  +  atMost(k-1)
exactly(k) =  atMost(k)   -  atMost(k-1)
```

Why is that a rescue? Because "at most `limit` distinct" **is** monotone. If a window has at most `limit` distinct values, every window inside it does too: removing elements never adds a new value. So for a fixed right end `r`, the valid starts are all the starts from some `left` up to `r`. One boundary, not two. And as `r` moves right, that `left` never moves back, because a window that already had too many values only gets worse when extended.

```text
for one right end r, picture the valid starts as bars:

starts:          0  1  2  3  4
atMost(2), r=3: [===========]      left = 0, 4 starts
atMost(1), r=3:          [==]      left = 3, 1 start
exactly(2):     [========]         the part that sticks out
                                   4 - 1 = 3 starts
```

The two-edged band from the hand trace is exactly the piece of the long bar that pokes out past the short bar. We never track the band directly; we track two one-edged bars and subtract.

Counting for one `limit` is the window from Fruit Into Baskets with one change. Keep `counts`, a map from value to how many times it is in the window. For each `r`: add `nums[r]`; while the map has more than `limit` keys, remove `nums[left]` (deleting the key when its count hits zero) and advance `left`. Then every start from `left` to `r` is valid, so add `r - left + 1`. That last line is the counting step: not "one more window", but "all of these windows that end here".

## Watch it work

`nums = [1, 2, 1, 2, 3]`, `k = 2`. First the pass for `atMost(2)`, then `atMost(1)`.

Frame 1: atMost(2), r = 0 to 2.

```text
idx:     0  1  2  3  4
nums:    1  2  1  2  3
        [1  2  1]
         L     R
counts {1:2, 2:1}  2 keys <= 2
adds: r0 +1, r1 +2, r2 +3     total 6
```

Nothing ever exceeded two keys, so the left edge stayed at 0 and each step added the full width.

Frame 2: atMost(2), r = 3.

```text
nums:    1  2  1  2  3
        [1  2  1  2]
         L        R
counts {1:2, 2:2}
add r - L + 1 = 4                total 10
```

Still two keys; four windows end at index 3 and all of them qualify.

Frame 3: atMost(2), r = 4, the shrink.

```text
nums:    1  2  1  2  3
                 [2  3]
                  L  R
add 3 -> {1:2,2:2,3:1} 3 keys > 2
drop 1 (L=1), drop 2 (L=2), drop 1 (L=3)
counts {2:1, 3:1}
add 4 - 3 + 1 = 2                total 12
```

The left edge had to pass every copy of `1` before the map was back to two keys; `atMost(2) = 12`.

Frame 4: atMost(1), all five steps.

```text
nums:    1  2  1  2  3
r=0:    [1]               L=0  +1
r=1:       [2]            L=1  +1
r=2:          [1]         L=2  +1
r=3:             [2]      L=3  +1
r=4:                [3]   L=4  +1
                                 total 5
```

Neighbours always differ, so only single elements have one distinct value; `atMost(1) = 5`.

Frame 5: subtract, column by column.

```text
r:            0   1   2   3   4
atMost(2):    1   2   3   4   2    sum 12
atMost(1):    1   1   1   1   1    sum  5
exactly(2):   0   1   2   3   1    sum  7
```

The answer is `12 - 5 = 7`, and the per-column differences match the hand count (three windows end at index 3, one ends at index 4).

In both passes, after each step the map held exactly the values between `L` and `R`, the window had at most `limit` keys, and `L` was the smallest start for which that was true.

## Why it is correct

Take one pass with some `limit`. Invariant after processing `r`: `left` is the smallest index such that `nums[left..r]` has at most `limit` distinct values. It holds after `r` because the inner loop only advances `left` while the window is invalid, and stops at the first valid start. It never needs to go back: if `nums[left-1..r-1]` already had too many values, then `nums[left-1..r]` does as well.

Given that invariant, the windows ending at `r` with at most `limit` distinct values are exactly those starting in `[left, r]`, by monotonicity (every start after a valid one is valid). There are `r - left + 1` of them. Summing over all `r` counts each qualifying subarray exactly once, by its right end. So `at_most(limit)` is correct, and the subtraction identity gives exactly `k`.

One detail the invariant depends on: `len(counts)` must equal the number of distinct values in the window. If a key's count drops to zero and the key stays in the map, the window looks like it has more distinct values than it does, and the left edge moves too far.

## Cost

- Time `O(n)`: two passes; in each, `right` and `left` each move across the array at most once, and every map operation is `O(1)` on average.
- Space `O(k)`: the map never holds more than `limit + 1` keys.

The brute force is `O(n²)`.

## Variations you will meet

- **Count Number of Nice Subarrays (LeetCode 1248).** Exactly `k` odd numbers in the window. Same identity: `atMost(k) - atMost(k - 1)`, with the count of odd numbers in place of the number of distinct values.
- **Binary Subarrays With Sum (LeetCode 930).** Exactly sum `goal` in a 0/1 array; again "at most" is monotone because all values are non-negative. (With negative values it is not, and you need prefix sums and a hash map instead, as in Subarray Sum Equals K.)
- **Count subarrays with at most `k` distinct.** Just one pass, no subtraction.
- **Exactly `k` without two passes.** You can keep two left pointers in a single loop, one for "at most `k`" and one for "at most `k - 1`", and add the distance between them. It is the same idea with the bars drawn on one picture.

## What to carry forward

A window needs a predicate that only gets worse as the window grows; when the question is "exactly", count "at most" twice and subtract, and when counting, add `r - left + 1` for all the windows that end at `r`. The next problem keeps a fixed-width window but asks for its maximum, which no counter can give us cheaply, so we will keep an ordered shortlist of candidates in a deque.
