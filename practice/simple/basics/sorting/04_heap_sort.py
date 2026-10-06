"""
Heap Sort (basics: sorting)
Sort a list in place with a max-heap that lives inside the list itself.
  [5, 2, 4, 6, 1, 3]  ->  [1, 2, 3, 4, 5, 6]

Idea: a max-heap keeps its biggest item at a[0] (the children of i are 2i + 1 and 2i + 2).
      Build the heap, then repeat: swap the root to the end of the heap part, shrink the
      heap by one, and sift the new root down. The sorted part grows from the right.

Pseudocode:
  for i from n // 2 - 1 down to 0: sift_down(i, n)   # build the heap, last parent first
  for end from n - 1 down to 1:
      swap a[0] and a[end]               # the max moves to its final slot
      sift_down(0, end)                  # the heap is now a[:end]

  sift_down(i, size):
      while i has a child inside size:
          c = the bigger child
          if a[c] <= a[i]: stop          # heap order holds
          swap a[i] and a[c]; i = c

Time O(n log n) always, space O(1) extra (sorts the copy in place). Not stable.
"""


def sift_down(a, i, size):
    while 2 * i + 1 < size:              # i has at least a left child
        c = 2 * i + 1
        if c + 1 < size and a[c + 1] > a[c]:
            c += 1                       # right child is bigger
        if a[c] <= a[i]:
            return                       # heap order holds
        a[i], a[c] = a[c], a[i]          # move the smaller value down
        i = c


def heap_sort(nums):
    a = list(nums)
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):  # build a max-heap, last parent first
        sift_down(a, i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]      # max goes to the sorted suffix
        sift_down(a, 0, end)             # repair the shrunk heap a[:end]
    return a


if __name__ == "__main__":
    print(heap_sort([5, 2, 4, 6, 1, 3]))  # [1, 2, 3, 4, 5, 6]
    print(heap_sort([3, 1, 2, 1]))        # [1, 1, 2, 3]
    print(heap_sort([]))                  # []
