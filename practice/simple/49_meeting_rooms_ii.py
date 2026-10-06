"""
Meeting Rooms II (LeetCode 253)
Return the minimum number of rooms needed to hold all meetings.
  [[0,30],[5,10],[15,20]]  ->  2

Idea: process meetings by start time. A min-heap holds the end time of each busy room;
      the top is the room that frees up first. Free finished rooms, then take one.

Pseudocode:
  sort by start
  ends = min-heap
  for start, end in meetings:
      while ends and ends.top <= start: pop     # those rooms are free now
      push end                                  # take a room
      rooms = max(rooms, len(ends))

Time O(n log n), space O(n).
"""
import heapq


def min_meeting_rooms(intervals):
    intervals = sorted(intervals, key=lambda iv: iv[0])     # sort by start
    ends = []                                    # min-heap of end times of busy rooms
    rooms = 0
    for start, end in intervals:
        while ends and ends[0] <= start:         # free rooms that have ended
            heapq.heappop(ends)
        heapq.heappush(ends, end)                # take a room
        rooms = max(rooms, len(ends))            # peak occupancy
    return rooms


if __name__ == "__main__":
    print(min_meeting_rooms([[0, 30], [5, 10], [15, 20]]))  # 2
    print(min_meeting_rooms([[7, 10], [2, 4]]))             # 1
    print(min_meeting_rooms([[1, 5], [2, 6], [3, 7]]))      # 3
