"""
Game of Life - Update in Place with Two-Bit States

Each cell is live (1) or dead (0). Live cells with 2 or 3 live neighbors (of 8)
survive, dead cells with exactly 3 come alive, all other cells are dead next.
Update the board in place: [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]] ->
[[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]].
"""


# --- algorithm ---
def count_live_neighbors(board, row, col):
    """Live cells in the 3 x 3 block around (row, col), clipped at the edges,
    reading bit 0 only, which still holds the current state. O(1)."""
    live = 0
    for near_row in range(max(0, row - 1), min(len(board), row + 2)):
        for near_col in range(max(0, col - 1), min(len(board[0]), col + 2)):
            if near_row == row and near_col == col:
                continue            # a cell is not its own neighbor
            live += board[near_row][near_col] & 1   # bit 0: current state
    return live


def game_of_life(board):
    """Pass 1 writes each next state into bit 1, pass 2 shifts it down to
    bit 0. O(m n) time, O(1) extra space."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            live = count_live_neighbors(board, row, col)
            alive = board[row][col] & 1
            if live == 3 or (alive == 1 and live == 2):
                board[row][col] = board[row][col] | 2   # bit 1: live next
    for row in range(len(board)):
        for col in range(len(board[0])):
            board[row][col] = board[row][col] >> 1      # keep only the next


# --- try it ---
board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
game_of_life(board)
print(board)        # -> [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
blinker = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
game_of_life(blinker)
print(blinker)      # -> [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
block = [[1, 1], [1, 1]]
game_of_life(block)
print(block)        # -> [[1, 1], [1, 1]]
