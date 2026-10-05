"""
Course Schedule III (LeetCode 630) - Hard
Chapter: heap
Pattern: Sort by deadline + max-heap of taken durations (swap out the longest)

Course i takes duration[i] days and must be finished on or before last_day[i]. You start on
day 1 and take courses one at a time, back to back. Return the maximum number of courses you
can complete.
Example: [[100,200],[200,1300],[1000,1250],[2000,3200]] -> 3. [[3,2],[4,3]] -> 0.
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def by_deadline(courses):
    """(deadline, duration) pairs sorted by deadline: any feasible set works in this order."""
    pairs = []
    for duration, last_day in courses:
        pairs.append((last_day, duration))
    pairs.sort()
    return pairs


def brute_force(courses):
    """Try every subset in deadline order; keep the largest feasible one. O(2^n n) time."""
    ordered = by_deadline(courses)
    n = len(ordered)
    best = 0
    for mask in range(1 << n):                 # bit i of mask = 1 means we take course i
        time = 0
        count = 0
        feasible = True
        for i in range(n):
            if (mask >> i) & 1 == 1:
                last_day, duration = ordered[i]
                time += duration
                count += 1
                if time > last_day:            # this course would finish past its deadline
                    feasible = False
                    break
        if feasible:
            best = max(best, count)
    return best


# --- optimal ---
def schedule_course(courses):
    """Take courses by deadline; when over time, drop the longest one taken so far. O(n log n)."""
    ordered = []                               # (deadline, duration) sorted by deadline
    for duration, last_day in courses:
        ordered.append((last_day, duration))
    ordered.sort()
    taken = []                                 # -duration of kept courses: root = the longest
    time = 0
    for last_day, duration in ordered:
        heapq.heappush(taken, -duration)
        time += duration
        if time > last_day:                    # over the deadline: evict the longest course
            longest = -heapq.heappop(taken)    # frees the most time, count stays the same
            time -= longest
    return len(taken)


# --- try the brute force ---
print(brute_force([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]))              # -> 3
print(brute_force([[3, 2], [4, 3]]))                                                    # -> 0
print(brute_force([[5, 5], [4, 6], [2, 6]]))                                            # -> 2
print(brute_force([[7, 17], [3, 12], [10, 20], [9, 10], [5, 20], [10, 19], [4, 18]]))   # -> 4


# --- try the optimal ---
print(schedule_course([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]))              # -> 3
print(schedule_course([[3, 2], [4, 3]]))                                                    # -> 0
print(schedule_course([[5, 5], [4, 6], [2, 6]]))                                            # -> 2
print(schedule_course([[7, 17], [3, 12], [10, 20], [9, 10], [5, 20], [10, 19], [4, 18]]))   # -> 4
