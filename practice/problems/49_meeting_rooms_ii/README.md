# Meeting Rooms II (LeetCode 253)

**Area:** intervals / heap · **Difficulty:** Medium · **Key operations:** sort by start, pop every end time <= start, push the new end, track the max heap size

## Problem

Given meeting time intervals `[start, end)`, return the minimum number of conference rooms needed so that no two meetings in the same room overlap. A meeting may start at the exact moment another one ends.

## Example

```
intervals = [[0,30],[5,10],[15,20]] -> 2

time   0    5    10   15   20   25   30
room A [-----------------------------]
room B      [----]    [----]
```

`[5,10]` and `[15,20]` never overlap each other, so they share a room, but both overlap `[0,30]`.

## Brute force

The number of rooms needed is the maximum number of meetings in progress at any instant. Sweep every time unit `t` from 0 to the latest end and count the meetings with `start <= t < end`; the answer is the peak.

O(n·C) time for coordinate range `C`, O(1) space. The wasted work: recounting from scratch at every instant, although the count only changes when a meeting starts or ends. (Counting only at each meeting's start time is O(n²) and still rescans all meetings each time.)

## From brute force to optimal

Process meetings in start order. The set of meetings in progress changes in just two ways: the new meeting joins, and every meeting whose end is at or before the new start leaves. To evict the finished ones cheaply we need the *smallest* end time among the running meetings, which is exactly what a min-heap of end times provides. For each arriving meeting, pop every end `<= start` (those rooms are free again), push its end, and the heap size is the number of rooms in use right now. The largest size seen is the answer.

## Intuition

Picture the rooms as shelves and each meeting as a bar laid on a shelf from its start to its end. Meetings arrive in start order. Before placing a new bar, look at the shelf that frees up soonest (the heap top): if that meeting has already ended, clear the shelf, and keep clearing while shelves are free. Then the new bar takes any free shelf, or a brand-new one. The tallest stack of shelves ever in use is the number of rooms you were forced to have. The heap only needs to answer "which room frees up first?", so it stores end times and nothing else.

## Walkthrough

Heap shown as its array (smallest at index 0).

```
sorted by start: [[0,30],[5,10],[15,20]]

[0,30]    nothing to free            push 30     ends [30]       in use 1   peak 1
[5,10]    top 30 > 5, nothing free   push 10     ends [10,30]    in use 2   peak 2
[15,20]   top 10 <= 15 -> pop 10     ends [30]
          top 30 > 15, stop          push 20     ends [20,30]    in use 2   peak 2
return 2
```

## Steps

1. Sort the intervals by start.
2. `ends = []` (min-heap), `rooms = 0`.
3. For each `[start, end]`: while the heap is non-empty and `ends[0] <= start`, pop (that room is free).
4. Push `end`. `rooms = max(rooms, len(ends))`.
5. Return `rooms`.

## Complexity

O(n log n) time: the sort, then one push and at most one pop per meeting. O(n) space for the heap.

## Pitfalls

- **`<` instead of `<=` when freeing.** A meeting ending exactly at the new start has finished; `[[1,5],[5,10]]` needs one room, not two.
- **Returning the final heap size.** The peak can happen early; `[[0,1],[0,1],[5,6]]` ends with one room in use but needed two.
- **Sorting by end.** A long early meeting then arrives last and finds rooms that were freed by meetings it actually overlaps: `[[1,2],[1,3],[0,10],[4,5]]` gives 2 instead of 3.
- **Pushing the start instead of the end.** The heap must hold when each room becomes free.
- **Popping only one room (`if` instead of `while`).** Several meetings can end before the new one starts; freeing one per arrival leaves stale entries in the heap. (The reported peak happens to stay correct, but the heap no longer shows the rooms actually in use, and you should be able to explain why.)
