"""
Word Search (LeetCode 79) - Medium
Area: backtracking
Key operations: DFS from every cell, match word[k] at depth k, mark the cell '#' while on the path, restore on return

Given an m x n board of letters and a word, return True if the word can be traced through
horizontally or vertically adjacent cells, each cell used at most once.
Example: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED" -> True
(word = "ABCB" -> False: the B would have to be reused)
"""
from typing import List


# --- helpers ---
def draw(board: List[List[str]]) -> str:
    return " / ".join("".join(row) for row in board)


# --- brute force ---
def brute_force(board: List[List[str]], word: str) -> bool:
    """Enumerate every self-avoiding path of len(word) cells from every start (path kept as a set) and
    compare the spelled string only at the leaf. O(m * n * 4^L * L): a path whose first letter is already
    wrong is still extended L - 1 more steps; the optimal compares at every step and cuts it at once."""
    rows, cols, L = len(board), len(board[0]), len(word)

    def paths(r: int, c: int, visited: set, letters: List[str]) -> bool:
        if len(letters) == L:
            return "".join(letters) == word
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if paths(nr, nc, visited | {(nr, nc)}, letters + [board[nr][nc]]):
                    return True
        return False

    return any(paths(r, c, {(r, c)}, [board[r][c]]) for r in range(rows) for c in range(cols))


# --- optimal ---
def solve(board: List[List[str]], word: str) -> bool:
    """From every cell, DFS that matches word[k] at depth k; a cell is overwritten with '#' while it is on
    the path and restored on the way back, so no cell is used twice. O(m * n * 3^L) time, O(L) stack."""
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, k: int) -> bool:
        if k == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[k]:
            return False
        saved, board[r][c] = board[r][c], "#"
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                 or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = saved
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


# --- demo ---
def demo():
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    return solve(board, "ABCCED")


# --- bugs ---
BUGS = [
    {
        "replace": "        saved, board[r][c] = board[r][c], \"#\"",
        "with":    "        saved = board[r][c]",
        "fix": "overwrite the cell with '#' while it is on the path so the search cannot step on it twice",
        "why": "Without the mark a cell can be reused, so 'ABCB' is found by stepping back onto the B that is already in the path.",
        "decoys": [
            {"line": "        board[r][c] = saved", "change": "should restore only when found is False"},
            {"line": "    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))", "change": "should start at depth 1"},
            {"line": "            return True", "change": "should return k == len(word)"},
        ],
    },
    {
        "replace": "        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[k]:",
        "with":    "        if r < 0 or r > rows or c < 0 or c > cols or board[r][c] != word[k]:",
        "fix": "the last valid row is rows - 1, so reject r >= rows (and c >= cols)",
        "why": "r == rows passes the check and board[rows] raises IndexError, so any search that walks off the bottom or right edge crashes.",
        "decoys": [
            {"line": "        board[r][c] = saved", "change": "should run before the four recursive calls"},
            {"line": "        return found", "change": "should return True"},
            {"line": "    rows, cols = len(board), len(board[0])", "change": "should be len(board[0]), len(board)"},
        ],
    },
    {
        "replace": "        if k == len(word):",
        "with":    "        if k == len(word) - 1:",
        "fix": "succeed only after all len(word) letters matched; k == len(word) - 1 skips the last letter",
        "why": "The last letter is never compared, so any in-bounds neighbour completes the word: 'ABCB' and 'ABCCEDX' become True on the example board.",
        "decoys": [
            {"line": "            return False", "change": "should return None"},
            {"line": "        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)", "change": "should pass k, not k + 1"},
            {"line": "                 or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))", "change": "should use and so every direction must succeed"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
