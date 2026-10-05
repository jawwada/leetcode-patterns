"""
Employee Free Time (LeetCode 759) - Hard
Chapter: intervals
Pattern: K-way merge of sorted interval lists with a min-heap, emitting gaps

schedule[i] is the sorted, non-overlapping list of working shifts [start, end] of employee i.
Return the finite gaps of positive length during which every employee is free, in sorted order.
Example: [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]] -> [[3, 4]]
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def nobody_works(shifts, gap_start, gap_end):
    """True when no shift reaches strictly inside (gap_start, gap_end). O(N) time."""
    for start, end in shifts:
        if start < gap_end and end > gap_start:
            return False
    return True


def brute_force(schedule):
    """Try every (shift end, shift start) pair as a gap; keep the empty ones. O(N^3) time."""
    all_shifts = []
    for shifts in schedule:
        for shift in shifts:
            all_shifts.append(shift)
    gaps = []
    for first in all_shifts:
        for second in all_shifts:
            gap_start = first[1]              # a gap begins where some shift ends
            gap_end = second[0]               # and finishes where some shift starts
            if gap_start < gap_end and nobody_works(all_shifts, gap_start, gap_end):
                if [gap_start, gap_end] not in gaps:
                    gaps.append([gap_start, gap_end])
    gaps.sort()
    return gaps


# --- optimal ---
def employee_free_time(schedule):
    """Merge all lists by start with a heap; a gap opens when a start passes the furthest end.
    O(N log k) time for N shifts and k employees."""
    heap = []                                 # (start, employee, position in that list)
    for employee in range(len(schedule)):
        if len(schedule[employee]) > 0:
            heapq.heappush(heap, (schedule[employee][0][0], employee, 0))
    free = []
    busy_until = None                         # furthest end of busy time seen so far
    while heap:
        start, employee, position = heapq.heappop(heap)
        end = schedule[employee][position][1]
        if busy_until is not None and start > busy_until:
            free.append([busy_until, start])  # nobody works between busy_until and start
        if busy_until is None or end > busy_until:
            busy_until = end
        if position + 1 < len(schedule[employee]):
            next_start = schedule[employee][position + 1][0]
            heapq.heappush(heap, (next_start, employee, position + 1))
    return free


# --- try the brute force ---
print(brute_force([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]))               # -> [[3, 4]]
print(brute_force([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]))       # -> [[5, 6], [7, 9]]
print(brute_force([[[1, 2]], [[2, 3]]]))                                   # -> []
print(brute_force([[[1, 2]], [], [[5, 6]]]))                               # -> [[2, 5]]


# --- try the optimal ---
print(employee_free_time([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]))               # -> [[3, 4]]
print(employee_free_time([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]))   # -> [[5, 6], [7, 9]]
print(employee_free_time([[[1, 2]], [[2, 3]]]))                                   # -> []
print(employee_free_time([[[1, 2]], [], [[5, 6]]]))                               # -> [[2, 5]]
