"""
The Skyline Problem (LeetCode 218) - Hard
Chapter: heap
Pattern: Sweep line over events + max-heap with lazy removal

Buildings are given as [left, right, height] rectangles on a shared ground line. Return the
skyline as key points [x, y] where the outline's height changes, sorted by x and ending with a
point of height 0; consecutive points must not share a height.
Example: [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
-> [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]].
"""
import heapq                       # heappush / heappop keep the smallest item at index 0
import math                        # math.inf: a right edge no sweep ever reaches


# --- brute force ---
def tallest_at(buildings, x):
    """Height of the tallest building covering x (left <= x < right), 0 if none."""
    tallest = 0
    for left, right, height in buildings:
        if left <= x < right:
            tallest = max(tallest, height)
    return tallest


def brute_force(buildings):
    """At every edge x rescan all buildings for the tallest one covering x. O(n^2) time."""
    edges = set()
    for left, right, height in buildings:
        edges.add(left)
        edges.add(right)
    out = []
    previous = 0
    for x in sorted(edges):                    # the outline can only change at an edge
        height = tallest_at(buildings, x)
        if height != previous:
            out.append([x, height])
            previous = height
    return out


# --- optimal ---
def get_skyline(buildings):
    """Sweep sorted edges with a max-heap of live buildings; drop ended ones lazily. O(n log n)."""
    events = []                                # (x, -height, right) for starts, (x, 0, 0) for ends
    for left, right, height in buildings:
        events.append((left, -height, right))  # at equal x: starts before ends, tallest first
        events.append((right, 0, 0))
    events.sort()
    live = [(0, math.inf)]                     # (-height, right): root = tallest; ground sentinel
    out = []
    previous = 0
    for x, neg_height, right in events:
        while live[0][1] <= x:                 # lazy removal: the tallest has already ended
            heapq.heappop(live)
        if neg_height != 0:
            heapq.heappush(live, (neg_height, right))
        tallest = -live[0][0]
        if tallest != previous:                # the maximum changed: a corner of the outline
            out.append([x, tallest])
            previous = tallest
    return out


# --- try the brute force ---
print(brute_force([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]))
# -> [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]
print(brute_force([[0, 2, 3], [2, 5, 3]]))    # -> [[0, 3], [5, 0]]
print(brute_force([[1, 5, 3], [2, 4, 3]]))    # -> [[1, 3], [5, 0]]
print(brute_force([[1, 3, 4], [3, 6, 2]]))    # -> [[1, 4], [3, 2], [6, 0]]


# --- try the optimal ---
print(get_skyline([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]))
# -> [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]
print(get_skyline([[0, 2, 3], [2, 5, 3]]))    # -> [[0, 3], [5, 0]]
print(get_skyline([[1, 5, 3], [2, 4, 3]]))    # -> [[1, 3], [5, 0]]
print(get_skyline([[1, 3, 4], [3, 6, 2]]))    # -> [[1, 4], [3, 2], [6, 0]]
