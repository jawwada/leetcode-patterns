"""
Meeting Rooms II (LeetCode 253) - Medium
Chapter: intervals
Pattern: Sort by start + min-heap of end times

Given meeting intervals [start, end), return the minimum number of conference rooms needed so
that no two meetings in the same room overlap. A meeting may start at the exact moment another
one ends.
Example: [[0,30],[5,10],[15,20]] -> 2; [[7,10],[2,4]] -> 1.
"""
import heapq                       # heappush / heappop keep the smallest at index 0


# --- brute force ---
def brute_force(intervals):
    """At every meeting's start time count the meetings in progress; take the max. O(n^2) time."""
    best = 0
    for start, _ in intervals:       # the peak always happens at some meeting's start
        running = 0
        for other_start, other_end in intervals:
            if other_start <= start and start < other_end:   # in progress at this instant
                running += 1
        best = max(best, running)
    return best


# --- optimal ---
def meeting_rooms_ii(intervals):
    """Sort by start; a min-heap of end times says when each busy room frees up. O(n log n)."""
    intervals.sort()
    ends = []                        # min-heap: end times of the meetings holding a room right now
    rooms = 0
    for start, end in intervals:
        while ends and ends[0] <= start:
            heapq.heappop(ends)      # that meeting is over: its room is free again
        heapq.heappush(ends, end)    # this meeting takes a room
        rooms = max(rooms, len(ends))    # rooms in use right now
    return rooms


# --- try the brute force ---
print(brute_force([[0, 30], [5, 10], [15, 20]]))                                 # -> 2
print(brute_force([[7, 10], [2, 4]]))                                            # -> 1
print(brute_force([[1, 5], [5, 10]]))                                            # -> 1
print(brute_force([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]]))      # -> 4


# --- try the optimal ---
print(meeting_rooms_ii([[0, 30], [5, 10], [15, 20]]))                            # -> 2
print(meeting_rooms_ii([[7, 10], [2, 4]]))                                       # -> 1
print(meeting_rooms_ii([[1, 5], [5, 10]]))                                       # -> 1
print(meeting_rooms_ii([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]])) # -> 4
