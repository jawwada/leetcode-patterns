# Majority Element

*LeetCode 169 · Easy · Pattern: Boyer-Moore voting · Reading time ~5 min*

## The problem

Given an array of size n, return the element that appears more than n / 2 times; a majority element always exists.
Follow-up: O(n) time and O(1) space.

```text
Example: nums = [2, 2, 1, 1, 1, 2, 2] -> 2.
```

## What the problem is really asking

One value fills more than half of the array. Find it. The follow-up asks for O(n) time and O(1) extra space.

The answer is a single value. With a Counter this is trivial, so the real question is the follow-up: can you find the
winner without keeping a tally for every candidate? "More than half" is the lever. It is a very strong promise, and the
solution exists only because of it.

```text
nums = [2, 2, 1, 1, 1, 2, 2]     n = 7, majority needs > 3
count:  2 -> 4 times   1 -> 3 times
answer: 2
```

## Do it by hand first

Imagine each number is a person in a room, wearing a shirt with their number. Tell them: "find anyone wearing a different
number than you, and both of you leave the room together." Keep doing that until no such pair exists.

```text
start:   2 2 2 2   1 1 1
pair:    2-1  2-1  2-1      three pairs leave
left:    2                  only 2s can remain
```

The 2s have four people, the 1s have three. Every pair removes at most one 2. Since the 2s outnumber everyone else
combined, someone wearing 2 is left over. What you kept track of was not a count per value, just "who is currently
unpaired and how many of them". That is the seed: one candidate, one count.

## The first honest attempt

For each element, count its occurrences with a full scan; return it once the count exceeds `n / 2`. Time O(n^2), space
O(1). The waste: the same value is recounted from scratch every time it reappears, and values that could never win are
counted too.

The natural fix is a `Counter`: one pass, O(n) time, but O(n) space. Sorting also works (the middle element of a sorted
array must be the majority) at O(n log n). Neither meets the follow-up.

```text
scan for v=2:  [2 2 1 1 1 2 2]  -> 4
scan for v=2:  [2 2 1 1 1 2 2]  -> 4   again
scan for v=1:  [2 2 1 1 1 2 2]  -> 3
scan for v=1:  [2 2 1 1 1 2 2]  -> 3   again ...
```

## The turning point

Claim: if you repeatedly cancel two different values against each other, the majority value is never fully cancelled.

Justification: each cancellation removes two elements with different values, so it removes at most one copy of the
majority value `m`. Let `c` be the number of copies of `m` and `n - c` the rest. Every cancellation that removes an `m`
also removes a non-`m`, so at most `n - c` copies of `m` can ever be removed. Since `c > n - c`, at least one copy survives.

Boyer-Moore streams that cancellation with two variables:

- `candidate`: the value of the currently unpaired people.
- `count`: how many of them there are.

For each `v`: if `count` is 0, nobody is unpaired, so `v` becomes the candidate. Then if `v == candidate`, `count` goes
up (another unpaired person of the same kind); otherwise it goes down (`v` pairs off with one of them and both leave).

The subtle part is that `count == 0` in the middle is normal. It means the prefix so far cancelled perfectly, not that the
majority "lost". The prefix that cancelled to zero contains at most half majority copies, so the majority still holds
more than half of what remains, and the same argument applies to the suffix.

## Watch it work

`nums = [2, 2, 1, 1, 1, 2, 2]`.

Frame 1

```text
nums:  [2, 2, 1, 1, 1, 2, 2]
        ^  ^
candidate = 2   count = 2       unpaired: 2 2
```

The first 2 starts a candidacy (count was 0); the second adds to it.

Frame 2

```text
nums:  [2, 2, 1, 1, 1, 2, 2]
              ^  ^
candidate = 2   count = 0       pairs: (2,1) (2,1)
```

Each 1 cancels one 2. The prefix `[2,2,1,1]` cancelled out completely.

Frame 3

```text
nums:  [2, 2, 1, 1, 1, 2, 2]
                    ^  ^
candidate = 1   count = 0       1 took over, then (1,2)
```

With count 0, the third 1 becomes candidate (count 1). The next 2 cancels it back to 0.

Frame 4

```text
nums:  [2, 2, 1, 1, 1, 2, 2]
                          ^
candidate = 2   count = 1       return 2
```

Count is 0 again, so the last 2 becomes candidate and is the survivor.

What stayed true in every frame: the elements processed so far split into cancelled pairs of different values plus
`count` unpaired copies of `candidate`.

## Why it is correct

Invariant: after processing a prefix, that prefix can be partitioned into pairs of unequal values plus exactly `count`
copies of `candidate`.

It holds at the start (empty prefix, count 0). Each step keeps it: a matching `v` joins the unpaired group; a mismatched
`v` pairs with one unpaired copy; when count is 0, `v` starts a new unpaired group.

At the end, the whole array is pairs-of-unequal-values plus `count` copies of `candidate`. Each pair contains at most one
copy of the majority `m`, so the pairs hold at most half the array's elements as `m`. Since `m` fills more than half, some
copy of `m` must be among the unpaired ones, and the unpaired ones are all `candidate`. So `candidate == m`.

## Cost

- Time: O(n). One pass.
- Space: O(1). Two scalars.

## Variations you will meet

- **No guarantee a majority exists.** The voting still returns some candidate, possibly wrong. Add a second pass that
  counts the candidate and checks `> n / 2`.
- **Majority Element II (more than n/3).** At most two such values exist. Keep two candidates and two counts; a value
  matching neither decrements both. Verify both with a second pass.
- **Online majority in a subarray.** Many range queries: store each value's positions and binary search, or use a segment
  tree whose merge is the Boyer-Moore merge.

## What to carry forward

When the question asks only for a winner, not the tallies, a single candidate plus a counter can replace the whole table;
cancellation is safe because the majority outnumbers everything else combined. The next problem uses the same tiny
memory, a single running count, but resets it at walls instead of cancelling.
