# Jump Game

*LeetCode 55 · Medium · Pattern: Greedy reach (furthest reachable index) · Reading time ~6 min*

## What the problem is really asking

You stand on index 0 of an array. The number on each square is the longest jump you may take from it; you may also take
any shorter jump, including none. Can you get to the last square?

The answer is a yes or no. Behind it is a graph: every index points to the next `nums[i]` indices, and the question is
whether the last index is connected to the first. What makes it look hard is that the number of jump sequences explodes.
What makes it actually easy is a shape the reachable squares are forced to have.

```text
index:   0   1   2   3   4
nums:  [ 3,  2,  1,  0,  4 ]
         \___________/
          every path from 0 lands on 3 eventually,
          and 3 has jump 0: the end (4) is out of reach
          -> False
```

## Do it by hand first

Take `[2, 3, 1, 1, 4]`. A person does not enumerate paths. They point at index 0 and say "from here I can get as far as
index 2". Then they glance at index 1: "and from there as far as 4, which is the end. Done."

Now try `[3, 2, 1, 0, 4]`. From 0, as far as 3. From 1, as far as 3. From 2, as far as 3. From 3, as far as 3. Index 4 is
beyond everything you have seen, and you have no squares left to stand on that could push further.

```text
standing on:   0    1    2    3    4
can reach to:  3    3    3    3    ?
                                   ^ never got here
best so far:   3    3    3    3
```

Your hand tracked one number: how far right you can possibly get, using only the squares you have already confirmed you
can stand on. Every square up to that number is fair game. Nothing beyond it is, yet.

## The first honest attempt

Depth-first search. From index `i`, try every jump length `1..nums[i]`, recurse, and return True if any branch reaches the
end. Without memoisation this is exponential; with a memo of "can index `i` reach the end?" it becomes O(n^2), because
each index still loops over up to `n` jump lengths.

The waste is visible on a tiny input. Many different paths land on the same index, and the search explores what happens
after it each time:

```text
nums = [3, 2, 1, 0, 4]

0 -> 1 -> 2 -> 3   stuck
0 -> 1 -> 3        stuck   } index 3 explored
0 -> 2 -> 3        stuck   } over and over,
0 -> 3             stuck   } same dead end
```

Whether index 3 can reach the end does not depend on how you arrived at index 3. The search keeps asking anyway.

## The turning point

Claim: the set of indices reachable from 0 is always a contiguous prefix `[0, reach]`.

Justify it. Suppose you can reach index `k`. Then some square `i < k` (or `k` itself, when `k = 0`) jumped to `k`, using a
jump of length `k - i` that was at most `nums[i]`. Any shorter jump from `i` is also allowed, so every index between `i`
and `k` is reachable too. Repeat that argument and there can be no hole: if `k` is reachable, so is everything to its
left.

That collapses the state of the whole search to one integer. Walk `i` from left to right. If `i <= reach`, you can stand
on `i`, and standing there lets you reach up to `i + nums[i]`, so `reach = max(reach, i + nums[i])`. If `i > reach`, then
`i` is outside the prefix; and since `reach` is built from every square before `i`, nothing will ever extend it. You are
stuck.

The order of the two checks is the entire bug surface of this problem:

```python
if i > reach:
    return False          # check you are allowed here...
reach = max(reach, i + jump)   # ...then extend
```

Swap the lines and you would happily "jump from" an index you never reached.

## Watch it work

`nums = [3, 2, 1, 0, 4]`. Start with `reach = 0`.

Frame 1

```text
index:   0   1   2   3   4
nums:  [ 3,  2,  1,  0,  4 ]
         ^ i=0          0 <= reach(0): stand here
shade:  [#   #   #   #]  .    reach = max(0, 0+3) = 3
```

The first square's jump shades the prefix up to index 3.

Frame 2

```text
nums:  [ 3,  2,  1,  0,  4 ]
             ^ i=1      1 + 2 = 3, no gain
shade:  [#   #   #   #]  .    reach = 3
```

Index 1 is inside the shade but reaches no further than index 0 did.

Frame 3

```text
nums:  [ 3,  2,  1,  0,  4 ]
                 ^ i=2  2 + 1 = 3, no gain
shade:  [#   #   #   #]  .    reach = 3
```

Same story from index 2.

Frame 4

```text
nums:  [ 3,  2,  1,  0,  4 ]
                     ^ i=3  3 + 0 = 3, no gain
shade:  [#   #   #   #]  .    reach = 3
```

The jump of 0 adds nothing; this is the trap square every path falls into.

Frame 5

```text
nums:  [ 3,  2,  1,  0,  4 ]
                         ^ i=4
shade:  [#   #   #   #]  .    4 > reach(3) -> return False
```

The pointer steps outside the shade: index 4 was never reachable.

For contrast, on `[2, 3, 1, 1, 4]` the reach goes 2, 4, 4, 4, 8: index 1 pushes it to the last index in the second step,
the pointer never leaves the shade, and the answer is True.

Across all frames, the shaded prefix was exactly the set of indices reachable from 0 using squares to the left of the
pointer, and it only ever grew. The algorithm never needed to know which path got there.

## Why it is correct

The invariant: before examining index `i`, `reach` is the largest index reachable from 0 by jumps that start at squares in
`[0, i - 1]`, and every index in `[0, reach]` is reachable.

Initially (`i = 0`, `reach = 0`) only index 0 is reached, and that is true. At step `i`:

- If `i <= reach`, index `i` is reachable by the invariant. From it every index in `[i, i + nums[i]]` is reachable, and
  that interval touches or overlaps the current prefix, so the union is again a prefix, ending at `max(reach, i +
  nums[i])`. The invariant holds for `i + 1`.
- If `i > reach`, then every jump that starts at a reachable square lands at or before `reach < i`. Every reachable square
  is in `[0, reach]`, and we have already accounted for all of their jumps. So no index `>= i` is reachable, including the
  last one. Returning False is correct.

If the loop finishes, every index was inside the prefix when visited, the last one included, so the answer is True.

The greedy flavour: at each square we commit to "the furthest point reachable so far" and never reconsider which path
achieved it. That is safe because the furthest point dominates every nearer one: a prefix ending further right contains
every prefix ending earlier.

## Cost

- **Time O(n):** one scan, a comparison and a `max` per index.
- **Space O(1):** the single integer `reach`.

The memoised DFS or the backward DP ("can index `i` reach a good index?") is O(n^2) time and O(n) space. A known middle
step is a backward greedy: keep `goal = n - 1`, and walking right to left set `goal = i` whenever `i + nums[i] >= goal`;
the answer is `goal == 0`. Also O(n), O(1).

## Variations you will meet

- **Jump Game II (LeetCode 45).** The end is guaranteed reachable; return the minimum number of jumps. The prefix idea
  survives, but now you also need to know when you have used up one jump's worth of squares. That is the next problem.
- **Jump Game III (LeetCode 1306).** From `i` you may jump exactly `i + arr[i]` or `i - arr[i]`. Reachable squares are no
  longer a prefix, so the greedy breaks; use BFS or DFS with a visited set.
- **Jump Game VII (LeetCode 1871).** You may only land on '0' squares, with jump lengths in `[minJump, maxJump]`. The
  reachable set has holes, so use a sliding-window count of reachable squares instead of one integer.
- **Early exit.** Return True as soon as `reach >= n - 1`. It does not change the complexity but avoids scanning a long
  tail.

## What to carry forward

When the reachable set is forced to be a prefix, the whole search collapses to one integer, the frontier, and the only
failure is the pointer stepping past it. The next problem keeps the frontier but counts how many times you had to jump to
push it, which turns the scan into BFS over intervals.
