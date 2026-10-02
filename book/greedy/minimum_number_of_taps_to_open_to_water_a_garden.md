# Minimum Number of Taps to Open to Water a Garden

*LeetCode 1326 · Hard · Pattern: Greedy reach (furthest reachable index) · Reading time ~10 min*

## What the problem is really asking

A garden is the stretch of number line from 0 to `n`. There is a tap at every integer point `i` in `[0, n]`, and tap `i`
waters the interval `[i - ranges[i], i + ranges[i]]`. Open as few taps as possible so that every point of `[0, n]` is
wet, or report -1 if even opening all of them leaves a dry patch.

The answer is a count, but behind it is a choice of a subset of intervals whose union covers `[0, n]`. This is the classic
interval covering problem dressed up with taps. Two things make it hard. First, there are `2^(n+1)` subsets. Second, the
input is not given as intervals sorted in any useful order; it is given as centres and radii, so the structure you need
(where each interval starts) is hidden.

```text
n = 7, ranges = [1, 2, 1, 0, 2, 1, 0, 1]

garden:   0   1   2   3   4   5   6   7
          |---|---|---|---|---|---|---|
tap 1:  [=========]                      [-1, 3]
tap 4:          [===============]        [ 2, 6]
tap 7:                          [=======]  [6, 8]
          answer 3: taps 1, 4, 7 cover [0, 7]
```

Watering "a point" means covering the continuous segment, so two intervals that merely touch, like `[0, 3]` and `[3, 6]`,
together cover `[0, 6]`. Tap 3 with range 0 covers only the single point 3, which waters nothing of any length.

## Do it by hand first

Put the garden on paper and walk from the left edge. Point 0 must be wet, so some tap covering 0 must be open. Which one?
Among the taps whose interval contains 0, you would naturally pick the one that reaches furthest right: tap 0 reaches 1,
tap 1 reaches 3. Take tap 1. Now `[0, 3]` is wet.

The next dry point is just right of 3. Which taps help? Any tap whose interval starts at or before 3 and ends after 3.
Tap 2 ends at 3 (useless), tap 4 starts at 2 and ends at 6, tap 5 starts at 4 (too late, it would leave a dry gap
between 3 and 4). Take tap 4. Now `[0, 6]` is wet. From 6, tap 7 starts at 6 and reaches 8. Take it. Three taps.

```text
wet so far      candidates (start <= wet edge)   pick
[0, 0]          tap0 ->1, tap1 ->3               tap 1
[0, 3]          tap2 ->3, tap4 ->6, tap3 ->3     tap 4
[0, 6]          tap5 ->6, tap6 ->6, tap7 ->8     tap 7
[0, 8] covers [0, 7]: 3 taps
```

Your hand kept one number, the right edge of the wet prefix, and for each candidate tap it asked one question: how far
right can it push that edge? That is the Jump Game frontier wearing a disguise.

## The first honest attempt

Enumerate subsets of taps in increasing size, and for each, check whether the union of their intervals covers `[0, n]`.
The first size that works is the answer. That is O(2^(n+1) * n) time; the repo's brute force does exactly this and is
only usable for `n` up to about 15.

A better honest attempt is the textbook interval covering greedy: convert each tap to `[max(0, i - r), i + r]`, sort by
left end, then repeatedly take, among intervals starting at or before the current wet edge, the one reaching furthest.
That is O(n log n) and correct. But it is worth seeing why plain subsets are wasteful first, because the waste tells you
what the greedy can ignore:

```text
subsets that contain tap 1 and tap 4:
  {1, 4, 7}          covers
  {1, 4, 7, 0}       covers  } tap 0's interval [0, 1]
  {1, 4, 7, 2}       covers  } lies inside tap 1's;
  {1, 4, 7, 0, 2}    covers  } it never changes anything
  ...
```

Most taps are dominated: their interval sits inside another tap's interval that starts no later. Subset search checks
every combination of dominated taps anyway.

It is also worth trying a tempting wrong greedy, because it fails in an instructive way: "open the tap that waters the
most still-dry ground, repeat". On `n = 8` with taps at 2, 4 and 6 of ranges 2, 3 and 2, tap 4 waters `[1, 7]`, the
widest, so this rule opens it first; then the ends `[0, 1]` and `[7, 8]` need taps 2 and 6, three in total. The answer is
two (taps 2 and 6 meet at 4). Wide in the middle is not what matters. What matters is how far you get past the dry point
on the left.

## The turning point

Claim: when everything left of position `p` is wet and `p` is the leftmost point that still needs covering, you lose
nothing by opening, among taps whose interval starts at or before `p`, the one whose interval ends furthest right.

That is the interval covering greedy, and the exchange argument for it is short (see "Why it is correct"). The second
observation turns it from O(n log n) into O(n): you never needed to sort. Left ends are integers in `[0, n]`, so you can
bucket. For each left end `l`, store

```python
reach[l] = max(reach[l], i + ranges[i])  # l = max(0, i - r)
```

the furthest right end of any tap starting at `l`. Clamping at 0 matters: a tap at `i = 1` with range 2 starts at -1,
which is the same as starting at 0 for a garden that begins at 0, and in Python `reach[-1]` would silently write to the
last slot.

Now read `reach` as a jump array. "Standing at position `l`, one more tap takes you to `reach[l]`." Covering `[0, n]` with
the fewest taps is reaching index `n` with the fewest jumps. That is Jump Game II, with two changes:

- Some positions have no tap starting there, so `reach[l]` is 0 (or less than `l`); the scan must handle "no progress".
- The garden may be uncoverable. At a round boundary `i == cur_end`, if `farthest <= i`, no tap starting anywhere in the
  wet prefix gets past `i`, so the stretch just right of `i` stays dry forever. Return -1, and check this BEFORE counting
  the tap.

As in Jump Game II, scan `i` only in `range(n)`: position `n` itself is the goal, not a place you must leave.

## Watch it work

`n = 7`, `ranges = [1, 2, 1, 0, 2, 1, 0, 1]`.

Frame 1

```text
tap i:    0     1    2    3    4    5    6    7
interval [-1,1][-1,3][1,3][3,3][2,6][4,6][6,6][6,8]
clamped  [0,1] [0,3] [1,3][3,3][2,6][4,6][6,6][6,8]

l:        0  1  2  3  4  5  6  7
reach:  [ 3, 3, 6, 3, 6, 0, 8, 0 ]
```

Bucketing by clamped left end: tap 1 wins bucket 0, tap 4 bucket 2, tap 7 bucket 6.

Frame 2

```text
l:        0  1  2  3  4  5  6  7
reach:  [ 3, 3, 6, 3, 6, 0, 8, 0 ]
          ^ i=0 = cur_end(0)   farthest = 3
wet:     [0]                   3 > 0 -> taps = 1, cur_end = 3
```

Point 0 is the end of the empty wet prefix: open the best tap starting at 0 (tap 1).

Frame 3

```text
reach:  [ 3, 3, 6, 3, 6, 0, 8, 0 ]
             ^  ^ i=1, 2        farthest = max(3, 3, 6) = 6
wet:     [0========3]           i < cur_end: keep scanning
taps = 1
```

Tap 4, starting at 2 inside the wet prefix, is noted as the best next tap.

Frame 4

```text
reach:  [ 3, 3, 6, 3, 6, 0, 8, 0 ]
                   ^ i=3 = cur_end(3)   farthest = 6
wet:     [0========3]           6 > 3 -> taps = 2, cur_end = 6
```

The scan hits the wet edge; open the remembered tap and the edge jumps to 6.

Frame 5

```text
reach:  [ 3, 3, 6, 3, 6, 0, 8, 0 ]
                      ^  ^ i=4, 5   farthest = max(6, 6, 0) = 6
wet:     [0=================6]  i < cur_end: keep scanning
taps = 2
```

Nothing starting at 4 or 5 reaches past 6; bucket 5 is empty.

Frame 6

```text
reach:  [ 3, 3, 6, 3, 6, 0, 8, 0 ]
                            ^ i=6 = cur_end(6)  farthest = 8
wet:     [0=================6]  8 > 6 -> taps = 3, cur_end = 8
loop ends at i = 6 (range(7)) -> return 3
```

Tap 7 reaches 8, past the end of the garden, and the scan stops before position 7.

Frame 7 (a failing garden: `n = 5`, `ranges = [0, 1, 0, 0, 1, 0]`)

```text
l:        0  1  2  3  4  5
reach:  [ 2, 0, 2, 5, 0, 5 ]
i=0: farthest 2, taps = 1, cur_end = 2
i=2 = cur_end: farthest = 2 <= 2 -> return -1
wet:     [0=====2] . [3=====5]    gap (2, 3) stays dry
```

The impossibility check fires at a round boundary, before a tap is counted.

Across all frames, `[0, cur_end]` was exactly the ground coverable by `taps` taps, and `farthest` was the furthest right
end of any tap starting inside the scanned part of it. Taps 0, 2, 3, 5 and 6 were never named; their buckets lost to
dominating taps or offered nothing new.

## Why it is correct

**The exchange argument for the choice.** Let `p` be the leftmost point not yet covered by the taps opened so far
(everything in `[0, p]` is wet, and we need to get past `p`). Greedy opens tap `g`: among taps with left end `<= p`, the
one with the largest right end. Take any optimal solution that agrees with greedy so far. It must contain some tap `o`
covering the stretch just right of `p`, so `o` starts at or before `p`. By the choice of `g`, `right(g) >= right(o)`.

```text
          p
 wet  ====|
 g      [=|==========]        right(g) >= right(o)
 o    [===|======]
            swap o -> g: everything o covered right of p,
            g covers too; left of p was wet already
```

Replace `o` with `g` in the optimal solution. Left of `p` nothing changes (it was wet before either tap). Right of `p`,
`g` covers everything `o` covered, because both start at or before `p` and `g` ends no earlier. So the new set still
covers the garden and has the same size. It is still optimal and now agrees with greedy on one more choice. Repeat, and
the optimal solution becomes greedy's.

**The invariant for the scan.** At a round boundary, `cur_end` is the furthest point coverable by `taps` taps, and
`farthest` is the maximum of `reach[l]` over every `l` in `[0, cur_end]`, which is the right end of exactly the tap the
exchange argument says to open. So each round opens the greedy tap without ever naming it.

**Why -1 is right.** If at a boundary `farthest <= i = cur_end`, then every tap that starts inside the wet prefix ends at
or before `cur_end`, and every tap starting further right leaves the stretch just after `cur_end` uncovered. No subset of
taps can water it.

## Cost

- **Bucketed scan (this solution).** Time O(n): one pass over the taps to fill `reach`, one Jump Game II scan. Space O(n)
  for the `reach` array.
- **Sort-based interval covering.** Time O(n log n) for the sort, O(n) for the sweep; space O(n) for the intervals.
- **Subset brute force.** Time O(2^(n+1) * n), space O(n).

An O(n^2) DP (`dp[x]` = fewest taps covering `[0, x]`, relaxing every tap over its range) is also a common first answer;
it is correct but discards the greedy structure.

## Variations you will meet

- **Video Stitching (LeetCode 1024).** Clips `[start, end]` must cover `[0, time]`. Identical after bucketing clips by
  start; the only difference is that the intervals come ready-made instead of as centre and radius.
- **Jump Game II (LeetCode 45).** This problem with `reach[i] = i + nums[i]` and the end guaranteed reachable. If an
  interviewer asks you to relate the two, the bucketing step is the whole answer.
- **Minimum number of arrows / interval point cover.** A different covering problem (points hitting intervals rather
  than intervals covering a line). It sorts by right end instead of left end; the exchange argument picks the rightmost
  point instead of the furthest-reaching interval.
- **Real-valued positions.** If centres and radii are not integers, you cannot bucket; fall back to the sort-by-left-end
  sweep, which is the same greedy at O(n log n).

## What to carry forward

Interval covering is Jump Game II once you bucket each interval by its left end: the wet prefix is the frontier, the best
tap in the prefix is the next jump, and a round where nothing gets past the edge means -1. The next problem keeps the
left-to-right sweep but replaces the frontier with a running fuel total, and shows how one failure lets you skip a whole
block of candidates at once.
