"""
Quick Sort (basics: sorting)
Sort a list by putting one pivot in its final slot, then sorting the items on each side of it.
  [5, 2, 4, 6, 1, 3]  ->  [1, 2, 3, 4, 5, 6]

Idea: partition around the last item (Lomuto). Sweep left to right and swap every item
      <= pivot into a growing "small" region at the front. The pivot belongs right after
      that region: smaller items sit left of it, bigger ones right, so each side sorts alone.

Pseudocode:
  quick_sort_range(a, lo, hi):
      if lo < hi:                        # 0 or 1 items are already sorted
          p = partition(a, lo, hi)
          quick_sort_range(a, lo, p - 1)
          quick_sort_range(a, p + 1, hi)

  partition(a, lo, hi):
      pivot = a[hi]; i = lo - 1          # a[lo..i] holds the items <= pivot
      for j in lo..hi-1:
          if a[j] <= pivot: i += 1, swap a[i] and a[j]
      swap a[i + 1] and a[hi]            # pivot lands in its final slot
      return i + 1

Time O(n log n) average, O(n^2) worst (e.g. sorted input with this pivot),
space O(log n) average for the recursion. In place, not stable.
"""


def partition(a, lo, hi):
    pivot = a[hi]                        # last item is the pivot
    i = lo - 1                           # a[lo..i] holds the items <= pivot
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]      # grow the small region
    a[i + 1], a[hi] = a[hi], a[i + 1]    # pivot goes right after it
    return i + 1


def quick_sort_range(a, lo, hi):
    if lo < hi:                          # 0 or 1 items: already sorted
        p = partition(a, lo, hi)
        quick_sort_range(a, lo, p - 1)   # items left of the pivot
        quick_sort_range(a, p + 1, hi)   # items right of the pivot


def quick_sort(nums):
    a = list(nums)                       # sort a copy in place
    quick_sort_range(a, 0, len(a) - 1)
    return a


if __name__ == "__main__":
    print(quick_sort([5, 2, 4, 6, 1, 3]))  # [1, 2, 3, 4, 5, 6]
    print(quick_sort([3, 1, 2, 1]))        # [1, 1, 2, 3]
    print(quick_sort([]))                  # []
