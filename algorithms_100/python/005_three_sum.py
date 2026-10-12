"""
3Sum - Sort, Fix One, Converge Two Pointers

Given an array of integers, return every triplet of values that sums to
zero, each distinct triplet once:
[-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0, 1]].
"""


# --- algorithm ---
def three_sum(nums):
    """Sort; fix nums[i], two pointers find pairs summing to -nums[i]. O(n²)."""
    nums = sorted(nums)             # sorted copy: equal values sit together
    triplets = []
    n = len(nums)
    for i in range(n - 2):
        if nums[i] > 0:
            break                   # smallest of the three is positive: done
        if i > 0 and nums[i] == nums[i - 1]:
            continue                # same first value, same triplets
        left = i + 1
        right = n - 1
        while left < right:         # Two Sum II on nums[i+1..n-1]
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1           # too small: a bigger second value
            elif total > 0:
                right -= 1          # too big: a smaller third value
            else:
                triplets.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1       # skip repeats of the second value
    return triplets


# --- try it ---
print(three_sum([-1, 0, 1, 2, -1, -4]))     # -> [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0, 0]))              # -> [[0, 0, 0]]
print(three_sum([0, 1, 1]))                 # -> []
print(three_sum([-2, 0, 0, 2, 2]))          # -> [[-2, 0, 2]]
