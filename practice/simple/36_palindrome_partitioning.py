"""
Palindrome Partitioning (LeetCode 131)
Return every way to cut s into pieces that are all palindromes.
  s = "aab"  ->  [["a", "a", "b"], ["aa", "b"]]

Idea: build the partition left to right. At position start, try every prefix s[start:end];
      only a palindromic prefix is chosen, then recurse on the rest and undo the choice.
      A non-palindrome prefix prunes every partition that would begin with it.

Pseudocode:
  backtrack(start):
      if start == len(s): record a copy of path
      for end in start+1 .. len(s):
          piece = s[start:end]
          if piece is a palindrome:
              path.append(piece); backtrack(end); path.pop()

Time O(n * 2^n) worst case, space O(n) recursion depth.
"""


def partition(s):
    result, path = [], []

    def backtrack(start):
        if start == len(s):                   # whole string used: record
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:          # only palindromic prefixes
                path.append(piece)            # choose
                backtrack(end)                # explore the rest
                path.pop()                    # undo

    backtrack(0)
    return result


if __name__ == "__main__":
    print(partition("aab"))  # [['a', 'a', 'b'], ['aa', 'b']]
    print(partition("a"))    # [['a']]
