"""
Game of Life (LeetCode 289) - Basics
Area: matrices
Key operations: count 8 neighbors with & 1, store the next state in bit 1, decode with >> 1

Each cell is 1 (live) or 0 (dead). A live cell with 2 or 3 live neighbors stays live, a dead cell
with exactly 3 live neighbors becomes live, everything else is dead. Update the board in place with
O(1) extra space: bit 0 keeps the current state while the pass runs, bit 1 receives the next state,
and a final pass shifts every cell right by one.
Example: [[0,1,0],[0,0,1],[1,1,1],[0,0,0]] -> [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]
"""


# --- brute force ---
def brute_force(board):
    """Count neighbors from the untouched input and write a NEW board. O(m*n) time, O(m*n) extra space."""
    m, n = len(board), len(board[0])
    out = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            live = sum(board[nr][nc] for nr in range(max(0, r - 1), min(m, r + 2)) for nc in range(max(0, c - 1), min(n, c + 2))) - board[r][c]
            out[r][c] = 1 if live == 3 or (live == 2 and board[r][c] == 1) else 0
    return out


# --- optimal ---
def solve(board):
    """Read neighbors with & 1 (current state only), write the next state into bit 1, then shift everything right. O(m*n), O(1) space."""
    m, n = len(board), len(board[0])
    for r in range(m):
        for c in range(n):
            live = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if (dr or dc) and 0 <= nr < m and 0 <= nc < n:
                        live += board[nr][nc] & 1
            if live == 3 or (live == 2 and board[r][c] & 1):
                board[r][c] |= 2
    for r in range(m):
        for c in range(n):
            board[r][c] >>= 1
    return board


# --- demo ---
def demo():
    return solve([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]])


# --- bugs ---
BUGS = [
    {
        "replace": "                        live += board[nr][nc] & 1",
        "with":    "                        live += board[nr][nc]",
        "fix": "read only bit 0 of a neighbor: cells above and to the left already carry their NEXT state in bit 1",
        "why": "A neighbor already encoded as 2 or 3 is counted as 2 or 3 live cells, so counts are inflated: the blinker [[0,0,0],[1,1,1],[0,0,0]] comes out wrong.",
        "decoys": [
            {"line": "                board[r][c] |= 2", "change": "should be = 2"},
            {"line": "            board[r][c] >>= 1", "change": "should be &= 1"},
            {"line": "                    nr, nc = r + dr, c + dc", "change": "should be r + dc, c + dr"},
        ],
    },
    {
        "replace": "            if live == 3 or (live == 2 and board[r][c] & 1):",
        "with":    "            if live == 3 or live == 2:",
        "fix": "two neighbors only KEEP a live cell alive; a dead cell needs exactly three to be born",
        "why": "Dead cells with two live neighbors are born: [[0,0,0],[0,1,0],[0,0,0]] grows instead of dying out.",
        "decoys": [
            {"line": "            live = 0", "change": "should start at board[r][c] & 1"},
            {"line": "            for dr in (-1, 0, 1):", "change": "should be (-1, 1)"},
            {"line": "    return board", "change": "should return a copy"},
        ],
    },
    {
        "replace": "                    if (dr or dc) and 0 <= nr < m and 0 <= nc < n:",
        "with":    "                    if 0 <= nr < m and 0 <= nc < n:",
        "fix": "skip (dr, dc) == (0, 0): a cell is not its own neighbor",
        "why": "Every live cell counts itself, so a live cell with 1 neighbor survives and one with 3 dies: the block [[1,1],[1,1]] is destroyed.",
        "decoys": [
            {"line": "                for dc in (-1, 0, 1):", "change": "should be range(-1, 1)"},
            {"line": "    m, n = len(board), len(board[0])", "change": "should be len(board[0]), len(board)"},
            {"line": "            if live == 3 or (live == 2 and board[r][c] & 1):", "change": "should be live >= 3"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
