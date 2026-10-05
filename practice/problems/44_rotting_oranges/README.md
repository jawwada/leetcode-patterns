# Rotting Oranges (LeetCode 994)

**Area:** graphs · **Difficulty:** Medium · **Key operations:** enqueue every rotten source, process one layer per minute, rot fresh neighbours, count fresh left

## Problem

An `m x n` grid holds `0` (empty), `1` (fresh orange) and `2` (rotten orange). Every minute, each rotten orange rots the fresh oranges directly above, below, left and right of it. Return the minimum number of minutes until no fresh orange remains, or `-1` if some fresh orange can never be reached.

## Example

```
grid = [[2,1,1],
        [1,1,0],
        [0,1,1]]      -> 4
```

The rot starts at the top-left corner and needs four minutes to reach the bottom-right orange. With `[[2,1,1],[0,1,1],[1,0,1]]` the orange at `(2,0)` is walled off by empty cells, so the answer is `-1`.

## Brute force

Simulate minute by minute. Each round, scan the entire grid; for every rotten cell, rot its fresh neighbours into a copy of the grid (so the round is simultaneous). Stop when a round changes nothing; return `-1` if a fresh orange is left.

O((mn)²) time: each round costs O(mn) and a snake-shaped path can need O(mn) rounds. O(mn) space for the copy. The wasted work: every round rescans every cell, although only the oranges that rotted in the *previous* round can rot anything new.

## From brute force to optimal

Only the frontier matters: the oranges that turned rotten at minute `t - 1` are the only ones that spread rot at minute `t`. Keep exactly that frontier in a queue. All initially rotten oranges go in first (they are the sources at minute 0); processing the whole queue once is one minute and produces the next frontier. This is a breadth-first search with many sources, where BFS depth equals the minute.

Counting the fresh oranges up front gives the stop condition for free: stop when `fresh` reaches 0 (the answer is the number of layers processed) or when the queue runs dry with `fresh > 0` (return `-1`). Each cell is enqueued at most once, so the whole thing is O(mn).

## Intuition

Picture dropping several stones into a pond at the same instant. Each stone starts a ring that grows by one cell per minute; where two rings meet they simply merge. The queue holds the current ring. The answer is the number of rings needed to touch the last fresh orange; an orange on an island of empty cells is never touched and forces `-1`. The loop guard `while queue and fresh` is the last ring not being counted: once the last fresh orange rots, the clock stops, even though the ring that rotted it is still in the queue.

## Walkthrough

`X` rotten, `o` fresh, `.` empty. The queue is the frontier that will spread in the next minute.

```
minute 0   fresh 6   queue [(0,0)]
    X o o
    o o .
    . o o
process (0,0): rots (1,0), rots (0,1)                 fresh 4
minute 1   queue [(1,0), (0,1)]
    X X o
    X o .
    . o o
process (1,0): rots (1,1)   process (0,1): rots (0,2)  fresh 2
minute 2   queue [(1,1), (0,2)]
    X X X
    X X .
    . o o
process (1,1): rots (2,1)   process (0,2): nothing     fresh 1
minute 3   queue [(2,1)]
    X X X
    X X .
    . X o
process (2,1): rots (2,2)                              fresh 0
minute 4   queue [(2,2)]
    X X X
    X X .
    . X X
fresh == 0 -> stop; (2,2) is still queued but never processed. Return 4.
```

## Steps

1. Copy the grid (do not mutate the caller's input). Scan it once: enqueue every rotten cell, count the fresh ones.
2. `minutes = 0`. While the queue is non-empty **and** `fresh > 0`:
3. Pop exactly `len(queue)` cells (the current layer). For each 4-neighbour that is in bounds and fresh: mark it rotten, `fresh -= 1`, enqueue it.
4. After the layer, `minutes += 1`.
5. Return `minutes` if `fresh == 0`, else `-1`.

## Complexity

O(mn) time: every cell is enqueued and popped at most once and each pop looks at four neighbours. O(mn) space for the queue (and the grid copy).

## Pitfalls

- **`while queue:` instead of `while queue and fresh:`.** The oranges rotted in the last minute still sit in the queue, so one more empty layer runs and `minutes` is one too big: `[[2, 1]]` gives 2 instead of 1.
- **Bound check `0 < nr`.** Row 0 is a valid row. With a strict bound the rot can never travel upward into the top row, so `[[1], [2]]` gives `-1` instead of 1.
- **Forgetting the `-1` case.** Returning `minutes` unconditionally reports the elapsed time even when a fresh orange was never reached.
- **No fresh oranges at all.** The answer is 0, not `-1`; the loop guard handles it because `fresh` starts at 0.
- **Rotting two steps in one minute.** Marking a cell rotten and processing it in the *same* layer would let rot jump two cells per minute. Taking `len(queue)` at the start of the layer keeps the layers separate.
- **Mutating the input grid.** Harmless on LeetCode, but it breaks any caller that reuses the grid (and the randomized cross-check here).
