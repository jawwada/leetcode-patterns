# Gas Station

*LeetCode 134 · Medium · Pattern: Greedy running sum with restart · Reading time ~7 min*

## What the problem is really asking

Stations sit on a circular road. At station `i` you can fill up `gas[i]` units, and driving from station `i` to station
`i + 1` burns `cost[i]` units. Your tank starts empty and has no limit. Find the station where you can start and drive
all the way around back to it without the tank ever going negative. The problem promises that if such a station exists,
it is unique; otherwise return -1.

Each station really contributes one number: its net effect `diff[i] = gas[i] - cost[i]`. The answer is an index, a
rotation of that circular list of diffs such that every running total along the way stays at or above zero. What makes it
hard is that there are `n` rotations and checking each one takes `n` steps.

```text
station:   0    1    2    3    4
gas:       1    2    3    4    5
cost:      3    4    5    1    2
diff:     -2   -2   -2   +3   +3

start at 3:  +3  +6  +4  +2  0     never negative -> 3
             (3) (4) (0) (1) (2)   stations visited in order
```

## Do it by hand first

Try station 0. You fill 1 and need 3 to reach station 1: the tank would be -2. Stuck immediately. Try 1: -2, stuck. Try
2: -2, stuck. Try 3: +3 at station 4, then +6, back around to station 0 with 6, leave with 4, station 1 leaves with 2,
station 2 leaves with 0. You made it. Answer 3.

But a sharper person notices something on the way. Suppose you start at station 0 on a different input and make it past
stations 0 and 1 with fuel to spare, then run dry leaving station 2. Is it worth trying station 1 next? You arrived at
station 1 with a non-negative tank. Starting at station 1 means arriving there with exactly 0, which is no better. So
station 1 is at least as doomed as 0 was. The same goes for station 2.

```text
start s ............ fail at f
  |  tank >= 0  |  tank >= 0  |  tank < 0
  s            s+1           ...          f
                ^ starting here = arriving with 0
                  instead of >= 0: no better
  -> every start in [s, f] is doomed; next try f+1
```

The thing your hand tracked was a running tank, plus the station where the current attempt began.

## The first honest attempt

For every start `s`, simulate the loop: add `diff[(s + k) % n]` for `k = 0..n-1`, and abandon `s` the moment the tank
goes negative. The first `s` that survives is the answer. O(n^2) time, O(1) space.

The repeated work is in what happens after a failure. When the attempt from `s` dies at `f`, the brute force moves to
`s + 1` and drives the same road again, recomputing the same diffs it just added:

```text
diff:   -2  +1  +1  -5  +4  ...
from 0: [-2] dead at 0
from 1:     [+1  +2  -3] dead at 3
from 2:         [+1  -4] dead at 3   } re-drives 2..3,
from 3:             [-5] dead at 3   } guaranteed to die
from 4:                 [+4 ...]
```

Starts 2 and 3 were already ruled out by the attempt from 1; the brute force cannot see that.

## The turning point

Claim: if, starting from `s` with an empty tank, the tank first goes negative after leaving station `f`, then no station
in `[s, f]` can be the answer, so the next candidate is `f + 1`.

Justify it. Take any `t` with `s < t <= f`. Driving from `s`, you arrived at `t` with tank `T >= 0` (the tank did not go
negative before `f`). From `t` to `f` the same diffs are added whichever start you used. Starting fresh at `t` gives
`0 + (diffs t..f)`, and starting from `s` gave `T + (diffs t..f)`, which was negative. Since `0 <= T`, the fresh start
is also negative by `f`. So `t` fails too. Station `s` itself failed by definition.

That makes one pass enough: carry `tank`, and whenever it goes negative at `i`, set `start = i + 1` and `tank = 0`. Each
station is added exactly once.

The second half of the claim answers "but what if the surviving candidate cannot wrap around?". Keep a separate `total`
of all diffs. If `total < 0`, no start works: fuel in is less than fuel out, whatever the order. If `total >= 0`, the
final candidate works, and the easiest way to see why is a picture.

Plot the running sum of diffs starting from station 0. The right start is the station just after the lowest point of the
curve. Starting there, you begin at the bottom, so every later point is above you; and since `total >= 0`, wrapping
around to the beginning lands no lower than where you began.

```text
prefix sum of diff, starting from station 0:
station:      0    1    2    3    4
prefix:      -2   -4   -6   -3    0
   0  |                           *
  -2  |       *
  -3  |                      *
  -4  |            *
  -6  |                 *   <- lowest point, after station 2
start = 3: every point after the minimum is higher
```

The restart rule finds exactly that minimum: the tank resets every time the running sum hits a new low, and the last
reset is just after the global low.

## Watch it work

`gas = [1, 2, 3, 4, 5]`, `cost = [3, 4, 5, 1, 2]`, so `diff = [-2, -2, -2, 3, 3]`. Start with `total = tank = start = 0`.

Frame 1

```text
station:   0    1    2    3    4
diff:     -2   -2   -2   +3   +3
           ^ i=0     tank 0 + -2 = -2 < 0
start: 0 -> 1        tank reset to 0      total = -2
```

Station 0 cannot start the trip; the candidate moves past it.

Frame 2

```text
diff:     -2   -2   -2   +3   +3
                ^ i=1  tank 0 + -2 = -2 < 0
start: 1 -> 2          tank reset to 0    total = -4
```

Station 1 fails on its own first leg.

Frame 3

```text
diff:     -2   -2   -2   +3   +3
                     ^ i=2  tank -2 < 0
start: 2 -> 3               tank reset    total = -6
```

Third failure; `total` is at its lowest, and the candidate becomes 3.

Frame 4

```text
diff:     -2   -2   -2   +3   +3
                          ^ i=3  tank 0 + 3 = 3
start = 3                        total = -3
```

From the candidate the tank climbs; no reset.

Frame 5

```text
diff:     -2   -2   -2   +3   +3
                               ^ i=4  tank 3 + 3 = 6
start = 3   total = 0 >= 0  -> return 3
```

The scan ends; the overall balance is non-negative, so the last candidate is the answer.

At every frame, `tank` was the fuel you would hold after station `i` if you had started at `start`, it was non-negative
whenever no reset happened, and every station before `start` had been proved unable to start the trip.

## Why it is correct

Two facts, each proved above, combine into the argument.

**Invariant of the scan.** After processing station `i`, no station in `[0, start - 1]` can be a valid start, and
driving from `start` to `i` never makes the tank negative (`tank >= 0`). The block-skipping lemma keeps the first part
true whenever a reset happens; the reset itself makes the second part true with an empty block.

**The final candidate works when `total >= 0`.** Let `m = start - 1`, the last station where a reset happened; the
prefix sum `P(m)` of diffs from station 0 is then the minimum of all prefix sums. (Each reset happened when the running
sum fell below the level of the previous reset, so the last reset is the lowest point.) Driving from `start`, after
reaching station `k` your tank is `P(k) - P(m)` for `k >= start`, which is `>= 0` because `P(m)` is the minimum; after
wrapping to station `k < start` your tank is `total - P(m) + P(k)`, which is `>= 0` because `total >= 0` and `P(k) >= P(m)`.
So the tank never goes negative anywhere on the loop.

**When `total < 0`.** Over a full loop you gain `total` fuel. A valid start would end the loop with a non-negative tank,
equal to `total`. Contradiction, so return -1.

## Cost

- **Time O(n):** one pass; each station's diff is added to `tank` and `total` once.
- **Space O(1):** three integers.

The brute force, simulating from every start, is O(n^2) time and O(1) space.

## Variations you will meet

- **No uniqueness guarantee.** The scan still returns a valid start when one exists (the station after the global
  minimum of the prefix curve); if several minima tie, any station just after one of them works.
- **Return all valid starts.** Every station right after a position where the prefix sum equals its global minimum is
  valid (when `total >= 0`). Compute prefix sums and collect them.
- **Maximum circular subarray sum (LeetCode 918).** The same "circle = total minus a middle piece" trick: the best wrapping
  segment is the total minus the worst non-wrapping one.
- **Bounded tank capacity.** If the tank holds at most `C`, extra gas is lost, the diffs are no longer additive, and the
  block-skipping lemma fails; you need a simulation with a deque or a different argument.

## What to carry forward

A running sum that goes negative condemns its whole block of starts at once, so restart just past the failure; the last
restart sits right after the lowest point of the prefix curve, and the total tells you whether it can close the loop. The
next problem keeps the left-to-right sweep with a carried value, but the value is a "must reach at least here" boundary,
and every letter pushes it right.
