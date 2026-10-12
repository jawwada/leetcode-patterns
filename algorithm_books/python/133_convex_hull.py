"""
Convex Hull - Andrew's Monotone Chain

Return the corners of the smallest convex polygon containing every (x, y)
point, counter-clockwise from the leftmost one (the lowest on a tie):
(0, 0) (1, 3) (2, 1) (2, 2) (3, 2) (4, 0) (4, 4) -> (0, 0) (4, 0) (4, 4) (1, 3)
"""


# --- algorithm ---
def cross(o, a, b):
    """> 0 when o -> a -> b turns left (counter-clockwise), as in #132. O(1)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def half_hull(pts):
    """One chain: a stack that keeps only left turns. O(n), since every
    point is pushed once and popped at most once."""
    chain = []                          # used as a stack: chain[-1] is the top
    for p in pts:
        while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
            chain.pop()                 # last turn is not counter-clockwise
        chain.append(p)
    return chain


def convex_hull(points):
    """Sort by (x, y); the lower chain runs left to right, the upper chain
    right to left. O(n log n) for the sort."""
    pts = sorted(set(points))           # by x, then y; duplicates dropped
    if len(pts) <= 2:
        return pts
    lower = half_hull(pts)
    upper = half_hull(pts[::-1])
    return lower[:-1] + upper[:-1]      # each chain ends where the other starts


# --- try it ---
pts = [(0, 0), (1, 3), (2, 1), (2, 2), (3, 2), (4, 0), (4, 4)]
print(convex_hull(pts))                 # -> [(0, 0), (4, 0), (4, 4), (1, 3)]
print(convex_hull([(0, 0), (1, 1), (2, 2), (1, 1)]))    # -> [(0, 0), (2, 2)]
print(convex_hull([(5, 5)]))            # -> [(5, 5)]
square = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1), (1, 0)]
print(convex_hull(square))              # -> [(0, 0), (2, 0), (2, 2), (0, 2)]
