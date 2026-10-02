"""
Meeting Rooms II (LeetCode 253)  — Medium
Pattern: Sort by start + min-heap of end times

Problem
-------
Given meeting intervals [start, end), return the minimum number of conference rooms
needed so that no two meetings in the same room overlap. A meeting may start exactly when
another ends.
Example: [[0,30],[5,10],[15,20]] -> 2.  [[7,10],[2,4]] -> 1.

Brute force
-----------
The answer is the maximum number of meetings in progress at any instant. For every
meeting's start time t, count how many meetings satisfy start <= t < end; take the max.
O(n^2) time, O(1) space. The waste: each start time rescans all n meetings even though
only the meetings that ended between consecutive start times changed the count.

From brute force to optimal
---------------------------
The redundancy is recounting "who is still running" from scratch at every start time.
Observation: process meetings in start order; the set of running meetings only changes by
(a) adding the new meeting and (b) removing meetings whose end <= new start. To remove
expired meetings cheaply we need quick access to the SMALLEST end time among running
meetings -- a min-heap of end times. When a new meeting arrives, pop every end <= its
start (those rooms are freed), push its end, and the heap size is the rooms in use now.
Max heap size over the sweep is the answer: O(n log n). (Plain list instead of a heap:
same algorithm but finding/removing the min is O(n), i.e. O(n^2).)

Intuition
---------
Sort by start so meetings arrive in chronological order. The heap holds "when does each
occupied room free up". For an arriving meeting, free every room whose meeting has
already ended (the top of the heap is the earliest to finish), then occupy a room. The
peak heap size is the number of rooms you were forced to have.

Geometric view
--------------
Bars on a time axis, sorted by left edge. A sweep line moves right to each start. Rooms
are shelves stacked vertically; each bar occupies a shelf from its start to its end. The
heap is the list of right edges of bars currently on shelves, sorted so the soonest-to-end
is on top. The answer is the tallest stack the sweep line ever crosses.

Steps
-----
1. Sort intervals by start.
2. heap = [] (end times), rooms = 0.
3. For [s, e]: while heap and heap[0] <= s: heappop; heappush(e); rooms = max(rooms, len(heap)).
4. Return rooms.

Complexity: O(n log n) time, O(n) space — sort plus one push/pop per meeting; heap holds <= n ends.
Pitfalls: using < instead of <= when freeing (back-to-back meetings share a room);
sorting by end; popping only one room instead of all expired ones (still correct for the
max, but the heap size then overcounts current usage -- be able to argue why).
"""
import heapq
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda iv: iv[0])
        ends = []  # min-heap of end times of meetings currently occupying a room
        rooms = 0
        for start, end in intervals:
            while ends and ends[0] <= start:
                heapq.heappop(ends)  # that room is free again
            heapq.heappush(ends, end)
            rooms = max(rooms, len(ends))
        return rooms


def brute_force(intervals: List[List[int]]) -> int:
    # At every meeting's start time, count how many meetings are in progress.
    best = 0
    for s, _ in intervals:
        running = sum(1 for a, b in intervals if a <= s < b)
        best = max(best, running)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[0, 30], [5, 10], [15, 20]], 2),
        ([[7, 10], [2, 4]], 1),
        ([[1, 5], [5, 10]], 1),
        ([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]], 4),
        ([[9, 10], [4, 9], [4, 17]], 2),
    )
    for iv, want in cases:
        assert brute_force([x[:] for x in iv]) == want
        assert s.minMeetingRooms([x[:] for x in iv]) == want
    print("ok")
