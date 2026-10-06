"""
N-Queens (LeetCode 51)
Place n queens on an n x n board so none attack each other; return every board.
  n = 4  ->  [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]

Idea: place one queen per row. A queen at (r, c) owns column c, diagonal r - c
      and anti-diagonal r + c, so three sets answer "is this square attacked?" in O(1).

Pseudocode:
  dfs(r):
      if r == n: record the board
      for c in 0 .. n-1:
          if c in cols or r-c in diag or r+c in anti: skip
          add c, r-c, r+c to the sets; queens.append(c)
          dfs(r + 1)
          remove them again                 # undo

Time O(n!), space O(n) for the sets and recursion.
"""


def solve_n_queens(n):
    result, queens = [], []                 # queens[r] = column of the queen in row r
    cols, diag, anti = set(), set(), set()

    def dfs(r):
        if r == n:                          # every row has a queen
            result.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
            return
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue                    # attacked
            cols.add(c); diag.add(r - c); anti.add(r + c)
            queens.append(c)
            dfs(r + 1)                      # next row
            queens.pop()
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)

    dfs(0)
    return result


if __name__ == "__main__":
    print(solve_n_queens(4))       # [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
    print(solve_n_queens(1))       # [['Q']]
    print(len(solve_n_queens(8)))  # 92
