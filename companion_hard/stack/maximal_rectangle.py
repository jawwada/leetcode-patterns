"""
Maximal Rectangle (LeetCode 85) - Hard
Chapter: stack
Pattern: Monotonic stack

Given an m x n binary matrix of '0'/'1' characters, return the area of the largest
rectangle containing only '1's.
Example: [["1","0","1","0","0"], ["1","0","1","1","1"], ["1","1","1","1","1"],
["1","0","0","1","0"]] -> 6 (the 2 x 3 block of 1s in rows 1-2, columns 2-4).
"""


# --- brute force ---
def full_of_ones(matrix, r1, c1, r2, c2):
    """True when every cell between corners (r1, c1) and (r2, c2) is '1'."""
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            if matrix[r][c] != "1":
                return False
    return True


def brute_force(matrix):
    """Try every pair of corners and check every cell inside. O(m^3 * n^3) time."""
    if len(matrix) == 0:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    best = 0
    for r1 in range(rows):
        for c1 in range(cols):
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):      # rescans cells shared with the last rectangle
                    if full_of_ones(matrix, r1, c1, r2, c2):
                        area = (r2 - r1 + 1) * (c2 - c1 + 1)
                        best = max(best, area)
    return best


# --- optimal ---
def largest_in_histogram(heights):
    """Largest rectangle under a histogram with a monotonic stack. O(n) time."""
    bars = heights + [0]                        # the final 0 flushes every open bar
    stack = []                                  # indices whose heights never decrease
    best = 0
    for i in range(len(bars)):
        while stack and bars[stack[-1]] > bars[i]:
            top = stack.pop()                   # bar i is the first shorter bar to its right
            if stack:
                left = stack[-1]                # nearest shorter bar to its left
            else:
                left = -1
            best = max(best, bars[top] * (i - left - 1))
        stack.append(i)
    return best


def maximal_rectangle(matrix):
    """Each row is the floor of a histogram of 1s; solve every histogram. O(m * n) time."""
    if len(matrix) == 0:
        return 0
    cols = len(matrix[0])
    heights = [0] * cols                        # consecutive 1s ending at the current row
    best = 0
    for row in matrix:
        for c in range(cols):
            if row[c] == "1":
                heights[c] += 1
            else:
                heights[c] = 0                  # a 0 cuts the column back to the ground
        best = max(best, largest_in_histogram(heights))
    return best


# --- try the brute force ---
print(brute_force([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
                   ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]))   # -> 6
print(brute_force([["0"]]))                                                  # -> 0
print(brute_force([["1", "1"], ["1", "1"]]))                                 # -> 4
print(brute_force([]))                                                       # -> 0


# --- try the optimal ---
print(maximal_rectangle([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
                         ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]))   # -> 6
print(maximal_rectangle([["0"]]))                                                  # -> 0
print(maximal_rectangle([["1", "1"], ["1", "1"]]))                                 # -> 4
print(maximal_rectangle([]))                                                       # -> 0
