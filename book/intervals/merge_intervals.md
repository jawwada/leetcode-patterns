# Merge Intervals
*LeetCode 56 · Medium · Pattern: Sort by start, sweep and merge · Reading time ~7 min*

## What the problem is really asking

You get a pile of closed intervals `[start, end]` in any order. Wherever two of them share at least one point, they are really one stretch of covered line, so glue them together. Return the smallest set of intervals that covers exactly the same points. Touching counts as sharing: `[1,4]` and `[4,5]` share the point 4 and become `[1,5]`.

The answer is a list of disjoint intervals: the connected pieces of the union. What makes it tricky is that overlap chains. `A` may not touch `C` directly, yet both touch `B`, so all three fuse. A rule that only looks at pairs misses that, and a rule that keeps re-checking pairs after every fusion is slow.

Our running example is `[[4,8],[1,5],[10,12],[2,3]]`:

```text
 input, drawn in sorted order (input order was 4-8,1-5,..)

[1,5]    [===========]
[2,3]       [==]
[4,8]             [===========]
[10,12]                             [=====]
         +--+--+--+--+--+--+--+--+--+--+--+
         1  2  3  4  5  6  7  8  9  10 11 12

 answer: [[1,8], [10,12]]

out      [====================]
out                                 [=====]
         +--+--+--+--+--+--+--+--+--+--+--+
         1  2  3  4  5  6  7  8  9  10 11 12
```

## Do it by hand first

Give a person these four bars on paper and ask them to merge. Nobody compares every pair. They put a finger at the far left, on the bar that starts first, `[1,5]`, and run the finger along it. As they go, they notice `[2,3]` sitting inside (nothing changes), then `[4,8]` starting before the finger has left the current bar at 5. "Still going," they say, and the finger now has to reach 8. At 8 the ink stops. The next bar starts at 10, so there is white space, and they write down `[1,8]`. Then they start again at 10 and write down `[10,12]`.

```text
 finger:  1 ---------------> 5 ---------> 8    gap    10 -> 12
          |  [2,3] inside    |  [4,8]     |           |
          |  (nothing new)   |  pushes    |  emit     | emit
          |                  |  to 8      |  [1,8]    | [10,12]
```

What did the hand keep track of? Two numbers: where the current block started, and how far right it has reached so far. Everything already written down is done and never revisited. That pair, "current block start and current reach", is the whole data structure.

The other thing the hand did, without saying so, was visit the bars from left to right by start. That is the sort.

## The first honest attempt

"Two intervals overlap if `a.start <= b.end` and `b.start <= a.end`. So: loop over every pair. When I find an overlapping pair, replace both with their union and start the scan again. Stop when a full scan finds nothing."

This is correct, and it handles chains: after `A` and `B` fuse, the fused bar meets `C` on a later scan. But count the work. A scan is O(n^2) pair checks, and there can be up to n - 1 fusions, each followed by a fresh scan, so the total is O(n^3).

Where is the repeated work? Look at what happens to a pair that was found disjoint:

```text
 list = [4,8] [1,5] [10,12] [2,3]

 scan 1: ([4,8],[1,5])   overlap -> fuse [1,8], restart
 scan 2: ([1,8],[10,12]) no
         ([1,8],[2,3])   overlap -> fuse [1,8], restart
 scan 3: ([1,8],[10,12]) no      -> nothing changed, stop

 ([1,8],[10,12]) is asked twice. With n bars, far-apart
 pairs like it are re-asked on every one of ~n scans.

 [1,8] [=========]      gap     [10,12] [===]
       |<---- tested again after every fusion ---->|
```

Most of those checks compare bars that sit at opposite ends of the line. They could never touch, and we keep asking anyway.

## The turning point

**Claim: once the intervals are sorted by start, each interval can only overlap the block currently being built, never an older one.**

Why: suppose blocks `P1, P2, ..., Pk` have already been closed and we are building `cur`. A block closed because the next bar started strictly after its reach, and every later bar starts at least that late. So nothing that comes later can reach back into `P1..Pk`. The only open question for the next bar `[s, e]` is how it relates to `cur`. As the background chapter showed, sorting by start leaves just three cases, and one comparison separates them:

```text
 cur = [cs, ce], next = [s, e], s >= cs guaranteed

 s <= ce, e <= ce   nested     cur [=========]
                               nxt    [==]       ce stays

 s <= ce, e >  ce   tail       cur [=====]
                               nxt    [=======]  ce -> e

 s >  ce            after      cur [=====]
                               nxt          [==] emit cur,
                                                 cur = nxt
```

The first two cases are both "overlap", and both are handled by `ce = max(ce, e)`. The third is "disjoint": `cur` is final, so emit it.

That turns the claim into an algorithm with one piece of state, the last interval in the output list, which is still open for extension:

```python
for s, e in intervals:                # sorted by start
    if s <= merged[-1][1]:            # overlaps the open block
        merged[-1][1] = max(merged[-1][1], e)
    else:
        merged.append([s, e])         # previous block is final
```

Notice what we did not need. We never store the earlier blocks anywhere except as output. We never look backwards. Each interval is examined once. The O(n^2)-per-scan pair loop became n single comparisons, and the only real cost left is the sort.

Also note the `<=`. The problem says touching intervals merge, so `s == ce` is overlap. If a problem says touching intervals do not merge, that one character changes, and nothing else does.

## Watch it work

Input `[[4,8],[1,5],[10,12],[2,3]]`. Sorted by start: `[1,5], [2,3], [4,8], [10,12]`.

**Frame 1.** The first sorted interval opens the first block.

```text
 sorted:  [1,5] [2,3] [4,8] [10,12]
            ^
 merged:  [[1,5]]          open block = [1,5], reach 5
```

The output list holds one open block.

**Frame 2.** `[2,3]`: start 2 <= reach 5, so it overlaps. Reach becomes max(5, 3) = 5.

```text
 sorted:  [1,5] [2,3] [4,8] [10,12]
                  ^
 [1,5]  [===========]
 [2,3]     [==]            nested: reach stays 5
 merged:  [[1,5]]
```

A nested bar changes nothing, and that is exactly why `max` is needed instead of `= e`.

**Frame 3.** `[4,8]`: start 4 <= reach 5, so it overlaps. Reach becomes max(5, 8) = 8.

```text
 sorted:  [1,5] [2,3] [4,8] [10,12]
                        ^
 [1,5]  [===========]
 [4,8]           [===========]   tail: reach 5 -> 8
 merged:  [[1,8]]
```

The open block grows to the right.

**Frame 4.** `[10,12]`: start 10 > reach 8, so it is disjoint. `[1,8]` is final, and `[10,12]` opens a new block.

```text
 sorted:  [1,5] [2,3] [4,8] [10,12]
                               ^
 merged:  [[1,8], [10,12]]
           final   open, reach 12
```

The input is exhausted, so the output is `[[1,8],[10,12]]`. This matches what the solution returns on this input.

Across all frames, two things held. Every block except the last in `merged` was final, and nothing later could touch it. The last block's end was the furthest reach of every interval seen so far that belongs to it.

## Why it is correct

Invariant, true after processing the first i sorted intervals: `merged` is exactly the merge of those i intervals, and its blocks are sorted and pairwise disjoint (separated by a gap).

- Base case: after one interval, `merged = [first]`. That is trivially right.
- Step: take the next interval `[s, e]`, with `s` at least every earlier start. Every closed block `P` (all but the last) ended before some later start, and that start is at most `s`, so `P.end < s` and `[s, e]` cannot touch `P`. That leaves the open block `[cs, ce]`. If `s <= ce`, the two share a point, so their union is the single interval `[cs, max(ce, e)]` (cs is the smaller start because of the sort). If `s > ce`, they share no point, and since every future start is at least `s > ce`, the open block can never be touched again. Closing it is safe, and `[s, e]` becomes the new open block.

After all n intervals, the invariant says `merged` is the merge of all of them. The chaining problem, where `A` and `C` fuse through `B`, is handled for free: `B` extends the open block's reach far enough that `C`'s start falls under it.

## Cost

- **Time O(n log n).** The sort dominates. The sweep is one O(1) comparison per interval.
- **Space O(n).** The output can hold n intervals. Python's sort (Timsort) may use O(n) extra memory too.

The brute force was O(n^3) time. A middle ground, sorting and then comparing each interval against all earlier blocks, is O(n^2) and pointless once you see the claim.

## Variations you will meet

- **Touching does not merge** (half-open intervals). Change `s <= ce` to `s < ce`. Nothing else moves.
- **Total covered length** instead of the list: during the same sweep, add `ce - cs` each time you close a block. Rectangle Area II at the end of this chapter uses exactly this, on y-intervals.
- **Intervals arrive in a stream** and you must report the merged set at any time (LeetCode 352, Data Stream as Disjoint Intervals). You can no longer sort once, so keep the blocks in an ordered structure and merge with the neighbours of each insertion point.
- **Already-sorted, disjoint input plus one new interval**: the next problem. The sort becomes unnecessary, and the merge becomes a three-phase scan.

## What to carry forward

Sort by start, and one comparison against the open block (`s <= end`, then `end = max(end, e)`) replaces every pairwise test. The next problem, Insert Interval, receives the list already sorted and disjoint, so it drops the sort and merges one newcomer in a single O(n) pass.
