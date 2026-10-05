# Shortest Subarray with Sum at Least K

*LeetCode 862 · Hard · Pattern: Monotonic deque · Reading time ~12 min*

## The problem

Given an integer array nums whose values may be negative and an integer k, return the length of the shortest non-empty
contiguous subarray with sum >= k, or -1 if there is none.

```text
Example: nums = [2,-1,2], k = 3 -> 3, because only the whole
  array reaches 3. nums = [1,2], k = 4 -> -1.
```

## What the problem is really asking

Given an integer array `nums` and a target `k`, find the length of the shortest non-empty contiguous subarray whose sum is at least `k`. Return `-1` if none exists. The twist that makes it a Hard: **values may be negative**.

Without the negatives, this is problem 2 of this chapter, Minimum Size Subarray Sum, and the answer is a plain shrinking window. So the first job is to understand exactly what negative numbers break.

```text
nums = [3, -2, 4, 1]      k = 5
        0   1  2  3

[3,-2,4,1] = 6   len 4   ok
[3,-2,4]   = 5   len 3   ok
[4,1]      = 5   len 2   ok   <- shortest
[-2,4,1]   = 3            no
answer: 2
```

The answer is a single length. The object we search over is a pair (start, end), and the difficulty is that with negatives, "sum of a window" stops being monotone in the window's size.

## Do it by hand first

Here is the plain window from problem 2 on a small array where it fails.

```text
nums = [1, -3, 5]     k = 5     true answer: 1 ([5])

grow:  [1]         sum 1
grow:  [1,-3]      sum -2
grow:  [1,-3,5]    sum 3   < 5, never shrinks
plain window says: no answer   WRONG
```

The rule "only shrink when the sum is big enough" assumed that dropping an element from the left makes the sum smaller. Here dropping `1` and `-3` makes the sum *larger*. The left edge is stuck behind a negative stretch that it should have abandoned.

So how does a person find `[5]`? Not by thinking about windows. You think "the sum from `i` to `j` is the running total at `j` minus the running total just before `i`". Write the running totals down:

```text
index i:    0   1   2   3
nums:           1  -3   5
P[i]:       0   1  -2   3      P[i] = sum of first i items

sum of nums[i..j-1] = P[j] - P[i]
[5] = P[3] - P[2] = 3 - (-2) = 5   ok, length 3 - 2 = 1
```

What your hand kept track of is a list of **past running totals**, and for each new total you asked "which earlier total is at least `k` below me, and as close as possible?". A low earlier total is a good start. That is the seed.

## The first honest attempt

Try every start `i`, extend `j` while keeping a running sum, and record `j - i + 1` whenever the sum reaches `k`. With negatives you cannot stop early, because a later element might push the sum back up and a shorter answer can still appear for a later start. Every pair is examined: `O(n²)` time, `O(1)` space.

The waste has two faces. First, sums are recomputed per start. Prefix sums fix that, but the pair search is still `O(n²)`. Second, and more important, many starts are hopeless and we keep trying them.

```text
P:       0   3   1   5   6
index:   0   1   2   3   4

start 1 has P = 3, start 2 has P = 1.
Start 2 is LATER (shorter windows) and LOWER
(bigger sums). For every end j, start 2 beats start 1.
Yet the brute force tries start 1 against every j.
```

## The turning point

**Claim: an earlier start `i1` is useless if a later start `i2` has a prefix sum that is no larger, `P[i2] <= P[i1]`. Once you also settle each start the first time it works, the remaining candidates form a deque with strictly increasing prefix sums.**

Restate the problem with prefix sums: find `i < j` with `P[j] - P[i] >= k` and `j - i` as small as possible. A start `i` is good when `P[i]` is low (big difference) and `i` is late (short gap). Two pruning rules follow.

**Rule 1, dominance (pop from the back).** If `i1 < i2` and `P[i1] >= P[i2]`, then for any end `j`, `P[j] - P[i2] >= P[j] - P[i1]`. So if `i1` works for `j`, `i2` works too, and `i2` gives a shorter subarray. `i1` can be deleted forever. This is exactly the rule from Sliding Window Maximum: a newer, better candidate kills an older, worse one. Here "better" means lower prefix. When a new index `j` arrives, pop every back candidate with `P >= P[j]`, then append `j`. The survivors have prefix sums **strictly increasing** from front to back.

**Rule 2, settling (pop from the front).** The front has the lowest prefix, so it is the start most likely to work for the current `j`. If `P[j] - P[front] >= k`, record `j - front`. Then pop the front. Why is that safe? Any later end `j' > j` paired with the same start gives a longer subarray, so this start has already given its best possible answer. After popping, check the new front too: several starts can be settled by the same `j`, and each later one gives a shorter answer.

```text
prefix sums as points; o = kept, x = popped by Rule 1
 P
 6 |                      o i=4
 5 |                 o i=3
 4 |
 3 |       x i=1  dominated by i=2
 2 |
 1 |            o i=2
 0 |  o i=0
   +----------------------------
      0    1    2    3    4     index

front (lowest, oldest) ... back (highest, newest)
```

Why is this still a sliding window? The front pointer only moves right (settled starts never come back), and the back only grows with newer indices. It is a window over *prefix indices* where the left edge moves for a different reason than in problem 2: not because the sum got too big, but because a start has been used up.

## Watch it work

`nums = [3, -2, 4, 1]`, `k = 5`, so `P = [0, 3, 1, 5, 6]`. The deque is written as `index:P`.

Frame 1: j = 0 and j = 1.

```text
index:  0   1   2   3   4
P:      0   3   1   5   6
j=0: push           dq [0:0]
j=1: 3-0 = 3 < 5    no settle
     3 > 0          keep back
                    dq [0:0, 1:3]
```

Nothing reaches `k` yet; the prefixes rise, so both starts are kept.

Frame 2: j = 2, a dominated start.

```text
P:      0   3   1   5   6
                ^ j
front: 1-0 = 1 < 5          no settle
back:  P[1]=3 >= 1 -> pop 1:3
                    dq [0:0, 2:1]
```

Index 1 is earlier and higher than index 2, so by Rule 1 it can never be the best start again.

Frame 3: j = 3, the first settle.

```text
P:      0   3   1   5   6
                    ^ j
front: 5-0 = 5 >= 5 -> best = 3, pop 0:0
front: 5-1 = 4 < 5  stop
back:  1 < 5 keep;  dq [2:1, 3:5]
```

The whole prefix `[3, -2, 4]` reaches 5; start 0 has now given its shortest possible answer and leaves.

Frame 4: j = 4, a shorter answer.

```text
P:      0   3   1   5   6
                        ^ j
front: 6-1 = 5 >= 5 -> best = min(3, 2) = 2
       pop 2:1
front: 6-5 = 1 < 5  stop
                    dq [3:5, 4:6]
```

Start 2 (just before `4`) pairs with end 4 to give `[4, 1]`, length 2; the loop ends and the answer is 2.

Frame 5: what the deque saved us.

```text
pairs (i, j) the brute force checks:  10
starts ever popped by Rule 1:  index 1
starts settled by Rule 2:      index 0, index 2
each index pushed once, popped at most once
```

Index 1 was never compared with ends 3 and 4, and index 0 was never compared with end 4.

Throughout, the deque held indices in increasing order with strictly increasing prefix sums, and every index that was removed was either dominated or had already produced its best answer.

## Why it is correct

We must show the true optimum `(i*, j*)` is recorded. Consider the moment the scan reaches `j*`.

First, `i*` was not removed by Rule 1. If some `i2` with `i* < i2 < j*` had `P[i2] <= P[i*]`, then `(i2, j*)` would also reach `k` and be shorter, contradicting optimality. So no index between `i*` and `j*` dominates `i*`, and Rule 1 cannot have popped it.

Second, `i*` was not settled by Rule 2 at some earlier end `j < j*`. If it had been, `P[j] - P[i*] >= k` with `j < j*`, a shorter answer, again a contradiction.

So `i*` is in the deque when `j*` arrives. Everything in front of it has a smaller prefix (the deque is increasing), so each front before it satisfies `P[j*] - P[front] > P[j*] - P[i*] >= k` and gets settled and popped, and then `i*` itself is settled, recording `j* - i*`. Every recorded value is a real valid subarray length, so the minimum recorded is the optimum.

Index `0` with `P[0] = 0` must be in the list of starts; without it, subarrays that begin at the first element are never considered.

## Cost

- Time `O(n)`: building prefix sums is one pass; each of the `n + 1` indices is appended once and popped at most once, so all `while` loops together do `O(n)` work.
- Space `O(n)`: the prefix array plus a deque that can hold up to `n + 1` indices (for an increasing array nothing is ever dominated).

The brute force is `O(n²)`. A middle option, keeping all prefixes in a sorted structure and binary-searching, is `O(n log n)`.

## Variations you will meet

- **Minimum Size Subarray Sum (problem 2).** With non-negative values, prefix sums are already increasing, so Rule 1 never fires and the deque is just a plain left pointer. This problem is that one with the dominance rule added.
- **Longest subarray with sum at least `k`.** Now you want the *farthest* start, so you keep the candidate starts that are lower than everything before them (a decreasing staircase from the left), and scan ends from the right.
- **Count or detect a subarray with sum exactly `k`.** The pairs condition is equality, not "at least", so there is no dominance; use a hash map of prefix counts (Subarray Sum Equals K).
- **Constrained Subsequence Sum.** The same back-pop dominance shows up in a DP over a window, as in the variations of Sliding Window Maximum.

## What to carry forward

When negatives break the shrinking window, move to prefix sums and keep only starts that are lower than every later start; settle the front as soon as it works, because a start never gets a better partner later. The next problem returns to a plain fixed window but asks for its median, where neither a counter nor a monotone deque is enough, and we will need two heaps that tolerate deletions.
