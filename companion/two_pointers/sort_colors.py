"""
Sort Colors (LeetCode 75) - Medium
Chapter: two_pointers
Pattern: Dutch national flag (three-way partition)

Given an array containing only 0s, 1s and 2s, sort it in place so all 0s come first,
then 1s, then 2s, without the library sort. Aim for one pass with O(1) space.
Example: nums = [2, 0, 2, 1, 1, 0] -> [0, 0, 1, 1, 2, 2].
"""


# --- brute force ---
def brute_force(nums):
    """Count the 0s, 1s and 2s, then rewrite the array. O(n) time, two passes."""
    counts = [0, 0, 0]
    for value in nums:
        counts[value] += 1
    i = 0
    for colour in range(3):
        for _ in range(counts[colour]):  # write that many copies of this colour
            nums[i] = colour
            i += 1


# --- optimal ---
def sort_colors(nums):
    """Three regions grow in one pass (Dutch national flag). O(n) time, O(1) space."""
    low = 0           # nums[:low] are all 0
    mid = 0           # nums[low:mid] are all 1; nums[mid:high + 1] not looked at yet
    high = len(nums) - 1  # nums[high + 1:] are all 2
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1  # mid stays: the value swapped in has not been examined yet


# --- try the brute force ---
a = [2, 0, 2, 1, 1, 0]
brute_force(a)
print(a)      # -> [0, 0, 1, 1, 2, 2]
b = [2, 0, 1]
brute_force(b)
print(b)      # -> [0, 1, 2]
c = [2, 2, 2, 1, 1, 0, 0]
brute_force(c)
print(c)      # -> [0, 0, 1, 1, 2, 2, 2]


# --- try the optimal ---
a = [2, 0, 2, 1, 1, 0]
sort_colors(a)
print(a)      # -> [0, 0, 1, 1, 2, 2]
b = [2, 0, 1]
sort_colors(b)
print(b)      # -> [0, 1, 2]
c = [2, 2, 2, 1, 1, 0, 0]
sort_colors(c)
print(c)      # -> [0, 0, 1, 1, 2, 2, 2]
