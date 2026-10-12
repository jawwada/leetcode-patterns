"""
Quick Sort - Partition Around a Random Pivot

Sort an array of integers in place, without a second array:
[6, 3, 7, 4, 1, 5, 2] -> [1, 2, 3, 4, 5, 6, 7].
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


def sort_range(nums, lo, hi):
    """Partition nums[lo..hi], then sort each side. Expected O(n log n) on
    distinct values; many equal values make it O(n^2), n levels deep."""
    if lo >= hi:                      # 0 or 1 values: sorted already
        return
    p = partition(nums, lo, hi)
    sort_range(nums, lo, p - 1)       # the pivot at p is final: skip it
    sort_range(nums, p + 1, hi)


def quick_sort(nums):
    """Sort the whole array in place and return it. Expected O(n log n)."""
    sort_range(nums, 0, len(nums) - 1)
    return nums


# --- try it ---
print(quick_sort([6, 3, 7, 4, 1, 5, 2]))   # -> [1, 2, 3, 4, 5, 6, 7]
print(quick_sort([2, -3, 2, 0, -3, 2]))    # -> [-3, -3, 0, 2, 2, 2]
print(quick_sort([1]))                     # -> [1]
print(quick_sort([]))                      # -> []
