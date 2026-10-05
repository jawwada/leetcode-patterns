"""
Quick Sort - Fundamentals
Chapter: fundamentals/sorting
Key operations: Lomuto partition around the last element, swap the pivot to its final slot, recurse

Pick the last element as the pivot. Walk j across the range keeping a[lo..i] as the elements <=
pivot: every time a[j] <= pivot grow that region by swapping a[j] in. Finally swap the pivot to
i + 1, its final position, and recurse on the two sides. O(n log n) on average, O(n^2) on sorted
input with this pivot, in place, not stable.
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""


# --- algorithm ---
def partition(a, lo, hi):
    """Lomuto: pivot a[hi]; a[lo..i] holds the values <= pivot; return the pivot's final index."""
    pivot = a[hi]
    i = lo - 1                         # end of the "small" region, empty at first
    for j in range(lo, hi):            # stop before hi: the pivot itself must not be swapped
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]  # the pivot goes to i + 1, right after the small region
    return i + 1


def sort_range(a, lo, hi):
    """Partition, then sort the two sides; a range of 0 or 1 elements is already sorted."""
    if lo < hi:
        p = partition(a, lo, hi)
        sort_range(a, lo, p - 1)       # the pivot at p is final: leave it out of both sides
        sort_range(a, p + 1, hi)


def quick_sort(nums):
    """Copy, then sort the whole range in place. O(n log n) average."""
    a = list(nums)
    sort_range(a, 0, len(a) - 1)
    return a


# --- try it ---
print(quick_sort([5, 2, 4, 6, 1, 3]))   # -> [1, 2, 3, 4, 5, 6]
print(quick_sort([3, 1, 2]))            # -> [1, 2, 3]
print(quick_sort([2, 2, 1]))            # -> [1, 2, 2]
print(quick_sort([]))                   # -> []
