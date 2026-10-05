"""
Kth Smallest Number in Multiplication Table (LeetCode 668) - Hard
Chapter: binary_search
Pattern: Binary search on the answer

An m x n multiplication table has table[i][j] = i * j with 1-indexed i and j. Return the k-th
smallest value in the table, 1 <= k <= m * n.
Example: m = 3, n = 3, k = 5 -> 3 (sorted table: 1, 2, 2, 3, 3, 4, 6, 6, 9)
"""


# --- brute force ---
def brute_force(m, n, k):
    """Build every product, sort them, read index k - 1. O(mn log(mn)) time."""
    products = []
    for row in range(1, m + 1):
        for col in range(1, n + 1):
            products.append(row * col)
    products.sort()
    return products[k - 1]


# --- optimal ---
def count_at_most(m, n, value):
    """How many table entries are <= value: one division per row. O(m) time."""
    count = 0
    for row in range(1, m + 1):
        count += min(n, value // row)     # row holds row, 2*row, ..., n*row
    return count


def kth_smallest_in_table(m, n, k):
    """Binary search the smallest value with at least k entries at or below it. O(m log(mn))."""
    if m > n:
        m, n = n, m                       # count over the shorter dimension
    left = 1
    right = m * n
    while left < right:
        mid = (left + right) // 2
        if count_at_most(m, n, mid) >= k:
            right = mid                   # enough entries at or below mid: try smaller
        else:
            left = mid + 1
    return left


# --- try the brute force ---
print(brute_force(3, 3, 5))     # -> 3
print(brute_force(2, 3, 6))     # -> 6
print(brute_force(9, 9, 81))    # -> 81
print(brute_force(1, 10, 7))    # -> 7


# --- try the optimal ---
print(kth_smallest_in_table(3, 3, 5))     # -> 3
print(kth_smallest_in_table(2, 3, 6))     # -> 6
print(kth_smallest_in_table(9, 9, 81))    # -> 81
print(kth_smallest_in_table(1, 10, 7))    # -> 7
