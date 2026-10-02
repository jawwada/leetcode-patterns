# Find in Mountain Array

*LeetCode 1095 · Hard · Pattern: Binary search on a hidden array (peak, then two sorted halves) · Reading time ~10 min*

## What the problem is really asking

A mountain array climbs strictly to a single summit and then descends strictly. You cannot see it. You can ask for its
length, and you can ask `get(i)` for the value at index i, but at most 100 times. The array can have 10,000 elements.
Return the smallest index whose value equals the target, or -1.

```text
idx      0   1   2   3   4   5   6
arr      1   2   3   4   5   3   1
                 ^               ^
         3 at idx 2      3 at idx 5
target 3 -> 2 (the smaller index)
```

The answer is one index. Three things make it hard:

1. The budget. With 10,000 elements and 100 reads, you cannot even look at 1% of the array. Every read must eliminate a
   large region.
2. The array is not sorted. It is two sorted pieces, one going up and one going down, and you do not know where they
   meet.
3. A value can appear twice, once on each slope, and you must report the left copy.

## Do it by hand first

Take `arr = [0, 2, 4, 5, 7, 6, 3, 1]` and target 3, and pretend you are paying a coin for each look.

```text
value
  7 |             *
  6 |                *
  5 |          *
  4 |       *
  3 |                   *
  2 |    *
  1 |                      *
  0 | *
    +-------------------------
      0  1  2  3  4  5  6  7   idx
      left slope  ^  right slope
                summit
```

If you knew where the summit was, the problem would split into two problems you already know: the left slope is an
ascending sorted array, and the right slope is a descending sorted array. Search each with ordinary binary search. Search
the left slope first; if the target is there, it is automatically the smaller index, because every left-slope index is
smaller than every right-slope index.

So by hand you would do three things: find the summit, search the climb, search the descent. What you kept track of was
which slope you were on. One look at a pair of neighbours tells you that: if the right neighbour is higher, you are on the
climb.

## The first honest attempt

Call `get(i)` for `i = 0, 1, 2, ...` and stop at the first match. That is correct, and it returns the smallest index
automatically. It uses up to n calls: 10,000 when 100 are allowed. Here the brute force is not just slow, it is rejected
outright.

The waste is that each `get` returns a value that says a lot about the shape, and the scan uses it only to test equality.

```text
scan for 3 on [0, 2, 4, 5, 7, 6, 3, 1]:
get(0)=0 get(1)=2 get(2)=4 get(3)=5 get(4)=7 get(5)=6 get(6)=3
7 calls. The pair get(3)=5 < get(4)=7 alone proved that
idx 0..3 are on the climb; three of those calls were redundant.
```

A second honest attempt: "binary search the whole array for the target." It fails because the array is not sorted. At
`mid = 3` you see 5, which is bigger than 3, and ordinary binary search goes left; that finds nothing if the only 3 is on
the right slope.

## The turning point

**Claim: the question "is the ground rising after index i?" is T on the climb and F from the summit on, so the summit is
a first-F search; after that, each slope is a sorted array.**

On a mountain, `get(i) < get(i+1)` is T for every i before the summit and F for the summit and every index after it:

```text
idx      0   1   2   3   4   5   6   7
arr      0   2   4   5   7   6   3   1
up?      T   T   T   T   F   F   F   F
                         ^ first F = summit
```

This is a genuinely monotone row, unlike the previous problem's, because there is exactly one summit. The background
template finds its first F: `while lo < hi`, compare `get(mid)` with `get(mid+1)`; T means `lo = mid + 1`, F means
`hi = mid`. Since `mid < hi <= n - 1`, `mid + 1` is always a legal index.

Then two closed-window searches:

- **Left slope, `[0, peak]`, ascending.** Standard: if `get(mid) < target`, go right; if bigger, go left.
- **Right slope, `[peak + 1, n - 1]`, descending.** The direction flips: if `get(mid) < target`, the target is higher up,
  which on a descending slope means to the *left*.

The solution writes both with one helper and a flag. The decision "go right" is `(v < target) == ascending`: on an
ascending slope go right when v is too small, on a descending slope go right when v is too big. Note the right search
starts at `peak + 1`; the summit was already covered by the left search.

Two smaller ideas complete it.

**Order of searches gives the minimum index.** Search the left slope first and return immediately on a hit. Every left
index is smaller than every right index, so a hit on the left is the answer. Only if the left slope has no copy do you
search the right.

**A cache protects the budget.** The summit search reads pairs `get(mid), get(mid+1)`, and consecutive rounds often reuse
an index (in the trace below, index 4 and 5 are read twice). Wrapping `get` in a dictionary means each index is paid for
once. Later searches also reuse values the summit search already fetched.

Budget check for n = 10,000: the summit search runs about `log2(10^4) ≈ 14` rounds with at most 2 reads each, about 28;
each slope search is at most about 14 reads. Total around 56 in the worst case, comfortably under 100. The brute force
would need up to 10,000.

## Watch it work

`arr = [0, 2, 4, 5, 7, 6, 3, 1]`, target 3. Row `get` shows only the values fetched so far (`?` = never read). The T/F
row is the hidden truth that the search is uncovering. `calls` counts distinct reads.

```text
Frame 1: peak search lo=0 hi=7 mid=3
idx      0   1   2   3   4   5   6   7
get      ?   ?   ?   5   7   ?   ?   ?
up?      T   T   T   T   F   F   F   F
         L           M               H
get(3)=5 vs get(4)=7  calls=2
```

5 < 7: index 3 is on the climb, so the summit is right of it. `lo = 4`.

```text
Frame 2: peak search lo=4 hi=7 mid=5
idx      0   1   2   3   4   5   6   7
get      ?   ?   ?   5   7   6   3   ?
up?      T   T   T   T   F   F   F   F
                         L   M       H
get(5)=6 vs get(6)=3  calls=4
```

6 > 3: index 5 is on the descent. The summit is at 5 or left of it: `hi = 5`.

```text
Frame 3: peak search lo=4 hi=5 mid=4
idx      0   1   2   3   4   5   6   7
get      ?   ?   ?   5   7   6   3   ?
up?      T   T   T   T   F   F   F   F
                       L/M   H
get(4)=7 vs get(5)=6  calls=4
```

Both values were cached, so this round is free. 7 > 6: `hi = 4 = lo`. Summit at index 4.

```text
Frame 4: left slope lo=0 hi=4 mid=2
idx      0   1   2   3   4   5   6   7
get      ?   ?   4   5   7   6   3   ?
P        T   T   F   F   F   .   .   .
         L       M       H
get(2)=4  calls=5
```

Now P is "get(i) < 3" on the climb. 4 is too big, and on an ascending slope that means go left: `hi = 1`.

```text
Frame 5: left slope lo=0 hi=1 mid=0
idx      0   1   2   3   4   5   6   7
get      0   ?   4   5   7   6   3   ?
P        T   T   F   F   F   .   .   .
       L/M   H
get(0)=0  calls=6
```

0 is too small: `lo = 1`.

```text
Frame 6: left slope lo=1 hi=1 mid=1
idx      0   1   2   3   4   5   6   7
get      0   2   4   5   7   6   3   ?
P        T   T   F   F   F   .   .   .
         L/M/H
get(1)=2  calls=7
```

2 is too small: `lo = 2 > hi`. The window is empty; the climb has no 3 (it jumps from 2 to 4). Move to the descent.

```text
Frame 7: right slope lo=5 hi=7 mid=6
idx      0   1   2   3   4   5   6   7
get      0   2   4   5   7   6   3   ?
P        .   .   .   .   .   T   F   F
                             L   M   H
get(6)=3  calls=7
```

On the descent, P is "get(i) > 3", meaning "the target is still further right". `get(6)` was cached from frame 2 and
equals 3. Return 6, after 7 distinct reads. Index 7 was never read.

Across the frames, each search kept its own invariant: the summit search kept the first F of `up?` in `[lo, hi]`; each
slope search kept the target (if present on that slope) in `[lo, hi]`. The cache meant that the three searches shared
what they learned.

## Why it is correct

**Summit.** For a mountain, `get(i) < get(i+1)` holds exactly for i before the summit. The row is T...TF...F, and the
half-open template returns its first F, which is the summit. Every update keeps the first F in `[lo, hi]`, and the window
shrinks every round because `lo <= mid < hi`.

**Slopes.** Indices `[0, peak]` hold strictly increasing values, and `[peak+1, n-1]` hold strictly decreasing values. On
each, the closed-window search keeps the invariant "if the target is on this slope, its index is in `[lo, hi]`", because
monotonicity tells it which side of mid is entirely too small or too big. Since each slope is strict, a value appears at
most once per slope, hence at most twice overall.

**Minimum index.** If the target is on the left slope, the left search finds it and returns, and every right-slope index
is larger. If it is not on the left slope, the only possible copy is on the right. Either way the returned index is the
smallest.

## Cost

Time O(log n) and O(log n) calls to `get`: three binary searches, the first using up to two reads per round. Space
O(log n) for the cache, which holds only the indices actually read.

Without the cache the summit search alone could spend about 2 log n reads, still within budget at n = 10,000, but the
cache costs nothing and removes the doubt.

## Variations you will meet

- **Peak Index in a Mountain Array (LeetCode 852).** Just the first stage: the summit search.
- **Return the largest index instead.** Search the right slope first and return on a hit, then fall back to the left.
- **Bitonic array, find target (no budget).** Same three-search plan, just with direct array access.
- **Find the summit with fewer reads.** Ternary or golden-section search compare two interior points; they do not beat
  the slope test asymptotically, and the slope test is simpler to get right.
- **Plateaus (non-strict mountain).** The `up?` row stops being clean when neighbours can be equal, and the guarantee
  fails as in the peak problem's variant.

## What to carry forward

Break an unfamiliar shape into familiar sorted pieces: a mountain is a first-F search for the summit plus two textbook
searches, and the order you search them in decides which copy you return. That is the last problem where the candidates
are array positions; the next problem, Koko Eating Bananas, makes the candidates the possible answers themselves.
