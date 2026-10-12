---
rank: 27
slug: meeting_rooms_ii
---

Given meetings as half-open intervals `[start, end)`, return the fewest rooms that can host them all; a meeting may start the moment another one ends. For `[[0, 30], [5, 10], [10, 20], [15, 25]]` the answer is 3: at time 15 the meetings `[0, 30)`, `[10, 20)` and `[15, 25)` are all running, while `[10, 20)` can take over the room that `[5, 10)` frees at 10.

The brute force stands at every meeting's start, counts the meetings in progress and keeps the maximum, `O(n²)`. That peak overlap is the answer, and a heap finds it in `O(n log n)`. Take the meetings in order of start and keep one entry per room in a min-heap: the time that room becomes free. Only the top matters, the room that frees up first. If it is free by the new meeting's start, the meeting takes it over: pop the old end, push the new one. If even that room is busy, every room is busy, and the meeting opens a new room with a push alone. The heap never shrinks, so its final size is the number of rooms, and none of them is wasted: a room opens only when every existing room holds a meeting that began no later and ends after `start`, so all of them overlap the newcomer at that instant.

The same number falls out of a sweep line. Turn each meeting into two events, `+1` at its start and `-1` at its end, sort them by time and run a counter across them; the counter's peak is the answer. At equal times the ends must come first, since a meeting that ends at 10 hands its room to one that starts at 10, and sorting `(time, delta)` pairs does that because `-1` sorts before `+1`.

```text
time     0    5    10   15   20   25   30
room 1   ├─────────────────────────────┤      [0, 30)
room 2        ├────┼─────────┤                [5, 10) then [10, 20)
room 3                  ├─────────┤           [15, 25)

meeting    earliest end ≤ start?        end times in the heap
[0, 30)    heap empty → new room 1      [30]
[5, 10)    30 > 5 → new room 2          [10, 30]
[10, 20)   10 ≤ 10 → reuse room 2       [20, 30]
[15, 25)   20 > 15 → new room 3         [20, 25, 30]
rooms = size of the heap = 3
```

```pseudo
FUNCTION MinMeetingRooms(intervals)
    ends ← empty min-heap                   // one end time per room
    FOR EACH [start, end] IN sorted(intervals)  // earliest start first
        IF len(ends) > 0 AND ends.top() ≤ start
            ends.pop()                      // the room that frees first is free
        ends.push(end)                      // this room is busy until end
    RETURN len(ends)
```

Sorting costs `O(n log n)` and each meeting makes at most one pop and one push, so the run is `O(n log n)` time and `O(n)` space. Reach for it whenever a problem asks how many things run at once: rooms, platforms, servers, bookings. Car Pooling is the sweep with passenger counts in place of `+1`; Divide Intervals Into Minimum Number of Groups is this problem with closed intervals, so a group frees up only when its end is strictly less than the new start; My Calendar III keeps the sweep in a sorted map. The classic mistake is testing `<` instead of `≤`, which treats `[1, 5)` and `[5, 10)` as a clash and answers 2 instead of 1. Another is popping every finished meeting in a loop and returning the final heap size, which has shrunk by then: `[[1, 10], [2, 3], [11, 12]]` answers 1 instead of 2.

*Practice:* LC 253 Meeting Rooms II · LC 1094 Car Pooling · LC 2406 Divide Intervals Into Minimum Number of Groups · LC 732 My Calendar III
