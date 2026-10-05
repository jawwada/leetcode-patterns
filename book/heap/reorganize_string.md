# Reorganize String

*LeetCode 767 · Medium · Pattern: Greedy most-frequent-first with a max-heap · Reading time ~8 min*

## The problem

Rearrange the characters of s so that no two adjacent characters are equal; return any valid arrangement, or an empty
string if impossible.

```text
Example: "aab" -> "aba". Example: "aaab" -> "".
```

## What the problem is really asking

Rearrange the letters of a string so that no two neighbours are equal. Return any arrangement that works, or the empty
string if none exists.

The answer is either a permutation of the input or a verdict of "impossible". So there are really two questions: when is it
possible, and if it is, how do you build one without trying permutations? Compared with Task Scheduler, the cooldown is
now exactly one position and idles are forbidden: there is no "_" to fill a gap with.

```text
s = "aaabbc"   counts a3 b2 c1   length 6

bad:   a a a b b c        a next to a
            ^^^
good:  a b a b a c        no equal neighbours
       0 1 2 3 4 5
```

## Do it by hand first

Try `"aaab"`. You need to separate three a's. Between three a's you need at least two other letters, and you only have one
b. Impossible, and you knew it from counting alone.

Try `"aaabbc"`. Put the a's down first, spaced out, at every other slot: positions 0, 2, 4. Then fill the gaps with the
rest.

```text
slot:    0   1   2   3   4   5
a's:     a   .   a   .   a   .
fill:    a   b   a   b   a   c
```

What your hand tracked was the **most frequent letter**, because it is the one that runs out of room. It can occupy at
most every other slot, which in a string of length n is `(n + 1) // 2` slots. That number is the feasibility test.

A second hand method, one letter at a time: always write the letter with the most copies left, unless you just wrote it, in
which case write the next most frequent one. For `"aaabbc"`: a (a has most), b (a was just used), a, b, a, c. You tracked
remaining counts, and the one letter that is temporarily banned.

## The first honest attempt

Try every permutation and return the first with no equal neighbours. There are n! orderings, and each check costs O(n),
so O(n! * n). For length 12 that is about half a billion permutations.

The repeated work is enormous and easy to see:

```text
"aaabbc" as positions of 6 distinct cards: a1 a2 a3 b1 b2 c
  a1 a2 a3 b1 b2 c      a2 a1 a3 b1 b2 c
  a1 a3 a2 b1 b2 c      a3 a2 a1 b1 b2 c   ... 12 copies of
  the same string "aaabbc", each built to the end and
  rejected, although "aa" at the front already failed
```

Swapping identical letters produces the same string over and over, and a permutation that starts `"aa"` is built all the
way out before being rejected. The constraint only depends on counts and neighbours, so a method that works with counts
should not need to enumerate anything.

## The turning point

**Claim: an arrangement exists exactly when the most frequent letter has at most `(n + 1) // 2` copies, and in that case
the rule "place the most frequent letter other than the one just placed" never gets stuck.**

The first half is the slot argument. The most frequent letter x with m copies needs m - 1 other letters between its copies,
so `m - 1 <= n - m`, which rearranges to `m <= (n + 1) / 2`. Draw the extreme:

```text
n = 5, (n+1)//2 = 3:   x . x . x     fits exactly
n = 4, (n+1)//2 = 2:   x . x .       a 3rd x has no room
"aaab": m = 3 > 2  -> ""
```

The second half is the greedy. Spending the most plentiful letter as early as possible keeps it from piling up at the end,
which is the only way to get stuck. Holding back the letter just written for one step enforces the neighbour rule. The
correctness section proves the greedy never runs out of choices.

To implement it we need, at every step, "the letter with the most copies left, excluding one letter". A max-heap of
`(-count, letter)` gives the most frequent in O(log 26). The exclusion is the trick: do not push the letter you just wrote
back into the heap right away. Hold it in a single variable, a one-slot parking spot, and only push it back after the
**next** letter has been popped. Then it cannot be chosen twice in a row.

```text
       heap (max count on top)      parked
              (-3, a)              [ empty ]
             /       \
        (-2, b)   (-1, c)
each step: pop top -> write it -> push parked back
           (if it still has copies) -> park the one just written
```

This is Task Scheduler's cooldown queue shrunk to one slot. There, an empty heap meant an idle; here it would mean
failure, and the feasibility check guarantees it never happens.

## Watch it work

`s = "aaabbc"`. Counts a3 b2 c1, length 6, `(6 + 1) // 2 = 3`, and the maximum count is 3, so it is feasible. Heap entries
are written as letter and count; the parked letter is shown after the step.

```text
Frame 1: heapify [a3, b2, c1]; pop a3, write a
heap   [b2, c1]          parked  a2
output a
```

Nothing was parked before, so nothing goes back. a, with two copies left, sits out the next step.

```text
Frame 2: pop b2, write b; push parked a2 back; park b1
heap   [a2, c1]          parked  b1
output ab
```

a could not be chosen this step because it was outside the heap. Now it is back and on top.

```text
Frame 3: pop a2, write a; push b1 back; park a1
heap   [b1, c1]          parked  a1
output aba
```

The majority letter is being spent at every second position, exactly the slot picture from the hand method.

```text
Frame 4: pop b1 (ties with c1; "b" < "c"), write b
push a1 back; park b0
heap   [a1, c1]          parked  b0
output abab
```

b and c tie on count; the tuple's second field breaks the tie.

```text
Frame 5: pop a1, write a; b0 has no copies, not pushed
heap   [c1]              parked  a0
output ababa
```

A parked letter with zero copies is simply dropped instead of being pushed back.

```text
Frame 6: pop c1, write c; a0 dropped; heap empty, stop
heap   []                parked  c0
output ababac            length 6 = len(s)  -> done
```

At every frame the parked letter was the one last written, so no letter could appear twice in a row. Every letter with
copies left was in exactly one place, the heap or the parking spot, and the heap was never empty while copies remained.

## Why it is correct

Let r be the number of letters still to place, and call the parked letter h. The greedy keeps this invariant:

- every letter x has `count(x) <= (r + 1) // 2`, and
- the parked letter has `count(h) <= r // 2`.

The second line is the stricter one because h cannot go in the very next slot, so it can only use every other slot after
that. At the start nothing is parked and the first line is the feasibility test.

**The heap is never empty while letters remain.** If it were, all r remaining letters would be copies of h, so
`count(h) = r <= r // 2`, which forces r = 0.

**The invariant survives a step.** Pop y, the letter with the largest count in the heap, and place it, so r drops by one.
For y: `count(y) - 1 <= (r + 1) // 2 - 1 = (r - 1) // 2`, which is the parked-letter bound for the new r. For the old h,
now back in the heap: `count(h) <= r // 2 = ((r - 1) + 1) // 2`, which is the first bound for the new r. For any other
letter x: if x had `(r + 1) / 2` copies with r odd, then y, being at least as frequent, also had that many, and together
they would exceed r letters, which is impossible. So x has at most `r // 2` copies, which again fits the first bound.

So the loop places all n letters, and since the parked letter is never written twice in a row, no two neighbours are
equal. If the feasibility test fails, the slot argument shows no arrangement exists, so returning `""` is correct.

## Cost

- **Heap greedy:** at most 26 distinct letters, so each heap operation is O(log 26) = O(1). n placements give O(n) time,
  plus O(n) for counting. O(26) extra space for the heap, O(n) for the output.
- **Even/odd slot fill:** sort letters by count, write the most frequent into slots 0, 2, 4, ..., then continue with
  the others, wrapping around to slots 1, 3, 5, .... Also O(n), no heap, and a nice second answer in an interview.
- **Permutations:** O(n! * n).

## Variations you will meet

- **Copies at least k apart (Rearrange String k Distance Apart).** The one-slot parking spot becomes a FIFO queue of
  length k: a letter returns to the heap only after k - 1 others have been written. The feasibility test is no longer a
  simple formula, so failure is detected when the heap empties while letters remain.
- **Allow idles, minimise length.** That is Task Scheduler, solved in the previous problem.
- **Longest Happy String (LeetCode 1405).** Three letters, at most two equal in a row, and you want the longest string.
  Same heap of counts, but the ban triggers only after two consecutive copies, and running out of options ends the string
  instead of returning failure.
- **Distant Barcodes (LeetCode 1054).** The same problem with integers; the even/odd slot fill is the cleanest solution.

## What to carry forward

Check that the largest count fits in `(n + 1) // 2` slots, then always write the most frequent letter that was not just
written, holding the last one aside for a single step. The next problem stretches that one-slot hold into a queue of
length k, so each letter must wait out k - 1 others before it can return.
