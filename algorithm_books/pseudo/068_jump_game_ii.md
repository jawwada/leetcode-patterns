---
rank: 68
slug: jump_game_ii
---

`nums[i]` is again the longest jump allowed from index `i`, and this time the last index is known to be reachable. Return the fewest jumps from index 0 to the last index. For `[2, 3, 1, 1, 4]` the answer is `2`: one step to index 1, then three steps to the end.

Fewest moves in an unweighted graph is BFS (#39), and the brute force runs it literally, enqueuing every index each jump can land on, `O(n²)` edges in the worst case. The insight is that every BFS level here is a contiguous interval. Level 0 is `[0, 0]`, and if level `k` ends at `b`, level `k + 1` is `[b + 1, farthest]`, where `farthest` is the largest `i + nums[i]` seen so far, because every spot up to a reach is a legal landing. So the queue collapses to two numbers: `current_end`, the right edge of the level being scanned, and `farthest`, the right edge of the next one. Walk `i` forward, pushing `farthest` out; when `i` reaches `current_end`, the level is used up, so count one more jump and move `current_end` to `farthest`.

Picture the indices tiled into consecutive bands, each band one jump farther from the start than the band before it. The scan reads each band once, measuring how far its best launcher reaches, and that reach is where the next band ends. The answer is the level number of the band that holds the last index. The loop stops just before the last index, because standing there needs no further jump.

```text
index        0    1    2    3    4
nums         2    3    1    1    4
level 0      ●                              [0, 0]  the start
level 1           ●────●                    [1, 2]  up to 0 + 2 = 2
level 2                     ●────●          [3, 4]  up to max(1 + 3, 2 + 1) = 4

  i   i + nums[i]   farthest   i = current_end?   jumps   current_end
  0        2            2         yes, jump         1          2
  1        4            4         no                1          2
  2        3            4         yes, jump         2          4
  3        4            4         no                2          4
  the loop stops before index 4: 2 jumps
```

```pseudo
FUNCTION MinJumps(nums)
    jumps ← 0
    current_end ← 0                        // right edge of the current level
    farthest ← 0                           // right edge of the next level
    FOR i FROM 0 TO len(nums) - 2          // never jump from the last index
        farthest ← max(farthest, i + nums[i])
        IF i = current_end                 // this level is used up
            jumps ← jumps + 1
            current_end ← farthest         // the next level ends here
    RETURN jumps
```

Every index is read once, so the cost is `O(n)` time and `O(1)` space, against `O(n²)` for the explicit BFS. Reach for this level-by-interval BFS whenever the positions reachable in `k` steps always form a contiguous range: covering a line with jumps, with video clips (LC 1024) or with garden taps (LC 1326), once each clip or tap is recorded as a reach from its left end. When the end might be unreachable, check at the end of each level whether `farthest` is still `i`; if so, nothing beyond can be reached, so return `-1`. The classic mistake is letting the loop run over the last index too: when the last index closes a level, the scan counts a jump it never takes, and `[2, 3, 1, 1, 4]` reports `3`.

*Practice:* LC 45 Jump Game II · LC 1024 Video Stitching · LC 1326 Minimum Number of Taps to Open to Water a Garden
