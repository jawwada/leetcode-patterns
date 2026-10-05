"""
Insertion Sort - Fundamentals
Chapter: fundamentals/sorting
Key operations: take the next element, shift larger prefix elements one slot right, fill the gap

Grow a sorted prefix one element at a time: take the next element, shift every element of the
sorted prefix that is bigger than it one slot to the right, and place it in the gap that opens.
O(n^2) in general, O(n) when nearly sorted; in place and stable (equal keys never shift past).
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""


# --- algorithm ---
def insertion_sort(nums):
    """Sorted prefix grows by one each round; the new element walks left to its slot. O(n^2)."""
    a = list(nums)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:   # j may reach 0: the first element must be able to shift too
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key                 # the gap is just right of the element that stopped the scan
    return a


# --- try it ---
print(insertion_sort([5, 2, 4, 6, 1, 3]))   # -> [1, 2, 3, 4, 5, 6]
print(insertion_sort([2, 1]))               # -> [1, 2]
print(insertion_sort([3, 3, 1]))            # -> [1, 3, 3]
print(insertion_sort([]))                   # -> []
