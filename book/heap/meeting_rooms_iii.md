# Meeting Rooms III

*LeetCode 2402 · Hard · Pattern: Two heaps (free rooms by id, busy rooms by end time) over a sorted sweep · Reading time ~11 min*

## What the problem is really asking

There are `n` rooms, numbered `0` to `n - 1`, and a list of meetings `[start, end)` with distinct start times. Meetings are handed out by a strict rule:

1. A meeting goes to the **lowest-numbered free room**.
2. If no room is free, the meeting **waits** until the earliest room frees up, then runs for its original duration. If several rooms free up at that same earliest moment, it takes the lowest-numbered one.
3. When rooms free up and several meetings are waiting, the one with the **earlier original start** goes first.

Return the room that hosted the most meetings (lowest number on ties).

Unlike the last few problems, there is no choice to optimise. The rule is fully specified; the task is to *simulate it fast*. The answer is a room number, and the difficulty is bookkeeping: delays push meetings later, which changes when rooms free up, which changes who gets delayed next. Our example: `n = 2`, meetings `A=[0,10)`, `B=[1,5)`, `C=[2,7)`, `D=[3,4)`.

```text
 time     0    5    10
          |....|....|.
 room 0   AAAAAAAAAAD        A [0,10)   D delayed to [10,11)
 room 1    BBBBCCCCC         B [1,5)    C delayed to [5,10)

 counts:  room 0 -> 2, room 1 -> 2   answer 0 (tie, lowest)
```

## Do it by hand first

Walk the meetings in order of start time, and keep a little note per room: "busy until when?"

- t=0, A arrives. Both rooms free; take the lowest, room 0. Room 0 busy until 10.
- t=1, B arrives. Room 1 is free. Room 1 busy until 5.
- t=2, C arrives. Room 0 busy until 10, room 1 until 5. Nothing is free. The earliest to free is room 1 at t=5. C waits and runs `[5, 10)` there (its duration is 5).
- t=3, D arrives. Room 0 until 10, room 1 until 10. Nothing free. The earliest is a tie at 10; take the lower number, room 0. D runs `[10, 11)`.

Each room hosted two meetings; room 0 wins the tie.

Look at the two questions your hand asked, over and over:

```text
 Q1: "which rooms are free right now, and which is lowest?"
     -> a set of idle rooms, ordered by room number
 Q2: "none free: which room frees first (lowest id on tie)?"
     -> a set of busy rooms, ordered by (end time, room number)
```

Both are "give me the minimum of a set that changes a little at a time". Two min-heaps.

## The first honest attempt

Keep an array `free_at[r]`. Sort meetings by start. For each meeting, scan all `n` rooms to find the lowest `r` with `free_at[r] <= start`; if there is none, scan again for the smallest `(free_at[r], r)` and delay. That is `O(m log m + m · n)`.

It is correct and it is the specification written as code. The waste: between consecutive meetings, only one or two rooms change state, but every meeting rescans all `n` rooms.

```text
 meeting  scan of rooms 0..n-1                changed since last
 A        [0 1 2 3 ... n-1]  all re-read      -
 B        [0 1 2 3 ... n-1]  all re-read      room 0 only
 C        [0 1 2 3 ... n-1]  all re-read      room 1 only
 D        [0 1 2 3 ... n-1]  all re-read      room 1 only
```

With `n` up to 100 and `m` up to `10^5` this passes, but the structure is the lesson: the scan is answering two minimum queries over sets that change incrementally.

## The turning point

**Claim: at the moment a meeting with original start `s` is handled, the rooms split cleanly into "free by time `s`" and "busy past time `s`", and the rule only ever needs the minimum of one of those two sets.**

Keep each set in its own heap:

- `free`: a min-heap of room ids. Root = lowest-numbered idle room.
- `busy`: a min-heap of `(end_time, room_id)`. Root = the room that frees first, and Python's tuple ordering breaks ties by room id for free, exactly as the rule demands.

For each meeting in start order:

1. **Release.** While `busy`'s root has `end_time <= s`, pop it and push its room id into `free`. Release *all* such rooms, not just one: a room numbered 0 that freed at time 3 must be visible even if room 5 freed at time 1. Use `<=`, because a meeting may start exactly when another ends (intervals are half-open).
2. **Assign.** If `free` is non-empty, pop its root; the meeting keeps its `end`. Otherwise pop `busy`'s root `(t, room)`; the meeting is delayed, so its new end is `t + (end - s)`.
3. **Record.** Push `(new_end, room)` into `busy` and increment `count[room]`.

Rule 3 of the problem (earlier original start gets priority among waiting meetings) is handled by the sort itself. We never hold a meeting back; we assign every meeting the moment we process it, in original start order, so an earlier meeting always claims the earliest-freeing room before a later one is even looked at.

One fact is easy to miss: rooms move *between* the heaps. Every room is in exactly one heap at all times. A room enters `busy` when it gets a meeting and returns to `free` only when a later meeting's start passes its end time. In the delayed case, a room goes from `busy` straight back into `busy` with a later end time.

## Watch it work

`free` is shown as a sorted list of ids; `busy` as a list of `(end, room)`, root first.

Frame 1: Meeting A `[0,10)`. Nothing to release. Free root is room 0.

```text
 time  0         10
 r0    AAAAAAAAAA
 r1
 free [1]     busy [(10,0)]     count [1, 0]
```

The lowest idle room wins.

Frame 2: Meeting B `[1,5)`. `busy` root ends at 10 > 1, no release. Room 1 is free.

```text
 time  0    5    10
 r0    AAAAAAAAAA
 r1     BBBB
 free []      busy [(5,1), (10,0)]    count [1, 1]
```

Both rooms are now busy, and the busy heap's root is the one finishing first, room 1 at time 5.

Frame 3: Meeting C `[2,7)`, duration 5. Root ends at 5 > 2, no release. `free` is empty: pop `(5,1)`, delay C to `[5,10)`.

```text
 time  0    5    10
 r0    AAAAAAAAAA
 r1     BBBBCCCCC          C slid from 2 to 5
 free []      busy [(10,0), (10,1)]   count [1, 2]
       busy as a triangle:   (10,0)
                             /
                         (10,1)
```

The delayed meeting is glued onto the end of B and keeps its length.

Frame 4: Meeting D `[3,4)`, duration 1. Root ends at 10 > 3, no release. `free` empty: pop `(10,0)`, beating `(10,1)` on the room-id tiebreak. D becomes `[10,11)`.

```text
 time  0    5    10
 r0    AAAAAAAAAAD
 r1     BBBBCCCCC
 free []      busy [(10,1), (11,0)]   count [2, 2]
```

The tuple ordering resolved the tie without any extra code.

Frame 5: Done. `count = [2, 2]`, the maximum is 2, first at room 0.

```text
 answer: count.index(max(count)) = 0
```

Across frames, every room was in exactly one heap, `free` held exactly the rooms whose last meeting ended by the current start, and `busy` held the others keyed by when they free up.

## Why it is correct

There is no greedy *choice* here: the problem dictates which room each meeting gets, so there is nothing to exchange. What must be proved is that the two heaps always answer the dictated questions exactly as the full scan would.

**Invariant.** Just after the release step for a meeting with original start `s`:

- `free` contains exactly the rooms whose current booking ends at or before `s`;
- `busy` contains exactly the other rooms, each keyed by `(time it frees, room id)`.

*Why it holds.* Initially all rooms are free. A room is pushed into `busy` only when assigned, with its true end time. Start times only increase, so a room that was free by an earlier start is still free by this one: rooms in `free` never need to move back on their own. And the release loop pops every busy room whose end is `<= s`; because `busy` is a min-heap on end time, once the root ends after `s`, every room in it does.

*Why it implies the answer.* The rule's first question is "lowest-numbered room among those free by `s`". By the invariant, that set is exactly `free`, and its minimum is the root. The rule's second question, asked only when no room is free by `s`, is "smallest `(free time, room id)`". By the invariant, that is `busy`'s root. So each meeting gets exactly the room the specification assigns, with exactly the specified end time, and the counts match the specification's counts.

**Order of waiting meetings.** The specification gives waiting meetings priority by original start. We process meetings in that order and assign each one immediately, so an earlier meeting always takes the earliest-freeing room before a later meeting can compete for it. If this were not the case (if we, say, processed meetings in order of their *delayed* start) the assignments could differ.

## Cost

- **Time `O(m log m + m log n)`.** Sorting the `m` meetings, then each meeting does a constant number of pushes and pops on heaps of size at most `n`. Each release moves one room, and there is at most one release per earlier assignment, so releases total `O(m)` across the run.
- **Space `O(n)`.** Each room sits in exactly one heap, plus the count array (sorting in place aside).

The scan version is `O(m log m + m · n)` time, `O(n)` space.

## Variations you will meet

- **Meeting Rooms II (LeetCode 253).** Unlimited rooms, and the question is how many you need. Only the `busy` heap (end times) survives; its size after each placement is the number of rooms in use.
- **Single-Threaded CPU (LeetCode 1834).** One processor, and the choice among waiting tasks is by shortest processing time. The heap now holds *waiting tasks* rather than rooms, and the clock jumps forward when the CPU idles.
- **Process Tasks Using Servers (LeetCode 1882).** Servers with weights: the `free` heap orders by `(weight, index)` and the `busy` heap by `(free time, weight, index)`. Exactly this two-heap dance with a richer key.
- **Return the timeline, not the winner.** Keep, per room, the list of `(actual start, actual end)` you assigned; the heaps do not change.

## What to carry forward

When the rule says "lowest free one, else the soonest-free one", keep two min-heaps and shuttle items between them as the sweep's clock advances: release everything that expired, then read a root. The next problem, The Skyline Problem, keeps the sweep but has only one heap, and deals with expired items lazily, throwing them away only when they reach the root.
