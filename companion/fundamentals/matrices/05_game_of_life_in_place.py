"""
Game of Life In Place - Fundamentals
Chapter: fundamentals/matrices
Key operations: count 8 neighbors with & 1, store the next state in bit 1, decode with >> 1

Each cell is 1 (live) or 0 (dead). A live cell with 2 or 3 live neighbors stays live, a dead cell
with exactly 3 live neighbors becomes live, everything else is dead. Update the board in place with
O(1) extra space: bit 0 keeps the current state while the pass runs, bit 1 receives the next state,
and a final pass shifts every cell right by one.
Example: [[0,1,0],[0,0,1],[1,1,1],[0,0,0]] -> [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]
"""


# --- algorithm ---
def count_live_neighbors(board, row, col):
    """Count the 8 neighbors' current state: read bit 0 only, bit 1 may already hold the next."""
    rows = len(board)
    cols = len(board[0])
    live = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue          # a cell is not its own neighbor
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                live += board[nr][nc] & 1
    return live


def game_of_life(board):
    """Write the next state into bit 1 during the pass, then shift every cell right. O(m*n)."""
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            live = count_live_neighbors(board, row, col)
            alive = board[row][col] & 1
            if live == 3 or (live == 2 and alive == 1):    # 2 neighbors only KEEP a cell alive
                board[row][col] |= 2
    for row in range(rows):
        for col in range(cols):
            board[row][col] >>= 1     # drop the old state, keep the new one
    return board


# --- try it ---
print(game_of_life([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]))
# -> [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
print(game_of_life([[0, 0, 0], [1, 1, 1], [0, 0, 0]]))     # -> [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
print(game_of_life([[1, 1], [1, 1]]))                      # -> [[1, 1], [1, 1]]
