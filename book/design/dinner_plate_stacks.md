# Dinner Plate Stacks
*LeetCode 1172 · Hard · Pattern: List of stacks + min-heap of "has room" indices with lazy invalidation · Reading time ~12 min*

## The problem

There are infinitely many stacks in a row, each holding at most capacity plates. push(val) places the plate on the
leftmost stack with room, pop() removes from the rightmost non-empty stack, and popAtStack(i) removes the top of stack
i; both pops return -1 when there is nothing to remove.

```text
Example: capacity=2, push 1,2,3,4,5 -> [1,2][3,4][5];
  popAtStack(0) -> 2; push(20) lands on stack 0 ->
  [1,20][3,4][5]; pop() -> 5.
```

## What the problem is really asking

There is an infinite row of stacks, numbered 0, 1, 2, ... from the left, and each can hold at most `capacity` plates.

- `push(val)` puts a plate on the **leftmost** stack that is not full.
- `pop()` removes the top plate from the **rightmost** non-empty stack.
- `popAtStack(i)` removes the top plate of stack i.

Both pops return -1 when there is nothing to remove. With up to 200,000 calls, every operation must be roughly O(log n).

```text
  capacity 2, push 1,2,3,4,5

   stack:   0      1      2
           [2]    [4]
           [1]    [3]    [5]

  popAtStack(0) -> 2      a hole opens in stack 0
  push(20)      -> lands in stack 0, not stack 2
  pop()         -> 5      from the rightmost stack
```

The answers are single plates, but the operations pull in opposite directions: `push` cares about the leftmost gap, `pop` about the rightmost non-empty stack, and `popAtStack` can punch holes anywhere in between.

## Do it by hand first

Picture the stacks as columns on a shelf, and keep a sticky note listing the column numbers that have room. `push` looks at the smallest number on the note. `popAtStack(i)` adds i to the note. When a column fills up, you cross it off.

```text
  columns:   0     1     2         note: {2}
            [1,2] [3,4] [5]

  popAtStack(0):
            [1]   [3,4] [5]         note: {0, 2}
  push(20): smallest on note is 0
            [1,20][3,4] [5]         note: {2}  (0 is full again)
```

For `pop`, you just look at the rightmost column, provided you never leave empty columns dangling at the right end.

Your hand kept track of: the columns themselves, a set of "room available" indices from which you always take the smallest, and a clean right edge.

## The first honest attempt

A list of stacks. `push` scans from index 0 for the first stack that is not full; if none, append a new stack. `pop` skips trailing empty stacks and pops the last one. `popAtStack(i)` indexes directly.

```text
  20,000 full stacks, then push:

  stack:  0     1     2    ...  19999   20000
         full  full  full  ...  full    (new)
          ?     ?     ?    ...   ?             20,000 checks
  next push: same walk again over the same full stacks
```

`push` is O(k) for k stacks. The waste is re-examining stacks known to be full. A full stack can only regain room in one way: a `popAtStack` on it (or a `pop`, which is a `popAtStack` on the last stack). Between those events, its fullness cannot change, so rechecking it is wasted.

## The turning point

**Claim: room appears only at the moment of a pop, at a known index, so record that index in a min-heap and let `push` read the smallest one instead of scanning.**

The heap holds indices of stacks that *may* have room. Its smallest element is the leftmost candidate.

```text
  heap as a triangle        heap as an array
         0                  [0, 2, 5]
        / \                  ^ open[0] = leftmost candidate
       2   5
```

- `popAtStack(i)` removes a plate from stack i and pushes i onto the heap: a hole now exists there.
- `push(val)` takes the heap's smallest index i, puts the plate on stack i, and if stack i is now full, pops i off the heap. If the heap is empty, every existing stack is full, so append a new stack and use its index.

There is one complication, and it is the heart of the problem: **entries can go stale**. An index in the heap can stop being valid in two ways:

1. *The stack filled up again.* If `popAtStack(0)` is called twice, index 0 enters the heap twice. Two pushes refill stack 0; the `push` that fills it removes one copy of 0, and the other copy still sits in the heap, pointing at a full stack.
2. *The stack disappeared.* `pop()` trims empty stacks from the right end. If stack 2 had an entry in the heap and stack 2 is trimmed away, the entry points past the end of the list.

Removing an arbitrary element from a heap is O(n). So we do not remove stale entries when they become stale. We remove them **lazily**: when `push` looks at the heap top, it checks "is this index inside the list and is that stack not full?" If not, it pops the entry and looks again. Each entry is pushed once and popped at most once, so the cleaning costs O(log n) amortised per operation.

The right edge needs its own invariant: **the last stack in the list is never empty**. After any pop, while the last stack is empty, remove it. Then `pop()` is simply `popAtStack(len(stacks) - 1)`, and it returns -1 only when there are no stacks at all.

```text
  why trimming matters:

  without trim:  [1] [ ] [ ]    pop() looks at stack 2,
                  0   1   2     finds it empty -> -1: WRONG
  with trim:     [1]            pop() looks at stack 0 -> 1
```

So the full state is: `stacks` (list of lists, last one non-empty) and `open` (a min-heap of candidate indices, possibly with stale or duplicate entries, but containing every stack that truly has room).

## Watch it work

Capacity 2. Operations: `push 1..5`, `popAtStack(0)`, `push(20)`, `push(21)`, `popAtStack(2)`, `pop()`, `push(30)`.

Frame 1 — after `push 1, 2, 3, 4, 5`.

```text
  stacks: [1,2] [3,4] [5]
            0     1    2
  open (heap array): [2]
```

Each time the heap was empty a new stack was opened and its index pushed; the index was retired as soon as that stack filled.

Frame 2 — `popAtStack(0)` returns 2.

```text
  stacks: [1]   [3,4] [5]
            0     1    2
  open: [0, 2]         top = 0
```

A hole opened at stack 0, so 0 was pushed and became the heap top.

Frame 3 — `push(20)`, then `push(21)`.

```text
  after push(20):  [1,20] [3,4] [5]     open: [2]
                   stack 0 full -> 0 popped from heap
  after push(21):  [1,20] [3,4] [5,21]  open: []
                   stack 2 full -> 2 popped from heap
```

The plate went left into the hole, not onto stack 2, and each index left the heap the moment its stack filled.

Frame 4 — `popAtStack(2)` returns 21.

```text
  stacks: [1,20] [3,4] [5]
  open: [2]
```

A hole opened at stack 2; the last stack is still non-empty, so nothing is trimmed.

Frame 5 — `pop()` returns 5.

```text
  popAtStack(2): stack 2 -> [], push 2 onto heap
  trim: stack 2 is empty and last -> removed
  stacks: [1,20] [3,4]
  open: [2, 2]          both entries are now stale
```

The heap still names index 2 twice, though stack 2 no longer exists; we do not clean that up yet.

Frame 6 — `push(30)`.

```text
  top 2: 2 >= len(stacks)=2 -> stale, heappop
  top 2: stale again        -> heappop
  heap empty -> append new stack 2, push index 2
  stacks: [1,20] [3,4] [30]
  open: [2]
```

The stale entries were discarded only when they reached the top and failed the check.

Across all frames, the last stack was never empty, and every stack with room had its index somewhere in the heap; stale entries were tolerated until the moment they were read.

## Why it is correct

Invariant:

- (a) `stacks[-1]` is non-empty (or there are no stacks); every stack has at most `capacity` plates.
- (b) Every index i < `len(stacks)` whose stack has room appears in `open` at least once. (Other entries may be present; they are stale.)

`push`: it discards top entries that fail the check "inside the list and not full". By (b), no discarded entry was the index of a stack with room, so the first entry that passes is the smallest index with room, the leftmost non-full stack, which is where the plate must go. If all entries are discarded, (b) says no existing stack has room, so a new stack on the right is the leftmost one with room. After placing the plate, if the stack became full we pop its index; any other copies of it become stale, harmless. (a) holds because we only add to stacks.

`popAtStack(i)`: if the stack exists and is non-empty, we remove its top plate, which is the definition. The stack now has room, and we push i, keeping (b). Trimming empty stacks off the right end restores (a); removing a stack beyond the end cannot violate (b), which only speaks about indices inside the list.

`pop()`: by (a), the last stack is the rightmost non-empty one, so `popAtStack(len - 1)` is exactly the rightmost non-empty stack's top, or -1 when there are no stacks.

## Cost

- Time: O(log n) amortised per operation. Each heap entry is pushed once (by a pop or a new stack) and popped at most once, so heap work is O(log n) per operation amortised. Trimming removes each stack at most once after it was created, O(1) amortised.
- Space: O(n): the stacks hold the n plates, and the heap holds at most one entry per pop or new stack still outstanding.

## Variations you will meet

- **Eager deletion with a sorted set.** Keep the indices of non-full stacks in a sorted container (`sortedcontainers.SortedList`) and remove an index exactly when its stack fills or is trimmed. No stale entries; O(log n) per operation; easier to reason about if the library is allowed.
- **Lazy deletion elsewhere.** The same "validate on read" trick is used in Sliding Window Median (heaps with delayed removals), Dijkstra with a binary heap (skip outdated distances), and Meeting Rooms III (rooms freed by time).
- **Maximum Frequency Stack (previous problem).** Also many stacks, but which stack to read is decided by a counter that moves by one; here the candidate set is sparse and arbitrary, so it needs a heap.
- **popAtStack with a maximum instead of a top.** Combine each stack with a Min Stack style auxiliary array, and the heap logic is unchanged.

## What to carry forward

When the only event that creates a candidate is known at the moment it happens, push the candidate into a heap then, and validate entries when you read them instead of deleting them when they die. The next problem, Data Stream as Disjoint Intervals, keeps a dynamic set of pieces on a number line, merging neighbours as numbers arrive, so the question shifts from "smallest index with room" to "which intervals touch this new point".
