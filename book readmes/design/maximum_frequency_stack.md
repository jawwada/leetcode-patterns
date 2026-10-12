# Maximum Frequency Stack
*LeetCode 895 · Hard · Pattern: Frequency buckets as stacks + max pointer · Reading time ~11 min*

## The problem

Design FreqStack with push(val) and pop(): pop removes and returns the most frequent element; on a tie, the one pushed
most recently among the tied values.

```text
Example: push 5,7,5,7,4,5 then pop -> 5 (frequency 3), pop -> 7
  (5 and 7 tie at 2, 7 is more recent), pop -> 5, pop -> 4.
```

## What the problem is really asking

Design a stack-like container with `push(val)` and `pop()`, where `pop` does not remove the top. It removes the **most frequent** value currently in the container; if several values tie for the highest frequency, it removes the one among them that was **pushed most recently**. Frequencies count copies currently present, so popping a value lowers its frequency.

Each `pop` returns one value, but deciding which one means ranking every value by `(frequency, recency of its latest copy)`, and that ranking shifts after every push and every pop.

```text
  push 5, 7, 5, 7, 4, 5

  contents (bottom -> top):  5  7  5  7  4  5
  frequency:   5 -> 3   7 -> 2   4 -> 1

  pop -> 5   (frequency 3, the unique max)
  pop -> 7   (5 and 7 now tie at 2; 7's latest copy is newer)
  pop -> 5   (5 at 2 beats 7 and 4 at 1)
  pop -> 4   (all tie at 1; 4 is the newest)
```

The hard part: "most recent among the tied" refers to the push order of individual copies, while "most frequent" refers to aggregates per value. We need both in O(1).

## Do it by hand first

Lay out horizontal trays, one per frequency level, bottom tray for "first copy", the next for "second copy", and so on. When you push a value, count how many copies of it are in the container now, say f, and drop a token for it on the *right end* of tray f.

```text
  push 5, 7, 5, 7, 4, 5

  tray 3:  5
  tray 2:  5  7
  tray 1:  5  7  4
           left = earlier   right = later
```

Now pop: go to the highest non-empty tray and take its rightmost token. That is 5. Next pop: tray 3 is empty, go to tray 2, rightmost is 7. Then 5 from tray 2. Then tray 1, rightmost is 4. The four answers match.

Your hand tracked: how many copies each value has (to know which tray to drop into), the trays themselves in left-to-right push order, and which tray is the top non-empty one.

## The first honest attempt

Keep the plain list in push order. On `pop`, count every value with a `Counter`, find the max count, then scan from the right for the first element whose value has that count, and delete it.

```text
  items: 5 7 5 7 4 5      pop #1
  count: {5:3, 7:2, 4:1}  <- built from all 6 items
  scan right-to-left: 5 has 3 -> remove index 5

  items: 5 7 5 7 4        pop #2
  count: {5:2, 7:2, 4:1}  <- built again from all 5 items
  scan: 4 (1) no, 7 (2) yes -> remove index 3
```

O(n) per pop. Two things are wasted: the counts are rebuilt from scratch though a single push or pop changes exactly one of them by one, and the right-to-left scan walks past elements whose frequency can never win.

## The turning point

The counting waste is easy: keep a persistent dict `freq[val]`, +1 on push, -1 on pop.

The scan is the interesting part. **Claim: at the moment a value reaches frequency f, it is the most recent value to have reached frequency f; so if we keep, for every f, a stack of values in the order they *reached* f, the answer to pop is always the top of the stack for the maximum frequency.**

Justification. Let `group[f]` be a stack, and on `push(val)` with new frequency f, push `val` onto `group[f]`. Consider the values whose current frequency is the maximum M. Each one's M-th copy is its latest copy, and that copy was pushed exactly when the value reached M, which is exactly when it was pushed onto `group[M]`. So the order of `group[M]` is the order of the latest copies among the tied values, and its top is the most recent one. That is precisely the tie-break the problem asks for.

The surprising part is what happens *after* a pop. We pop `val` from `group[M]`; its frequency drops to M-1. Do we need to move it to `group[M-1]`? No: it is already there. When `val` reached M-1 earlier, it was pushed onto `group[M-1]`, and that entry was never removed. So every value with current frequency f appears in **every** `group[1..f]`, once in each, at the position where it reached that level.

```text
  value 5 with frequency 3 sits in three trays:

  group[3]:  5
  group[2]:  5 ...
  group[1]:  5 ...
  pop removes only the top copy; the lower ones are
  already correctly placed for frequency 2 and 1
```

And the max pointer? Keep an integer `maxfreq`. On push it becomes `max(maxfreq, f)`. On pop, if `group[maxfreq]` became empty, decrement it by exactly one. That is always right, because the value we just popped now has frequency `maxfreq - 1` and sits in `group[maxfreq - 1]`, so that group is non-empty. No search is ever needed.

This is the same "counts move by one, so the extreme moves by one" argument as the `min_freq` of LFU Cache, applied to a maximum.

Notice what we did *not* need. There is no per-value pointer into a linked list, no deletion from the middle of anything, and no tie-break timestamp. LFU and All O`one had to move a key between buckets because each key lived in exactly one bucket. Here a value lives in all of its levels at once, so a pop only ever removes from the top of one stack, and the lower levels never need fixing.

## Watch it work

Operations: `push 5, 7, 5, 7, 4, 5`, then four `pop`s. Stacks are drawn bottom to top, left to right.

Frame 1 — after `push 5, 7, 5`.

```text
  freq:     {5:2, 7:1}
  group[1]: [5, 7]
  group[2]: [5]                 maxfreq = 2
```

5 reached 1, then 7 reached 1, then 5 reached 2.

Frame 2 — after `push 7, 4`.

```text
  freq:     {5:2, 7:2, 4:1}
  group[1]: [5, 7, 4]
  group[2]: [5, 7]              maxfreq = 2
```

7 reached 2 after 5 did, so it sits above 5 in `group[2]`.

Frame 3 — after `push 5`.

```text
  freq:     {5:3, 7:2, 4:1}
  group[1]: [5, 7, 4]
  group[2]: [5, 7]
  group[3]: [5]                 maxfreq = 3
```

5 is the first value to reach 3, so a new level opens and `maxfreq` rises.

Frame 4 — `pop()` returns 5.

```text
  freq:     {5:2, 7:2, 4:1}
  group[1]: [5, 7, 4]
  group[2]: [5, 7]
  group[3]: []                  maxfreq = 3 -> 2
```

The top of `group[3]` was taken; the group emptied, so `maxfreq` dropped by one, and 5's copy in `group[2]` already represents it.

Frame 5 — `pop()` returns 7.

```text
  freq:     {5:2, 7:1, 4:1}
  group[1]: [5, 7, 4]
  group[2]: [5]                 maxfreq = 2
```

The top of `group[2]` is 7, the later of the two values tied at 2.

Frame 6 — `pop()` returns 5, then `pop()` returns 4.

```text
  after pop 5:  group[2]: []   maxfreq = 2 -> 1
                group[1]: [5, 7, 4]
  after pop 4:  group[1]: [5, 7]   maxfreq = 1
  freq: {5:1, 7:1, 4:0}
```

With everything at frequency 1, pop is ordinary stack behaviour on `group[1]`.

In every frame, a value with frequency f appeared once in each of `group[1]` through `group[f]`, and `group[maxfreq]` was the highest non-empty group.

## Why it is correct

Invariant:

- (a) `freq[v]` is the number of copies of v currently in the container.
- (b) For each f >= 1, `group[f]` contains exactly the values v with `freq[v] >= f`, each once, ordered by the time v's f-th copy was pushed.
- (c) `maxfreq` is the largest f with `group[f]` non-empty (0 if empty).

Push of v: `freq[v]` becomes f; v now qualifies for level f for the first time and its f-th copy is the newest push, so appending it to `group[f]` keeps (b). (c) holds after `maxfreq = max(maxfreq, f)`.

Pop: by (b) and (c), `group[maxfreq]` holds exactly the values of maximal frequency, ordered by when their latest copy (the `maxfreq`-th) was pushed. Its top is therefore the most frequent value with the most recent copy, the correct answer. Removing it from `group[maxfreq]` and decrementing its frequency to `maxfreq - 1` keeps (a) and (b), since its entries at lower levels are still valid. If `group[maxfreq]` is now empty, `group[maxfreq - 1]` still contains the popped value, so `maxfreq - 1` is the new maximum, keeping (c).

## Cost

- Time: O(1) per `push` and `pop`: one dict update and one list append or pop.
- Space: O(n) for n pushed-and-not-popped elements: each copy occupies exactly one slot in exactly one group (the k-th copy of v lives in `group[k]`).

The heap alternative, keyed by `(-frequency, -push_index)`, is correct and O(log n), with lazy handling of outdated entries; interviewers accept it but expect the bucket version as the follow-up.

## Variations you will meet

- **Pop the least frequent instead.** Ties and minimum interact badly: popping a value drops it to a lower level that may not exist in a "reached f" sense. Use LFU-style buckets with an `OrderedDict` and a min pointer.
- **Peek without pop.** Return the top of `group[maxfreq]` without removing it; trivially O(1).
- **LFU Cache and All O`one (previous problems).** Same family: frequencies change by one, so the extreme bucket moves by one and is tracked by an integer or a sentinel.
- **Top-k frequent in a stream.** The frequency-bucket picture is also the O(n) bucket-sort solution for top-k frequent elements.

## What to carry forward

Give each frequency level its own stack and record a value at a level the moment it reaches it; lower levels then already hold the right state after a pop, and a max pointer that moves by one finishes the job. The next problem, Dinner Plate Stacks, also juggles many stacks, but the question becomes *which stack has room*, answered with a min-heap of indices that is cleaned lazily.
