"""
Quickselect - Kth Largest in Expected O(n)

Find the kth largest value of an unsorted array (duplicates count) without
sorting it; the array is reordered in place:
[3, 2, 1, 5, 6, 4], k = 2 -> 5.
"""
import random   # random.randint(a, b) can return a or b too


# --- algorithm ---
def partition(nums, lo, hi):
    """Lomuto partition of nums[lo..hi] around a random pivot; return the
    pivot's final index. O(hi - lo) time."""
    pick = random.randint(lo, hi)
    nums[pick], nums[hi] = nums[hi], nums[pick]  # park the pivot at the end
    pivot = nums[hi]
    store = lo                        # invariant: nums[lo..store-1] < pivot
    for i in range(lo, hi):
        if nums[i] < pivot:           # a small value joins the left region
            nums[store], nums[i] = nums[i], nums[store]
            store += 1
    nums[store], nums[hi] = nums[hi], nums[store]  # pivot between the regions
    return store


def kth_largest(nums, k):
    """Partition, then keep only the side that holds index n - k.
    Expected O(n) time on distinct values, O(1) extra space."""
    target = len(nums) - k            # the answer's index in sorted order
    lo = 0
    hi = len(nums) - 1
    while True:
        p = partition(nums, lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1                # the answer is right of the pivot
        else:
            hi = p - 1                # the answer is left of the pivot


# --- try it ---
print(kth_largest([3, 2, 1, 5, 6, 4], 2))            # -> 5
print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # -> 4
print(kth_largest([7], 1))                           # -> 7
print(kth_largest([-2, 0, -5], 3))                   # -> -5
