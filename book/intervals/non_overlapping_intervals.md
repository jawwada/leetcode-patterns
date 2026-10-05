# Non-overlapping Intervals
*LeetCode 435 · Medium · Pattern: Greedy by earliest end (interval scheduling) · Reading time ~7 min*

## The problem

Given intervals [start, end], return the minimum number of intervals to remove so that the remaining ones are pairwise
non-overlapping. Touching intervals such as [1,2] and [2,3] do not overlap.

```text
Example: [[1,2],[2,3],[3,4],[1,3]] -> 1 (remove [1,3]);
  [[1,2],[1,2],[1,2]] -> 2.
```

## What the problem is really asking

You have a pile of intervals. Delete as few as you can so that the survivors are pairwise non-overlapping. Here touching is allowed: `[1,2]` and `[2,3]` can both stay. Return the number deleted.

Flip it around and it gets clearer. Minimising deletions is the same as **maximising how many intervals you keep** without collisions, because deleted = n - kept. That is the classic *interval scheduling* problem: one lecture hall, many requested talks, fit in as many as possible.

The answer is a single integer. The hard part is the choice: when two intervals collide, which one should go? A wrong local choice can block several good intervals later.

Running example: `[[1,100],[11,22],[1,11],[2,12]]`, answer 2.

```text
[1,11]    [=========]
[2,12]     [=========]
[11,22]             [==========]
[1,100]   [======================> ...100]
         |----|----|----|----|----
         0    5    10   15   20

 keep [1,11] and [11,22] (they touch at 11: allowed)
 delete [2,12] and [1,100]           -> answer 2
```

## Do it by hand first

Try it as a person. "Which do I keep first?" Your eye goes to the left, and there are two bars starting at 1. `[1,100]` is enormous, and keeping it would block everything else, so you instinctively reject it. You take `[1,11]` instead. Why that one? Because it **gets out of the way soonest**. Then you ask which bar can come after 11. `[2,12]` starts at 2, before 11, so it collides. `[11,22]` starts exactly at 11, so it fits. Keep it. Nothing else fits after 22. You kept 2 and deleted 2.

```text
 hall timeline:  1 ------- 11 ---------- 22 ...........
 booked:         [ [1,11]  ][  [11,22]   ]
 rejected:       [2,12] (starts at 2 < 11)
                 [1,100] (starts at 1 < 22)
```

What did your hand keep track of? One number: **the moment the hall becomes free again**, which is the end of the last kept talk. Every candidate was judged by one comparison, `start >= free_at`. The real skill was in *which order* you considered candidates. You favoured the ones that finish early.

## The first honest attempt

"Try every subset. For each subset, check all pairs for overlap. Keep the largest valid subset, and the answer is n minus its size."

That is O(2^n * n^2): 2^n subsets, each with up to n^2 pair checks. At n = 30 that is already about 10^12. The repeated work is twofold. Subsets that contain the same bad pair, for example both `[1,11]` and `[2,12]`, are each rejected separately, over and over. And most valid subsets are obviously dominated: any subset containing `[1,100]` has a twin with `[1,11]` in its place that is at least as good.

```text
 subsets containing the clash ([1,11],[2,12]):
   {[1,11],[2,12]}                  rejected
   {[1,11],[2,12],[11,22]}          rejected again
   {[1,11],[2,12],[1,100]}          rejected again
   {[1,11],[2,12],[11,22],[1,100]}  rejected again
 same clash, re-discovered 2^(n-2) times
```

A smarter-sounding attempt is "sort by start and keep whatever fits". On our example that sorts `[1,100]` first (it is listed before `[1,11]` and the sort is stable), keeps it, and then deletes all three others. That gives 3, which is wrong. The order of consideration is the whole problem.

## The turning point

**Claim: among all intervals, the one with the earliest end can always be part of some optimal kept set.**

This is an *exchange argument*. Take any optimal kept set `OPT`, listed left to right, and let its first interval be `f`. Let `g` be the interval with the globally earliest end, so `g.end <= f.end`. Replace `f` with `g` in `OPT`. Does anything break? Every other interval `x` in `OPT` comes after `f`, so `x.start >= f.end >= g.end`. That means `g` does not collide with any of them. The new set is valid and has the same size, so it is also optimal, and it contains `g`.

```text
 OPT:      [---- f ----]   [-- x --]  [-- y --]
 swap:     [- g -]         [-- x --]  [-- y --]
                 ^ g.end <= f.end <= x.start: still fits
```

Once `g` is committed, every interval that starts before `g.end` collides with `g` and must go. What remains is the same problem on the intervals with `start >= g.end`, and the claim applies again. Repeating this is exactly:

1. Sort by end.
2. Walk in that order with `last_end` = the end of the last kept interval (start at minus infinity).
3. If `start >= last_end`, keep it and set `last_end = end`. Otherwise delete it (`removed += 1`).

Why does walking in end order implement "repeatedly take the earliest-ending remaining interval that fits"? Because the first interval in end order that passes `start >= last_end` is exactly the earliest-ending interval that fits after the last kept one. The ones skipped before it all collided.

Now the failure of sort-by-start makes sense. The earliest *start* says nothing about how much room you leave to the right. `[1,100]` starts first and hogs the line. The earliest *end* is precisely the quantity that measures "room left for everyone else".

Note the `>=` in step 3. The problem allows touching, so `start == last_end` fits. In Merge Intervals the same touch meant "fuse". Here it means "compatible". Same geometry, opposite verdict, so read the statement.

## Watch it work

Input `[[1,100],[11,22],[1,11],[2,12]]`. Sorted by end: `[1,11], [2,12], [11,22], [1,100]`.

**Frame 1.** `[1,11]`: 1 >= minus infinity, so keep it. `last_end = 11`.

```text
 order: [1,11] [2,12] [11,22] [1,100]
          ^
 hall:  [==========]               last_end=11
        1          11              removed=0
```

The earliest finisher is booked first.

**Frame 2.** `[2,12]`: 2 < 11, so it collides. Delete it.

```text
 order: [1,11] [2,12] [11,22] [1,100]
                 ^
 hall:  [==========]               last_end=11
         [2,12] x                  removed=1
```

It ends later than the kept one, so the kept one was the better choice.

**Frame 3.** `[11,22]`: 11 >= 11, touching is allowed, so keep it. `last_end = 22`.

```text
 order: [1,11] [2,12] [11,22] [1,100]
                        ^
 hall:  [==========][===========]  last_end=22
        1          11           22 removed=1
```

The fence jumps to 22.

**Frame 4.** `[1,100]`: 1 < 22, so delete it.

```text
 order: [1,11] [2,12] [11,22] [1,100]
                                 ^
 hall:  [==========][===========]  last_end=22
        [1,100] x                  removed=2
```

The answer is 2, which matches the solution's output.

Invariant across frames: the kept intervals were pairwise compatible, and `last_end` was the end of the latest one. Because we walked in end order, `last_end` was also the smallest possible end for a kept set of that size.

## Why it is correct

Use a "greedy stays ahead" invariant. Let the greedy kept intervals be `g1, g2, ...` and any valid kept set be `o1, o2, ...`, both in left-to-right order. Claim: `g_k.end <= o_k.end` for every k where both exist.

- k = 1: `g1` is the earliest-ending interval overall, so `g1.end <= o1.end`.
- Step: `o_{k+1}.start >= o_k.end >= g_k.end`, so `o_{k+1}` was still a legal choice when greedy picked its (k+1)-th. Greedy picks the earliest-ending legal one, so `g_{k+1}.end <= o_{k+1}.end`.

If the other set had more intervals than greedy, its `o_{m+1}` would start after `o_m.end >= g_m.end`, so it would be legal after greedy's last pick. Greedy would then have kept something, which is a contradiction. So greedy keeps the maximum, and n - kept is the minimum number of deletions. The `removed` counter is exactly n - kept.

## Cost

- **Time O(n log n).** Sorting by end. The sweep is O(n) with one comparison each.
- **Space O(1) extra** beyond the sort: `last_end` and `removed`.

Subset enumeration was O(2^n * n^2). A DP over intervals sorted by end (best kept count ending at i) is O(n^2), or O(n log n) with binary search. It is correct, but it is the tool for the *weighted* version, not this one.

## Variations you will meet

- **Minimum Number of Arrows to Burst Balloons** (452). Here touching balloons share a point, so one arrow pops both. Same greedy by end, but the compatibility test becomes `start > last_end`. The answer is the count of kept intervals, not the deletions.
- **Maximum Length of Pair Chain** (646). Pairs `[a,b]` chain if `b < c`. This is interval scheduling with strict inequality, so return the kept count.
- **Weighted interval scheduling** (1235, Maximum Profit in Job Scheduling). Each interval has a value, and the exchange argument breaks, because a short cheap job is not obviously better than a long valuable one. Sort by end and do DP with binary search for the last compatible job.
- **Many halls instead of one**: you no longer delete anything, and you ask how many halls are needed. That is the next problem.

## What to carry forward

To fit the most intervals into one line, always keep the one that ends first. The exchange argument proves it, and the only state is `last_end`. The next problem, Meeting Rooms II, keeps every interval and asks how many parallel lines (rooms) you need, so the single `last_end` grows into a min-heap of end times, one per occupied room.
