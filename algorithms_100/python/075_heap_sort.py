"""
Heap Sort - Build a Max-Heap, Swap the Max to the End

Sort an array of integers in place, with O(1) extra space and an O(n log n)
bound even in the worst case: [4, 10, 3, 5, 1] -> [1, 3, 4, 5, 10].
"""


# --- algorithm ---
def sift_down(nums, i, n):
    """Max-heap sift-down: swap nums[i] with its larger child until no child
    is larger; only nums[0..n-1] is the heap. O(log n)."""
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and nums[left] > nums[largest]:
            largest = left
        if right < n and nums[right] > nums[largest]:
            largest = right
        if largest == i:                # no child is larger: done
            return
        nums[i], nums[largest] = nums[largest], nums[i]
        i = largest


def heap_sort(nums):
    """Build a max-heap, then move the max to the end n - 1 times.
    O(n log n) time, O(1) extra space."""
    n = len(nums)
    for i in range(n // 2 - 1, -1, -1):          # build: last parent to root
        sift_down(nums, i, n)
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]  # the max joins the sorted tail
        sift_down(nums, 0, end)                  # the heap is nums[0..end-1]
    return nums


# --- try it ---
print(heap_sort([4, 10, 3, 5, 1]))    # -> [1, 3, 4, 5, 10]
print(heap_sort([2, -7, 2, 0, -7]))   # -> [-7, -7, 0, 2, 2]
print(heap_sort([9]))                 # -> [9]
print(heap_sort([]))                  # -> []
