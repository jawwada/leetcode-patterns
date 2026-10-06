"""
Game of Life, In Place (basics: matrices)
Compute the next generation of a 0/1 board in place, with O(1) extra space.
  [[0, 0, 0], [1, 1, 1], [0, 0, 0]]  ->  [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

Idea: a cell is live next turn if it has 3 live neighbors, or 2 and is live now.
      Keep the current state in bit 0 and write the next state into bit 1, so neighbors
      still read the old state (cell & 1). A last pass shifts bit 1 down into place.

Pseudocode:
  for each cell:
      live = how many of the 8 neighbors have bit 0 set
      if live == 3, or (live == 2 and the cell is live now):
          cell |= 2                        # next state goes into bit 1
  for each cell: cell >>= 1                # next state becomes the state

Time O(m*n), space O(1).
"""


def live_neighbors(board, r, c):
    m, n = len(board), len(board[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nr, nc = r + dr, c + dc
            if (dr, dc) != (0, 0) and 0 <= nr < m and 0 <= nc < n:  # not itself, inside
                count += board[nr][nc] & 1   # bit 0 = current state
    return count


def game_of_life(board):
    m, n = len(board), len(board[0])
    for r in range(m):
        for c in range(n):
            alive = board[r][c] & 1          # current state
            live = live_neighbors(board, r, c)
            if live == 3 or (live == 2 and alive == 1):   # born or survives
                board[r][c] |= 2             # next state goes into bit 1
    for r in range(m):
        for c in range(n):
            board[r][c] >>= 1                # bit 1 becomes the state
    return board


if __name__ == "__main__":
    print(game_of_life([[0, 0, 0], [1, 1, 1], [0, 0, 0]]))  # [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    print(game_of_life([[1, 1], [1, 0]]))                   # [[1, 1], [1, 1]]
    print(game_of_life([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))  # [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
