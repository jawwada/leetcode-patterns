"""
Max Points on a Line (LeetCode 149) - Hard
Chapter: math_geometry
Pattern: Anchor point + slope as a reduced fraction

Given n distinct points on the plane, return the largest number of them that lie on one
straight line.
Example: [[1,1],[2,2],[3,3]] -> 3; [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]] -> 4
(the line through (1,4), (2,3), (3,2), (4,1)).
"""
from math import gcd       # gcd(a, b): greatest common divisor, used to reduce a fraction


# --- brute force ---
def brute_force(points):
    """For every pair, count the points on the line through it. O(n^3) time, O(1) space."""
    n = len(points)
    best = min(n, 2)                               # 1 or 2 points always share a line
    for i in range(n):
        for j in range(i + 1, n):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            on_line = 0
            for k in range(n):
                kx = points[k][0] - points[i][0]
                ky = points[k][1] - points[i][1]
                if dx * ky - dy * kx == 0:         # cross product 0: k is on the line through i, j
                    on_line += 1
            best = max(best, on_line)
    return best


# --- optimal ---
def max_points_on_a_line(points):
    """Anchor each point; count the other points per reduced direction. O(n^2) time, O(n) space."""
    n = len(points)
    best = 1
    for i in range(n):
        counts = {}                                # reduced direction (dx, dy) -> points that way
        for j in range(i + 1, n):                  # pairs with j < i were counted from anchor j
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            g = gcd(dx, dy)                        # > 0 because the points are distinct
            dx = dx // g
            dy = dy // g
            if dx < 0 or (dx == 0 and dy < 0):     # one sign per direction, so 1/3 == 2/6 == -1/-3
                dx = -dx
                dy = -dy
            key = (dx, dy)
            counts[key] = counts.get(key, 0) + 1
        for key in counts:
            best = max(best, counts[key] + 1)      # +1 for the anchor itself
    return best


# --- try the brute force ---
print(brute_force([[1, 1], [2, 2], [3, 3]]))                           # -> 3
print(brute_force([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))   # -> 4
print(brute_force([[0, 0]]))                                           # -> 1
print(brute_force([[0, 0], [0, 1], [0, -1], [1, 5]]))                  # -> 3


# --- try the optimal ---
print(max_points_on_a_line([[1, 1], [2, 2], [3, 3]]))                           # -> 3
print(max_points_on_a_line([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))   # -> 4
print(max_points_on_a_line([[0, 0]]))                                           # -> 1
print(max_points_on_a_line([[0, 0], [0, 1], [0, -1], [1, 5]]))                  # -> 3
