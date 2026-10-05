# Merge Intervals (LeetCode 56)

**Area:** intervals · **Difficulty:** Medium · **Key operations:** sort by start, compare start with the last merged end, extend end with max, open a new interval

## Problem

Given a list of intervals `[start, end]`, merge every group of overlapping intervals and return the non-overlapping intervals that cover exactly the same points. Intervals that merely touch, such as `[1,4]` and `[4,5]`, count as overlapping.

## Example

```
intervals = [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]

 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
 [-----]
    [-----------]
                      [-----]
                                           [--------]
 [--------------]     [-----]              [--------]
```

## Brute force

Paint every point each interval covers onto a number line, then read off the maximal painted runs. To keep `[1,2]` and `[3,4]` apart, paint in half units (`2*start .. 2*end`), so a gap of one unit stays unpainted.

O(n·C) time and O(C) space for coordinate range `C`. The wasted work: touching every point inside every interval, when only the endpoints decide anything. (The other classic brute force, repeatedly merging any overlapping pair until nothing changes, is O(n³) and wastes work re-testing pairs already known to be disjoint.)

## From brute force to optimal

Sort by start. Then an interval can only overlap the interval currently being built (the last merged one): anything that starts later than the current end cannot reach back, and anything before was already absorbed. So sweep once left to right. If the next start is at or before the current end, extend the current end to the max of both ends; otherwise the current interval is finished and the next one opens a new block. One sort and one linear pass.

## Intuition

Picture the intervals as bars laid above a number line, ordered by left edge. A sweep line moves right; the right edge of the bar being built is a frontier. Every bar whose left edge is at or before the frontier is fused into the current bar and may push the frontier further right, but never left: a bar nested inside the current one leaves the frontier where it is, which is why the end is updated with `max`. The first bar that starts past the frontier can never be reached by anything earlier, so the block closes there.

## Walkthrough

```
sorted by start: [[1,3],[2,6],[8,10],[15,18]]

open [1,3]                                        merged [[1,3]]
[2,6]    start 2 <= last end 3  -> extend to max(3,6)=6     merged [[1,6]]
[8,10]   start 8 >  last end 6  -> open new                 merged [[1,6],[8,10]]
[15,18]  start 15 > last end 10 -> open new                 merged [[1,6],[8,10],[15,18]]
```

## Steps

1. If the list is empty return `[]`.
2. Sort by start (a copy; do not mutate the caller's list).
3. `merged = [copy of the first interval]`.
4. For each following `[start, end]`: let `last = merged[-1]`. If `start <= last[1]`, set `last[1] = max(last[1], end)`; else append `[start, end]`.
5. Return `merged`.

## Complexity

O(n log n) time for the sort, then a single O(n) sweep. O(n) space for the output (plus the sorted copy).

## Pitfalls

- **`<` instead of `<=`.** Touching intervals must merge: `[[1,4],[4,5]]` is `[[1,5]]`.
- **`last[1] = end` instead of `max`.** A short interval nested inside the current one would shrink it: `[[1,4],[2,3]]` must stay `[[1,4]]`.
- **Sorting by end (or not sorting).** A long interval that arrives after shorter ones overlaps blocks the sweep already closed; `[[1,10],[2,3],[4,5]]` sorted by end becomes `[[2,3],[4,10]]`.
- **Aliasing the input.** Appending the caller's inner list and then extending it in place silently rewrites the input; copy it.
- **Comparing with `merged[0]`.** Only the *last* merged interval can still grow.
