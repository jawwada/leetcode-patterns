# Jump Game II

*LeetCode 45 · Medium · Pattern: Greedy reach (furthest reachable index) · Reading time ~7 min*

## What the problem is really asking

Same board as Jump Game: `nums[i]` is the longest jump allowed from index `i`. This time the last index is guaranteed to be
reachable, and you must report the fewest jumps that get you there.

The answer is a count. It is a shortest-path question on a graph where index `i` has edges to `i+1 .. i+nums[i]`, all of
weight one, so BFS would solve it. What makes it interesting is that BFS is wasteful here: the graph has up to `n^2` edges,
yet the answer can be read off in one pass with three integers.

```text
index:   0   1   2   3   4
nums:  [ 2,  3,  1,  1,  4 ]
         |___^           |
          jump 1    jump 2: 1 -> 4
         0 -> 1 -> 4     answer 2
```

## Do it by hand first

On `[2, 3, 1, 1, 4]`, think in rounds. With zero jumps you are on index 0. With one jump, index 0 can take you to 1 or 2.
With two jumps: from 1 you can reach up to 4, from 2 up to 3, so everything up to index 4 is covered, the end included.
Two jumps.

```text
jumps used:   0        1          2
reachable:   [0]     [1 2]     [3 4]
             nums[0]=2 -> up to 2
                     from 1: up to 4
                     from 2: up to 3   -> next round ends at 4
```

Notice what your hand wrote down for each round: not a list of individual squares, but a block of consecutive squares, and
for the next round only the furthest right end any square in the current block could reach. The rounds are intervals that
sit end to end.

## The first honest attempt

Run BFS from index 0. Pop an index, push every landing spot `i+1 .. i+nums[i]` that has not been visited, record its
distance, and stop when the last index pops. With a visited array each index is enqueued once, but each pop still loops
over up to `nums[i]` targets, so the work is O(n^2) in the worst case (O(n + total jump lengths) in general).

The waste is in the inner loop. Each popped index re-scans landing spots that a previous index in the same round already
covered:

```text
round 1 = {1, 2}
pop 1: scan 2, 3, 4      -> enqueue 3, 4
pop 2: scan 3            -> already seen
            ^ re-scanned: index 2's whole range lies inside
              index 1's range, yet BFS walks it again
```

BFS treats each square as its own node. But every square in a round is equivalent for counting purposes: they all cost
the same number of jumps. The only thing about the round that matters to the future is how far right it lets you go next.

## The turning point

Claim: the indices reachable with exactly `j` jumps (and not fewer) form a contiguous interval, and the next interval is
`[end_j + 1, max(i + nums[i] for i in round j)]`.

Justify it. Round 0 is `[0, 0]`. If everything reachable in at most `j` jumps is the prefix `[0, end_j]` (the Jump Game
argument: reachable sets are prefixes), then everything reachable in at most `j + 1` jumps is the prefix up to the
furthest landing from any square in `[0, end_j]`. The squares newly added form the gap between the two prefix ends, an
interval.

That turns BFS into a single scan with three integers:

- `cur_end`: right edge of the round you are currently walking through.
- `farthest`: the furthest landing seen from any square scanned so far.
- `jumps`: how many rounds have been opened.

Walk `i` left to right, updating `farthest`. When `i` reaches `cur_end`, you have scanned the whole current round, so the
next round is everything up to `farthest`: count one more jump and set `cur_end = farthest`.

One boundary detail matters. Scan only `i` in `range(n - 1)`. If the last index were scanned and happened to equal
`cur_end`, you would open a round to leave a square you never need to leave, counting one jump too many.

The greedy reading: when you are forced to jump, you do not decide which square you jumped from. You just credit yourself
with the best one in the round. That is the "take the jump that reaches furthest" rule, applied lazily.

## Watch it work

`nums = [2, 3, 1, 1, 4]`. Start with `jumps = cur_end = farthest = 0`. The loop scans `i = 0..3`.

Frame 1

```text
index:   0   1   2   3   4
nums:  [ 2,  3,  1,  1,  4 ]
         ^ i=0 = cur_end    farthest = max(0, 0+2) = 2
round:  [0]                 end of round 0 -> jumps = 1
                            cur_end = 2
```

Round 0 is just index 0; leaving it costs the first jump and opens round 1 = `[1, 2]`.

Frame 2

```text
nums:  [ 2,  3,  1,  1,  4 ]
             ^ i=1          farthest = max(2, 1+3) = 4
round:      [1   2]         i < cur_end(2): keep scanning
jumps = 1
```

Index 1 reaches the last index, but we have not finished scanning round 1 yet.

Frame 3

```text
nums:  [ 2,  3,  1,  1,  4 ]
                 ^ i=2 = cur_end   farthest = max(4, 3) = 4
round:      [1   2]         end of round 1 -> jumps = 2
                            cur_end = 4
```

Round 1 is fully scanned; the next round is `[3, 4]`, and it contains the target.

Frame 4

```text
nums:  [ 2,  3,  1,  1,  4 ]
                     ^ i=3  farthest = max(4, 4) = 4
round:              [3   4] i < cur_end(4): nothing to do
jumps = 2   loop ends (i=4 not scanned) -> return 2
```

Index 4 is never scanned, so no spurious third jump is counted.

Across the frames, `[previous cur_end + 1, cur_end]` was always exactly the set of squares reachable in `jumps` jumps but
not fewer, and `farthest` was the right edge of the next round under construction.

## Why it is correct

Invariant: when the scan pointer sits at `i` inside round `j` (that is, `i` lies in `(end_{j-1}, cur_end]`), `jumps = j`,
every index in `[0, cur_end]` is reachable in at most `j` jumps, no index beyond `cur_end` is, and `farthest` is the
furthest landing from any index in `[0, i]`.

It holds initially: round 0 is `[0, 0]` with zero jumps. When `i == cur_end`, `farthest` covers every square in `[0,
cur_end]`, which is everything reachable in at most `j` jumps, so the prefix reachable in at most `j + 1` jumps is exactly
`[0, farthest]`. Setting `jumps = j + 1` and `cur_end = farthest` restores the invariant for the next round. Because the
end is guaranteed reachable, `farthest > cur_end` at every round boundary before the end is covered, so the scan never
stalls.

Why is the count minimal? Because each round is the full set of squares reachable in that many jumps. The last index sits
in round `j` for the first `j` such that `cur_end >= n - 1`, which by definition means it cannot be reached in `j - 1`.

The same fact as a "greedy stays ahead" argument on actual paths: let `p_k` be where any path stands after `k` jumps, and
`end_k` the greedy round edge after `k` jumps. Then `p_k <= end_k` for all `k`. It is true at `k = 0` (both are 0). If `p_k
<= end_k`, the next landing `p_{k+1} <= p_k + nums[p_k]`, and `p_k` lies inside `[0, end_k]`, a square that `farthest`
already took into account, so `p_{k+1} <= end_{k+1}`. No path can therefore reach the last index in fewer rounds than
greedy does.

## Cost

- **Time O(n):** a single scan, constant work per index.
- **Space O(1):** three integers.

BFS with a visited array is O(n^2) time in the worst case and O(n) space; the naive recursion "min over all jumps from
`i`" is exponential.

## Variations you will meet

- **Reachability unknown.** If the end might be unreachable, check at each round boundary whether `farthest <= i`; if so,
  no square in the round pushes further, return -1. The next problem needs exactly this check.
- **Return the path.** At each round boundary remember which index produced `farthest`; those indices are the jump points.
- **Video stitching (LeetCode 1024) and minimum taps (LeetCode 1326).** The input is a set of intervals rather than jump
  lengths. Bucket each interval by its left end to turn it into "from here you can reach there", then run this scan.
- **Weighted jumps or costs per square.** Once jumps have different costs, rounds no longer measure cost, and you need
  Dijkstra or a DP with a monotonic deque.

## What to carry forward

Minimum jumps is BFS whose layers are intervals, so you only need each layer's right edge and the furthest reach seen
while walking it. The next problem disguises the same scan: the garden's taps are intervals, and turning them into jump
lengths makes it this problem plus a failure case.
