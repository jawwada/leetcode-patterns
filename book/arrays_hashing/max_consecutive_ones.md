# Max Consecutive Ones

*LeetCode 485 · Easy · Pattern: Running counter with reset · Reading time ~4 min*

## What the problem is really asking

The array holds only 0s and 1s. Return the length of the longest unbroken run of 1s.

The answer is one number, a length. Nothing here is hard to compute; the lesson is how little you need to remember to
compute it. It is the purest example of a running accumulator, the idea behind prefix sums, Kadane's algorithm and
sliding windows.

```text
index:  0  1  2  3  4  5
nums:  [1, 1, 0, 1, 1, 1]
        |__|     |_____|
        run 2    run 3     -> answer 3
```

## Do it by hand first

Read left to right and count out loud. "One, two, ... zero, start over. One, two, three." Each time you say a number you
compare it with the biggest number you have said so far.

```text
nums:     1  1  0  1  1  1
you say:  1  2  0  1  2  3
biggest:  1  2  2  2  2  3
```

You kept track of two things: the count you are currently saying, and the largest you have said. A 0 resets the first;
nothing ever lowers the second. That is the whole data structure: two integers.

## The first honest attempt

For every start index `i`, walk right while the element is 1 and record how far you got. Take the maximum. Time O(n^2)
in the worst case (an array of all 1s), space O(1).

The waste is easy to see. A run of `r` ones is walked once from each of its `r` starting positions. The tail of the run
is counted over and over.

```text
start 3:  1 1 0 [1 1 1]    walk 3
start 4:  1 1 0  1[1 1]    walk 2  (same 1s again)
start 5:  1 1 0  1 1[1]    walk 1  (and again)
```

## The turning point

Claim: the length of the run ending at index `j` depends only on the length of the run ending at `j - 1`.

Specifically, `run(j) = run(j - 1) + 1` if `nums[j] == 1`, and `run(j) = 0` if `nums[j] == 0`. A 0 is a wall: no run can
cross it, so everything before it is irrelevant to what comes after. Between walls, the run grows by exactly one per step.

So instead of starting a fresh walk at each index, carry one integer `run` left to right. Then the answer is the largest
value `run` ever takes, which a second integer `best` records.

```python
run = run + 1 if x == 1 else 0
best = max(best, run)
```

The placement of the `best` update matters. If you only update `best` when you hit a 0 (the moment a run "ends"), a run
that reaches the end of the array never gets recorded, and `[0, 1, 1]` returns 0. Updating inside the run, every time it
grows, avoids that.

Why "ending at `j`" and not "starting at `j`"? Because we read left to right. When we stand at `j`, we know everything
to the left and nothing to the right, so a quantity defined by what ends here is computable now. This framing reappears
in maximum subarray, longest increasing subsequence and most one-dimensional DP.

## Watch it work

`nums = [1, 1, 0, 1, 1, 1]`.

Frame 1

```text
index:  0  1  2  3  4  5
nums:  [1, 1, 0, 1, 1, 1]
        ^  ^ j
run = 2   best = 2
```

Two 1s; `run` climbs to 2 and `best` follows it.

Frame 2

```text
index:  0  1  2  3  4  5
nums:  [1, 1, 0, 1, 1, 1]
              ^ j  (wall)
run = 0   best = 2
```

The 0 resets `run`. `best` keeps 2.

Frame 3

```text
index:  0  1  2  3  4  5
nums:  [1, 1, 0, 1, 1, 1]
                 ^  ^ j
run = 2   best = 2
```

A new run starts; it ties the old best but does not beat it.

Frame 4

```text
index:  0  1  2  3  4  5
nums:  [1, 1, 0, 1, 1, 1]
                       ^ j  (array ends)
run = 3   best = 3   -> return 3
```

The run reaches the end; because `best` updated inside the run, the trailing 3 is counted.

In every frame, `run` was the length of the run of 1s ending exactly at `j`, and `best` was the largest such length up to
`j`.

## Why it is correct

Invariant after processing index `j`: `run` is the number of consecutive 1s ending at `j` (0 if `nums[j]` is 0), and
`best` is the maximum of `run` over indices `0..j`.

Base: before any index, both are 0. Step: the recurrence from the turning point gives the new `run` exactly, and taking
`max(best, run)` extends the maximum by one more index. Every run of 1s ends at some index, and at that index `run` equals
its full length, so `best` sees every run's length. After the last index, `best` is the maximum over all runs.

## Cost

- Time: O(n). One pass.
- Space: O(1). Two integers.

## Variations you will meet

- **Max Consecutive Ones II (flip at most one 0).** Keep two counters: run length with no flip, and run length with one
  flip used. Or think of it as a window allowed to contain one 0.
- **Max Consecutive Ones III (flip at most k zeros).** The wall is no longer a single 0. Use a sliding window that holds at
  most `k` zeros and shrink from the left when it holds more.
- **Maximum subarray (Kadane).** Replace "+1 on a 1, reset on a 0" with "add the value, and reset when the running sum
  goes negative". Same carried-state shape.
- **Longest run of any repeated character.** Reset when the current element differs from the previous one.

## What to carry forward

Define the state as "best thing ending here" and carry it forward, updating the global best inside the loop, not at the
walls. The next problem goes back to sets, but runs 27 of them at once and needs a little arithmetic to route each cell to
the right ones.
