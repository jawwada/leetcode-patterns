"""
Minimum Moves to Move a Box to Their Target Location (LeetCode 1263) - Hard
Chapter: graphs
Pattern: 0-1 BFS (deque shortest path)

A grid holds walls '#', floor '.', the player 'S', a box 'B' and a target 'T'. The player walks
4-directionally for free; walking into the box pushes it one cell if the cell beyond is floor.
Return the minimum number of pushes to get the box onto the target, or -1.
Example: ["######","#T####","#..B.#","#.##.#","#...S#","######"] -> 3 (push left twice, walk
round below the box, push up).
"""
import heapq                             # heappush / heappop keep the smallest item at index 0
import math                              # math.inf for "no distance known yet"
from collections import deque            # popleft and appendleft are O(1)


# --- helpers ---
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]     # down, up, right, left


def find(grid, symbol):
    """(row, col) of the first cell holding symbol."""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == symbol:
                return (row, col)
    return None


def is_free(grid, row, col):
    """True when (row, col) is inside the grid and not a wall."""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != "#"


def next_state(grid, state, d_row, d_col):
    """Step the player once: (new state, pushes spent), or None when the step is blocked."""
    box_row, box_col, player_row, player_col = state
    new_row, new_col = player_row + d_row, player_col + d_col     # where the player steps
    if not is_free(grid, new_row, new_col):
        return None
    if (new_row, new_col) != (box_row, box_col):
        return ((box_row, box_col, new_row, new_col), 0)          # a plain walk, free
    if not is_free(grid, box_row + d_row, box_col + d_col):       # stepping into the box = push
        return None
    return ((box_row + d_row, box_col + d_col, new_row, new_col), 1)


# --- brute force ---
def brute_force(grid):
    """Dijkstra with a heap over (box, player) states; edge costs are only 0 or 1. O(S log S)."""
    box_row, box_col = find(grid, "B")
    player_row, player_col = find(grid, "S")
    target = find(grid, "T")
    start = (box_row, box_col, player_row, player_col)
    best = {start: 0}                                 # state -> fewest pushes known
    heap = [(0, start)]
    while heap:
        pushes, state = heapq.heappop(heap)           # O(log S) just to order 0s before 1s
        if (state[0], state[1]) == target:
            return pushes
        if pushes > best[state]:
            continue                                  # a stale heap entry
        for d_row, d_col in DIRECTIONS:
            step = next_state(grid, state, d_row, d_col)
            if step is None:
                continue
            new_state, cost = step
            if pushes + cost < best.get(new_state, math.inf):
                best[new_state] = pushes + cost
                heapq.heappush(heap, (pushes + cost, new_state))
    return -1


# --- optimal ---
def minimum_moves(grid):
    """0-1 BFS: free walks go to the front of the deque, pushes to the back. O(S) time."""
    box_row, box_col = find(grid, "B")
    player_row, player_col = find(grid, "S")
    target = find(grid, "T")
    start = (box_row, box_col, player_row, player_col)
    pushes_to = {start: 0}
    queue = deque([start])
    while queue:
        state = queue.popleft()                       # the deque stays sorted: all d, then d + 1
        pushes = pushes_to[state]
        if (state[0], state[1]) == target:
            return pushes
        for d_row, d_col in DIRECTIONS:
            step = next_state(grid, state, d_row, d_col)
            if step is None:
                continue
            new_state, cost = step
            if pushes + cost < pushes_to.get(new_state, math.inf):
                pushes_to[new_state] = pushes + cost
                if cost == 0:
                    queue.appendleft(new_state)       # same distance: handle it before the rest
                else:
                    queue.append(new_state)
    return -1


# --- try the brute force ---
print(brute_force(["######", "#T####", "#..B.#", "#.##.#", "#...S#", "######"]))   # -> 3
print(brute_force(["######", "#T####", "#..B.#", "####.#", "#...S#", "######"]))   # -> -1
print(brute_force(["######", "#T..##", "#.#B.#", "#....#", "#...S#", "######"]))   # -> 5
print(brute_force(["#####", "#.T.#", "#...#", "#.#.#", "#S.B#", "#####"]))         # -> -1
print(brute_force(["T.BS."]))                                                      # -> 2


# --- try the optimal ---
print(minimum_moves(["######", "#T####", "#..B.#", "#.##.#", "#...S#", "######"]))   # -> 3
print(minimum_moves(["######", "#T####", "#..B.#", "####.#", "#...S#", "######"]))   # -> -1
print(minimum_moves(["######", "#T..##", "#.#B.#", "#....#", "#...S#", "######"]))   # -> 5
print(minimum_moves(["#####", "#.T.#", "#...#", "#.#.#", "#S.B#", "#####"]))         # -> -1
print(minimum_moves(["T.BS."]))                                                      # -> 2
