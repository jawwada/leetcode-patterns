# Car Fleet

*LeetCode 853 · Medium · Pattern: Monotonic stack · Reading time ~8 min*

## What the problem is really asking

Cars sit on a one-lane road, all driving toward the same `target`. Car `i` starts at `position[i]` with constant `speed[i]`. Nobody can pass. If a faster car catches a slower one before (or exactly at) the target, it slows down and the two travel bumper to bumper from then on; they are one *fleet*. Count how many fleets arrive.

The answer is a count. What makes it look hard is that catching up is transitive and cascading: car A catches car B, then the merged fleet runs at B's speed and might never catch C, or might. Simulating the road in time sounds like event processing with collisions. The trick is that you never have to simulate anything.

```text
target = 12
road:   |-----|---|-----|---|---|
pos:    0     3   5     8   10  12
car:    E     D   C     B   A   T
speed:  1     3   1     4   2
time:   12    3   7     1   1      (target - pos) / speed
```

`time` is each car's solo arrival time, the moment it would reach the target if the road were empty. The correct answer here is 3 fleets: {A, B}, {C, D}, {E}.

## Do it by hand first

Stand at the target and look back down the road. Take the cars in order from closest to the target to farthest.

```text
A  pos 10  time 1   first car: leads fleet #1 (arrives t=1)
B  pos 8   time 1   would arrive at t=1, not later than
                    the fleet ahead -> catches it. joins #1
C  pos 5   time 7   later than t=1 -> never catches #1
                    leads fleet #2 (arrives t=7)
D  pos 3   time 3   earlier than t=7 -> catches #2, joins
E  pos 0   time 12  later than t=7 -> leads fleet #3
```

Each car only had to be compared with one number: the arrival time of the fleet immediately in front of it. If it would arrive later than that fleet, nobody ahead can slow it, so it starts its own. If it would arrive at the same time or earlier, it must hit that fleet's tail first and inherit its arrival time. Your hand kept a list of fleet arrival times, and only ever looked at the last one. That list is a stack, and it only grows upward with larger times.

## The first honest attempt

Without the sorting insight, the natural statement is: car `i` leads its own fleet if and only if no car ahead of it (larger position) has a solo arrival time at least as large as `t_i`. Any such car `j` is slower to the finish, so `i` catches either `j` or something `j` is stuck behind.

Checking that for every car against every car ahead is O(n^2) time, O(1) space.

```text
car (pos)  compares against all cars ahead
E (0)      D C B A        <- C's time 7 rediscovered
D (3)        C B A        <- C's time 7 rediscovered
C (5)          B A
B (8)            A
            ~~~~~~~
"slowest finish time among cars ahead" is
recomputed from scratch for every car
```

The waste: the question for every car is "what is the latest arrival time among cars ahead of me?", and that quantity is rebuilt from nothing each time when it could be carried along as we move back down the road.

## The turning point

**Claim: after sorting cars by position from the target backwards, a car forms a new fleet exactly when its solo time is strictly greater than the arrival time of the fleet directly ahead; otherwise it merges and changes nothing.**

Justification. The fleet directly ahead arrives at time `T`, which is the latest of all arrival times among cars ahead (fleets further ahead arrive earlier, otherwise they would have been caught by this one). If `t_i > T`, our car is the slowest thing on the road from here on; nothing ahead holds it back, so it arrives alone at `t_i`. If `t_i <= T`, the car would reach the target no later than the fleet ahead, but it cannot pass, so it meets that fleet's tail at or before the target and finishes at `T`. Merging never changes `T`.

So keep a stack of fleet arrival times. Process cars closest-first. Compare each car's time with the top: if larger, push it; otherwise do nothing. The stack is strictly increasing from bottom to top, a rising staircase, and the answer is its height.

Sorting is the only expensive step; the sweep is O(n).

There is a second way to write the same sweep that shows the monotonic-stack pop explicitly. Process cars from the back of the road forward (smallest position first). Each new car is *ahead* of everything on the stack. Every stacked car whose time is `<=` the new car's time will catch it, so pop them; their fate (absorbed) is fixed right there. The stack then holds a descending staircase of times, and its final height is the same count. We trace the push-only version, the one in the solution, but both are the same idea seen from opposite ends of the road.

## Watch it work

Cars sorted by position descending: A(10, t=1), B(8, t=1), C(5, t=7), D(3, t=3), E(0, t=12). The staircase lists fleet arrival times bottom-first, one `#` per unit of time.

Frame 1 — car A, the stack is empty.

```text
sorted: A  B  C  D  E
time:   1  1  7  3  12
        ^
staircase:
  #1 t=1  |#             <- top
```

A leads the first fleet.

Frame 2 — car B, time 1, not greater than the top (1).

```text
sorted: A  B  C  D  E
time:   1  1  7  3  12
           ^
1 > 1 ? no -> B merges into fleet #1
staircase:
  #1 t=1  |#             <- top (unchanged)
```

B reaches A exactly at the target; that still counts as one fleet, which is why the test is strict `>`.

Frame 3 — car C, time 7 > 1.

```text
sorted: A  B  C  D  E
time:   1  1  7  3  12
              ^
staircase:
  #1 t=1  |#
  #2 t=7  |#######       <- top
```

Frame 4 — car D, time 3, not greater than 7.

```text
sorted: A  B  C  D  E
time:   1  1  7  3  12
                 ^
3 > 7 ? no -> D catches C, finishes at t=7
staircase:
  #1 t=1  |#
  #2 t=7  |#######       <- top (unchanged)
```

Frame 5 — car E, time 12 > 7.

```text
sorted: A  B  C  D  E
time:   1  1  7  3  12
                    ^
staircase:
  #1 t=1  |#
  #2 t=7  |#######
  #3 t=12 |############  <- top
fleets = len(stack) = 3
```

The staircase rose at every push and was never disturbed by a merge. The top was always the arrival time of the fleet immediately ahead of the car being considered, and each car's fate was settled the moment it met that top.

## Why it is correct

**Invariant.** After processing the `k` cars closest to the target, the stack holds, bottom to top, the arrival times of exactly the fleets those `k` cars form, in order of position, strictly increasing.

Initially there are no cars and no fleets. Suppose it holds for `k` cars and the next car `c` (the next one back) has solo time `t`. Cars further back cannot affect cars ahead, since nobody passes; so the fleets among the first `k` cars are final. Only `c`'s own fate is open, and it is decided by the fleet directly ahead, the top of the stack, with arrival time `T`.

- If `t > T`, `c` cannot catch that fleet, and since every fleet further ahead arrives even earlier, it catches none of them. It forms a new fleet arriving at `t > T`, and pushing `t` keeps the stack strictly increasing.
- If `t <= T`, `c` reaches the tail of the fleet ahead no later than the target and is absorbed; the fleet still arrives at `T`. The stack is unchanged and still correct.

**Fate fixed at decision time.** This is the "answer fixed at pop time" property of the chapter in its push-only form: once a car is compared with the top, its classification (leader or absorbed) never changes, because only cars further back are processed later and they cannot influence anyone ahead. In the pop version, a popped car's answer, "absorbed by a fleet ahead", is likewise final the instant it is popped.

After all cars, the stack height is the number of fleets.

## Cost

Time O(n log n): the sort dominates; the stack sweep is O(n) because each car is examined once.

Space O(n): for the sorted pairs and, in the worst case (every car its own fleet), the stack.

The brute force is O(n^2) time, O(1) space.

## Variations you will meet

- **Without a stack.** Since we only ever read the top, keep one variable `last_time` and a counter. Same algorithm, O(1) extra space beyond the sort.
- **Car Fleet II** (LeetCode 1776). Report *when* each car collides with the car ahead. Now merges change speeds over time, and the stack (processed from the front) must pop cars that are already absorbed before you collide with them. That is the pop version for real.
- **Integer time comparison.** To avoid floats, compare `(target - p1) * s2` against `(target - p2) * s1`.
- **Bucket sort on positions.** Positions are distinct integers below `target`, so an array of size `target` replaces the sort and gives O(n + target).

## What to carry forward

Sort so that "the thing that can affect me" is always what you just processed, and the stack top is the only number you need. A car's fate is sealed when it meets the top.

The next problem goes back to brackets, but stacks *indices* with a barrier at the bottom, so a pop can measure how long a valid run is.
