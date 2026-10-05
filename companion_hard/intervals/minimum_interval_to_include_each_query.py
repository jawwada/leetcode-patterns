"""
Minimum Interval to Include Each Query (LeetCode 1851) - Hard
Chapter: intervals
Pattern: Offline queries sorted + sweep by start + min-heap by size with lazy removal

Given intervals [left, right] and queries q, answer each query with the size (right - left + 1)
of the smallest interval containing q, or -1 if none does. Keep the original query order.
Example: intervals = [[1, 4], [2, 4], [3, 6], [4, 4]], queries = [2, 3, 4, 5] -> [3, 3, 1, 4]
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def brute_force(intervals, queries):
    """For each query scan every interval and keep the smallest one that contains it. O(nm)."""
    answers = []
    for q in queries:
        best = -1
        for left, right in intervals:
            if left <= q <= right:
                size = right - left + 1
                if best == -1 or size < best:
                    best = size
        answers.append(best)
    return answers


# --- optimal ---
def min_interval(intervals, queries):
    """Answer queries in sorted order; intervals enter a min-heap by size as their left edge
    passes and are dropped lazily once their right edge is behind. O((n + m) log(n + m))."""
    intervals = sorted(intervals)             # by left edge
    order = []                                # (query value, original position)
    for position in range(len(queries)):
        order.append((queries[position], position))
    order.sort()
    answers = [-1] * len(queries)
    candidates = []                           # min-heap of (size, right)
    next_interval = 0
    for q, position in order:
        while next_interval < len(intervals) and intervals[next_interval][0] <= q:
            left, right = intervals[next_interval]
            heapq.heappush(candidates, (right - left + 1, right))   # it has started
            next_interval += 1
        while candidates and candidates[0][1] < q:
            heapq.heappop(candidates)         # the smallest candidate ended before q: drop it
        if candidates:
            answers[position] = candidates[0][0]
    return answers


# --- try the brute force ---
print(brute_force([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]))        # -> [3, 3, 1, 4]
print(brute_force([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]))    # -> [2, -1, 4, 6]
print(brute_force([[5, 9]], [4]))                                         # -> [-1]
print(brute_force([[1, 10], [3, 4], [3, 4]], [4, 4, 1]))                  # -> [2, 2, 10]


# --- try the optimal ---
print(min_interval([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]))        # -> [3, 3, 1, 4]
print(min_interval([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]))    # -> [2, -1, 4, 6]
print(min_interval([[5, 9]], [4]))                                         # -> [-1]
print(min_interval([[1, 10], [3, 4], [3, 4]], [4, 4, 1]))                  # -> [2, 2, 10]
