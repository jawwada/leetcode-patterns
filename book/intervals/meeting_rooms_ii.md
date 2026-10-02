# Meeting Rooms II
*LeetCode 253 · Medium · Pattern: Sort by start + min-heap of end times · Reading time ~8 min*

## What the problem is really asking

Meetings are half-open intervals `[start, end)`. A meeting ending at 10 frees its room for one starting at 10. Every meeting must happen, and two meetings in the same room may not overlap. What is the fewest rooms that works?

Restated geometrically: stack the bars on top of each other and find **the tallest point of the pile**. If at some instant k meetings are running, you need at least k rooms. Conversely, if you never have more than k running at once, k rooms suffice, because whenever a meeting starts, fewer than k are running, so some room is free. So the answer is a single integer, the maximum overlap.

What makes it hard is that "running at this instant" changes constantly. Meetings end while others start, and recounting from scratch at every moment is wasteful.

Running example: `[[1,10],[2,7],[3,19],[8,12],[10,20],[11,30]]`, answer 4.

```text
[1,10]    [========)
[2,7]      [====)
[3,19]      [===============)
[8,12]           [===)
[10,20]            [=========)
[11,30]             [==================)
         |----|----|----|----|----|----|
         0    5    10   15   20   25   30
                      ^
            at t=11: [3,19) [8,12) [10,20) [11,30) -> 4
```

## Do it by hand first

Imagine you are the receptionist with a whiteboard of rooms. Meetings show up in order of start time. For each one you ask: "Is any room free right now?" To answer quickly, you look at the room that frees up **soonest**. If even that one is still busy, every room is busy, so you open a new room.

```text
 t=1  [1,10) arrives   rooms: R1 busy till 10
 t=2  [2,7)  arrives   soonest free 10 > 2  -> open R2 (7)
 t=3  [3,19) arrives   soonest free 7 > 3   -> open R3 (19)
 t=8  [8,12) arrives   soonest free 7 <= 8  -> reuse R2 (12)
 t=10 [10,20) arrives  soonest free 10 <= 10 -> reuse R1 (20)
 t=11 [11,30) arrives  soonest free 12 > 11 -> open R4 (30)
```

What did you track? A collection of "room frees at time X" numbers. You only ever asked two things of it: what is the smallest number, and remove it or add a new one. That is a min-heap's job description. You also processed meetings in start order, which is the sort.

## The first honest attempt

"The peak overlap happens at some meeting's start. Coverage only goes up at a start, so a maximum is reached right at one. So for every start time t, count meetings with `start <= t < end`, and take the max."

That is O(n^2) time and O(1) space. Where is the repeated work? Look at consecutive start times. Between t = 10 and t = 11, almost nothing changed: one meeting started, none ended. Yet the brute force rescans all six meetings at t = 11 as if it knew nothing.

```text
 t=10: test [1,10) [2,7) [3,19) [8,12) [10,20) [11,30) -> 3
 t=11: test [1,10) [2,7) [3,19) [8,12) [10,20) [11,30) -> 4
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        identical questions; only [11,30) is new
```

The count at one start time is the count at the previous start time, plus one for the arriving meeting, minus the meetings that ended in between. If we could find those ending meetings without scanning everything, each step would be cheap.

## The turning point

**Claim: when meetings are processed in start order, the meetings to retire before the new one are exactly those with the smallest end times, so a min-heap of end times gives you the running set in O(log n) per change.**

Justify it. Keep a collection `ends` holding the end time of every meeting that is currently running, meaning it has started and has not yet ended. When a meeting `[s, e)` arrives, which running meetings have finished by time s? Exactly those with `end <= s`. Those are the smallest values in `ends`, because anything with end <= s is smaller than anything with end > s. So: peek at the minimum, and pop while `min <= s`. Then push `e`. After that, `len(ends)` is the number of meetings running at time s, and the answer is the maximum of that over all arrivals.

```text
 the running set as a heap (triangle) and as Python's array

          7                ends = [7, 10, 19]
        /   \                      ^ ends[0] is the min
      10     19            pop while ends[0] <= next start
```

Two details deserve attention.

**`<=`, not `<`.** Meetings are half-open. One ending at 10 and one starting at 10 can share a room, so `end == start` frees the room. With `<`, the receptionist would open an unnecessary room every time meetings run back to back.

**`while`, not `if`.** Several rooms can free up between two arrivals. If you pop only one per arrival, the heap holds some dead rooms. The peak is still correct in fact (the heap then counts rooms ever opened, and you only open a room when the minimum end is still busy, which means every room is busy), but `len(ends)` no longer means "running right now". Using `while` keeps the meaning clean.

The same skyline can also be computed with +1/-1 events, as in the background chapter. The heap version is worth learning here because the next two problems need the heap. My Calendar III uses events.

## Watch it work

Sorted by start: `[1,10) [2,7) [3,19) [8,12) [10,20) [11,30)`. State: the heap `ends` (triangle and array) and `rooms` = max size so far.

**Frame 1.** `[1,10)`: the heap is empty, so nothing to pop. Push 10.

```text
 arrive [1,10)        10          ends  = [10]
                                  rooms = 1
```

One meeting is running.

**Frame 2.** `[2,7)`: min 10 > 2, so nothing is free. Push 7, which rises to the top.

```text
 arrive [2,7)          7          ends  = [7, 10]
                      /           rooms = 2
                    10
```

The heap keeps the soonest-ending room on top, and 7 beats 10.

**Frame 3.** `[3,19)`: min 7 > 3. Push 19.

```text
 arrive [3,19)         7          ends  = [7, 10, 19]
                      / \         rooms = 3
                    10   19
```

Three meetings run at t = 3.

**Frame 4.** `[8,12)`: min 7 <= 8, so pop 7 (`[2,7)` is over). The next min is 10 > 8, so stop. Push 12.

```text
 arrive [8,12)  pop 7  10         ends  = [10, 19, 12]
                      / \         rooms = 3
                    19   12
```

The array is `[10, 19, 12]`, not sorted. Only `ends[0]` is guaranteed to be the minimum.

**Frame 5.** `[10,20)`: min 10 <= 10, so pop 10 (back-to-back reuse). The next min is 12 > 10. Push 20.

```text
 arrive [10,20) pop 10  12        ends  = [12, 19, 20]
                       / \        rooms = 3
                     19   20
```

Here `<=` saved a room.

**Frame 6.** `[11,30)`: min 12 > 11, so nothing is free. Push 30, and the size hits 4.

```text
 arrive [11,30)         12        ends  = [12, 19, 20, 30]
                       /  \       rooms = 4
                     19    20
                    /
                  30
```

All meetings are processed, and the answer is 4, matching the solution.

Invariant across frames: after each arrival at time s, `ends` held exactly the end times of meetings with `start <= s < end`, so its size was the live overlap at s, and `rooms` was the maximum of those sizes so far.

## Why it is correct

Two halves.

**Lower bound.** At the arrival in Frame 6 (t = 11), the heap holds 4 meetings that all contain t = 11. Four meetings running at one instant need four distinct rooms, so no schedule uses fewer than the peak heap size.

**Upper bound.** Assign rooms greedily: an arriving meeting takes any room whose meeting has ended (one exists if the heap popped something), or else a new room. Rooms in use at any arrival equals the heap size, so the number of rooms ever opened equals the peak heap size.

Together the answer is exactly the peak. The heap invariant itself holds by induction. Before an arrival at s, the heap has every running meeting from the previous arrival time. Popping all ends `<= s` removes exactly those that finished, and nothing that finished can be hidden below a larger value, by heap order. Pushing `e` adds the newcomer.

## Cost

- **Time O(n log n).** Sorting is O(n log n). Each meeting is pushed once and popped at most once, at O(log n) each.
- **Space O(n).** In the worst case all meetings overlap and the heap holds n ends.

With a plain list instead of a heap, finding and removing the minimum is O(n), so the total is O(n^2). The event-sweep version is also O(n log n) for the sort with O(n) for the events, and it is often shorter to write.

## Variations you will meet

- **Meeting Rooms I** (252): can one person attend all? Sort by start and check `prev.end <= next.start` for each adjacent pair, which is the same as asking whether the peak is 1.
- **Minimum platforms / car pooling** (1094): each interval carries a weight (passengers). Push +w and -w events and check the running sum against capacity. Use the event version with weights.
- **Which room does each meeting get?** (2402, Meeting Rooms III): keep two heaps, free rooms by index and busy rooms by end time. Delays push meetings later.
- **Bookings arrive one at a time** and you must report the peak after each: My Calendar III, two problems ahead.

## What to carry forward

The minimum number of rooms is the maximum overlap, and a min-heap of end times, popped while `top <= start`, keeps the live set as the sweep moves through starts. The next problem, Employee Free Time, uses a heap again, but now to pull intervals in start order out of k separately sorted schedules, and it watches the gaps instead of the peaks.
