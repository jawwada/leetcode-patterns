"""
Combinations n Choose k - Fundamentals
Chapter: fundamentals/backtracking
Key operations: choose i, recurse from i + 1, prune when numbers left < open slots, unchoose

Return every combination of k numbers chosen from 1..n, each combination in increasing order
(LeetCode 77). Results sorted.
Example: n = 4, k = 2 -> [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
"""


# --- algorithm ---
def backtrack(n, k, start, path, res):
    """Extend path with each number from start to n; stop once the path has k numbers."""
    if len(path) == k:
        res.append(path[:])   # copy: path keeps changing below
        return
    for i in range(start, n + 1):
        if n - i + 1 < k - len(path):   # numbers left (i..n) cannot fill the open slots: prune
            break
        path.append(i)                  # choose
        backtrack(n, k, i + 1, path, res)
        path.pop()                      # unchoose


def combinations(n, k):
    """Start-index template plus a size check. O(k * C(n, k))."""
    res = []
    backtrack(n, k, 1, [], res)
    return sorted(res)


# --- try it ---
print(combinations(4, 2))   # -> [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
print(combinations(3, 3))   # -> [[1, 2, 3]]
print(combinations(3, 1))   # -> [[1], [2], [3]]
print(combinations(2, 3))   # -> []
