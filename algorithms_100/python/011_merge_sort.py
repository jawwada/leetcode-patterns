"""
Merge Sort - Divide, Sort Halves, Merge

Sort an array of integers in ascending order and return the result as a new
list: [5, 2, 4, 7, 1, 3, 2, 6] -> [1, 2, 2, 3, 4, 5, 6, 7].
"""


# --- algorithm ---
def merge(left, right):
    """Two sorted lists into one: keep taking the smaller front. O(n) time."""
    merged = []
    i = 0                               # front of left
    j = 0                               # front of right
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:         # a tie takes the left one: stable
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    while i < len(left):                # one side is used up: copy the rest
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


def merge_sort(nums):
    """Sort each half recursively, then merge. O(n log n) time, O(n) space."""
    if len(nums) <= 1:
        return list(nums)               # 0 or 1 values: sorted already (copy)
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])       # nums[0..mid-1]
    right = merge_sort(nums[mid:])      # nums[mid..n-1]
    return merge(left, right)


# --- try it ---
print(merge_sort([5, 2, 4, 7, 1, 3, 2, 6]))   # -> [1, 2, 2, 3, 4, 5, 6, 7]
print(merge_sort([3, -1, 0, -1]))             # -> [-1, -1, 0, 3]
print(merge([1, 4], [2, 3]))                  # -> [1, 2, 3, 4]
print(merge_sort([]))                         # -> []
