# Top K Frequent Elements

*LeetCode 347 · Medium · Pattern: Frequency count + bucket sort · Reading time ~6 min*

## What the problem is really asking

Given an integer array and a number `k`, return the `k` values that occur most often, in any order. The answer is
guaranteed unique, so there is never a tie at the cut-off.

The answer is a set of `k` values. The work splits into two parts: counting how often each value appears, which is easy,
and selecting the top `k` by count, which is where the interesting choice lies. Sorting gets you O(n log n); the follow-up
asks you to beat that.

```text
nums = [4, 1, 4, 2, 1, 4, 3]     k = 2

value:  4    1    2    3
count:  3    2    1    1
        ^^^^^^^^^ top 2 -> [4, 1]
```

## Do it by hand first

You would tally first. Read the array once, making tick marks next to each value. Then look at the tallies and pick the
biggest.

```text
4: |||
1: ||
2: |
3: |
```

How do you "pick the biggest" by eye? You don't sort the rows; you look for the longest row of ticks, then the next.
Someone used to counting might go further: write the counts as column headings 1, 2, 3 and drop each value under its
count. Then just read from the highest heading down.

```text
count:   1     2     3
        [2 3] [1]   [4]     read right to left: 4, 1
```

You kept two things: a tally per value (a dict), then a shelf per count (an array indexed by count). The second is bucket
sort.

## The first honest attempt

Count with a `Counter`, sort the distinct values by count descending, take the first `k`. Time O(n log n) in the worst
case (all values distinct), space O(n).

This is a perfectly good first answer and the right thing to say aloud. The waste is that sorting fully orders every
distinct value, including all the ones below the cut-off. We need the top `k`, and we are paying to rank the bottom
`n - k` too.

```text
sorted by count:  4(3)  1(2)  2(1)  3(1)
                  ^^^^^^^^^^  ^^^^^^^^^^
                  needed      ranked anyway, then thrown away
```

## The turning point

Claim: the sort keys are frequencies, and every frequency is an integer between 1 and `n`. Keys from a small known range
can be used directly as array indices, which sorts by placement instead of by comparison.

Justification: a value cannot appear more than `n` times or fewer than once. So make an array `buckets` of `n + 1` lists
(index 0 unused, index `n` for a value that fills the whole array). For each `(value, count)`, append `value` to
`buckets[count]`. Now position in the array is the frequency. Walking the array from index `n` down to 1 visits values in
non-increasing frequency, with no comparisons. Stop as soon as you have collected `k`.

This is the background's bucket sort: when keys are small integers, shelves beat comparisons. The comparison-sort lower
bound of `n log n` applies only to algorithms that learn about order by comparing; bucket sort learns it by indexing.

```text
memory after bucketing (n = 7):
index:   0    1      2    3    4    5    6    7
       [ [] [2,3]  [1]  [4]   []   []   []   [] ]
                                             ^ sweep starts here
```

Why `n + 1` and not `n`? Because a count can equal `n` (an array of one repeated value). Index `n` must exist.

There is a middle ground worth naming: a min-heap of size `k`, keyed by count. Push each `(count, value)`; if the heap
exceeds `k`, pop the smallest. That is O(n log k), it works for streams, and it is the answer when you cannot afford
`n + 1` buckets. When `k` is close to `n`, quickselect on the counts gives average O(n) too.

## Watch it work

`nums = [4, 1, 4, 2, 1, 4, 3]`, `k = 2`, `n = 7`.

Frame 1

```text
nums:  [4, 1, 4, 2, 1, 4, 3]
freq = {4:3, 1:2, 2:1, 3:1}
```

One pass of `Counter` tallies each value. Four distinct values.

Frame 2

```text
for (value, count) in freq:
  4 -> buckets[3]   1 -> buckets[2]
  2 -> buckets[1]   3 -> buckets[1]

index:   0    1      2    3    4..7
       [ [] [2,3]  [1]  [4]   [] ... ]
```

Each distinct value is dropped on the shelf named by its count.

Frame 3

```text
sweep count = 7, 6, 5, 4:  empty buckets
index:   0    1      2    3    4    5    6    7
       [ [] [2,3]  [1]  [4]   []   []   []   [] ]
                                ^----^----^----^ skipped
result = []
```

The highest shelves are empty; the sweep passes them in O(1) each.

Frame 4

```text
count = 3: take 4         result = [4]
count = 2: take 1         result = [4, 1]   len == k
index:   0    1      2    3
       [ [] [2,3]  [1]  [4] ... ]
                    ^    ^
return [4, 1]
```

We stop as soon as `k` values are collected; shelf 1 is never read.

Across frames, `buckets[f]` held exactly the values with frequency `f`, and the sweep only ever moved downward, so the
result was always the most frequent values seen so far in non-increasing order.

## Why it is correct

After bucketing, every distinct value sits in exactly one bucket, the one equal to its count. The sweep visits buckets
from `n` down to 1, so it emits values in non-increasing order of frequency. The first `k` values emitted are therefore
`k` values whose frequencies are at least as large as every value not emitted. Because the problem guarantees the top `k`
is unique, there is no tie at the boundary that could make a different set equally valid, and stopping at exactly `k`
gives the answer.

## Cost

- Bucket sort: O(n) time. Counting is one pass, bucketing touches each distinct value once, and the sweep touches `n + 1`
  buckets and at most `k` values. O(n) space for the counter and the buckets.
- Heap of size `k`: O(n log k) time, O(n + k) space.
- Full sort: O(n log n) time, O(n) space.

## Variations you will meet

- **Top K Frequent Words.** Ties are now broken alphabetically and the output must be ordered. Buckets still work (sort
  each bucket's words), but a heap with key `(-count, word)` or a size-k heap with a reversed word comparison is common.
- **Sort Characters By Frequency.** Same buckets, but output every value, repeated `count` times, from the top shelf
  down.
- **K-th largest element.** No counting; the values themselves are the keys. Bucket only if values are in a small range;
  otherwise a size-k heap or quickselect.
- **Stream of values.** You cannot bucket a moving target cheaply; keep counts in a dict and a heap (with lazy deletion),
  or a count-to-values structure like the one in "All O(1) Data Structure".

## What to carry forward

When the keys you would sort by are small bounded integers, use them as indices instead: count, shelve by count, sweep
from the top. The next problem is another "every position needs an aggregate of the others" question, solved by
accumulating from the left and from the right instead of recomputing.
