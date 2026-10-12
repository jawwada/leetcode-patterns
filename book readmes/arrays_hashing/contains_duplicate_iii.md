# Contains Duplicate III
*LeetCode 220 · Hard · Pattern: Sliding window of value buckets · Reading time ~9 min*

## The problem

Given an integer array nums and integers indexDiff (k) and valueDiff (t), return True if there are two distinct
indices i, j with |i - j| <= k and |nums[i] - nums[j]| <= t.

```text
Example: nums = [1,2,3,1], k = 3, t = 0 -> True (the two 1s are
  3 apart). nums = [1,5,9,1,5,9], k = 2, t = 3 -> False.
```

## What the problem is really asking

You get an array `nums` and two limits: `indexDiff` (call it `k`) and `valueDiff` (call it `t`). Is there a pair of different positions that are close in *both* senses at once: at most `k` apart in index, and at most `t` apart in value? Return True or False.

The answer is a single yes/no, but it hides two constraints of different kinds. "Close in index" is a sliding window, which you met in Contains Duplicate II. "Close in value" is new: in Contains Duplicate II we asked for *equal* values, which a hash set answers in O(1). Here we ask for *nearby* values, and a hash set cannot answer "is anything within 2 of 13?" because hashing scatters nearby numbers to unrelated places.

```text
nums = [8, 1, 15, 10, 13]    k = 2, t = 2

 idx:   0   1   2    3    4
 val:   8   1   15   10   13
        |_________|             8,10: values 2 apart but
            index 3 apart       index gap 3 > k   -> no
                 |________|
                 15,13: index 2 apart, values 2 apart -> YES
```

The pair (8, 10) is the trap: close in value, too far in index. The pair (15, 13) satisfies both.

## Do it by hand first

Walk left to right, holding a window of the last `k` values in your head. For each new value, you want to know: is anything in my window within `t` of it? With a short window you would just compare against each one. But with a long window you would do what people do with a pile of numbered cards: sort them roughly into *labelled trays*, say a tray for 0-2, a tray for 3-5, a tray for 6-8, and so on.

```text
trays: [0..2] [3..5] [6..8] [9..11] [12..14] [15..17]
window:                       10               15
new card 13 -> its tray is [12..14]
  look in [12..14]  : empty
  look in [9..11]   : 10, |13-10| = 3 > 2  no
  look in [15..17]  : 15, |13-15| = 2 <= 2 YES
```

You never had to look further than the tray of the new card and its two neighbours. What your hand kept track of was *which tray each windowed card is in*. That tray map is the seed of the data structure.

## The first honest attempt

For each `i`, compare `nums[i]` with each of the next `k` values, and return True on the first pair within `t`. O(n * k) time, O(1) space. When `k` is close to n, that is O(n^2).

```text
i=2 compares 15 with:   10  13
i=3 compares 10 with:       13  ...
i=4 compares 13 with:           ...
windows overlap in k-1 elements, but each window is
rescanned from scratch: nothing about the values in
the window is remembered between steps
```

A better middle step keeps the window in sorted order and, for each new `x`, checks only its nearest neighbours in that order (predecessor and successor): anything farther in sorted order is also farther in value. With a balanced search tree that is O(n log k). But Python has no built-in balanced tree, and insertion into a plain sorted list is O(k). The real waste is that we are paying for *exact order*, while the question only needs *approximate* order: "within t".

## The turning point

**Claim: with buckets of width t + 1, two values in the same bucket are always within t, and two values within t are always in the same or an adjacent bucket.**

Define `bucket(x) = x // (t + 1)`. Bucket `b` holds the values from `b*(t+1)` to `b*(t+1) + t`, a block of exactly `t + 1` consecutive integers. So:

- **Same bucket implies close.** Two values in one bucket differ by at most `t`. A collision is an immediate yes, no comparison needed.
- **Close implies same or adjacent.** If `|a - b| <= t`, they cannot be two buckets apart, because a whole bucket in between would force a difference of at least `t + 1`. So besides the own bucket, only buckets `b - 1` and `b + 1` can hold a partner, and there it is a "maybe", so we compare explicitly.

```text
t = 2, width 3
bucket:   ...  |  b-1  |   b   |  b+1  |  ...
values:        | 9..11 |12..14 |15..17 |
x = 13 lives in b. Anything within 2 of 13 is in 11..15,
which only touches b-1, b, b+1.
```

Why width `t + 1`? It is the *widest* width for which "same bucket implies close" still holds: a bucket of `t + 2` integers would contain two values `t + 1` apart, and a collision would be a false yes. Any narrower integer width also works for `t >= 1` (with width `t`, values exactly `t` apart still land in adjacent buckets, never two apart), but `t = 0` is a legal input, and width `t` would then mean dividing by zero. Width `t + 1` is correct for every `t >= 0`, so it is the one to remember.

Now combine with the window. Keep a dictionary from bucket id to the value living there, containing only the last `k` indices. Here is the surprise that makes it O(1): **each bucket holds at most one value**. If a second value ever arrived in an occupied bucket, we would have returned True on the spot. So the dictionary maps bucket to a single value, and evicting the element that leaves the window is a single `del` of its bucket.

One more detail: use floor division, `x // width`. For negative numbers, `int(x / width)` rounds toward zero and would merge the values -2..2 into a single bucket 0 of width 5, breaking the "same bucket implies close" rule. Python's `//` floors, so -1 goes to bucket -1 as it should.

## Watch it work

`nums = [8, 1, 15, 10, 13]`, `k = 2`, `t = 2`, width 3. The map is shown after each step.

```text
Frame 1   i=0  x=8   bucket 8//3 = 2
          check b2, b1, b3: all empty
          map {2: 8}                 window idx {0}
```
The first value just moves in.

```text
Frame 2   i=1  x=1   bucket 1//3 = 0
          check b0, b-1, b1: all empty
          map {2: 8, 0: 1}           window idx {0, 1}
```
Still nothing nearby; the window is now full (k = 2).

```text
Frame 3   i=2  x=15  bucket 15//3 = 5
          check b5, b4, b6: all empty
          insert, then evict nums[0]=8 (bucket 2)
          map {0: 1, 5: 15}          window idx {1, 2}
```
15 enters and 8 leaves, because index 0 is now too far from index 3.

```text
Frame 4   i=3  x=10  bucket 10//3 = 3
          check b3: empty; b2: empty (8 was evicted!)
                b4: empty
          insert, then evict nums[1]=1 (bucket 0)
          map {5: 15, 3: 10}         window idx {2, 3}
```
8 would have been within 2 of 10, but it left in Frame 3, which is exactly the index rule.

```text
Frame 5   i=4  x=13  bucket 13//3 = 4
          check b4: empty
                b3: 10, |13-10| = 3 > 2   no
                b5: 15, |13-15| = 2 <= 2  YES
          return True   (indices 2 and 4)
```
A neighbour bucket held a partner close enough in value, and it is in the window, so it is close in index too.

In every frame, the map held exactly the values at the previous `k` indices, one per bucket. A check never looked at more than three buckets.

## Why it is correct

The invariant: at the start of step `i`, the map is `{bucket(nums[j]) : nums[j]}` for exactly the indices `j` in `[i - k, i - 1]` (clipped at 0), and all those buckets are distinct. It holds at the start (empty map). During step `i`, if no pair was found, we insert `nums[i]` into a bucket that was empty (otherwise we would have returned), and if `i >= k` we delete the bucket of `nums[i - k]`. Because buckets are distinct, that key held exactly `nums[i - k]`, so the delete removes precisely the element leaving the window. The invariant holds for step `i + 1`.

Soundness: every True compares `x` with a value in the map, which is at most `k` indices back and within `t` (either same bucket, or checked explicitly). Completeness: take any valid pair `j < i`. At step `i`, `nums[j]` is in the map (it is within the last `k` indices) unless we already returned True earlier. Since `|nums[i] - nums[j]| <= t`, its bucket is `b`, `b - 1` or `b + 1`, all of which we check. So the pair is found.

## Cost

- **Time O(n):** each step does a constant number of dictionary operations (three lookups, one insert, one delete).
- **Space O(min(n, k)):** the map never holds more than `k` entries.

For comparison: brute force O(n * k) time, O(1) space; sorted window O(n log k) time with a balanced tree, O(k) space.

## Variations you will meet

- **t = 0 is Contains Duplicate II (219).** Width 1 means bucket = value, the neighbour checks never succeed, and the map becomes a sliding hash set of the last `k` values.
- **Unbounded k.** The window is the whole array; this is "do any two values differ by at most t", answerable by sorting and checking adjacent pairs, or by the same buckets without eviction.
- **Counting pairs instead of existence.** The one-value-per-bucket trick dies, because you can no longer stop at the first collision. You need counts per bucket plus a sorted structure (or a Fenwick tree, coming at the end of this chapter) for the neighbour buckets.
- **Nearest value in the window.** If the question is "what is the closest value", buckets give only a yes/no; a sorted container (`sortedcontainers.SortedList`, or `bisect` on a list for small k) gives predecessor and successor.

## What to carry forward

Closeness in index is a window; closeness in value is a bucket of width t + 1, and only three buckets ever need checking. Buckets answer "is something near?", but they cannot answer "how many are smaller?". The next problem, Count of Smaller Numbers After Self, asks exactly that for every element, and the tool that answers it is merge sort, counting as it merges.
