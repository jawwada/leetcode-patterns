"""
Jump Game IV (LeetCode 1345) - Hard
Chapter: graphs
Pattern: BFS on implicit graph with value buckets consumed once

From index i of arr you may jump to i + 1, to i - 1, or to any j with arr[j] == arr[i].
Return the minimum number of jumps from index 0 to the last index.
Example: arr = [100,-23,-23,404,100,23,23,23,3,404] -> 3 (0 -> 4 -> 3 -> 9).
"""
from collections import deque      # popleft is O(1)


# --- brute force ---
def brute_force(arr):
    """BFS; find equal values by scanning the whole array at every pop. O(n^2) time, O(n) space."""
    n = len(arr)
    jumps_to = [-1] * n                       # -1 means not reached yet
    jumps_to[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        if i == n - 1:
            return jumps_to[i]
        neighbours = [i - 1, i + 1]
        for j in range(n):                    # O(n) scan for every index popped
            if arr[j] == arr[i] and j != i:
                neighbours.append(j)
        for j in neighbours:
            if 0 <= j < n and jumps_to[j] == -1:
                jumps_to[j] = jumps_to[i] + 1
                queue.append(j)
    return jumps_to[n - 1]


# --- optimal ---
def indices_by_value(arr):
    """value -> list of every index holding it."""
    indices_of = {}
    for i in range(len(arr)):
        if arr[i] not in indices_of:
            indices_of[arr[i]] = []
        indices_of[arr[i]].append(i)
    return indices_of


def jump_game_iv(arr):
    """BFS in layers; each value's index bucket is used once, then dropped. O(n) time and space."""
    n = len(arr)
    if n == 1:
        return 0
    indices_of = indices_by_value(arr)
    seen = [False] * n
    seen[0] = True
    queue = deque([0])
    jumps = 0
    while queue:
        for _ in range(len(queue)):           # one layer = one jump
            i = queue.popleft()
            if i == n - 1:
                return jumps
            neighbours = [i - 1, i + 1]
            if arr[i] in indices_of:
                neighbours += indices_of[arr[i]]
                del indices_of[arr[i]]        # all of this value is queued now: never rescan
            for j in neighbours:
                if 0 <= j < n and not seen[j]:
                    seen[j] = True
                    queue.append(j)
        jumps += 1
    return -1


# --- try the brute force ---
print(brute_force([100, -23, -23, 404, 100, 23, 23, 23, 3, 404]))   # -> 3
print(brute_force([7]))                                             # -> 0
print(brute_force([7, 6, 9, 6, 9, 6, 9, 7]))                        # -> 1
print(brute_force([11, 22, 7, 7, 7, 7, 7, 7, 7, 22, 13]))           # -> 3
print(brute_force([5] * 1000))                                      # -> 1


# --- try the optimal ---
print(jump_game_iv([100, -23, -23, 404, 100, 23, 23, 23, 3, 404]))   # -> 3
print(jump_game_iv([7]))                                             # -> 0
print(jump_game_iv([7, 6, 9, 6, 9, 6, 9, 7]))                        # -> 1
print(jump_game_iv([11, 22, 7, 7, 7, 7, 7, 7, 7, 22, 13]))           # -> 3
print(jump_game_iv([5] * 1000))                                      # -> 1
