"""
Smallest Range Covering Elements from K Lists (LeetCode 632) - Hard
Chapter: heap
Pattern: K-way merge with a min-heap of list pointers (track the running max)

Given k sorted integer lists, find the smallest range [a, b] that contains at least one number
from every list; [a, b] beats [c, d] if b - a < d - c, or if equal and a < c.
Example: [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]] -> [20,24].
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def covers(lists, low, high):
    """True when every list has at least one value inside [low, high]."""
    for row in lists:
        found = False
        for value in row:
            if low <= value <= high:
                found = True
                break
        if not found:
            return False
    return True


def brute_force(lists):
    """Try every (low, high) pair of values that occur; keep the narrowest that covers. O(V^2 N)."""
    values = set()
    for row in lists:
        for value in row:
            values.add(value)
    values = sorted(values)
    best = None
    for a in range(len(values)):
        for b in range(a, len(values)):            # the first covering high for this low is best
            if covers(lists, values[a], values[b]):
                if best is None or values[b] - values[a] < best[1] - best[0]:
                    best = [values[a], values[b]]
                break
    return best


# --- optimal ---
def smallest_range(lists):
    """One pointer per list in a min-heap: root = low end, running max = high end. O(N log k)."""
    heap = []                                  # (value, list index, position): root = smallest
    current_max = lists[0][0]
    for i in range(len(lists)):
        heapq.heappush(heap, (lists[i][0], i, 0))
        current_max = max(current_max, lists[i][0])
    best = [heap[0][0], current_max]
    while True:
        value, i, j = heapq.heappop(heap)      # smallest current element = low end of the range
        if current_max - value < best[1] - best[0]:
            best = [value, current_max]
        if j + 1 == len(lists[i]):             # list i is exhausted: no later range covers it
            return best
        next_value = lists[i][j + 1]
        heapq.heappush(heap, (next_value, i, j + 1))
        current_max = max(current_max, next_value)   # the high end only moves right


# --- try the brute force ---
print(brute_force([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]))   # -> [20, 24]
print(brute_force([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))                        # -> [1, 1]
print(brute_force([[1, 5], [4, 8]]))                                         # -> [4, 5]
print(brute_force([[-5, 0, 7], [2, 3], [-1, 9]]))                            # -> [-1, 2]


# --- try the optimal ---
print(smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]))   # -> [20, 24]
print(smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))                        # -> [1, 1]
print(smallest_range([[1, 5], [4, 8]]))                                         # -> [4, 5]
print(smallest_range([[-5, 0, 7], [2, 3], [-1, 9]]))                            # -> [-1, 2]
