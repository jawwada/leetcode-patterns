# Longest Consecutive Sequence

*LeetCode 128 · Medium · Pattern: Hash set with sequence-start detection · Reading time ~6 min*

## What the problem is really asking

Given an unsorted array of integers, find the length of the longest set of values that form an unbroken run of
consecutive integers, like 1, 2, 3, 4. The values can appear anywhere in the array, in any order. You must run in O(n).

The answer is a length. The run lives on the number line, not in the array: positions do not matter, only which values
are present. The O(n) requirement is what makes it a real problem, because sorting would make it easy.

```text
nums = [100, 4, 200, 1, 3, 2]

number line:
  1  2  3  4  .  .  ...  100  ...  200
  #  #  #  #                #         #
  |__________|              |         |
   run of 4               run 1     run 1     -> answer 4
```

## Do it by hand first

Most people would sort the cards: 1, 2, 3, 4, 100, 200, and then read off runs. That is O(n log n), fine by hand but not
allowed here.

Try it without sorting. Put the numbers on a table where you can instantly check "is 5 here?". Now pick up 3. Is 2 here?
Yes. So 3 is in the middle of something; ignore it for now. Pick up 1. Is 0 here? No. So 1 is the bottom of a run. Count
upward: 2 yes, 3 yes, 4 yes, 5 no. Length 4.

```text
"is x-1 here?"   x=3: 2 is here -> not a start, skip
                 x=1: 0 missing -> START, walk 1,2,3,4 -> 4
```

You kept two things: a fast "is this value present" table (a set), and the rule "only count up from a value with no left
neighbour".

## The first honest attempt

For each `x`, count upward: is `x + 1` in the array, then `x + 2`, and so on. Each "in the array" check on a list is a
linear scan.

Two kinds of waste here. First, the membership scans: O(n) each. Second, every run is re-walked from every one of its
members. The run 1-2-3-4 is counted starting from 1 (4 steps), from 2 (3 steps), from 3, from 4. On an array that is one
long run, that is `n + (n-1) + ... + 1` membership checks, each O(n): O(n^3).

```text
run on the number line:  1  2  3  4
walk from 1:            [1->2->3->4]
walk from 2:               [2->3->4]     same steps again
walk from 3:                  [3->4]     and again
walk from 4:                     [4]
```

## The turning point

Fix the membership cost first: put every value in a set, so `x + 1 in values` is O(1) average. That alone brings the
brute force to O(n^2). Still too slow, because of the second waste.

Claim: every run has exactly one natural starting point, its smallest value, and it is recognisable locally: `x` is the
start of a run if and only if `x - 1` is not in the set.

Justification: if `x - 1` is present, then `x` extends a run that began further left, so any walk from `x` measures a
proper suffix of a longer run and cannot be the answer. If `x - 1` is absent, nothing lies immediately left of `x`, so
`x` is the bottom of its run.

So the algorithm: for each `x` in the set, skip it if `x - 1` is present. Otherwise walk up `x + 1, x + 2, ...` while
present, and record the length.

This has a nested loop and still runs in O(n). Here is the amortised argument from the background, in action. Charge each
probe of the inner `while` to the value it finds. Each value `v` is found only by the walk that starts at the bottom of
`v`'s run, and each run has exactly one bottom, so each value is found at most once in total. Every walk also makes one
failed probe at its end, and there is at most one walk per run, so at most `n` failed probes. Total inner work is at most
`2n`, no matter how the runs are arranged.

One more practical detail: loop over the set, not over the original array. If the array is `[1, 1, 1, 1, 2, 3, ...]`,
every copy of 1 passes the start test and re-walks the same run, which breaks the amortisation.

## Watch it work

`nums = [100, 4, 200, 1, 3, 2]`. Python happens to iterate this set as 1, 2, 3, 100, 4, 200; the algorithm does not
depend on that order.

Frame 1

```text
values = {1, 2, 3, 4, 100, 200}
number line:  1  2  3  4  ...  100  ...  200
              #  #  #  #        #         #
best = 0
```

Building the set is one O(n) pass; duplicates would collapse here.

Frame 2

```text
x = 1:  0 in values? no -> START
number line:  1  2  3  4  5
              #->#->#->#  x     walk stops at 5
length = 4    best = 4
```

1 has no left neighbour, so we walk up: 2, 3, 4 present, 5 absent.

Frame 3

```text
x = 2:  1 in values? yes -> skip
x = 3:  2 in values? yes -> skip
              1  2  3  4
              #  #  #  #
                 ^  ^  not starts: already counted from 1
best = 4
```

Two O(1) checks, no walking. This is where the brute force would have wasted 3 + 2 steps.

Frame 4

```text
x = 100: 99 in values? no -> START
         101 in values? no   length = 1   best = 4
x = 4:    3 in values? yes -> skip
```

100 is a run of its own. 4, like 2 and 3, sits inside the run from 1.

Frame 5

```text
x = 200: 199 in values? no -> START
         201 in values? no   length = 1   best = 4
return 4
```

Three starts were found (1, 100, 200), one per run, and each value was walked over exactly once.

Across frames, `best` was the longest run among the starts processed so far, and every value had been stepped on by at
most one walk.

## Why it is correct

Every maximal run of consecutive values present in the set has exactly one smallest element `s`, and `s - 1` is absent
by maximality. So the loop starts a walk at `s` exactly once. The walk steps up while values are present, and stops at the
first absent one, which is exactly one past the top of the run, so the walk measures the run's full length. Values that
are not run bottoms never start a walk, but their runs are measured from their bottoms anyway.

Since every maximal run is measured once and `best` takes the maximum, the result is the length of the longest run.

## Cost

- Time: O(n). Building the set is O(n); the outer loop does one O(1) test per distinct value; inner probes total at most
  `2n` by the amortised count.
- Space: O(n) for the set.

## Variations you will meet

- **Sort first.** O(n log n) time, O(1) extra space if sorting in place. Walk the sorted array, skipping equal neighbours
  and resetting when the gap exceeds 1. Mention it, then explain why the set version meets the O(n) requirement.
- **Union-find.** Union each `x` with `x + 1` when both are present; the largest component is the answer. Also near O(n),
  and the natural tool if values arrive as a stream and you need the answer after each insert.
- **Dict of run boundaries for a stream.** When `x` arrives, look up the run lengths ending at `x - 1` and starting at
  `x + 1`, merge, and update only the two new endpoints. O(1) per insert.
- **Binary tree longest consecutive path.** Same "extend from the previous value" logic, but along parent-child edges.

## What to carry forward

A run is determined by its bottom; test "is `x - 1` absent?" to start each run exactly once, and justify the nested loop
by charging each step to the value it lands on. The next problem returns to the two sum dict, but the values being looked
up are prefix sums, which turns "find a pair" into "count subarrays".
