"""
Sliding Puzzle (LeetCode 773) - Hard
Chapter: graphs
Pattern: BFS on implicit graph (board-state strings)

A 2x3 board holds tiles 1..5 and one blank 0. A move swaps the blank with a 4-directionally
adjacent tile. Return the minimum number of moves to reach [[1,2,3],[4,5,0]], or -1 if the
board can never be solved.
Example: [[1,2,3],[4,0,5]] -> 1; [[4,1,2],[5,0,3]] -> 5; [[1,2,3],[5,4,0]] -> -1.
"""
from collections import deque            # popleft is O(1)
from itertools import permutations       # every ordering of a sequence, as tuples


# --- helpers ---
NEIGHBOURS = [[1, 3], [0, 2, 4], [1, 5], [0, 4], [1, 3, 5], [2, 4]]   # grid neighbours of cell i


def flatten(board):
    """[[1,2,3],[4,0,5]] -> "123405": a string is hashable, so it can go in a set."""
    text = ""
    for row in board:
        for tile in row:
            text += str(tile)
    return text


def swap(state, i, j):
    """Return the state string with the characters at i and j exchanged."""
    chars = list(state)
    chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


# --- brute force ---
def one_move(a, b):
    """True when b is a by sliding one tile: two cells differ, one holds the blank, adjacent."""
    changed = []
    for i in range(6):
        if a[i] != b[i]:
            changed.append(i)
    if len(changed) != 2:
        return False
    first, second = changed
    if a[first] != "0" and a[second] != "0":
        return False
    return second in NEIGHBOURS[first]


def brute_force(board):
    """BFS, but find neighbours by testing all 720 boards for a one-move difference. O(720^2)."""
    boards = []
    for order in permutations("012345"):
        boards.append("".join(order))
    start = flatten(board)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, moves = queue.popleft()
        if state == "123450":
            return moves
        for other in boards:                 # 719 failed comparisons per board
            if other not in seen and one_move(state, other):
                seen.add(other)
                queue.append((other, moves + 1))
    return -1


# --- optimal ---
def sliding_puzzle(board):
    """BFS over board strings; a neighbour is one swap of the blank. O(720 * 3) time and space."""
    start = flatten(board)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, moves = queue.popleft()
        if state == "123450":
            return moves
        blank = state.index("0")
        for cell in NEIGHBOURS[blank]:       # slide a neighbouring tile into the blank
            next_state = swap(state, blank, cell)
            if next_state not in seen:
                seen.add(next_state)
                queue.append((next_state, moves + 1))
    return -1


# --- try the brute force ---
print(brute_force([[1, 2, 3], [4, 0, 5]]))   # -> 1
print(brute_force([[1, 2, 3], [5, 4, 0]]))   # -> -1
print(brute_force([[4, 1, 2], [5, 0, 3]]))   # -> 5
print(brute_force([[1, 2, 3], [4, 5, 0]]))   # -> 0


# --- try the optimal ---
print(sliding_puzzle([[1, 2, 3], [4, 0, 5]]))   # -> 1
print(sliding_puzzle([[1, 2, 3], [5, 4, 0]]))   # -> -1
print(sliding_puzzle([[4, 1, 2], [5, 0, 3]]))   # -> 5
print(sliding_puzzle([[1, 2, 3], [4, 5, 0]]))   # -> 0
