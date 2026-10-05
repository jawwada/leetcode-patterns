"""
Pacific Atlantic Water Flow (LeetCode 417) - Medium
Chapter: graphs
Pattern: Multi-source reverse BFS/DFS from the boundary

An m x n height grid touches the Pacific along its top and left edges and the Atlantic along
its bottom and right edges. Water flows from a cell to a 4-neighbour whose height is less than
or equal to its own. Return every cell from which water can reach both oceans.
Example: [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
-> [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]].
"""
from collections import deque      # popleft is O(1)


# --- brute force ---
def brute_force(heights):
    """Flow downhill from every cell separately; keep it if both oceans are reached. O((mn)^2)."""
    rows = len(heights)
    cols = len(heights[0])
    result = []
    for start_r in range(rows):
        for start_c in range(cols):
            seen = {(start_r, start_c)}
            stack = [(start_r, start_c)]
            pacific = False
            atlantic = False
            while stack:
                r, c = stack.pop()
                if r == 0 or c == 0:
                    pacific = True
                if r == rows - 1 or c == cols - 1:
                    atlantic = True
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                        if heights[nr][nc] <= heights[r][c]:   # water only flows down or level
                            seen.add((nr, nc))
                            stack.append((nr, nc))
            if pacific and atlantic:
                result.append([start_r, start_c])
    return result


# --- optimal ---
def climb(heights, sources):
    """BFS uphill from one ocean's border cells; return a grid of the cells that drain to it."""
    rows = len(heights)
    cols = len(heights[0])
    reached = []
    for r in range(rows):
        reached.append([False] * cols)
    queue = deque()
    for r, c in sources:
        reached[r][c] = True
        queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and not reached[nr][nc]:
                if heights[nr][nc] >= heights[r][c]:   # reverse the flow: walk uphill from the sea
                    reached[nr][nc] = True
                    queue.append((nr, nc))
    return reached


def pacific_atlantic_water_flow(heights):
    """Climb from each ocean's edge once; the answer is the cells both climbs reach. O(mn) time."""
    rows = len(heights)
    cols = len(heights[0])
    pacific_edge = []
    atlantic_edge = []
    for r in range(rows):
        pacific_edge.append((r, 0))              # left column
        atlantic_edge.append((r, cols - 1))      # right column
    for c in range(cols):
        pacific_edge.append((0, c))              # top row
        atlantic_edge.append((rows - 1, c))      # bottom row
    from_pacific = climb(heights, pacific_edge)
    from_atlantic = climb(heights, atlantic_edge)
    result = []
    for r in range(rows):
        for c in range(cols):
            if from_pacific[r][c] and from_atlantic[r][c]:
                result.append([r, c])
    return result


# --- try the brute force ---
big = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
print(brute_force(big))                      # -> [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
print(brute_force([[1]]))                    # -> [[0, 0]]
print(brute_force([[1, 2], [4, 3]]))         # -> [[0, 1], [1, 0], [1, 1]]  ((0,0) is a pit)
print(brute_force([[3, 3, 3], [3, 1, 3], [3, 3, 3]]))   # -> every cell except the pit [1, 1]


# --- try the optimal ---
big = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
print(pacific_atlantic_water_flow(big))      # -> [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
print(pacific_atlantic_water_flow([[1]]))    # -> [[0, 0]]
print(pacific_atlantic_water_flow([[1, 2], [4, 3]]))    # -> [[0, 1], [1, 0], [1, 1]]
print(pacific_atlantic_water_flow([[3, 3, 3], [3, 1, 3], [3, 3, 3]]))   # -> all but the pit [1, 1]
