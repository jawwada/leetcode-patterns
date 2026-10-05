# Maximum Subarray

*LeetCode 53 · Medium · Pattern: Greedy running sum (Kadane) · Reading time ~7 min*

## The problem

Given an integer array nums, return the largest sum of any contiguous non-empty subarray.

```text
Example: nums = [-2,1,-3,4,-1,2,1,-5,4] returns 6, from the
  subarray [4,-1,2,1].
```

## What the problem is really asking

You get a list of integers, some negative. Pick one unbroken stretch of it (at least one element long) so that the sum of
the stretch is as large as possible, and report that sum.

The answer is a single number, but behind it sits a choice of two endpoints, a start and an end. There are about `n^2 / 2`
such choices. What makes it hard is that negatives can sit inside a good stretch: in the example below the best run swallows
a `-1` because the numbers on either side of it more than pay for it. So you cannot simply "skip the negatives".

```text
index:   0   1   2   3   4   5   6
nums:  [ 2, -3,  4, -1,  2, -4,  1 ]
                 [-----------]
                  4 + -1 + 2 = 5     <- answer 5
```

## Do it by hand first

Read left to right and keep a running total, the way you would tally a bank balance.

Start with 2. Add -3: the balance is -1. Now you are about to add 4. Ask yourself: do I want to bring this -1 along? Of
course not. Any stretch that ends at the 4 is better off starting at the 4 than dragging a debt of -1 in front of it. So
you tear up the old tally and start fresh at 4. Add -1: 3. Add 2: 5, the best so far. Add -4: 1. That is still positive, so
it is still worth carrying: add 1 and you get 2, which beats starting fresh at 1.

```text
nums:     2   -3    4   -1    2   -4    1
tally:    2   -1    4    3    5    1    2
                    ^ restart (old tally -1 < 0)
best:     2    2    4    4    5    5    5
```

Your hand kept track of exactly two things: the tally of the stretch that ends where you are standing, and the best tally
you have seen at any moment. That pair is the whole algorithm.

## The first honest attempt

Try every start `i`. From each start, walk the end `j` to the right, adding `nums[j]` to a running total, and remember the
largest total seen. That is O(n^2) time and O(1) space, which is too slow at `n = 10^5`. (The truly naive version re-sums
each `(i, j)` from scratch and costs O(n^3).)

Where is the waste? Look at all the stretches that end at index 4. The brute force computes each of them separately, once
for each start, even though they share almost everything:

```text
ending at j = 4 (value 2):
  start 0:  2 -3  4 -1  2   = 4
  start 1:    -3  4 -1  2   = 2
  start 2:        4 -1  2   = 5   <- best ending at 4
  start 3:          -1  2   = 1
  start 4:              2   = 2
            ^^^^ every row re-adds the same tail; only the
                 choice of start differs
```

Every one of those rows is "some prefix glued in front of the tail `[..., 2]`". The rows differ only in which prefix gets
glued on, and the brute force never notices that the best prefix to glue on was already decided one step earlier.

## The turning point

Claim: the best stretch ending at `j` is either `nums[j]` alone, or the best stretch ending at `j - 1` with `nums[j]`
appended. Nothing else can win.

Why? Any stretch ending at `j` that is longer than one element is "a stretch ending at `j - 1`, plus `nums[j]`". The plus
`nums[j]` part is the same for all of them, so the best of them uses the best stretch ending at `j - 1`. The only other
candidate is the one-element stretch `[nums[j]]`.

So between steps you carry a single number `cur`, the best sum of a stretch ending exactly here, and update it with:

```python
cur = max(x, cur + x)    # extend, or restart at x
best = max(best, cur)
```

Read the `max` greedily: extend only if the carried sum helps, which means only if `cur > 0`. A negative carried sum is dead
weight; any stretch that kept it would be better without it. That is the greedy rule "drop a negative prefix and never look
back". Nothing to the right of the drop can make you regret it, because the dropped prefix was negative and would subtract
from every future stretch that included it.

The second variable, `best`, exists because the answer does not have to end at the last index. The best stretch can end
anywhere; we read the maximum of `cur` over all positions.

## Watch it work

`nums = [2, -3, 4, -1, 2, -4, 1]`. Start with `cur = best = 2`.

Frame 1

```text
index:   0   1   2   3   4   5   6
nums:  [ 2, -3,  4, -1,  2, -4,  1 ]
             ^ x = -3
extend: 2 + -3 = -1   restart: -3   -> cur = -1
best = 2
```

Extending beats restarting, but the carried sum is now negative.

Frame 2

```text
nums:  [ 2, -3,  4, -1,  2, -4,  1 ]
                 ^ x = 4
extend: -1 + 4 = 3    restart: 4    -> cur = 4
best = 4               (stretch [4])
```

The -1 debt is dropped: the stretch restarts at index 2.

Frame 3

```text
nums:  [ 2, -3,  4, -1,  2, -4,  1 ]
                     ^ x = -1
extend: 4 + -1 = 3    restart: -1   -> cur = 3
best = 4               (stretch [4, -1])
```

The -1 is swallowed because the carry (4) is still positive.

Frame 4

```text
nums:  [ 2, -3,  4, -1,  2, -4,  1 ]
                         ^ x = 2
extend: 3 + 2 = 5     restart: 2    -> cur = 5
best = 5               (stretch [4, -1, 2])
```

The swallowed -1 paid off: this is the answer.

Frame 5

```text
nums:  [ 2, -3,  4, -1,  2, -4,  1 ]
                             ^ x = -4
extend: 5 + -4 = 1    restart: -4   -> cur = 1
best = 5
```

The carry drops but stays positive, so it is still worth keeping.

Frame 6

```text
nums:  [ 2, -3,  4, -1,  2, -4,  1 ]
                                 ^ x = 1
extend: 1 + 1 = 2     restart: 1    -> cur = 2
best = 5   -> return 5
```

Extending a positive carry beats restarting; the best never moves again.

Across every frame, `cur` was the best sum of a stretch ending exactly at the pointer, and `best` was the best sum of any
stretch ending at or before it. A restart happened only when the carry entering a step was negative (Frame 2).

## Why it is correct

The invariant: after processing index `j`, `cur` equals the maximum sum over all stretches that end exactly at `j`, and
`best` equals the maximum over all stretches that end anywhere in `[0, j]`.

It holds at `j = 0`: the only stretch ending at 0 is `[nums[0]]`, and we set both to `nums[0]`.

Suppose it holds at `j - 1`. Every stretch ending at `j` is either `[nums[j]]` or (a stretch ending at `j - 1`) +
`nums[j]`. The best of the second kind is `cur_old + nums[j]` by the invariant. So `max(nums[j], cur_old + nums[j])` is the
best stretch ending at `j`, which is exactly the update. Then `best` takes the max of its old value (best ending before `j`)
and the new `cur` (best ending at `j`), so it covers everything ending in `[0, j]`. At `j = n - 1`, `best` is the answer.

In exchange-argument language: suppose an optimal stretch starts with a prefix whose sum is negative. Swap that stretch
for the same stretch with the prefix removed. It is still contiguous, still non-empty, and its sum went up. So some
optimal stretch never begins with a negative-sum prefix, which is precisely the kind of stretch the restart rule produces.

## Cost

- **Time O(n):** one pass, two `max` calls per element.
- **Space O(1):** two integers, `cur` and `best`.

The brute force is O(n^2) time with a running total (O(n^3) without), O(1) space.

## Variations you will meet

- **Return the subarray, not the sum.** Remember the index where `cur` last restarted; when `best` improves, record that
  start and the current index as the answer's endpoints.
- **Circular array (LeetCode 918).** The best wrap-around stretch is "total minus the minimum stretch in the middle", so
  run Kadane twice (once for max, once for min). If every number is negative, the min stretch is the whole array; fall back
  to the plain max.
- **Maximum product subarray (LeetCode 152).** Multiplication does not have the "negative prefix is dead weight" property:
  a negative times a negative is positive. The next problem fixes this by carrying two numbers.
- **Divide and conquer follow-up.** Split in half; the answer is in the left, the right, or crosses the middle (best suffix
  of left plus best prefix of right). O(n log n), and the same four summaries make it a segment-tree problem when the
  array receives point updates.

## What to carry forward

A running sum that goes negative is a debt no future stretch wants: drop it, restart at the next element, and record the
highest point reached. The next problem keeps the same one-pass carry but has to carry the worst value as well as the best,
because a negative number swaps them.
