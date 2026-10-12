"""
Orientation and Segment Intersection - The Cross Product Decides Left or Right

Decide whether the path o -> a -> b turns left, turns right or runs straight,
and whether two segments share a point. Points are (x, y) integer pairs:
segments (0, 0)-(4, 4) and (0, 4)-(4, 0) -> True, they cross at (2, 2).
"""


# --- algorithm ---
def cross(o, a, b):
    """Cross product of o->a and o->b: > 0 left turn, < 0 right turn,
    0 straight. O(1)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p, q, r):
    """For r on the line pq: is r inside the box spanned by p and q? O(1)."""
    inside_x = min(p[0], q[0]) <= r[0] <= max(p[0], q[0])
    inside_y = min(p[1], q[1]) <= r[1] <= max(p[1], q[1])
    return inside_x and inside_y


def segments_intersect(p1, p2, q1, q2):
    """Each segment's ends lie on opposite sides of the other's line, or an
    end touches the other segment. O(1)."""
    d1 = cross(q1, q2, p1)              # side of p1 seen from q1 -> q2
    d2 = cross(q1, q2, p2)
    d3 = cross(p1, p2, q1)              # side of q1 seen from p1 -> p2
    d4 = cross(p1, p2, q2)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True                     # both pairs straddle: a clean crossing
    if d1 == 0 and on_segment(q1, q2, p1):
        return True                     # p1 lies on segment q1 q2
    if d2 == 0 and on_segment(q1, q2, p2):
        return True
    if d3 == 0 and on_segment(p1, p2, q1):
        return True
    if d4 == 0 and on_segment(p1, p2, q2):
        return True
    return False


# --- try it ---
print(cross((0, 0), (4, 0), (2, 3)))                        # -> 12
print(segments_intersect((0, 0), (4, 4), (0, 4), (4, 0)))   # -> True
print(segments_intersect((0, 0), (2, 2), (3, 3), (5, 5)))   # -> False
print(segments_intersect((0, 0), (4, 0), (2, 0), (2, 3)))   # -> True
print(segments_intersect((0, 0), (4, 0), (0, 1), (4, 2)))   # -> False
