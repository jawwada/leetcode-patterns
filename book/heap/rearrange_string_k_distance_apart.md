# Rearrange String k Distance Apart

*LeetCode 358 · Hard · Pattern: Greedy max-heap by remaining count + fixed-length cooldown queue · Reading time ~10 min*

## What the problem is really asking

You get a string `s` and a number `k`. Shuffle the letters so that any two copies of the same letter sit at least `k` positions apart, meaning that if `a` sits at index `i`, the next `a` can sit at index `i + k` at the earliest. Return any shuffle that works, or the empty string if none exists. When `k` is 0 or 1 there is no real constraint and `s` itself is a valid answer.

The answer is a permutation of the input, so you are not inventing anything. You are deciding an order. The difficulty is that the decision at slot 3 constrains slots 4, 5, ..., `3 + k - 1`, and a bad early choice may only show itself as a dead end many slots later.

The last two problems were close cousins. Task Scheduler let the CPU sit idle, so it only had to count the idle slots. Reorganize String was this exact problem with `k = 2`, where "do not repeat the previous letter" can be enforced by holding one letter aside for a single turn. Here the hold-aside has to last `k - 1` turns, so a single "previous" variable stops being enough.

```text
s = "aaadbbcc", k = 2

counts:  a:3  b:2  c:2  d:1        n = 8

one valid answer:
 index:  0 1 2 3 4 5 6 7
 char :  a b a c a b c d
         a---a---a          every gap between equal
           b-------b        letters is >= 2
               c-----c
```

## Do it by hand first

Take `s = "aaabc"` and `k = 2`. A person does not try orderings at random. They see three `a`s and realise the `a`s are the trouble: three `a`s spaced 2 apart need positions 0, 2, 4, which is the whole length of a 5-letter string. So they lay the `a`s down first and fill the gaps with whatever is left.

```text
k = 2, s = "aaabc"

 step 1: place the a's as early as allowed
   slot:  0 1 2 3 4
          a _ a _ a
 step 2: fill gaps with the rest
          a b a c a     done
```

Now try `k = 3` on the same letters. The `a`s need positions 0, 3, 6, but the string only has positions 0 to 4. You can see the failure with nothing but arithmetic.

Two things were in the hand's head the whole time. First: "which letter has the most copies still to place?" That is a maximum over a changing set of counts. Second: "which letters did I use recently and so cannot use right now?" That is a short list of the last few placed letters, with the oldest falling off as each new letter is placed. A max-heap and a queue will do these two jobs.

## The first honest attempt

Fill slot by slot with backtracking. At each slot, try every letter that still has copies and does not appear in the previous `k - 1` slots. If you reach a slot where nothing fits, undo the last choice and try the next one. If you fill all `n` slots, return the result.

This is correct, but in the worst case it explores exponentially many prefixes. To see where the time goes, run it on `s = "abccc"`, `k = 2`, trying letters in alphabetical order. These are the exact prefixes it visits:

```text
""
 a -> ab -> abc        dead: c,c left, gap rule blocks
   -> ac -> acb -> acbc     dead: one c left, just used c
 b -> ba -> bac        dead
   -> bc -> bca -> bcac     dead
 c -> ca -> cab -> cabc     dead
        -> cac -> cacb -> cacbc   FOUND
```

There are 19 prefixes for a 5-letter string. All of the dead branches fail for the same reason: they postponed `c`, the letter with the most copies left, and later there were not enough slots to spread the remaining `c`s out. The search keeps discovering this one fact over and over, under different prefixes. It also tries `ab...` and `ba...` as separate worlds even though `a` and `b` each have one copy and are interchangeable as far as feasibility goes.

## The turning point

**Claim: among the letters allowed at the current slot, placing the one with the most remaining copies is never a mistake.**

Why it holds: the letter with the most copies left is the one under the most pressure. Each copy of it needs its own slot, and consecutive copies need `k` slots between them. If you put some other allowed letter `y` here and save the most frequent letter `x` for later, you have made the stretch that has to hold all of `x`'s copies one slot shorter, and `x` was the letter with the least room to spare. Turned around: take any valid answer that puts `y` here, find the next place it uses `x`, and swap the two. `x` lands here, and it is allowed here, so the swap does not break the gap rule for `x`. `y` lands later, and since `y` had no more copies than `x`, it is never more crowded than `x` was. So a valid answer that starts with the greedy choice always exists, and you never need to branch. The backtracking tree collapses to a single path.

The claim leaves two operations to make fast:

1. **"Most remaining copies among allowed letters."** Keep the allowed letters in a **max-heap keyed by remaining count**. Python's `heapq` is a min-heap, so store `(-count, letter)`. The top is the letter to place.
2. **"Allowed" means "not used in the last `k - 1` slots".** When you place a letter, take it out of the heap and put it at the back of a **FIFO cooldown queue**. When the queue has `k` entries, the front entry was placed exactly `k` slots ago, so it is rested. Pop it and, if it still has copies, push it back into the heap.

The queue gets a new entry at every slot, including entries whose count has dropped to 0. That is what makes "length of the queue" equal "number of slots elapsed". If you skipped zero-count letters, the queue would release the next letter too early.

The failure condition comes for free. If you reach a slot and the heap is empty, every letter with copies left is still resting. No letter can legally go here, and since the greedy choice was always safe, no earlier choice could have avoided this. Return `""`.

## Watch it work

`s = "aaadbbcc"`, `k = 2`. Heap entries are drawn as `letter count` (stored in code as `(-count, letter)`, so ties break alphabetically). With `k = 2` the queue reaches length 2 right after each placement and immediately releases its front, so between steps the bench holds the one letter placed last.

Frame 1: heapify the counts.

```text
heap (max by count)          bench (FIFO)
        a3                   [ ]
       /  \
     c2    b2
     /
   d1
array: [a3, c2, b2, d1]
out:   ""
```

`a` sits at the apex because it has the most copies.

Frame 2: slot 0. Pop `a3`, write `a`, bench gets `a2`.

```text
heap                         bench
        b2                   [a2]
       /  \
     c2    d1
array: [b2, c2, d1]
out:   "a"
```

The bench has length 1, less than `k`, so nobody is released. `b2` rises to the top because `b` comes before `c` in the tie-break.

Frame 3: slot 1. Pop `b2`, write `b`, bench is `[a2, b1]`, which has length `k`, so `a2` is released back into the heap.

```text
heap                         bench
        a2                   [b1]
       /  \
     d1    c2
array: [a2, d1, c2]
out:   "ab"
```

`a` was placed 2 slots ago, so it is legal again, and it is still the most pressured letter.

Frame 4: slot 2. Pop `a2`, write `a`, bench `[b1, a1]` releases `b1`.

```text
heap                         bench
        c2                   [a1]
       /  \
     d1    b1
array: [c2, d1, b1]
out:   "aba"
```

`c` now has the most copies among rested letters, so it takes the apex.

Frame 5: slot 3. Pop `c2`, write `c`, release `a1`.

```text
heap                         bench
        a1                   [c1]
       /  \
     d1    b1
array: [a1, d1, b1]
out:   "abac"
```

All counts are now 1, and the letter names break the ties.

Frame 6: slots 4 to 7. Each pop writes a letter. Letters whose count hits 0 still pass through the bench and are then dropped instead of re-pushed.

```text
slot 4: pop a1 -> "abaca"     release c1   heap [b1,d1,c1]
slot 5: pop b1 -> "abacab"    drop a0      heap [c1,d1]
slot 6: pop c1 -> "abacabc"   drop b0      heap [d1]
slot 7: pop d1 -> "abacabcd"  drop c0      heap [ ]

final:  a b a c a b c d     all equal letters >= 2 apart
```

Across every frame, each letter with copies left was in exactly one place: in the heap (rested) or on the bench (resting). The bench always held the letters placed in the last `k - 1` slots, in placement order. The heap top was always the rested letter with the largest remaining count.

## Why it is correct

**Invariant.** Before each slot `p`: (a) the bench holds exactly the letters placed at slots `p - k + 1 .. p - 1`, oldest first; (b) the heap holds every other letter that still has copies, with its true remaining count. Placing a letter appends it to the bench. When the bench reaches length `k`, its front was placed at slot `p - k + 1`, so it can legally go at slot `p + 1`, which is exactly when it becomes available again. So every letter popped from the heap is legal at the current slot, and the output never breaks the gap rule.

**Greedy choice is safe (exchange sketch).** Suppose some valid completion of the current prefix puts letter `y` at slot `p`, while the greedy choice `x` is also rested and has `count(x) >= count(y)`. In that completion, swap the names `x` and `y` from slot `p` onward for as many copies as `y` has. `x` was rested, so it is legal at `p`. Every later position that held a `y` now holds an `x` and the reverse, so the gaps that were legal for one letter are now used by the other. The leftover copies of `x` stay where they were. If any valid answer exists, one exists that agrees with greedy at slot `p`. Repeat the argument slot by slot. Put in counting terms: the binding constraint is always the letter with the most copies (it needs `(f - 1) * k + 1` slots of span), and spending the current slot on it is what keeps that constraint satisfiable. The solution file checks this against exhaustive backtracking on 200 random inputs, and the two always agree on whether an answer exists.

**Failure is real.** If the heap is empty at slot `p`, every letter with copies left was used in the last `k - 1` slots. Greedy never makes a fatal choice, so the input has no answer. In `"aaabc"`, `k = 3`:

```text
slot:   0 1 2 3 4
out:    a b c a ?        heap [ ]   bench [c0, a1]
                         a is resting, nothing rested
                         -> return ""
```

A quick sanity check that matches the hand reasoning: with `f` the top count and `m` the number of letters having that count, an answer exists exactly when `(f - 1) * k + m <= n`. Here `(3 - 1) * 3 + 1 = 7 > 5`.

## Cost

- **Time: O(n log A)**, where `A <= 26` is the alphabet size. Each of the `n` slots does one heap pop and at most one heap push, on a heap of at most `A` entries. Counting the letters is O(n).
- **Space: O(A)** for the heap and the bench (the bench holds at most `min(k, n)` entries, and only letters with copies left go back to the heap), plus O(n) for the output.

## Variations you will meet

- **Task Scheduler (LeetCode 621).** Same cooldown, but idling is allowed and you return a length instead of a string. The heap-plus-queue simulation still works if you let the clock tick on an empty heap. Its counting formula, `max(len, (f - 1) * k + m)` in this chapter's distance-`k` terms, skips the simulation.
- **Reorganize String (LeetCode 767).** The special case `k = 2`. The bench shrinks to a single "previous letter" variable, which is why it can be written without a deque.
- **Return the lexicographically smallest valid answer.** Greedy by count no longer picks the right letter. You need a feasibility check (the `(f - 1) * k + m <= n` style bound on the remaining multiset) and you try letters in alphabetical order, keeping the first one whose placement leaves a feasible remainder.
- **Different cooldown per letter.** The FIFO bench breaks, because letters no longer come off rest in the order they went on. Replace it with a min-heap keyed by "slot when rested", the same pattern as the server-scheduling problems later in this chapter.

## What to carry forward

Two containers split the letters by state: a max-heap for "ready, most urgent first" and a FIFO queue for "resting, released in arrival order after exactly `k` ticks". Greedy picks the top of the ready heap, and the queue's length is the clock.

The next problem, Merge k Sorted Lists, uses the heap in a new way: instead of holding counts that change, it holds one current element from each of `k` sorted feeds and keeps refilling from the feed it just took from.
