---
rank: 50
slug: interval_scheduling
---

Given intervals `[start, end]` with `start < end`, keep as many as possible so that no two overlap; ends that only touch, such as `[1, 3]` and `[3, 5]`, do not count as overlapping. The fewest removals that leave the rest non-overlapping is then everything not kept. From `[[1, 3], [2, 4], [3, 5], [1, 8], [6, 7]]` three can stay, `[1, 3]`, `[3, 5]` and `[6, 7]`, so two must go.

The brute force tries every subset, `O(2^n)` of them. The greedy question is which interval to keep first, and the answer is the one that ends earliest, because it leaves the most room for everything after it. Sort by end, then sweep once: keep an interval if it starts at or after `last_end`, the end of the last kept one, and skip it otherwise. Merge Intervals (#18) sorts by start because it wants to glue overlaps together; scheduling sorts by end because it wants to leave room.

The exchange argument shows that the earliest end is a safe first choice. Take any optimal selection and its first interval by end. The earliest-ending interval overall ends no later, so swapping it in keeps every other chosen interval compatible: each of them starts at or after the old first one's end, hence at or after the new one's end too. The optimum keeps its size and now begins with the greedy choice, and the same argument repeats on the intervals that start after it. On the timeline, `last_end` is a finish line that only moves right, and each kept interval pushes it as little as possible.

```text
sorted by end    1   2   3   4   5   6   7   8
[1, 3]           ├───────┤                       keep, last_end = 3
[2, 4]               ├───────┤                   drop, 2 < 3
[3, 5]                   ├───────┤               keep, 3 ≥ 3, last_end = 5
[6, 7]                               ├───┤       keep, 6 ≥ 5, last_end = 7
[1, 8]           ├───────────────────────────┤   drop, 1 < 7
kept 3, removed 2
```

```pseudo
FUNCTION MaxNonOverlapping(intervals)
    by_end ← empty list
    FOR EACH (start, end) IN intervals
        by_end.append((end, start))        // end first: the sort orders by end
    by_end.sort()
    kept ← 0
    last_end ← -∞                          // end of the last kept interval
    FOR EACH (end, start) IN by_end
        IF start ≥ last_end                // fits after the last kept one
            kept ← kept + 1
            last_end ← end
    RETURN kept

FUNCTION MinRemovals(intervals)            // LC 435
    RETURN len(intervals) - MaxNonOverlapping(intervals)
```

Sorting costs `O(n log n)` and the sweep `O(n)`, plus `O(n)` space for the sorted copy. Reach for the earliest end when a problem asks for the most non-overlapping intervals, the fewest removals to get there (LC 435), the longest chain of pairs (LC 646) or the fewest arrows that burst every balloon (LC 452), whose count equals the number kept when touching counts as overlapping. Attending one event per day (LC 1353) runs the same earliest-deadline idea day by day with a min-heap of end days. Read the touching rule carefully: `start ≥ last_end` keeps touching intervals, while balloons and pair chains need `start > last_end`. The classic mistake is sorting by start: on `[[1, 10], [2, 3], [4, 5]]` the long `[1, 10]` comes first, is kept, and blocks both short intervals inside it, keeping one where two fit.

*Practice:* LC 435 Non-overlapping Intervals · LC 452 Minimum Number of Arrows to Burst Balloons · LC 646 Maximum Length of Pair Chain · LC 1353 Maximum Number of Events That Can Be Attended
