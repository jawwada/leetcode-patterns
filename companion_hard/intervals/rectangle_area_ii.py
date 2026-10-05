"""
Rectangle Area II (LeetCode 850) - Hard
Chapter: intervals
Pattern: Sweep line over sorted events

Given n axis-aligned rectangles [x1, y1, x2, y2] with coordinates up to 1e9, return the total
area covered by their union modulo 1e9 + 7; overlapping regions count once.
Example: [[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]] -> 6
"""


# --- brute force ---
def brute_force(rectangles):
    """Compress coordinates, paint every cell of every rectangle, add the painted cells. O(n^3)."""
    xs = []
    ys = []
    for x1, y1, x2, y2 in rectangles:
        xs.append(x1)
        xs.append(x2)
        ys.append(y1)
        ys.append(y2)
    xs = sorted(set(xs))                      # the distinct edges cut the plane into cells
    ys = sorted(set(ys))
    painted = []
    for i in range(len(xs) - 1):
        painted.append([False] * (len(ys) - 1))
    for x1, y1, x2, y2 in rectangles:
        for i in range(xs.index(x1), xs.index(x2)):
            for j in range(ys.index(y1), ys.index(y2)):
                painted[i][j] = True          # cell (i, j) lies inside this rectangle
    area = 0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if painted[i][j]:
                area += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return area % (10 ** 9 + 7)


# --- optimal ---
def covered_length(intervals):
    """Length of the union of y-intervals: sort by start, merge, add. O(k log k) time."""
    total = 0
    reach = None                              # the highest y counted so far
    for start, end in sorted(intervals):
        if reach is not None and start < reach:
            start = reach                     # clip away the part already counted
        if end > start:
            total += end - start
            reach = end
    return total


def rectangle_area(rectangles):
    """Sweep a vertical line over the x-edges; each strip is width * covered y-length.
    O(n^2 log n) time."""
    events = []
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 1, y1, y2))        # the rectangle enters the sweep line
        events.append((x2, -1, y1, y2))       # the rectangle leaves it
    events.sort()
    active = []                               # y-intervals the line is cutting right now
    area = 0
    previous_x = events[0][0]
    for x, kind, y1, y2 in events:
        area += (x - previous_x) * covered_length(active)   # the strip left of x
        previous_x = x
        if kind == 1:
            active.append((y1, y2))
        else:
            active.remove((y1, y2))
    return area % (10 ** 9 + 7)


# --- try the brute force ---
print(brute_force([[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]]))    # -> 6
print(brute_force([[0, 0, 1000000000, 1000000000]]))              # -> 49
print(brute_force([[0, 0, 3, 3], [1, 1, 2, 2]]))                  # -> 9
print(brute_force([[0, 0, 1, 1], [2, 2, 3, 3]]))                  # -> 2


# --- try the optimal ---
print(rectangle_area([[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]]))    # -> 6
print(rectangle_area([[0, 0, 1000000000, 1000000000]]))              # -> 49
print(rectangle_area([[0, 0, 3, 3], [1, 1, 2, 2]]))                  # -> 9
print(rectangle_area([[0, 0, 1, 1], [2, 2, 3, 3]]))                  # -> 2
