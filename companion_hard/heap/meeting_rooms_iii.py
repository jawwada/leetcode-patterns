"""
Meeting Rooms III (LeetCode 2402) - Hard
Chapter: heap
Pattern: Two heaps (free rooms by id, busy rooms by end time) over a sorted sweep

There are n rooms numbered 0..n-1 and meetings [start, end) with distinct starts. Each meeting
takes the lowest-numbered free room; if none is free it is delayed until the earliest room frees
up (ties: lowest number), keeping its duration. Return the room hosting the most meetings
(lowest number on ties). Example: n = 2, [[0,10],[1,5],[2,7],[3,4]] -> 0.
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- helpers ---
def busiest_room(count):
    """The index of the largest count, lowest index on ties."""
    best = 0
    for room in range(len(count)):
        if count[room] > count[best]:
            best = room
    return best


# --- brute force ---
def brute_force(n, meetings):
    """For every meeting scan all n rooms: lowest free one, else the earliest to free up. O(m n)."""
    meetings = sorted(meetings)
    free_at = [0] * n                          # free_at[room] = when that room becomes free
    count = [0] * n
    for start, end in meetings:
        room = -1
        for candidate in range(n):             # lowest-numbered room already free
            if free_at[candidate] <= start:
                room = candidate
                break
        if room < 0:                           # all busy: the one that frees first, lowest id
            room = 0
            for candidate in range(1, n):
                if free_at[candidate] < free_at[room]:
                    room = candidate
            end = free_at[room] + (end - start)    # delayed, same duration
        free_at[room] = end
        count[room] += 1
    return busiest_room(count)


# --- optimal ---
def most_booked(n, meetings):
    """Min-heap of free room ids and min-heap of (end, room) for busy rooms. O((m + n) log n)."""
    meetings = sorted(meetings)
    free = []                                  # room ids: the root is the lowest free room
    for room in range(n):
        heapq.heappush(free, room)
    busy = []                                  # (end time, room): the root frees up first
    count = [0] * n
    for start, end in meetings:
        while len(busy) > 0 and busy[0][0] <= start:   # release every room that has finished
            finished_end, room = heapq.heappop(busy)
            heapq.heappush(free, room)
        if len(free) > 0:
            room = heapq.heappop(free)
        else:                                  # all busy: wait for the earliest end, lowest id
            earliest_end, room = heapq.heappop(busy)
            end = earliest_end + (end - start)     # delayed, same duration
        heapq.heappush(busy, (end, room))
        count[room] += 1
    return busiest_room(count)


# --- try the brute force ---
print(brute_force(2, [[0, 10], [1, 5], [2, 7], [3, 4]]))               # -> 0
print(brute_force(3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]))      # -> 1
print(brute_force(1, [[0, 5], [1, 2], [3, 4]]))                        # -> 0
print(brute_force(4, [[18, 19], [3, 12], [17, 19], [2, 13], [7, 10]])) # -> 0


# --- try the optimal ---
print(most_booked(2, [[0, 10], [1, 5], [2, 7], [3, 4]]))               # -> 0
print(most_booked(3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]))      # -> 1
print(most_booked(1, [[0, 5], [1, 2], [3, 4]]))                        # -> 0
print(most_booked(4, [[18, 19], [3, 12], [17, 19], [2, 13], [7, 10]])) # -> 0
