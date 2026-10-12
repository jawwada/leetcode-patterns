---
rank: 66
slug: interval_list_intersections
---

Given two lists of closed intervals, each sorted and pairwise disjoint, return every stretch the two lists share. For `[[0, 2], [5, 10], [13, 23], [24, 25]]` and `[[1, 5], [8, 12], [15, 24], [25, 26]]` the answer is `[[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]`; the single point `[5, 5]` is shared because `[1, 5]` ends exactly where `[5, 10]` begins.

Comparing every pair costs `O(m n)`. Both lists are sorted, though, so one sweep from left to right handles them, like the merge step of merge sort (#17): one pointer per list, each resting on its current interval. Two closed intervals share exactly the stretch from the later start to the earlier end, `[max(starts), min(ends)]`, and they share anything at all only when that start is at most that end. After recording the overlap, if any, drop the interval that ends first. It can meet nothing further on in the other list: the next interval there starts after the current one ends, which is no earlier than the end of the interval being dropped. The interval that ends later may still reach into its partner's next interval, so it stays.

Picture both lists as rows of bars over one number line, with a vertical line sweeping to the right. The result is wherever both rows are covered at once, and the pointers advance in the order in which the bars end. A tie needs no special case: when both intervals end at the same point, either one can go, and the code drops the one from `second`. On the fourth step below, `[13, 23]` and `[8, 12]` do not overlap at all, since `13 > 12`, and the step simply drops `[8, 12]`, which ends first.

```text
        0         5         10        15        20        25
first   ├───┤     ├─────────┤     ├───────────────────┤ ├─┤
second    ├───────┤     ├───────┤     ├─────────────────┤ ├─┤
result    ├─┤     ●     ├───┤         ├───────────────┤ ● ●

first[i]   second[j]   start   end   overlap    ends first
[0, 2]     [1, 5]          1     2   [1, 2]     first:  i ← 1
[5, 10]    [1, 5]          5     5   [5, 5]     second: j ← 1
[5, 10]    [8, 12]         8    10   [8, 10]    first:  i ← 2
[13, 23]   [8, 12]        13    12   none       second: j ← 2
[13, 23]   [15, 24]       15    23   [15, 23]   first:  i ← 3
[24, 25]   [15, 24]       24    24   [24, 24]   second: j ← 3
[24, 25]   [25, 26]       25    25   [25, 25]   first:  i ← 4
```

```pseudo
FUNCTION IntervalIntersection(first, second)
    result ← empty list
    i ← 0
    j ← 0
    WHILE i < len(first) AND j < len(second)
        (first_start, first_end) ← first[i]
        (second_start, second_end) ← second[j]
        overlap_start ← max(first_start, second_start)    // the later start
        overlap_end ← min(first_end, second_end)          // the earlier end
        IF overlap_start ≤ overlap_end
            result.append([overlap_start, overlap_end])   // a point counts too
        IF first_end < second_end
            i ← i + 1               // first[i] can meet nothing further on
        ELSE
            j ← j + 1               // second[j] can meet nothing further on
    RETURN result
```

Each step advances one pointer, so the sweep takes at most `m + n` steps: `O(m + n)` time and `O(1)` extra space beyond the output. The signals are two sorted schedules, calendars or sets of busy or free times, and a question about when both hold at once. Meeting Scheduler sorts both people's free slots and runs this sweep, stopping at the first overlap that is at least the meeting's duration long. A single unsorted list of intervals calls for the sort and sweep of Merge Intervals (#26) instead. The classic mistake is advancing the pointer whose interval starts first: with `[[0, 10]]` against `[[1, 2], [3, 4]]` it drops `[0, 10]` after the first overlap and never finds `[3, 4]`. Testing the overlap with `<` in place of `≤` is the other one; it silently loses the single points `[5, 5]`, `[24, 24]` and `[25, 25]` above.

*Practice:* LC 986 Interval List Intersections · LC 56 Merge Intervals · LC 1229 Meeting Scheduler
