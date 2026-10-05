"""
Kth Largest Element in an Array (LeetCode 215) - Medium
Chapter: heap
Pattern: Quickselect (partition, recurse one side)

Given an integer array nums and k, return the k-th largest element in sorted order
(duplicates count), without fully sorting.
Example: nums=[3,2,1,5,6,4], k=2 -> 5. Example: nums=[3,2,3,1,2,4,5,5,6], k=4 -> 4.
"""
import random     # a random pivot keeps quickselect fast on every input


# --- brute force ---
def brute_force(nums, k):
    """Sort everything descending and read position k - 1. O(n log n) time."""
    ordered = sorted(nums, reverse=True)      # orders every pair, we need one position
    return ordered[k - 1]


# --- optimal ---
def find_kth_largest(nums, k):
    """Quickselect: partition around a pivot, keep only the side with the answer. O(n) average."""
    nums = list(nums)                 # work on a copy
    target = len(nums) - k            # index of the answer in ascending order
    low = 0
    high = len(nums) - 1
    while low < high:
        pivot_index = partition(nums, low, high)
        if pivot_index == target:
            return nums[pivot_index]
        if pivot_index < target:
            low = pivot_index + 1     # the answer is among the bigger values
        else:
            high = pivot_index - 1    # the answer is among the smaller values
    return nums[low]


def partition(nums, low, high):
    """Put a random pivot at its final sorted index within nums[low..high]; return that index."""
    pivot_index = random.randint(low, high)
    nums[pivot_index], nums[high] = nums[high], nums[pivot_index]   # park the pivot at the end
    pivot = nums[high]
    store = low                       # everything before store is smaller than the pivot
    for i in range(low, high):
        if nums[i] < pivot:
            nums[i], nums[store] = nums[store], nums[i]              # swap it into the small side
            store += 1
    nums[store], nums[high] = nums[high], nums[store]               # the pivot lands at store
    return store


# --- try the brute force ---
print(brute_force([3, 2, 1, 5, 6, 4], 2))             # -> 5
print(brute_force([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))    # -> 4
print(brute_force([1], 1))                            # -> 1
print(brute_force([2, 2, 2, 2], 3))                   # -> 2


# --- try the optimal ---
print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))             # -> 5
print(find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))    # -> 4
print(find_kth_largest([1], 1))                            # -> 1
print(find_kth_largest([2, 2, 2, 2], 3))                   # -> 2
