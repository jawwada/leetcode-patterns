---
rank: 58
slug: multi_source_bfs
---

In a grid, `0` is an empty cell, `1` a fresh orange and `2` a rotten one. Every minute, each fresh orange next to a rotten one, up, down, left or right, turns rotten. Return the number of minutes until no fresh orange is left, or `-1` if some orange can never rot. In `[[2, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 2]]` the two rotten corners infect everything in `2` minutes.

Rot that spreads one step a minute is BFS (#30) on a graph whose nodes are the orange cells: the minute an orange rots is its distance to the nearest rotten orange, and the answer is the largest of those distances. The brute force runs a separate BFS from each of the `k` rotten oranges and keeps the minimum per cell, `O(k · rows · cols)`. One BFS does it all if every rotten orange enters the queue at minute 0. Imagine an extra node joined to every rotten orange: a single BFS from it reaches each cell through the nearest rotten orange, and seeding the queue with all of them is that same BFS with its first step already taken. The layer loop of level-order traversal (#24) counts the minutes, because each pass pops exactly the oranges that rotted in the minute before.

Picture several stones dropped into a pond at the same moment. Their ripples spread in lockstep, and wherever two meet, a cell belongs to whichever ripple arrived first. In the example each corner alone would need 5 minutes, but the two waves meet in the middle, and the combined map is the cell-by-cell minimum of the two single-source maps. Counting `fresh` up front gives both the stop condition and the `-1` test: the loop ends the moment the last fresh orange rots, and an orange still fresh when the queue runs dry is walled off from every rotten one.

```text
the minute each cell rots (· is empty)

grid        both at once     only (0,0)     only (2,3)
2 1 1 1     0 1 2 2          0 1 2 3        5 4 3 2
1 · 1 1     1 · 2 1          1 · 3 4        4 · 2 1
1 1 1 2     2 2 1 0          2 3 4 5        3 2 1 0
            answer 2         answer 5       answer 5

minute 0: the queue holds (0,0) (2,3)             fresh 9
minute 1: rots (1,0) (0,1) (1,3) (2,2)            fresh 5
minute 2: rots (2,0) (0,2) (0,3) (1,2) (2,1)      fresh 0: stop, 2 minutes
```

```pseudo
DIRECTIONS ← [(1, 0), (-1, 0), (0, 1), (0, -1)]

FUNCTION OrangesRotting(grid)
    rows ← len(grid)
    cols ← len(grid[0])
    queue ← empty queue
    fresh ← 0
    FOR row FROM 0 TO rows - 1
        FOR col FROM 0 TO cols - 1
            IF grid[row][col] = 2
                queue.enqueue((row, col))  // every source starts at minute 0
            ELSE IF grid[row][col] = 1
                fresh ← fresh + 1
    minutes ← 0
    WHILE queue is not empty AND fresh > 0
        FOR i FROM 1 TO len(queue)         // len read once: this layer only
            (row, col) ← queue.dequeue()
            FOR EACH (d_row, d_col) IN DIRECTIONS
                next_row ← row + d_row
                next_col ← col + d_col
                inside ← 0 ≤ next_row < rows AND 0 ≤ next_col < cols
                IF inside AND grid[next_row][next_col] = 1
                    grid[next_row][next_col] ← 2   // rot now: enqueued once
                    fresh ← fresh - 1
                    queue.enqueue((next_row, next_col))
        minutes ← minutes + 1
    IF fresh > 0
        RETURN -1                          // walled off from every rotten one
    RETURN minutes
```

Each cell enters the queue at most once and is looked at from at most four neighbors, so the search takes `O(rows · cols)` time and space. Reach for multi-source BFS whenever a problem asks for each cell's distance to the nearest of many sources, or how long something takes to spread from several starting points at once: the distance to the nearest `0` (LC 542), to the nearest gate (LC 286), or the water cell farthest from any land (LC 1162). The classic mistake is looping while the queue is non-empty and counting the final pass, in which the last oranges to rot infect nobody: that answers 3 here instead of 2. The `fresh > 0` condition stops the clock on the right minute.

*Practice:* LC 994 Rotting Oranges · LC 542 01 Matrix · LC 286 Walls and Gates · LC 1162 As Far from Land as Possible
