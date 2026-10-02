# Contains Duplicate II

*LeetCode 219 · Easy · Pattern: Hash map of last-seen index · Reading time ~5 min*

## What the problem is really asking

Is there a value that appears twice with the two copies at most `k` positions apart? Return True or False.

The answer is a yes/no, but the condition mixes two things: equality of values and closeness of positions. A plain
"contains duplicate" only needs a set. Here a duplicate that is too far apart does not count, so you must remember not
just that a value appeared, but where.

```text
k = 2
index:  0  1  2  3  4  5
nums:  [4, 1, 2, 4, 1, 1]
        4--------4          distance 3 > 2   no
           1--------1       distance 3 > 2   no
                    1--1    distance 1 <= 2  YES
```

## Do it by hand first

Walk along with a finger. At each number, glance back: "when did I last see this?" At index 3 you see 4, last seen at 0,
three steps ago: too far. At index 4 you see 1, last seen at 1: too far again. At index 5 you see 1, last seen at 4: one
step. Done.

What did you glance back at? Never all earlier copies, only the most recent one. If the most recent copy is too far, every
older copy is farther still. Your memory was "for each value, the last position I saw it". That is a dict from value to
index.

```text
value -> last index, at index 5:
  4 -> 3
  1 -> 4      5 - 4 = 1 <= 2
  2 -> 2
```

## The first honest attempt

For each `i`, compare `nums[i]` with the next `k` elements. Return True on any match. Time O(n * k), space O(1). With
`k` close to `n` this is quadratic.

The waste: windows of neighbouring indices overlap almost entirely, and every window is re-read from scratch. Worse,
the scan compares `nums[i]` against values that are not equal to it, when equality is something a hash table answers
instantly.

```text
k = 2
i=0: [4 | 1  2] 4  1  1
i=1:  4 [1 | 2  4] 1  1
i=2:  4  1 [2 | 4  1] 1
             ^^^^ overlap re-read each time
```

## The turning point

Claim: for each value, only its most recent earlier occurrence can matter.

Justification: suppose `v` appears at positions `p1 < p2 < i`. Then `i - p2 < i - p1`. If the nearer copy `p2` is more
than `k` away, so is `p1`. If `p1` is within `k`, so is `p2`. Either way, checking `p2` gives the same verdict as checking
every older copy. So we keep exactly one number per value.

The structure is a dict `last` from value to most recent index. At each `i`:

1. If `v` is in `last` and `i - last[v] <= k`, return True.
2. Otherwise set `last[v] = i`, overwriting.

The overwrite is not a detail; it is the algorithm. Storing the first occurrence instead (with `setdefault`) would compare
against the farthest copy and miss pairs. In our example, that would keep `1 -> 1` and see distance 4 at index 5.

There is a second valid design: keep a set of the last `k` values as a sliding window. Add `nums[i]`, and remove
`nums[i - k]` once the window exceeds size `k`. A value already in the set is a near duplicate. That uses O(min(n, k))
space. The dict version is simpler to get right; the window version is what you build on in contains duplicate III.

## Watch it work

`nums = [4, 1, 2, 4, 1, 1]`, `k = 2`.

Frame 1

```text
index:  0  1  2  3  4  5
nums:  [4, 1, 2, 4, 1, 1]
        ^  ^  ^ i = 0..2
last = {4:0, 1:1, 2:2}      all first sightings
```

Three new values; each is simply recorded.

Frame 2

```text
index:  0  1  2  3  4  5
nums:  [4, 1, 2, 4, 1, 1]
        ^        ^ i = 3    3 - last[4] = 3 - 0 = 3 > 2
last = {4:3, 1:1, 2:2}      overwrite 4 -> 3
```

4 repeats, but too far. Overwrite so the next 4 measures from here.

Frame 3

```text
index:  0  1  2  3  4  5
nums:  [4, 1, 2, 4, 1, 1]
           ^        ^ i = 4   4 - last[1] = 4 - 1 = 3 > 2
last = {4:3, 1:4, 2:2}        overwrite 1 -> 4
```

Same story for 1: a repeat, too far, overwrite.

Frame 4

```text
index:  0  1  2  3  4  5
nums:  [4, 1, 2, 4, 1, 1]
                    ^  ^ i = 5   5 - last[1] = 5 - 4 = 1 <= 2
return True
```

Because of the overwrite in Frame 3, `last[1]` is 4, not 1, and the distance is 1.

Across frames, `last[v]` was always the largest index less than `i` holding `v`. Each step did one lookup and one write.

## Why it is correct

Invariant: before processing index `i`, `last[v]` equals the largest index `j < i` with `nums[j] == v`, for every value
seen so far.

If a qualifying pair exists, take the one whose larger index `i` is smallest. At step `i`, the nearest earlier copy is at
`last[v]`, and by the turning-point argument it is within `k` whenever any earlier copy is. So the check fires at the
latest by step `i`. Conversely, every True we return names two distinct indices with equal values at distance at most
`k`, so it is never a false positive. After the check we write `last[v] = i`, which restores the invariant for `i + 1`.

## Cost

- Time: O(n). One pass, average O(1) per dict operation.
- Space: O(n) for the dict (one entry per distinct value); O(min(n, k)) with the sliding-window set.

## Variations you will meet

- **Contains Duplicate I.** No distance limit, so presence is enough: a set, or compare `len(set(nums))` with `len(nums)`.
- **Contains Duplicate III.** Values need only be within `t` of each other, not equal. Hashing by exact value fails, so
  you hash by value bucket of width `t + 1` inside the same window of `k` indices.
- **Minimum distance between equal values.** Same dict; instead of returning, record `min(i - last[v])` and keep going.
- **`k = 0`.** Two distinct indices cannot be 0 apart, so the answer is always False; the algorithm handles it naturally.

## What to carry forward

When the nearest past occurrence dominates all older ones, store only the latest index and overwrite on every sighting.
The next problem shrinks the memory even further: no dict at all, just one candidate and one counter.
