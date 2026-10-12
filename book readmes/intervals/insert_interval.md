# Insert Interval
*LeetCode 57 · Medium · Pattern: Sort by start, sweep and merge · Reading time ~7 min*

## The problem

intervals is sorted by start and pairwise non-overlapping. Insert newInterval, merging where necessary, and return the
list still sorted and non-overlapping.

```text
Example: [[1,3],[6,9]] with new [2,5] -> [[1,5],[6,9]];
  [[1,2],[3,5],[6,7],[8,10],[12,16]] with new [4,8] ->
  [[1,2],[3,10],[12,16]].
```

## What the problem is really asking

You hold a list of closed intervals that is already clean. It is sorted by start and no two of its intervals touch or overlap, which is exactly what Merge Intervals produces. One new interval arrives. Put it in, fuse whatever it collides with, and hand back a list that is clean again.

The answer is again a sorted list of disjoint intervals. The difficulty is not correctness, since you could just append and rerun Merge Intervals. The difficulty is noticing how much the input already promises, and using it to get O(n) instead of O(n log n).

Running example: `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `new = [4,8]`.

```text
 before (the new bar drawn on its own row)

[1,2]    [==]
[3,5]          [=====]
[6,7]                   [==]
[8,10]                        [=====]
[12,16]                                   [===========]
new               [===========]
         +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16

 after: [[1,2], [3,10], [12,16]]

out      [==]
out            [====================]
out                                       [===========]
         +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
```

`[4,8]` reaches into `[3,5]`, swallows `[6,7]` whole, and touches `[8,10]` at the point 8. All four fuse into `[3,10]`.

## Do it by hand first

On paper you would not redraw the whole list. You would slide your eye along it from the left and ask one question of each bar: "Is this bar entirely to the left of the new one?" `[1,2]` ends at 2, before 4. Yes, so copy it. `[3,5]` ends at 5, which is not before 4, so the copying phase is over.

Now you are in the collision zone. You hold the new bar `[4,8]` in your other hand and let it absorb bars. `[3,5]` makes its left edge 3. `[6,7]` is inside and changes nothing. `[8,10]` touches at 8 and stretches the right edge to 10. Then `[12,16]` starts at 12, past 10. The collision zone is over, so you write the fused bar `[3,10]` and copy everything that remains without looking at it.

```text
 eye moves -->
 [1,2]  | [3,5] [6,7] [8,10] | [12,16]
 copy   |   absorb into new  | copy rest
 left   |   new: [4,8]->[3,10]| untouched
```

What did you keep track of? An index into the list and the growing new interval, `[start, end]`. The list naturally split into three runs: left of the new bar, colliding with it, right of it.

## The first honest attempt

"I already have Merge Intervals. Append `new`, sort, merge."

```text
 [[1,2],[3,5],[6,7],[8,10],[12,16]] + [4,8]
 sort  -> [1,2] [3,5] [4,8] [6,7] [8,10] [12,16]   O(n log n)
 merge -> sweep, comparing each to the open block  O(n)
```

That is O(n log n) time and O(n) space, and it is correct. The repeated work is in two places. First, the sort re-establishes an order we were handed for free. Only one element is out of place, and a full sort spends n log n comparisons to discover that. Second, the merge sweep tests `[1,2]` against `[3,5]`, `[12,16]` against `[8,10]`, and so on. These pairs of original intervals are guaranteed disjoint by the problem statement, and we are asking about them anyway.

```text
 wasted checks (originals vs originals, known disjoint):
 [1,2]?[3,5]   [3,5]?[4,8]   ...   [8,10]?[12,16]
   no            (needed)              no
```

Only comparisons that involve the new interval can ever say "yes".

## The turning point

**Claim: the intervals that collide with `new` form one contiguous run of the sorted list, so the output is three runs in order: untouched-left, one fused interval, untouched-right.**

Justify it. The list is sorted by start and disjoint, so it is also sorted by end: if `a` comes before `b` and they do not overlap, then `a.end < b.start <= b.end`. Now:

- An interval is **left** of `new` exactly when `iv.end < new.start`. Because ends increase along the list, all such intervals form a prefix.
- An interval is **right** of `new` exactly when `iv.start > new.end`. Because starts increase, all such intervals form a suffix.
- Whatever lies between the prefix and the suffix overlaps `new` (it is neither left nor right of it), so it gets fused.

```text
 index:   0      1      2      3       4
        [1,2]  [3,5]  [6,7]  [8,10] [12,16]
        |left| |------ overlap ------| |right|
        end<4    start<=end of new     start>new.end
```

So one left-to-right pass with an index `i` and three loops does it. While `intervals[i].end < start`, copy and advance. While `intervals[i].start <= end`, absorb with `start = min(start, s)` and `end = max(end, e)`, then advance. Then append `[start, end]`, then copy the rest.

Why `min` for the start? Only the first absorbed interval can start before `new`, and Merge Intervals never needed a `min` because it sorted first. Here `new` was not sorted in, so the first colliding original can stick out to its left. `[3,5]` does exactly that. Why `max` for the end? Same reason as before: an absorbed interval might be nested and end earlier.

The middle loop compares against the current, already-grown `end`, so an original that touches only the grown part is still caught. This is the running reach of Merge Intervals in disguise.

## Watch it work

`intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `new = [4,8]`. State: index `i`, the growing `[start, end]`, and `out`.

**Frame 1.** Left phase: `[1,2]` has end 2 < start 4, so copy it.

```text
 i=0  [1,2] [3,5] [6,7] [8,10] [12,16]
        ^
 new = [4,8]     out = [[1,2]]
```

The prefix of untouched-left intervals is just this one.

**Frame 2.** `[3,5]`: end 5 is not < 4, so the left phase ends. Start 3 <= end 8, so absorb: start = min(4,3) = 3, end = max(8,5) = 8.

```text
 i=1  [1,2] [3,5] [6,7] [8,10] [12,16]
              ^
 new = [3,8]     out = [[1,2]]
```

The left edge moved, which is why `min` is needed.

**Frame 3.** `[6,7]`: start 6 <= 8, so absorb. start stays 3, end = max(8,7) = 8.

```text
 i=2  [1,2] [3,5] [6,7] [8,10] [12,16]
                    ^
 new = [3,8]     out = [[1,2]]
```

Nested inside, so nothing changes.

**Frame 4.** `[8,10]`: start 8 <= 8 (touching counts), so absorb. end = max(8,10) = 10.

```text
 i=3  [1,2] [3,5] [6,7] [8,10] [12,16]
                           ^
 new = [3,10]    out = [[1,2]]
```

The `<=` matters here. With `<`, `[8,10]` would wrongly stay separate.

**Frame 5.** `[12,16]`: start 12 > end 10, so the overlap phase ends. Append `[3,10]`, then copy the suffix.

```text
 i=4  [1,2] [3,5] [6,7] [8,10] [12,16]
                                  ^
 out = [[1,2], [3,10], [12,16]]
```

This matches the solution's output.

Invariant across frames: `out` always held exactly the intervals to the left of index `i` that do not touch the growing bar, and `[start, end]` was the union of `new` with every interval absorbed so far. Index `i` only moved forward.

## Why it is correct

Before the middle loop, every copied interval has `end < new.start`, so it shares no point with `new`. It also shares no point with any original that will be fused, because the originals are pairwise disjoint. So the copied prefix appears unchanged in the true answer.

During the middle loop, the invariant is: `[start, end]` equals the union of `new` and `intervals[first..i-1]`, and that union is one connected interval. When `intervals[i].start <= end`, it overlaps that union (its end is at least `new.start`, from the failed left test, and its start is at most `end`). So the union stays connected, and its bounds become the min and max.

When the loop stops, `intervals[i].start > end`. Every later interval starts even later, so none of the remaining intervals touch the fused bar, and they are pairwise disjoint by the input promise. Appending the fused bar and then the suffix yields a sorted, disjoint list that covers exactly the original points plus `new`. That is the definition of the answer.

Edge cases fall out without special code. An empty list skips both loops and returns `[new]`. A `new` past everything copies everything, then appends `new` at the end. A `new` before everything absorbs nothing, gets appended first, and is followed by the whole list.

## Cost

- **Time O(n).** Index `i` moves from 0 to n exactly once across the three phases, with O(1) work per step. No sort.
- **Space O(n).** The output holds up to n + 1 intervals. Extra state is two integers and an index.

If you only need to locate the phases, binary search on ends and starts finds the boundaries in O(log n). Building the output list still costs O(n), so in Python this does not change the asymptotics. It does matter when the structure is a balanced tree you can splice.

## Variations you will meet

- **Remove an interval** instead of inserting one (LeetCode 1272, Remove Interval). Same three phases, but the middle phase emits up to two clipped stubs (`[s, toBeRemoved.start]` and `[toBeRemoved.end, e]`) instead of fusing.
- **Many insertions over time** (LeetCode 715 Range Module, LeetCode 352). Rerunning the O(n) pass per insertion is O(n^2) total. Keep the intervals in a sorted container and binary-search the phase boundaries.
- **Half-open convention**: touching no longer fuses, so the middle test becomes `start < end`, and the left test becomes `iv.end <= new.start`.
- **Unsorted input**: you are back to Merge Intervals, so sort first.

## What to carry forward

When the input is already sorted and disjoint, an insertion splits the list into three contiguous runs (left, collide, right), and one pointer walks all three in O(n). The next problem, Non-overlapping Intervals, changes the question from "fuse the collisions" to "throw out the fewest bars so none collide", and that change flips the sort key from start to end.
