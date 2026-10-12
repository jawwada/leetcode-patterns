"""
Heapify by Hand (basics: heaps)
Rearrange a list into a min-heap (every parent <= its children) without heapq.
  [9, 4, 7, 1, 2, 6, 3]  ->  [1, 2, 3, 4, 9, 6, 7]

Idea: node i has children 2i+1 and 2i+2, so the last parent is n//2 - 1 and the leaves are
      already heaps. Sift parents down from the last one to the root: when i's turn comes, both
      subtrees under it are heaps. Total work is O(n), less than n separate pushes.

Pseudocode:
  sift_down(a, i):
      while True:
          smallest = index of the smallest among a[i] and its children
          if smallest == i: stop                   # no child is smaller
          swap a[i], a[smallest]; i = smallest
  build_min_heap(a):
      for i from n//2 - 1 down to 0: sift_down(a, i)

Time O(n) to build (one sift is O(log n)), space O(n) for the copy.
"""


def sift_down(a, i, n):
    while True:
        left, right, smallest = 2 * i + 1, 2 * i + 2, i
        if left < n and a[left] < a[smallest]:
            smallest = left
        if right < n and a[right] < a[smallest]:
            smallest = right
        if smallest == i:                # no child is smaller: in place
            return
        a[i], a[smallest] = a[smallest], a[i]   # swap with the smaller child
        i = smallest                     # keep sinking from there


def build_min_heap(nums):
    a = list(nums)                       # work on a copy
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):  # last parent down to the root (index 0)
        sift_down(a, i, n)
    return a


if __name__ == "__main__":
    print(build_min_heap([9, 4, 7, 1, 2, 6, 3]))  # [1, 2, 3, 4, 9, 6, 7]
    print(build_min_heap([5, 4, 3, 2, 1]))        # [1, 2, 3, 5, 4]
    print(build_min_heap([]))                     # []
