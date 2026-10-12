"""
Merge Sort (basics: sorting)
Sort a list by splitting it in half, sorting each half, and merging the two sorted halves.
  [5, 2, 4, 6, 1, 3]  ->  [1, 2, 3, 4, 5, 6]

Idea: a list of 0 or 1 items is already sorted. Two sorted lists merge in one pass:
      keep taking the smaller front item (left one on ties, which keeps the sort stable).

Pseudocode:
  merge_sort(a):
      if len(a) <= 1: return a
      left  = merge_sort(first half)
      right = merge_sort(second half)
      return merge(left, right)

  merge(left, right):
      i = j = 0
      while both have items: append the smaller front item, advance that side
      append whatever is left over

Time O(n log n) always (log n levels, O(n) merging per level), space O(n).
"""


def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:          # <= : left wins ties (stable)
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]    # one side may have leftovers


def merge_sort(a):
    if len(a) <= 1:                      # base case: already sorted
        return list(a)
    mid = len(a) // 2
    return merge(merge_sort(a[:mid]), merge_sort(a[mid:]))


if __name__ == "__main__":
    print(merge_sort([5, 2, 4, 6, 1, 3]))  # [1, 2, 3, 4, 5, 6]
    print(merge_sort([3, 1, 2, 1]))        # [1, 1, 2, 3]
    print(merge_sort([]))                  # []
