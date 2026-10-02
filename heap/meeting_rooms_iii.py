"""
Meeting Rooms III (LeetCode 2402)  — Hard
Pattern: Two heaps (free rooms by id, busy rooms by end time) over a sorted sweep

Problem
-------
There are n rooms numbered 0..n-1 and meetings [start, end) with distinct starts. Each meeting
takes the lowest-numbered free room; if none is free it is delayed until the earliest room
frees up (ties: lowest number), keeping its original duration. Return the room that hosts the
most meetings (lowest number on ties).
Example: n=2, [[0,10],[1,5],[2,7],[3,4]] -> 0 (room 0: [0,10],[10,11]; room 1: [1,5],[5,10]
after the delay; both host 2, so answer 0).

Brute force
-----------
Keep an array end[r] of when each room becomes free. Process meetings in start order; for each
one scan all n rooms: pick the lowest-numbered room with end[r] <= start, or, if none, the
room with the smallest end[r] (lowest number on ties) and delay the meeting to that time.
O(m log m + m*n) time, O(n) space. The waste: every meeting rescans all n rooms although the
set of free rooms changes by only a few entries between consecutive meetings.

From brute force to optimal
---------------------------
The redundancy is the full scan over rooms to answer two questions: "lowest free room id" and
"earliest-ending busy room". Each is a min-query over a set that only changes incrementally, so
give each its own min-heap: free holds room ids, busy holds (end, room). Sweeping meetings by
start, first move every busy room with end <= start into free (expired meetings). If free is
non-empty its root is the answer; otherwise the busy root (end, room) is the earliest to free
up, with ties broken by room id automatically by tuple ordering; the meeting is rescheduled to
[end, end + duration] in that room. Each meeting does O(1) heap operations, each room moves
between heaps at most once per meeting: O((m + n) log n) after the O(m log m) sort.

Intuition
---------
Two queues of rooms: idle ones ordered by number, busy ones ordered by when they finish.
Meetings arrive in time order, so before placing one we release every room whose meeting has
finished by now. The lowest idle room wins; if there are none the soonest-free room wins and
the meeting simply slides forward to that moment. Counting assignments per room gives the
answer.

Geometric view
--------------
Rooms are horizontal lanes stacked top to bottom, time runs right. Meetings are bars placed
on lanes at their start; a sweep line at each new start pulls finished bars' lanes into the
"free" pile (a min-heap by lane number) and leaves running bars in the "busy" pile (a min-heap
by right edge). A new bar lands in the top-most free lane, or, if every lane is occupied at the
sweep line, is pushed right until the earliest right edge and glued onto that lane.

Steps
-----
1. Sort meetings by start. free = heapified [0..n-1]; busy = [] of (end, room); count = [0]*n.
2. For (s, e): while busy and busy[0].end <= s: pop and push its room onto free.
3. If free: room = heappop(free); end = e.
   Else: (t, room) = heappop(busy); end = t + (e - s).
4. heappush(busy, (end, room)); count[room] += 1.
5. Return the index of the max count (first one on ties).

Complexity: O(m log m + (m + n) log n) time, O(n) space — sort, then O(1) heap ops per meeting on
heaps of size <= n.
Pitfalls: Not releasing ALL expired rooms before choosing (a lower-numbered free room would be
missed); forgetting to preserve the duration when delaying; releasing with < instead of <=
(a meeting may start exactly when a room frees).
"""
import heapq
from typing import List


class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()
        free = list(range(n))                          # min-heap of idle room ids
        busy = []                                      # min-heap of (end time, room id)
        count = [0] * n
        for start, end in meetings:
            while busy and busy[0][0] <= start:        # release every room that has finished
                _, room = heapq.heappop(busy)
                heapq.heappush(free, room)
            if free:
                room = heapq.heappop(free)
            else:                                      # all busy: wait for the earliest, lowest id
                t, room = heapq.heappop(busy)
                end = t + (end - start)                # same duration, delayed start
            heapq.heappush(busy, (end, room))
            count[room] += 1
        return count.index(max(count))


def brute_force(n: int, meetings: List[List[int]]) -> int:
    # Scan all n rooms for every meeting: lowest free room, else earliest-free room.
    meetings = sorted(meetings)
    free_at = [0] * n
    count = [0] * n
    for start, end in meetings:
        room = next((r for r in range(n) if free_at[r] <= start), -1)
        if room < 0:
            room = min(range(n), key=lambda r: (free_at[r], r))
            end = free_at[room] + (end - start)
        free_at[room] = end
        count[room] += 1
    return count.index(max(count))


if __name__ == "__main__":
    s = Solution()
    cases = (
        ((2, [[0, 10], [1, 5], [2, 7], [3, 4]]), 0),
        ((3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]), 1),
        ((1, [[0, 5], [1, 2], [3, 4]]), 0),                 # one room, everything queues
        ((4, [[18, 19], [3, 12], [17, 19], [2, 13], [7, 10]]), 0),
        ((2, [[0, 2], [2, 3], [1, 5]]), 0),                  # release at exactly start
    )
    for args, want in cases:
        assert s.mostBooked(args[0], [m[:] for m in args[1]]) == want, (args, want)
        assert brute_force(*args) == want, (args, want)
    import random
    random.seed(2402)
    for _ in range(200):
        n = random.randint(1, 5)
        starts = random.sample(range(0, 40), random.randint(1, 10))
        ms = [[st, st + random.randint(1, 15)] for st in starts]
        assert s.mostBooked(n, [m[:] for m in ms]) == brute_force(n, ms), (n, ms)
    print("ok")
