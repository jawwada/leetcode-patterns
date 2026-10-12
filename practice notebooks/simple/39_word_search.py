"""
Word Search (LeetCode 79)
Can the word be traced through up/down/left/right neighbours, each cell used at most once?
  board = ["ABCE", "SFCS", "ADEE"], word = "ABCCED"  ->  True   ("ABCB" -> False)

Idea: start a DFS from every cell. At depth k the cell must equal word[k].
      Mark the cell '#' while it is on the path so it cannot be reused; restore it on the way back.

Pseudocode:
  dfs(r, c, k):
      if k == len(word): return True
      if (r, c) off board or board[r][c] != word[k]: return False
      mark board[r][c] = '#'
      found = dfs on the 4 neighbours with k + 1
      restore board[r][c]
      return found
  return any dfs(r, c, 0) over all cells

Time O(m * n * 3^L), space O(L) recursion depth.
"""


def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, k):
        if k == len(word):                                   # matched every letter
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[k]:
            return False
        saved, board[r][c] = board[r][c], "#"                # mark: on the path
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                 or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = saved                                  # restore on the way back
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


if __name__ == "__main__":
    board = [list("ABCE"), list("SFCS"), list("ADEE")]
    print(exist(board, "ABCCED"))  # True
    print(exist(board, "SEE"))     # True
    print(exist(board, "ABCB"))    # False
