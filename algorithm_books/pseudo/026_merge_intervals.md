---
rank: 26
slug: merge_intervals
---

Given closed intervals `[start, end]` in any order, merge every group that overlaps or touches and return the result sorted by start. `[[1, 3], [8, 12], [2, 6], [9, 10], [12, 14]]` becomes `[[1, 6], [8, 14]]`: `[2, 6]` overlaps `[1, 3]`, `[9, 10]` lies inside `[8, 12]`, and `[12, 14]` touches it at 12.

The brute force compares every pair and merges any two that overlap, repeating until nothing changes, which is at least `O(n²)`. Sorting by start removes all of that searching. Lay the sorted intervals on a number line and sweep from left to right. Each interval starts at or after every interval before it, so the only one it can reach is the merged interval being built at the right end of the output, `merged[-1]`. One comparison settles it. If the new start is at most the last merged end, the two share a point and the last interval stretches to cover the new one. Otherwise there is a gap on the line, and no later interval can bridge it, because every later interval starts no earlier than the new one. The last merged interval is final, and a new one begins.

The stretch takes the larger of the two ends, not the new end, because a short interval can sit entirely inside the current one, as `[9, 10]` sits inside `[8, 12]`. The test is `≤` rather than `<` because closed intervals that touch share a point, so `[8, 12]` and `[12, 14]` become one.

```text
           0   2   4   6   8   10  12  14
[1, 3]       ├───┤
[2, 6]         ├───────┤
[8, 12]                    ├───────┤
[9, 10]                      ├─┤
[12, 14]                           ├───┤
merged       ├─────────┤   ├───────────┤

sorted     start ≤ last merged end?            merged after
[1, 3]     merged is empty → append            [1, 3]
[2, 6]     2 ≤ 3 → end ← max(3, 6) = 6         [1, 6]
[8, 12]    8 > 6 → append                      [1, 6] [8, 12]
[9, 10]    9 ≤ 12 → end ← max(12, 10) = 12     [1, 6] [8, 12]
[12, 14]   12 ≤ 12 → end ← max(12, 14) = 14    [1, 6] [8, 14]
```

```pseudo
FUNCTION MergeIntervals(intervals)
    merged ← empty list                     // merged[-1] is its last interval
    FOR EACH [start, end] IN sorted(intervals)          // by start
        IF len(merged) > 0 AND start ≤ merged[-1][1]
            merged[-1][1] ← max(merged[-1][1], end)     // overlap: stretch it
        ELSE
            merged.append([start, end])                 // a gap: a new interval
    RETURN merged
```

The sort costs `O(n log n)` and the sweep `O(n)`, with `O(n)` space for the output. Reach for sort-then-sweep whenever a problem hands you ranges, bookings or segments and asks for their union, their overlaps or the gaps between them. When the list is already sorted and disjoint, as in Insert Interval (#65), skip the sort: copy the intervals that end before the new one starts, absorb every interval that overlaps it by taking the smaller start and the larger end, then copy the rest, all in `O(n)`. Interval List Intersections (#66) walks two sorted lists with two pointers instead, and Meeting Rooms needs only the comparison: after sorting, any start before the previous end is a conflict. The classic mistake is stretching to `end` instead of `max(merged[-1][1], end)`: on the example, `[9, 10]` shrinks `[8, 12]` to `[8, 10]`, and `[12, 14]` is wrongly left on its own.

*Practice:* LC 56 Merge Intervals · LC 57 Insert Interval · LC 986 Interval List Intersections · LC 252 Meeting Rooms
