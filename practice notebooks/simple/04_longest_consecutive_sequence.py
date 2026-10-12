"""
Longest Consecutive Sequence (LeetCode 128)
Return the length of the longest run of consecutive integers (in any order) in O(n).
  [100, 4, 200, 1, 3, 2]  ->  4   (1, 2, 3, 4)

Idea: put everything in a set. Only start counting from a number x whose x - 1
      is missing (the start of a run), so each number is walked over just once.

Pseudocode:
  values = set(nums)
  for x in values:
      if x - 1 in values: skip       # not a run start
      count up while x + length in values
      best = max(best, length)

Time O(n), space O(n).
"""


def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:              # not the start of a run
            continue
        length = 1
        while x + length in values:      # walk up the run
            length += 1
        best = max(best, length)
    return best


if __name__ == "__main__":
    print(longest_consecutive([100, 4, 200, 1, 3, 2]))              # 4
    print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))      # 9
    print(longest_consecutive([]))                                  # 0
