"""
Rotate Image (LeetCode 48) - Basics
Area: matrices
Key operations: transpose by swapping across the diagonal, reverse each row, in place

Rotate an n x n matrix 90 degrees clockwise in place. Transposing mirrors the matrix over its main
diagonal (rows become columns); reversing every row then turns that mirror into a clockwise rotation.
Example: [[1,2,3],[4,5,6],[7,8,9]] -> [[7,4,1],[8,5,2],[9,6,3]]
"""


# --- brute force ---
def brute_force(matrix):
    """New matrix: cell (r, c) lands at (c, n-1-r). O(n^2) time and O(n^2) extra space, which the in-place version removes."""
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            result[c][n - 1 - r] = matrix[r][c]
    return result


# --- optimal ---
def solve(matrix):
    """Transpose (swap each pair above/below the diagonal once), then reverse every row. O(n^2), O(1) space."""
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix


# --- demo ---
def demo():
    return solve([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


# --- bugs ---
BUGS = [
    {
        "replace": "        for j in range(i + 1, n):",
        "with":    "        for j in range(n):",
        "fix": "swap each pair ONCE: only the cells above the diagonal (j > i) drive the swap",
        "why": "Visiting both (i, j) and (j, i) swaps every pair twice, which undoes the transpose; the result is just each row reversed.",
        "decoys": [
            {"line": "    for i in range(n):", "change": "should be range(n - 1)"},
            {"line": "        row.reverse()", "change": "should be row.sort(reverse=True)"},
            {"line": "    return matrix", "change": "should return matrix[::-1]"},
        ],
    },
    {
        "replace": "            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]",
        "with":    "            matrix[i][j] = matrix[j][i]",
        "fix": "swap both cells at once; copying one direction overwrites the upper triangle and loses it",
        "why": "The upper triangle is replaced by the lower one, so the matrix becomes symmetric instead of transposed: [[1,2],[3,4]] gives [[3,1],[4,3]].",
        "decoys": [
            {"line": "    n = len(matrix)", "change": "should be len(matrix[0])"},
            {"line": "    for row in matrix:", "change": "should iterate matrix[::-1]"},
            {"line": "        for j in range(i + 1, n):", "change": "should be range(i, n)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
