---
rank: 65
slug: insert_interval
---

Given closed intervals `[start, end]` sorted by start and pairwise disjoint, insert one more, merging it with every interval it overlaps or touches, and return the list still sorted and disjoint. Inserting `[4, 8]` into `[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]` gives `[[1, 2], [3, 10], [12, 16]]`: the new interval swallows `[3, 5]`, `[6, 7]` and `[8, 10]`, which it touches at 8.

The brute force appends the new interval and runs Merge Intervals (#26), paying `O(n log n)` to sort a list that was sorted all along. Because the intervals are sorted and disjoint, their starts and their ends both increase from left to right, so the new interval splits the line into three runs: the intervals that end before it starts, the ones that overlap or touch it, and the ones that start after it ends. Each run is contiguous, since once an interval ends at or after the new start every later one does too, and once one starts beyond the new end every later one starts further right. So a single index walks three loops. The first copies while `end < new_start`. The second absorbs while `start ≤ new_end`, stretching the new interval to the smaller start and the larger end. After the grown interval is appended, the third copies the rest.

Picture the new interval as a bar laid across the line: whatever it touches melts into it, and whatever lies strictly left or right stays as it was. Only the first absorbed interval can lower the start and only the last can raise the end, but `min` and `max` at every step are simpler and just as right. Touching counts as overlap for closed intervals, which is why the first loop runs on a strict `<` and the second on `≤`.

```text
             0   2   4   6   8   10  12  14  16
[1, 2]         ├─┤                              before: copy
[3, 5]             ├───┤                        overlap: absorb
[6, 7]                   ├─┤                    overlap: absorb
[8, 10]                      ├───┤              overlap: absorb
[12, 16]                             ├───────┤  after: copy
new [4, 8]           ├───────┤
result         ├─┤ ├─────────────┤   ├───────┤

i   interval   test                            action
0   [1, 2]     2 < 4: ends before it starts    copy
1   [3, 5]     5 < 4? no, loop 1 ends          go to loop 2
1   [3, 5]     3 ≤ 8                           absorb → [3, 8]
2   [6, 7]     6 ≤ 8                           absorb → [3, 8]
3   [8, 10]    8 ≤ 8, touching                 absorb → [3, 10]
4   [12, 16]   12 ≤ 10? no, loop 2 ends        append [3, 10]
4   [12, 16]   loop 3                          copy
```

```pseudo
FUNCTION InsertInterval(intervals, new_interval)
    result ← empty list
    new_start ← new_interval[0]
    new_end ← new_interval[1]
    i ← 0
    n ← len(intervals)
    WHILE i < n AND intervals[i][1] < new_start      // ends before it starts
        result.append(intervals[i])
        i ← i + 1
    WHILE i < n AND intervals[i][0] ≤ new_end        // overlaps or touches it
        new_start ← min(new_start, intervals[i][0])  // the new interval grows
        new_end ← max(new_end, intervals[i][1])
        i ← i + 1
    result.append([new_start, new_end])              // added exactly once
    WHILE i < n                                      // starts after it ends
        result.append(intervals[i])
        i ← i + 1
    RETURN result
```

Each interval is examined once and copied at most once, so the insert takes `O(n)` time and `O(n)` space for the new list, with no sort. Binary search could find where the overlapping run begins in `O(log n)`, but writing the output costs `O(n)` anyway. Reach for the three loops whenever a list is already sorted and disjoint and one more interval arrives; Range Module (#142) keeps such a list, and its `add_range` is this insert. The classic mistake is `≤` in the first loop, which copies an interval that merely touches the new one, so `[[1, 4]]` with `[4, 6]` becomes `[[1, 4], [4, 6]]` instead of `[[1, 6]]`. A one-loop version has its own trap: it appends the new interval when the first interval after it shows up, so without one more append after the loop it loses the new interval whenever that belongs at the very end.

*Practice:* LC 57 Insert Interval · LC 56 Merge Intervals · LC 715 Range Module · LC 352 Data Stream as Disjoint Intervals
