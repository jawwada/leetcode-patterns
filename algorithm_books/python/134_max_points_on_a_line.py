"""
Max Points on a Line - Slopes as Reduced Fractions

Given distinct points with integer coordinates, return the largest number of
them that lie on one straight line:
(1, 1) (3, 2) (5, 3) (4, 1) (2, 3) (1, 4) -> 4, the line x + y = 5.
"""
import math                             # gcd is Euclid's algorithm, #128


# --- algorithm ---
def slope_key(p, q):
    """Direction p -> q as a reduced fraction (dy, dx) with dx > 0;
    every vertical pair gets (1, 0). O(log C) for the gcd."""
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    if dx == 0:
        return (1, 0)                   # vertical line
    if dx < 0:
        dx = -dx                        # p -> q and q -> p: the same line
        dy = -dy
    g = math.gcd(dy, dx)                # positive, since dx > 0
    return (dy // g, dx // g)           # exact divisions


def max_points(points):
    """Anchor each point and group the later points by slope; the biggest
    group plus the anchor is a line. O(n^2) slopes."""
    n = len(points)
    if n <= 2:
        return n
    best = 0
    for i in range(n):
        counts = {}                     # slope key -> points on that line
        for j in range(i + 1, n):
            key = slope_key(points[i], points[j])
            counts[key] = counts.get(key, 0) + 1
            if counts[key] + 1 > best:
                best = counts[key] + 1  # + 1 for the anchor itself
    return best


# --- try it ---
pts = [(1, 1), (3, 2), (5, 3), (4, 1), (2, 3), (1, 4)]
print(max_points(pts))                          # -> 4
print(max_points([(1, 1), (2, 2), (3, 3)]))     # -> 3
print(max_points([(0, 0), (0, 5), (0, -2), (3, 1)]))  # -> 3
print(slope_key((3, 2), (1, 4)))                # -> (-1, 1)
