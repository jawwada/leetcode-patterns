"""
Merge Sort - Fundamentals
Chapter: fundamentals/sorting
Key operations: split in half, sort each half recursively, merge two sorted runs, left wins ties

Split the array in half, sort each half, and merge the two sorted runs: repeatedly take the smaller
head, the left one on ties (that is what keeps the sort stable), then append whatever run is left.
O(n log n) in every case, O(n) extra space for the merged runs.
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""


# --- algorithm ---
def merge(left, right):
    """Two pointers over two sorted runs; take the smaller head, left wins ties. O(n + m)."""
    out = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:        # <= : on a tie take the left run first (keeps it stable)
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])               # exactly one run still has elements; append both to be safe
    out.extend(right[j:])
    return out


def merge_sort(nums):
    """Split, sort both halves, merge. O(n log n): log n levels of O(n) merging."""
    if len(nums) <= 1:                 # a run of one element is already sorted: stop the recursion
        return list(nums)
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return merge(left, right)


# --- try it ---
print(merge_sort([5, 2, 4, 6, 1, 3]))   # -> [1, 2, 3, 4, 5, 6]
print(merge([1, 4], [2, 3, 5]))         # -> [1, 2, 3, 4, 5]
print(merge_sort([2, 1]))               # -> [1, 2]
print(merge_sort([]))                   # -> []
