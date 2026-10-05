"""
Perfect Rectangle (LeetCode 391) - Hard
Chapter: math_geometry
Pattern: Corner parity + area invariant

Given axis-aligned rectangles [x1, y1, x2, y2], return True iff together they cover some
rectangle exactly: no gaps and no overlaps.
Example: [[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]] -> True (they tile [1,1,4,4]);
[[1,1,2,3],[1,3,2,4],[3,1,4,2],[3,2,4,4]] -> False (a gap in the middle).
"""


# --- helpers ---
def bounding_box(rectangles):
    """Smallest x1, smallest y1, largest x2, largest y2 over all rectangles."""
    min_x = rectangles[0][0]
    min_y = rectangles[0][1]
    max_x = rectangles[0][2]
    max_y = rectangles[0][3]
    for x1, y1, x2, y2 in rectangles:
        min_x = min(min_x, x1)
        min_y = min(min_y, y1)
        max_x = max(max_x, x2)
        max_y = max(max_y, y2)
    return min_x, min_y, max_x, max_y


# --- brute force ---
def brute_force(rectangles):
    """No pair overlaps, and the areas add up to the bounding box. O(n^2) time, O(1) space."""
    n = len(rectangles)
    for i in range(n):
        ax1, ay1, ax2, ay2 = rectangles[i]
        for j in range(i + 1, n):
            bx1, by1, bx2, by2 = rectangles[j]
            if ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2:
                return False                       # the two overlap with positive area
    min_x, min_y, max_x, max_y = bounding_box(rectangles)
    area = 0
    for x1, y1, x2, y2 in rectangles:
        area += (x2 - x1) * (y2 - y1)
    return area == (max_x - min_x) * (max_y - min_y)


# --- optimal ---
def perfect_rectangle(rectangles):
    """Toggle each corner in a set: only the 4 outline corners survive; check the area. O(n)."""
    corners = set()
    area = 0
    for x1, y1, x2, y2 in rectangles:
        area += (x2 - x1) * (y2 - y1)
        for point in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]:
            if point in corners:
                corners.remove(point)              # a corner shared by 2 or 4 rectangles cancels
            else:
                corners.add(point)
    min_x, min_y, max_x, max_y = bounding_box(rectangles)
    outline = {(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)}
    return corners == outline and area == (max_x - min_x) * (max_y - min_y)


# --- try the brute force ---
tiling = [[1, 1, 3, 3], [3, 1, 4, 2], [3, 2, 4, 4], [1, 3, 2, 4], [2, 3, 3, 4]]
gap = [[1, 1, 2, 3], [1, 3, 2, 4], [3, 1, 4, 2], [3, 2, 4, 4]]
overlap = [[1, 1, 3, 3], [3, 1, 4, 2], [1, 3, 2, 4], [2, 2, 4, 4]]
print(brute_force(tiling))                                       # -> True
print(brute_force(gap))                                          # -> False
print(brute_force(overlap))                                      # -> False
print(brute_force([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 2, 2]]))   # -> False (corners cancel)


# --- try the optimal ---
tiling = [[1, 1, 3, 3], [3, 1, 4, 2], [3, 2, 4, 4], [1, 3, 2, 4], [2, 3, 3, 4]]
gap = [[1, 1, 2, 3], [1, 3, 2, 4], [3, 1, 4, 2], [3, 2, 4, 4]]
overlap = [[1, 1, 3, 3], [3, 1, 4, 2], [1, 3, 2, 4], [2, 2, 4, 4]]
print(perfect_rectangle(tiling))                                       # -> True
print(perfect_rectangle(gap))                                          # -> False
print(perfect_rectangle(overlap))                                      # -> False
print(perfect_rectangle([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 2, 2]]))   # -> False (corners cancel)
