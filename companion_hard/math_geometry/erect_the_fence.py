"""
Erect the Fence (LeetCode 587) - Hard
Chapter: math_geometry
Pattern: Convex hull (monotone chain)

Given the positions of trees, fence the whole garden with the shortest rope and return every
tree on the fence: the corners of the convex hull plus trees lying on an edge, in any order.
Example: [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]] -> [[1,1],[2,0],[4,2],[3,3],[2,4]] ((2,2) is
strictly inside); [[1,2],[2,2],[4,2]] -> all three.
"""


# --- helpers ---
def cross(o, a, b):
    """Cross product of (a - o) and (b - o): > 0 left turn, < 0 right turn, 0 collinear."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def as_lists(points):
    """Turn a collection of (x, y) tuples back into [x, y] lists."""
    result = []
    for p in points:
        result.append([p[0], p[1]])
    return result


# --- brute force ---
def brute_force(trees):
    """A pair is a fence edge iff every tree is on one side of its line. O(n^3) time."""
    n = len(trees)
    if n < 3:
        return as_lists(trees)
    on_fence = set()
    for i in range(n):
        for j in range(i + 1, n):
            left = 0
            right = 0
            on_line = []
            for k in range(n):
                side = cross(trees[i], trees[j], trees[k])
                if side > 0:
                    left += 1
                elif side < 0:
                    right += 1
                else:
                    on_line.append((trees[k][0], trees[k][1]))
            if left == 0 or right == 0:            # nobody on the other side: a supporting line
                for p in on_line:
                    on_fence.add(p)
    return as_lists(on_fence)


# --- optimal ---
def half_hull(points):
    """One chain of the hull: pop the top while the turn is clockwise; collinear trees stay."""
    chain = []
    for p in points:
        while len(chain) >= 2 and cross(chain[-2], chain[-1], p) < 0:
            chain.pop()                            # clockwise turn: the middle tree is inside
        chain.append(p)
    return chain


def erect_the_fence(trees):
    """Sort, then build the lower and upper chains with a stack. O(n log n) time, O(n) space."""
    points = []
    for x, y in trees:
        points.append((x, y))
    points.sort()                                  # by x, then by y
    lower = half_hull(points)                      # left to right along the bottom
    upper = half_hull(points[::-1])                # right to left along the top
    on_fence = set(lower + upper)                  # the two end trees appear in both chains
    return as_lists(on_fence)


# --- try the brute force ---
garden = [[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]
print(sorted(brute_force(garden)))                   # -> [[1, 1], [2, 0], [2, 4], [3, 3], [4, 2]]
print(sorted(brute_force([[1, 2], [2, 2], [4, 2]])))   # -> [[1, 2], [2, 2], [4, 2]]
print(sorted(brute_force([[0, 0]])))                 # -> [[0, 0]]
edge = [[0, 0], [0, 1], [0, 2], [1, 1]]
print(sorted(brute_force(edge)))                     # -> [[0, 0], [0, 1], [0, 2], [1, 1]]


# --- try the optimal ---
garden = [[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]
print(sorted(erect_the_fence(garden)))               # -> [[1, 1], [2, 0], [2, 4], [3, 3], [4, 2]]
print(sorted(erect_the_fence([[1, 2], [2, 2], [4, 2]])))   # -> [[1, 2], [2, 2], [4, 2]]
print(sorted(erect_the_fence([[0, 0]])))             # -> [[0, 0]]
edge = [[0, 0], [0, 1], [0, 2], [1, 1]]
print(sorted(erect_the_fence(edge)))                 # -> [[0, 0], [0, 1], [0, 2], [1, 1]]
