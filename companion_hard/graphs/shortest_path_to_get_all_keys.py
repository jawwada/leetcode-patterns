"""
Shortest Path to Get All Keys (LeetCode 864) - Hard
Chapter: graphs
Pattern: BFS over augmented states (position + bitmask/budget)

A grid has '.' empty cells, '#' walls, '@' the start, lowercase keys and matching uppercase locks
(at most 6 pairs). You walk 4-directionally, pick up keys automatically, and may pass a lock only
while holding its key. Return the fewest moves to collect every key, or -1.
Example: ["@.a..","###.#","b.A.B"] -> 8 (fetch a, go down the gap, pass A, reach b); ["@Aa"] -> -1.
"""
from collections import deque            # popleft is O(1)
from itertools import permutations       # every ordering of a sequence, as tuples


# --- helpers ---
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]     # down, up, right, left


def find_symbols(grid):
    """Map '@' and every key letter to its (row, col)."""
    position = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell = grid[row][col]
            if cell == "@" or cell.islower():
                position[cell] = (row, col)
    return position


# --- brute force ---
def moves_between(grid, start, goal, held):
    """Plain BFS from start to goal; walls and locks whose key is not held block the way."""
    rows, cols = len(grid), len(grid[0])
    moves_to = {start: 0}
    queue = deque([start])
    while queue:
        row, col = queue.popleft()
        if (row, col) == goal:
            return moves_to[(row, col)]
        for d_row, d_col in DIRECTIONS:
            new_row, new_col = row + d_row, col + d_col
            if not (0 <= new_row < rows and 0 <= new_col < cols):
                continue
            cell = grid[new_row][new_col]
            if cell == "#" or (cell.isupper() and cell.lower() not in held):
                continue
            if (new_row, new_col) not in moves_to:
                moves_to[(new_row, new_col)] = moves_to[(row, col)] + 1
                queue.append((new_row, new_col))
    return -1


def brute_force(grid):
    """Try every pickup order; BFS leg by leg with the keys held so far. O(k! * k * m * n)."""
    position = find_symbols(grid)
    keys = []
    for symbol in sorted(position):
        if symbol != "@":
            keys.append(symbol)
    best = -1
    for order in permutations(keys):              # the same (cell, keys held) is searched again
        total = 0
        current = position["@"]
        held = set()
        for key in order:
            leg = moves_between(grid, current, position[key], held)
            if leg == -1:
                total = -1                        # this order is blocked
                break
            total += leg
            current = position[key]
            held.add(key)
        if total != -1 and (best == -1 or total < best):
            best = total
    return best


# --- optimal ---
def keys_after_entering(grid, row, col, held):
    """The key bitmask after stepping onto (row, col), or -1 when that cell cannot be entered."""
    if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        return -1
    cell = grid[row][col]
    if cell == "#":
        return -1
    if cell.islower():
        return held | (1 << (ord(cell) - ord("a")))         # pick the key up: set its bit
    if cell.isupper() and not held & (1 << (ord(cell) - ord("A"))):
        return -1                                           # a lock and we hold no key for it
    return held


def shortest_path_all_keys(grid):
    """One BFS over states (row, col, keys held as a bitmask). O(m * n * 2^k) time and space."""
    all_keys = 0                                  # bit i set = key chr(97 + i) is on the grid
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "@":
                start = (row, col, 0)
            elif grid[row][col].islower():
                all_keys = all_keys | (1 << (ord(grid[row][col]) - ord("a")))
    queue = deque([start])
    seen = {start}
    moves = 0
    while queue:
        for _ in range(len(queue)):               # one layer = one move
            row, col, held = queue.popleft()
            if held == all_keys:
                return moves
            for d_row, d_col in DIRECTIONS:
                new_held = keys_after_entering(grid, row + d_row, col + d_col, held)
                state = (row + d_row, col + d_col, new_held)
                if new_held != -1 and state not in seen:   # same cell, more keys: a new state
                    seen.add(state)
                    queue.append(state)
        moves += 1
    return -1


# --- try the brute force ---
print(brute_force(["@.a..", "###.#", "b.A.B"]))                         # -> 8
print(brute_force(["@..aA", ".#B#.", "....b"]))                         # -> 6
print(brute_force(["@Aa"]))                                             # -> -1
print(brute_force(["@...a", ".###.", "b.B.A", "..C..", "c...."]))       # -> 12


# --- try the optimal ---
print(shortest_path_all_keys(["@.a..", "###.#", "b.A.B"]))                         # -> 8
print(shortest_path_all_keys(["@..aA", ".#B#.", "....b"]))                         # -> 6
print(shortest_path_all_keys(["@Aa"]))                                             # -> -1
print(shortest_path_all_keys(["@...a", ".###.", "b.B.A", "..C..", "c...."]))       # -> 12
