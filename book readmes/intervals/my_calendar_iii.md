# My Calendar III
*LeetCode 732 · Hard · Pattern: Difference array / prefix-sum sweep · Reading time ~9 min*

## The problem

Implement MyCalendarThree. book(startTime, endTime) adds the half-open event [start, end) and returns the largest k
such that some instant is covered by k events after this booking. Events are never rejected.

```text
Example: book(10,20) -> 1; book(50,60) -> 1; book(10,40) -> 2;
  book(5,15) -> 3; book(5,10) -> 3; book(25,55) -> 3.
```

## What the problem is really asking

You are building a calendar object. Each call `book(start, end)` adds a half-open event `[start, end)`. Nothing is ever rejected. After each booking, return the largest k such that some instant is covered by k events, which is the peak overlap of everything booked so far.

Geometrically, this is Meeting Rooms II asked again after every insertion: stack all the bars and report the height of the tallest point. The answer per call is one integer, and it can only stay the same or grow.

Two things make it Hard. The input is **online**: you must answer after each booking without knowing the future ones. And the coordinates go up to 10^9, so you cannot keep an array indexed by time.

Running example: book `(10,20) (50,60) (10,40) (5,15) (5,10) (25,55)`, with answers `1 1 2 3 3 3`.

```text
 all six bookings as bars (each column = 5 time units)

 [10,20)        ######
 [50,60)                              ######
 [10,40)        ##################
 [5,15)      ######
 [5,10)      ###
 [25,55)                 ##################
         +--+--+--+--+--+--+--+--+--+--+--+--+
         0  5  10 15 20 25 30 35 40 45 50 55 60

 coverage skyline (height = events covering that time)

3 |       ###
2 |    #########   #########      ###
1 |    #################################
  +-------------------------------------
   0     10    20    30    40    50    60
 peak 3, during [10,15)
```

## Do it by hand first

Forget code and look at the skyline. How would you draw it by hand from the bookings? You would not count bars at every instant. You would walk left to right and adjust a pen's height at each bar end: **up one where a bar starts, down one where a bar ends**. Between those points the height cannot change.

```text
 time:     5   10   15   20   25   40   50   55   60
 change:  +2   +1   -1   -1   +1   -1   +1   -1   -1
 height:   2    3    2    1    2    1    2    1    0
                ^ peak 3
```

Look at time 10: three things happen there. `[10,20)` and `[10,40)` start, and `[5,10)` ends. The net change is +1. You did not care which bars caused it. You only needed **the net change at each boundary**, plus the boundaries in sorted order. That pair, "boundary to net change" and "boundaries sorted", is the whole data structure. It is a difference array, sparse because only boundaries that actually occur get an entry.

## The first honest attempt

"Store every booking. The peak is reached at some booking's start, because coverage only rises at starts. So after each book, for every start s, count events with `start <= s < end`, and take the max."

That costs O(n^2) per call with n bookings so far, so O(n^3) over n calls. At n = 400 (the LeetCode limit) that is 6.4 * 10^7 basic steps, which is slow but plausible. At larger n it collapses.

Where is the repeated work? For each candidate point, it re-asks every booking "do you cover me?", even though neighbouring points differ by only the bars that start or end between them:

```text
 point 10: test 6 bars -> 3
 point 15: test 6 bars -> 2   (only [5,15) changed!)
 point 20: test 6 bars -> 1   (only [10,20) changed!)
 each point rescans everything; one counter walking
 the sorted points would do it in a single pass
```

And between calls, everything is recomputed from scratch, although only one bar was added.

## The turning point

**Claim: the coverage at time t equals (number of starts <= t) minus (number of ends <= t). So if you store +1 at each start and -1 at each end, a left-to-right prefix sum over the sorted boundaries reconstructs the whole skyline, and its maximum is the answer.**

Why it holds: an event `[s, e)` covers t exactly when `s <= t` and not `e <= t`. Counting over all events, the events with `s <= t` either have `e <= t` (already ended) or not (still running). So running = started - ended. A prefix sum over `delta` computes exactly started - ended at every boundary, because each start contributed +1 and each end -1.

Why half-open intervals come out right for free: at a coordinate where one event ends and another starts, their +1 and -1 land in **the same** `delta` slot and cancel before the prefix sum reads them. The sum never shows the phantom overlap. In the example, `[5,10)` ending at 10 and two events starting at 10 net to +1, not "+2 then -1".

```text
 dense difference array (if time were small):
 index:  ... 5  6..9  10  ...  15 ...
 delta:     +2   0    +1       -1
 prefix:     2   2     3        2     <- coverage

 sparse version (what we store):
 delta  = {5:+2, 10:+1, 15:-1, 20:-1, 25:+1, ...}
 points = [5, 10, 15, 20, 25, ...]     kept sorted
```

The dense array would need 10^9 slots. The sparse version is a hand-rolled coordinate compression: only coordinates that appear as a boundary get a slot, and between two consecutive boundaries the coverage is constant, so nothing is lost.

Turning that into `book`:

1. Add +1 at `start` and -1 at `end` in the dict. If a coordinate is new, insert it into the sorted `points` list with `bisect.insort`. The binary search is O(log n) and the list shift is O(n).
2. Sweep `points` in order, adding `delta[p]` to a running `active`, and keep the max.
3. Return the max.

Each call is O(n), so the total is O(n^2), down from O(n^3).

Why not "just update the max incrementally"? Because adding a bar raises coverage on a whole range, and the new peak could be anywhere inside it. Getting that in O(log n) needs a segment tree that supports "add 1 on a range" and "global max" with lazy propagation, over compressed or dynamically created nodes. That is the follow-up. The sweep is the version to produce first, and it passes comfortably.

## Watch it work

Each frame shows `delta` in sorted-point order and the prefix sum under it. The answer is the max of the prefix row.

**Frame 1.** `book(10,20)`: two new points.

```text
 point:    10   20
 delta:    +1   -1
 prefix:    1    0            -> return 1
```

One bar, so the peak is 1.

**Frame 2.** `book(50,60)`: two more points. The bars are disjoint.

```text
 point:    10   20   50   60
 delta:    +1   -1   +1   -1
 prefix:    1    0    1    0  -> return 1
```

The prefix returns to 0 between the bars, so the peak is still 1.

**Frame 3.** `book(10,40)`: 10 already exists, so `delta[10]` becomes +2. The point 40 is inserted.

```text
 point:    10   20   40   50   60
 delta:    +2   -1   -1   +1   -1
 prefix:    2    1    0    1    0 -> return 2
```

Two starts share one slot. The prefix sees both at once.

**Frame 4.** `book(5,15)`: points 5 and 15 are inserted.

```text
 point:     5   10   15   20   40   50   60
 delta:    +1   +2   -1   -1   -1   +1   -1
 prefix:    1    3    2    1    0    1    0 -> return 3
                 ^ peak
```

Coverage hits 3 in `[10,15)`.

**Frame 5.** `book(5,10)`: `delta[5]` becomes +2, and `delta[10]` becomes +2 - 1 = +1.

```text
 point:     5   10   15   20   40   50   60
 delta:    +2   +1   -1   -1   -1   +1   -1
 prefix:    2    3    2    1    0    1    0 -> return 3
```

The end of `[5,10)` cancels against the starts at 10. Half-open behaviour falls out without any special case.

**Frame 6.** `book(25,55)`: points 25 and 55 are inserted.

```text
 point:  5  10  15  20  25  40  50  55  60
 delta: +2  +1  -1  -1  +1  -1  +1  -1  -1
 prefix: 2   3   2   1   2   1   2   1   0 -> return 3
```

New local bumps appear at 25 and 50, but the global peak is still 3. These are exactly the values the solution returns: `1 1 2 3 3 3`.

Invariant across frames: `points` was sorted and held every distinct boundary, `delta[p]` was (starts at p) minus (ends at p), and the prefix sum at p equalled the coverage on `[p, next point)`.

## Why it is correct

Take any instant t and let p be the largest boundary `<= t` (if none exists, no event has started and coverage is 0). No boundary lies in `(p, t]`, so the set of running events is the same at t as at p. The prefix sum at p is the sum of `delta[q]` over `q <= p`, which is (#starts <= p) - (#ends <= p), which is the number of running events at p, as argued in the turning point. So the prefix row lists the coverage of every constant piece of the timeline. Its maximum is the maximum coverage over all t, which is the requested k.

Why is the maximum not missed between boundaries? Because coverage is constant between consecutive boundaries, as shown. Why do touching events not overlap? Because coverage on `[p, next)` is read after adding all of `delta[p]`, ends and starts together, and an event ending at p has stopped covering p by definition of half-open.

## Cost

- **Time O(n) per `book`, O(n^2) over n calls.** Up to 2n points. `insort` is O(log n) to find the slot and O(n) to shift, and the sweep is O(n).
- **Space O(n).** The dict and the list each hold at most 2n entries.

Follow-up: a lazy segment tree with range add and global max, built dynamically over `[0, 10^9]` or over compressed coordinates if all bookings are known in advance, gives O(log C) per call. Brute force is O(n^2) per call.

## Variations you will meet

- **My Calendar I / II** (729, 731): reject a booking if it would create a double (I) or triple (II) booking. Same `delta` sweep, but check the peak after tentatively adding, and roll back if it is too high.
- **Static batch, small coordinates** (1094 Car Pooling, 1109 Corporate Flight Bookings): all bookings known up front and times bounded, so use a real array `diff[s] += w; diff[e] -= w` and one `accumulate`. That is O(n + C) with no sorting.
- **Range addition queries on an array** (370): the textbook difference array. Apply k range-adds in O(1) each, then one prefix sum.
- **Report the peak and where it occurs**: track the point where `active` hit its max during the sweep. The peak interval is from that point to the next point.

## What to carry forward

Coverage is a step function, so store only the steps (+1 at starts, -1 at ends, netted per coordinate), and a prefix sum over the sorted boundaries redraws the skyline. The final problem, Rectangle Area II, runs this same sweep in two dimensions: a vertical line steps through x-boundaries, and at each stop it measures the covered length of y-intervals using Merge Intervals.
