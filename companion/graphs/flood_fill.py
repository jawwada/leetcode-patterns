"""
Flood Fill (LeetCode 733) - Easy
Chapter: graphs
Pattern: Grid flood fill (DFS/BFS)

Given an image as a grid of colours, a start pixel (sr, sc) and a new colour, recolour the
start pixel and every pixel 4-connected to it that has the start pixel's original colour.
Example: image=[[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, color=2 -> [[2,2,2],[2,2,0],[2,0,1]]
(the bottom-right 1 is not connected to the start, so it keeps its colour).
"""


# --- brute force ---
def brute_force(image, sr, sc, color):
    """Resweep the whole grid until no old-colour pixel next to a marked one is left. O((mn)^2)."""
    rows = len(image)
    cols = len(image[0])
    old = image[sr][sc]
    marked = []                      # marked[r][c] is True once the pixel belongs to the region
    for r in range(rows):
        marked.append([False] * cols)
    marked[sr][sc] = True
    changed = True
    while changed:                   # one full sweep per round; stop when a sweep adds nothing
        changed = False
        for r in range(rows):
            for c in range(cols):
                if marked[r][c] or image[r][c] != old:
                    continue
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and marked[nr][nc]:
                        marked[r][c] = True      # touches the region: it joins
                        changed = True
                        break
    for r in range(rows):
        for c in range(cols):
            if marked[r][c]:
                image[r][c] = color
    return image


# --- optimal ---
def flood_fill(image, sr, sc, color):
    """DFS with a stack from the start; paint on push so each pixel is pushed once. O(mn) time."""
    old = image[sr][sc]
    if old == color:                 # nothing would change, and painting could not mark visited
        return image
    rows = len(image)
    cols = len(image[0])
    image[sr][sc] = color
    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == old:
                image[nr][nc] = color    # paint now: a painted pixel no longer matches old
                stack.append((nr, nc))
    return image


# --- try the brute force ---
print(brute_force([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2))   # -> [[2,2,2],[2,2,0],[2,0,1]]
print(brute_force([[0, 0, 0], [0, 0, 0]], 0, 0, 0))               # -> [[0,0,0],[0,0,0]]
print(brute_force([[1, 0, 1], [1, 0, 1], [1, 1, 1]], 0, 2, 3))   # -> [[3,0,3],[3,0,3],[3,3,3]]


# --- try the optimal ---
print(flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2))    # -> [[2,2,2],[2,2,0],[2,0,1]]
print(flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0))                # -> [[0,0,0],[0,0,0]]
print(flood_fill([[1, 0, 1], [1, 0, 1], [1, 1, 1]], 0, 2, 3))    # -> [[3,0,3],[3,0,3],[3,3,3]]
