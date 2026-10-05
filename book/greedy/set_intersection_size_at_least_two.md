# Set Intersection Size At Least Two

*LeetCode 757 · Hard · Pattern: Greedy by earliest end (interval scheduling) · Reading time ~9 min*

## The problem

Given closed integer intervals [start, end], find the smallest set of integers S such that every interval contains at
least two elements of S; return |S|.

```text
Example: [[1,3],[3,7],[8,9]] -> 5 (S = {2,3,4,8,9}).
  [[1,3],[1,4],[2,5],[3,5]] -> 3 (S = {2,3,5}).
```

## What the problem is really asking

You get closed integer intervals `[start, end]`. Choose a set `S` of integers, as small as possible, such that every interval contains at least two members of `S`. Return `|S|`.

The answer is a size. Picture intervals as bars over a number line, and `S` as pins you push into the line. Every bar must be pierced by at least two pins. One pin can pierce many bars at once, so the game is to put pins where bars overlap the most. The hard part is that "two per bar" breaks the classic one-pin argument in small ways: which two points, and what to do when a bar already has one pin.

```text
intervals: [1,3] [3,7] [8,9]

  1   2   3   4   5   6   7   8   9
  [=======]
          [===============]
                              [===]
pins: ^   ^   ^               ^   ^
      2   3   4               8   9
[1,3] has 2,3   [3,7] has 3,4   [8,9] has 8,9
answer 5
```

## Do it by hand first

Take `[[1,3], [1,4], [2,5], [3,5], [5,8]]`. A sensible human looks at the bar that finishes first, because it has the least room to wait. It must get two pins somewhere in `[1, 3]`. Where? As far right as possible, at 2 and 3, because every other bar ends at 3 or later, so a pin further right lands inside more of them.

```text
  1   2   3   4   5   6   7   8
  [=======]            [1,3]  needs 2 -> pins 2,3
  [===========]        [1,4]  has 2,3  -> ok
      [===========]    [2,5]  has 2,3  -> ok
          [=======]    [3,5]  has 3    -> +1 at 5
                  [===========] [5,8] has 5 -> +1 at 8
pins: 2   3       5           8     total 4
```

Your hand kept track of only the last two pins it had placed. Earlier pins are further left, and since bars are being handled by end, a later bar that contains an older pin also contains the two newest. Two integers are the entire state.

## The first honest attempt

Brute force: let the candidate points be every integer from the smallest start to the largest end, and try every subset by increasing size until one pierces every bar twice.

```text
points 1..8 -> 2^8 subsets
size 2: {1,2} {1,3} ... each checked against all 5 bars
size 3: {1,2,3} ...
size 4: ... {2,3,5,8} works
   the same bar [1,3] is re-checked inside every subset,
   though its fate is decided by pins in [1,3] alone
```

Exponential in the coordinate range. The waste is that subsets never use the obvious ordering: once the earliest-ending bar's needs are met in the best way, the rest of the problem only cares about how far right those pins sit.

Now the tempting wrong greedies, both of which feel natural.

```text
Wrong 1: put pins at the LEFT of a needy bar (s, s+1)
  [[1,3],[3,7]]
  [1,3] -> pins 1,2 ; [3,7] has none -> pins 3,4
  total 4, but {2,3,7} works -> 3

Wrong 2: sort by end, ties by start ASCENDING
  [[0,1],[1,5],[3,5],[5,6]]
  [0,1] -> 0,1 ; [1,5] has 1 -> +5 ;
  [3,5] has 5 only -> +5 again (duplicate!)
  returns 4, true answer 5
```

Wrong 1 places pins where future bars cannot see them. Wrong 2 is subtler: when two bars share an end, the wide one goes first and grabs the end point, then the narrow one "adds" the same point again and is left with a single real pin. Processing the narrow bar first (start descending) makes its pins land inside the wide bar too.

## The turning point

**Claim: process bars by end ascending (ties: start descending); whenever a bar is short of pins, add the missing ones at its right edge, `e` and if needed `e - 1`.**

Why the right edge? All bars processed later end at `e` or after. A pin `p <= e` lies inside a later bar `[s', e']` exactly when `p >= s'`. So among pins inside the current bar, a larger one is inside every later bar that a smaller one is inside, and possibly more. Rightmost pins dominate.

Why only two numbers of state? Pins are added in increasing order (each new pin is a right edge, and right edges never decrease). Let `a < b` be the two largest pins. For the next bar `[s, e]`, since `b <= e`, the number of pins inside it is decided by where `s` falls:

```text
           a       b             e
  --------[*]-----[*]------------|
case s > b:          s[========] -> 0 inside: add e-1, e
case a < s <= b:  s[===========] -> 1 inside: add e
case s <= a:   s[==============] -> 2 inside: nothing
```

Any older pin is below `a`, so if `s <= a` there are already two, and if `s > a` the older pins cannot help. Three cases, constant work each.

The tie rule is what makes "add `e`" safe in case 2. If `b` already equals `e`, adding `e` would duplicate a pin. That can only happen when the previous bar also ended at `e`. With start descending, that previous bar was the narrower one, it already holds two pins after its turn, and the wider current bar contains every point of it, so the current bar lands in case 3 and adds nothing.

## Watch it work

Example: `[[1,3], [1,4], [2,5], [3,5], [5,8]]`. The solution returns 4.

Frame 1. Sort by (end ascending, start descending).

```text
sorted: [1,3] [1,4] [3,5] [2,5] [5,8]
                    ^^^^^ ^^^^^
             tie at end 5: start 3 before 2
a = -1, b = -1, count = 0
```

Frame 2. `[1,3]`: `s = 1 > b = -1`, no pins inside. Add 2 and 3.

```text
  1 2 3 4 5 6 7 8
  [===]                a=2 b=3
    * *                count 2
```

Frame 3. `[1,4]`: `s = 1`, not `> b = 3`, not `> a = 2`. Both pins inside.

```text
  1 2 3 4 5 6 7 8
  [=====]              a=2 b=3
    * *                count 2 (no change)
```

Frame 4. `[3,5]`: `s = 3`, not `> b = 3`, but `> a = 2`. Only pin 3 is inside; add 5.

```text
  1 2 3 4 5 6 7 8
      [===]            a=3 b=5
    * *   *            count 3
```

Frame 5. `[2,5]`: `s = 2`, not `> b = 5`, not `> a = 3`. Pins 3 and 5 are inside.

```text
  1 2 3 4 5 6 7 8
    [=====]            a=3 b=5
    * *   *            count 3 (no change)
```

The narrow bar went first and its new pin 5 also serves the wide one.

Frame 6. `[5,8]`: `s = 5`, not `> b = 5`, but `> a = 3`. Only pin 5 is inside; add 8.

```text
  1 2 3 4 5 6 7 8
          [=====]      a=5 b=8
    * *   *     *      count 4
S = {2, 3, 5, 8}
```

Across the frames, every processed bar held at least two pins, and `a`, `b` were always the two largest pins placed so far. Pins only ever moved rightward, landing on right edges.

## Why it is correct

Validity: after handling each bar, it contains at least two pins (case analysis above), and pins are never removed, so every bar ends up satisfied.

Minimality uses a "greedy stays ahead" exchange argument. Order the bars as sorted, and compare the greedy with any valid set `O`. The claim, by induction over bars: after the first `k` bars, the greedy has used no more pins than `O` uses to satisfy those bars, and if the counts tie, the greedy's two largest pins are each at least as far right as `O`'s two largest pins among those satisfying the first `k` bars.

Step. Suppose the greedy needs to add pins for bar `[s, e]`. If it adds two, then `s > b`, so neither of the greedy's pins is inside; by the hypothesis `O`'s top pins are no further right, so they are not inside either, and `O` must also spend two pins in `[s, e]`. The greedy spends two and puts them at `e - 1, e`, the furthest right possible: ahead again. If it adds one, `O` has at most one of its earlier pins inside (its second largest is no further right than `a < s`), so `O` too must add at least one, and the greedy's choice `e` is the rightmost possible. In each case `O` pays at least what the greedy pays, and the greedy's top pins stay at least as far right.

The exchange view of the same idea: in `O`, take a pin inside `[s, e]` that is not at the greedy's position and slide it right to `e` (or `e - 1`). Earlier bars already have their two pins from earlier choices, and later bars end at or after `e`, so sliding right can only add bars to the pin's coverage. Repeat until `O` matches the greedy, never increasing its size.

## Cost

Time O(n log n) for the sort; the sweep is O(n) with constant work per bar.

Space O(1) beyond the sort: two integers and a counter. The brute force was exponential in the coordinate range.

## Variations you will meet

- **At least one point per interval (Minimum Number of Arrows to Burst Balloons).** Same sweep with one tracked point: sort by end, shoot at `e` whenever `s > last`.
- **At least `k` points per interval.** Keep the `k` largest chosen points in a sorted structure; a needy bar adds its missing points at `e, e-1, ...` skipping any already chosen.
- **Different demand per interval.** Sorting by end still works, but deciding where the `d` new points go needs the set of free positions near `e`; a union-find "next free slot to the left" keeps it fast.
- **Non-overlapping Intervals / interval scheduling.** The same earliest-end-first ordering, but the goal flips from covering every interval to keeping as many disjoint ones as possible.

## What to carry forward

Sort by deadline, satisfy each demand as late as possible, and keep only the state later demands can see; prove it by showing the greedy is never behind any rival. The next problem leaves intervals behind for a seating chart, where the right greedy is "fix one couch at a time" and the proof that it is optimal comes from counting cycles.
