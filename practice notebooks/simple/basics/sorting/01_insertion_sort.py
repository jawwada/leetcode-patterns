"""
Insertion Sort (basics: sorting)
Sort a list by growing a sorted prefix one item at a time.
  [5, 2, 4, 6, 1, 3]  ->  [1, 2, 3, 4, 5, 6]

Idea: like sorting cards in your hand. Take the next item, shift every bigger item of the
      sorted prefix one slot right, and drop the item into the gap that opens.
      Only strictly bigger items move, so equal items keep their order (stable).

Pseudocode:
  for i in 1..n-1:
      key = a[i]; j = i - 1
      while j >= 0 and a[j] > key:
          a[j + 1] = a[j]; j -= 1        # shift the bigger item right
      a[j + 1] = key                     # drop key into the gap

Time O(n^2), O(n) when nearly sorted; space O(1) extra (sorts the copy in place).
"""


def insertion_sort(nums):
    a = list(nums)                       # work on a copy
    for i in range(1, len(a)):
        key = a[i]                       # next item to insert
        j = i - 1
        while j >= 0 and a[j] > key:     # walk left past bigger items
            a[j + 1] = a[j]              # shift it one slot right
            j -= 1
        a[j + 1] = key                   # drop key into the gap
    return a


if __name__ == "__main__":
    print(insertion_sort([5, 2, 4, 6, 1, 3]))  # [1, 2, 3, 4, 5, 6]
    print(insertion_sort([3, 1, 2, 1]))        # [1, 1, 2, 3]
    print(insertion_sort([]))                  # []
