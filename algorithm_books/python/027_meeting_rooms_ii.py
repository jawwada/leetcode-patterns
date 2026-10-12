"""
Meeting Rooms II - Minimum Rooms with a Heap of End Times

Given meetings as half-open intervals [start, end), return the fewest rooms
that can host them all; a meeting may start the moment another one ends:
[[0, 30], [5, 10], [10, 20], [15, 25]] -> 3.
"""
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def min_meeting_rooms(intervals):
    """Sort by start; a min-heap holds the time each room frees up.
    O(n log n) time, O(n) space."""
    ends = []                               # min-heap: one end time per room
    for start, end in sorted(intervals):    # earliest start first
        if len(ends) > 0 and ends[0] <= start:
            heapq.heappop(ends)             # the room that frees first is free
        heapq.heappush(ends, end)           # this room is busy until end
    return len(ends)


# --- try it ---
meetings = [[0, 30], [5, 10], [10, 20], [15, 25]]
print(min_meeting_rooms(meetings))                      # -> 3
print(min_meeting_rooms([[0, 30], [5, 10], [15, 20]]))  # -> 2
print(min_meeting_rooms([[7, 10], [2, 4]]))             # -> 1
print(min_meeting_rooms([]))                            # -> 0
