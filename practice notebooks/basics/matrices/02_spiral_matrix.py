"""
Spiral Matrix (LeetCode 54) - Basics
Area: matrices
Key operations: four shrinking bounds, emit one side per step, re-check bounds before the bottom and left sides

Return every element of an m x n matrix in clockwise spiral order. Keep four bounds (top, bottom,
left, right); emit the top row and move top down, the right column and move right in, then, if a
row/column is still left, the bottom row backwards and the left column upwards.
Example: [[1,2,3],[4,5,6],[7,8,9]] -> [1, 2, 3, 6, 9, 8, 7, 4, 5]
"""


# --- brute force ---
def brute_force(matrix):
    """Walk right/down/left/up, turning whenever the next cell is outside or visited. O(m*n) with an O(m*n) visited set."""
    if not matrix or not matrix[0]:
        return []
    m, n = len(matrix), len(matrix[0])
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c, d, seen, out = 0, 0, 0, set(), []
    for _ in range(m * n):
        out.append(matrix[r][c])
        seen.add((r, c))
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < m and 0 <= nc < n) or (nr, nc) in seen:
            d = (d + 1) % 4
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return out


# --- optimal ---
def solve(matrix):
    """Peel one ring per loop with four bounds that shrink after each side. O(m*n), O(1) extra space."""
    if not matrix or not matrix[0]:
        return []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        seg = [matrix[top][c] for c in range(left, right + 1)]
        out += seg
        top += 1
        seg = [matrix[r][right] for r in range(top, bottom + 1)]
        out += seg
        right -= 1
        if top <= bottom:
            seg = [matrix[bottom][c] for c in range(right, left - 1, -1)]
            out += seg
            bottom -= 1
        if left <= right:
            seg = [matrix[r][left] for r in range(bottom, top - 1, -1)]
            out += seg
            left += 1
    return out


# --- demo ---
def demo():
    return solve([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


# --- bugs ---
BUGS = [
    {
        "replace": "        if top <= bottom:",
        "with":    "        if top < bottom:",
        "fix": "the bottom row still exists when top == bottom (one row left), so the check is <=",
        "why": "When one row remains after the top side, it is skipped: [[1,2,3],[4,5,6]] loses 5 and 4.",
        "decoys": [
            {"line": "    while top <= bottom and left <= right:", "change": "should be < in both"},
            {"line": "        top += 1", "change": "should move after the right column"},
            {"line": "        right -= 1", "change": "should be right = bottom"},
        ],
    },
    {
        "replace": "            seg = [matrix[bottom][c] for c in range(right, left - 1, -1)]",
        "with":    "            seg = [matrix[bottom][c] for c in range(right, left, -1)]",
        "fix": "a descending range stops BEFORE its end, so the end must be left - 1 to include column left",
        "why": "The bottom-left corner of every ring is missed: the 3x3 example gives [1, 2, 3, 6, 9, 8, 4, 5].",
        "decoys": [
            {"line": "        seg = [matrix[top][c] for c in range(left, right + 1)]", "change": "should be range(left, right)"},
            {"line": "            bottom -= 1", "change": "should be bottom = top"},
            {"line": "        if left <= right:", "change": "should be if left < right"},
        ],
    },
    {
        "replace": "        if left <= right:",
        "with":    "        if left < right:",
        "fix": "the left column still exists when left == right (one column left), so the check is <=",
        "why": "When one column remains after the right side, it is skipped: [[1,2],[3,4],[5,6]] loses 3.",
        "decoys": [
            {"line": "            seg = [matrix[r][left] for r in range(bottom, top - 1, -1)]", "change": "should be range(bottom, top, -1)"},
            {"line": "            left += 1", "change": "should be left = right"},
            {"line": "        seg = [matrix[r][right] for r in range(top, bottom + 1)]", "change": "should be range(top - 1, bottom + 1)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
