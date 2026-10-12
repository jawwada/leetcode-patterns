---
rank: 67
slug: jump_game
---

Each `nums[i]` is the longest jump allowed from index `i`, and any shorter jump is allowed too. Starting at index `0`, decide whether the last index can be reached. `[2, 3, 1, 1, 4]` can be crossed, one step to index 1 and then three to the end, while `[3, 2, 1, 0, 4]` cannot, because every path lands on the `0` at index 3.

The brute force explores jump sequences, exponentially many by plain recursion, or `O(n²)` with a reachable flag per index. The insight is that the reachable indices always form one solid block `[0, farthest]`: whoever can stand on `i` can also stand on every index from `i` to `i + nums[i]`, and those stretches overlap into a single interval. So the whole state is one number. Scan left to right while `i` stays inside the block, stretch the block to `i + nums[i]`, and answer yes the moment it covers the last index. If the scan steps past `farthest`, index `i` is unreachable, and so is everything beyond it, since no reachable index jumps that far.

Picture every index casting a shadow forward over the spots it can jump to. The walk begins under the shadow of index 0, and every index under the shadow extends it with its own, so the reachable region grows as one bar. A zero inside the bar is harmless while some earlier shadow passes over it; it becomes a wall only when no shadow reaches beyond it, which is exactly what happens at index 3 below.

```text
nums = [2, 3, 1, 1, 4]          index   0   1   2   3   4
  i = 0 reaches 2, farthest = 2         ●───────┤
  i = 1 reaches 4, farthest = 4             ●───────────┤   4 ≥ 4: true ✓
nums = [3, 2, 1, 0, 4]          index   0   1   2   3   4
  i = 0 reaches 3, farthest = 3         ●───────────┤
  i = 1 reaches 3, farthest = 3             ●───────┤
  i = 2 reaches 3, farthest = 3                 ●───┤
  i = 3 reaches 3, farthest = 3                     ●
  i = 4 > farthest = 3: the loop ends, false ✗
```

```pseudo
FUNCTION CanJump(nums)
    farthest ← 0                           // indices 0..farthest are reachable
    i ← 0
    WHILE i ≤ farthest                     // i is a spot we can really stand on
        farthest ← max(farthest, i + nums[i])
        IF farthest ≥ len(nums) - 1        // the reach covers the last index
            RETURN true
        i ← i + 1
    RETURN false                           // walked past the reach: a wall
```

Each index is visited at most once with constant work, so the scan costs `O(n)` time and `O(1)` space. Reach for the farthest reach whenever moves go forward along a line and every spot up to a move's length is a legal landing: reachability collapses to one number. When jumps are exact, as in Jump Game III (LC 1306) where index `i` leads only to `i + arr[i]` and `i - arr[i]`, the block argument fails and the problem becomes a graph search over indices, the BFS of #39. Counting the fewest jumps is #68, which reads this same scan level by level. The classic mistake is dropping the `i ≤ farthest` guard and scanning every index: on `[3, 2, 1, 0, 4]` the scan then reads index 4, where it can never stand, stretches the reach to `8` and wrongly answers true.

*Practice:* LC 55 Jump Game · LC 45 Jump Game II · LC 1306 Jump Game III
