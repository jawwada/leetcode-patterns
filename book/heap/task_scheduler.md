# Task Scheduler

*LeetCode 621 · Medium · Pattern: Max-heap + cooldown queue simulation · Reading time ~8 min*

## The problem

Given tasks as uppercase letters and a cooldown n, each unit of time the CPU runs one task or idles, and two identical
tasks must be at least n units apart. Return the minimum total time to finish all tasks.

```text
Example: tasks=[A,A,A,B,B,B], n=2 -> 8 (A B idle A B idle A B).
```

## What the problem is really asking

A CPU runs one task per time unit, or sits idle. Tasks are letters, and two copies of the same letter must be separated by
at least n time units. You may run tasks in any order. Return the fewest time units needed to run all of them, idles
included.

The answer is a single number: the length of the shortest legal timeline. The hard part is that order matters a great
deal and there are many orders. Spend the wrong letter early and you are left at the end with several copies of one letter
and nothing to put between them, which means idles.

```text
tasks = A A A B B B     n = 2   (copies of a letter need
                                 2 slots between them)
time:   1  2  3  4  5  6  7  8
       [A][B][_][A][B][_][A][B]      length 8
        |<- 3 ->|  A at 1, next A at 4: gap of 2 slots
```

## Do it by hand first

Take `A A A B B B C`, n = 2. A human sees that A and B each have three copies and C only one, and that the scarce resource
is "things to put between the A's".

A good hand strategy: at each time unit, among letters that are allowed to run now, run the one with the most copies left.
Remember when each letter last ran so you know when it is allowed again.

```text
t  run  left after          cooling (allowed again at)
1  A    A2 B3 C1            A@4
2  B    A2 B2 C1            A@4 B@5
3  C    A2 B2 C0            A@4 B@5
4  A    A1 B2               B@5 A@7
5  B    A1 B1               A@7 B@8
6  _    (nothing allowed)   A@7 B@8
7  A    A0 B1               B@8
8  B    done                -> 8
```

Your hand kept two things: the remaining count per letter, so you could pick the biggest, and a list of letters waiting
out their cooldown, each stamped with the time it comes back. A "biggest remaining" lookup and a "who comes back next"
lookup: one structure for each.

## The first honest attempt

Simulate tick by tick. At each tick, scan all 26 letters, find those whose last run was more than n ticks ago, run the
one with the most copies left, or idle if none qualifies.

That is O(T * 26) where T is the answer. Two kinds of repeated work show up:

```text
tick 5: scan A..Z, check 26 cooldowns, find max count
tick 6: scan A..Z, check 26 cooldowns, find max count
         ^ only ONE count changed since tick 5
tick 7: scan A..Z ...
         ^ A's return time (7) was known at tick 4
```

And when n is huge, say n = 100 with tasks `A A`, the loop idles through 100 ticks one at a time, each with a full scan,
although the moment A ran we already knew exactly when it could run again.

## The turning point

**Claim: always running the available letter with the most copies left is optimal, and the two lookups it needs are a
max-heap of counts and a FIFO queue of cooling letters.**

Why most-copies-first? The letter with the most copies is the one most likely to be stranded at the end with nothing to
separate its copies. Running it whenever you can spreads its copies as early as possible and keeps every other letter
available as filler between them. Running a rarer letter instead only shrinks the pool of fillers you will need later.
The correctness section turns this into a counting argument.

Now the data structures.

**Max-heap of remaining counts.** "Which ready letter has the most copies?" is the question a heap answers in O(log 26).
`heapq` is a min-heap, so we store negated counts: `-3` sits above `-2`. We do not even need the letters themselves, only
their counts, because identity never affects the schedule length.

**FIFO queue of cooling counts.** A letter run at time t may run again at time t + n + 1. Every letter goes through the
same cooldown length, so letters leave the queue in the same order they entered. A plain `deque` is therefore sorted by
return time for free, and "who comes back next?" is just the head. No second heap is needed.

```text
   heap (ready, biggest on top)        cooling queue (FIFO)
            [-3]                  front -> (ready 3, -2) (4, -2)
           /    \                          ^ next to return
        [-2]    [-1]
   pop top -> run it -> if copies remain, append to queue
   when queue head's time arrives -> push it back on heap
```

The code stamps each queue entry with `time + n` and moves it back into the heap at the end of that tick, so the letter is
available from tick `time + n + 1`, which is exactly the cooldown rule.

**Skip idle stretches.** If the heap is empty but the queue is not, nothing can run until the queue head's time. Instead
of looping through idle ticks, set the clock to just before that time. With `A A` and n = 5:

```text
t=1: run A, queue [(6, A1)], heap empty
     jump: time = 6 - 1 = 5      (ticks 2..5 skipped)
t=6: idle tick; A released at end of tick 6
t=7: run A                         -> answer 7
```

The loop now runs once per task plus once per idle stretch, not once per idle tick.

## Watch it work

`tasks = A A A B B B`, n = 2. The state is shown after each tick finishes. Heap entries are negated counts written as
letters for readability.

```text
Frame 1: t=1  run A (3 -> 2), park it until end of t=3
heap  [B3]                 queue  (3, A2)
timeline  A
```

A had the biggest count (tied with B; either choice works). It now waits in the queue.

```text
Frame 2: t=2  run B (3 -> 2), park it until end of t=4
heap  []                   queue  (3, A2) (4, B2)
timeline  A B
```

The heap is empty. The jump rule sets time to 3 - 1 = 2, which is where we already are, so nothing is skipped.

```text
Frame 3: t=3  heap empty -> idle; A released at end of t=3
heap  [A2]                 queue  (4, B2)
timeline  A B _
```

This idle is forced: both letters are cooling. At the end of the tick A's stamp matches the clock and it returns.

```text
Frame 4: t=4  run A (2 -> 1); B released at end of t=4
heap  [B2]                 queue  (6, A1)
timeline  A B _ A
```

A runs exactly n + 1 = 3 ticks after its first run. B's stamp 4 matches the clock and it returns.

```text
Frame 5: t=5 run B (2 -> 1); t=6 idle, A released
after t=6: heap [A1]        queue  (7, B1)
timeline  A B _ A B _
```

The same pattern as frames 2 and 3: two runs, then one forced idle.

```text
Frame 6: t=7 run A (1 -> 0, not parked), B released
         t=8 run B (1 -> 0); heap and queue empty
timeline  A B _ A B _ A B      answer = 8
```

Letters with zero copies left are not re-queued, so the loop ends when both containers are empty.

Throughout, the heap held exactly the letters allowed to run right now, the queue held the cooling letters in order of
return, and every letter sat in exactly one of the two places until its last copy ran.

## Why it is correct

Two facts pin the answer down.

**A lower bound.** Let the largest count be `M`, and let `c` letters share that count. The copies of one such letter
need `M - 1` gaps of at least n slots each, so a frame of `(M - 1) * (n + 1)` slots, plus one slot for each of the c
letters in the last row:

```text
n = 2, M = 3, c = 2 (A and B)
row 1:  A B _
row 2:  A B _       (M - 1) rows of width n + 1
last :  A B         plus c slots
total = 2 * 3 + 2 = 8
```

Also, every task needs its own slot, so the answer is at least `len(tasks)`. Hence the answer is at least
`max(len(tasks), (M - 1) * (n + 1) + c)`.

**The greedy meets the bound.** Running the largest available count first keeps the remaining counts as even as possible.
An idle happens only when every remaining letter is cooling, and that can only occur while the most frequent letters
still dominate the frame; once there are enough distinct letters to fill every row, the greedy never idles and the total
equals `len(tasks)`. In either case the greedy hits the larger of the two bounds, so it is optimal. The simulation's
cooldown rule (return at `t + n + 1`) is the statement's constraint, so the produced timeline is legal.

## Cost

- **Heap + queue simulation:** at most 26 letters live in the heap or queue, so each heap operation is O(log 26) = O(1).
  The loop runs once per task plus once per idle stretch, so O(len(tasks)) time and O(26) space.
- **Closed form:** `max(len(tasks), (M - 1) * (n + 1) + c)` computed from the counts in O(len(tasks)) time and O(26)
  space. Faster, but only answers this exact question.
- **Tick-by-tick brute force:** O(T * 26), where T can be large when n is large.

## Variations you will meet

- **Return the schedule itself.** The closed form cannot; the simulation can, by recording letters and idles. Keep letters
  in the heap as `(-count, letter)`.
- **Tasks must run in the given order (Task Scheduler II, LeetCode 2365).** No choice remains, so no heap: walk the list
  and keep a map from task to the earliest next allowed day.
- **No idles allowed; return any arrangement or report failure.** That is the next problem, Reorganize String, with
  n = 1.
- **Each copy must be at least k apart in a string, not in time.** Rearrange String k Distance Apart: the same heap and
  queue, but if the heap ever runs dry while the queue still holds letters, you fail instead of idling.

## What to carry forward

Pick the biggest remaining count from a max-heap, park what you used in a FIFO queue stamped with its return time, and
jump the clock across idle gaps. The next problem is the same greedy with a cooldown of one and no idles allowed, which
turns the question into "is it possible at all?".
