# Minimum Window Substring

*LeetCode 76 · Hard · Pattern: Variable-size sliding window · Reading time ~11 min*

## What the problem is really asking

Given a string `s` and a target `t`, find the shortest stretch of `s` that contains every character of `t`, counting repeats. If `t = "AABC"`, the stretch needs at least two `A`s, a `B` and a `C`. Extra characters are allowed. Order does not matter. If no stretch works, return the empty string.

So the answer is a substring, and the test it must pass is a **cover** test: for every character `c`, the window holds at least as many `c`s as `t` does. This is the first time in the chapter that the test is "at least" on a whole histogram. Problems 7 and 8 asked for *equality* with a target histogram; problems 3 to 6 asked for "at most" on some budget. Here surplus is fine and only shortage hurts.

```text
s = A D O B E C O D E B A N C       t = "ABC"
    0 1 2 3 4 5 6 7 8 9 10 11 12

                      [B  A  N  C]
                       9 10 11 12
answer: "BANC" (length 4)
```

What makes it hard: the window has no fixed width, the target is a multiset rather than a single number, and the condition we optimise (short) fights the condition we must keep (covering). Growing helps coverage; shrinking helps length.

## Do it by hand first

Read `ADOBECODEBANC` left to right with `t = ABC` in mind. A person would keep a short checklist in the margin: "need A, need B, need C", and tick items off as they appear.

```text
read:  A  D  O  B  E  C
       ^tick A    ^tick B  ^tick C  -> all ticked at index 5
window so far: ADOBEC (6)

can I drop letters from the front and still have all three?
  drop A -> lose the only A. No.
```

Then you keep reading. At index 10 you see another `A`, and now the old front is wasteful: `ADOBE` before the `C` can all go, because `B` and `A` reappear later. You chop the front back to `CODEBA`. At index 12 another `C` arrives, and you can chop all the way to `BANC`.

What did your hand keep track of? Two things: a **per-letter balance** ("still need one more C", or "I have a spare B") and **one summary number**, how many ticks are still missing. You did not re-scan the window to know whether it covered `t`; you glanced at the summary number.

## The first honest attempt

For each start `i`, walk `j` right while counting letters, stop at the first `j` where the window covers `t`, record it, then move on to `i + 1` and recount. Checking "covers `t`" by comparing two histograms costs `O(alphabet)` per step, so the whole thing is `O(n² · alphabet)`.

The waste is visible if you draw consecutive starts.

```text
s:        A D O B E C O D E B A N C
start 0: [A D O B E C]                 counted 6
start 1:   [D O B E C O D E B A]       recount D..C again
start 2:     [O B E C O D E B A]       recount O..A again

the right end found for start 1 is never to
the left of the one found for start 0
```

That last line is the key fact hiding in the brute force: when the start moves right, the end of the first covering window never moves left. The brute force throws the right end back to `i` every time and walks it forward again.

## The turning point

**Claim: both edges only ever need to move right. If `[left, right]` covers `t`, so does every wider window; if it does not, no window inside it does either.**

This is the monotone property that every variable window in this chapter has needed. Covering is preserved by growing (you only add letters) and destroyed only by shrinking. So for the current `right`, there is a single best `left`: the largest one that still covers. When `right` moves on, that best `left` can only stay or move right, because a window that did not cover before cannot start covering by losing characters on the left.

The algorithm follows: grow `right` one character at a time. As soon as the window covers `t`, shrink `left` as far as it can go while still covering, record the window, then evict one more character to break coverage and resume growing.

The remaining problem is to make "does it cover?" an `O(1)` question. Here is the bookkeeping, which is the margin checklist in code:

- `need[c]` starts as the count of `c` in `t` (and `0` for letters not in `t`). Every time `c` enters the window we decrement it; every time it leaves we increment it. Positive means "still short by this many", zero means "exactly enough", negative means "surplus".
- `missing` starts as `len(t)`. When `c` enters and `need[c]` was positive, the window just filled a real gap, so `missing` drops by one. Surplus entries do not change it.

The window covers `t` exactly when `missing == 0`. And the shrinking loop has an equally cheap stopping rule: the front character can be dropped without losing coverage exactly when `need[s[left]] < 0`, that is, when the window holds a spare copy of it. Letters not in `t` start at zero and go negative as soon as they enter, so they always count as spares. One rule covers both kinds of junk.

```text
need after reading "ADOBEC":
  A:0  B:0  C:0   D:-1  O:-1  E:-1   missing = 0
front is A with need 0 -> not spare -> stop shrinking
```

## Watch it work

`s = "ADOBECODEBANC"`, `t = "ABC"`. Only `need` for A, B, C is shown; every other letter is always at or below zero.

Frame 1: first gaps filled.

```text
A D O B E C O D E B A N C
L     R
need A:0 B:0 C:1      missing 1
```

`A` at 0 and `B` at 3 each filled a gap; `D` and `O` were surplus and left `missing` alone.

Frame 2: first cover.

```text
A D O B E C O D E B A N C
L         R
need A:0 B:0 C:0      missing 0
front A has need 0 -> cannot shrink
record [0,5] "ADOBEC" (6)
evict A -> A:1, missing 1, L = 1
```

The window covered `t` but its front was essential, so it was recorded as is, then broken on purpose.

Frame 3: surplus builds up.

```text
A D O B E C O D E B A N C
  L               R
need A:1 B:-1 C:0     missing 1
```

The second `B` drove `need[B]` to -1, a spare, but `missing` stayed 1 because `A` is still short.

Frame 4: second cover, long shrink.

```text
A D O B E C O D E B A N C
          L         R
D, O, B, E all spare -> dropped; front C is needed
record [5,10] "CODEBA" (6, not shorter)
evict C -> C:1, missing 1, L = 6
```

The `A` at 10 closed the last gap; the left edge skipped four spare letters in one sweep, and dropping `B` at 3 took `need[B]` from -1 back to 0.

Frame 5: one more step with no gain.

```text
A D O B E C O D E B A N C
            L         R
need A:0 B:0 C:1      missing 1
```

`N` is not in `t`; it goes negative and changes nothing that matters.

Frame 6: the best cover.

```text
A D O B E C O D E B A N C
                  L     R
O, D, E spare -> dropped; front B has need 0
record [9,12] "BANC" (4)  <- new best
evict B -> L = 10
```

The new `C` closed the gap, the edge slid past three spares to the `B` at 9, and the four-letter window beat the old best of six. The loop ends and `"BANC"` is returned.

In every frame `need` described exactly the letters between `L` and `R`, `missing` was the total shortfall, and after each recording the left edge sat on a character that was not spare.

## Why it is correct

Two invariants hold after every step. First, `need[c]` equals (count of `c` in `t`) minus (count of `c` in the window), so `missing`, which is the sum of the positive parts of `need`, is zero exactly when the window covers `t`. Each update preserves this: an entering `c` with `need[c] > 0` reduces a positive part by one, and with `need[c] <= 0` it reduces nothing.

Second, for every right end `r`, consider the shortest covering window that ends at `r`, if one exists. Call its start `a(r)`. Because covering is monotone, `a(r)` never decreases as `r` grows. The left pointer never passes `a(r)`: it only steps over spare characters (dropping a spare keeps coverage, so we are still at or before `a(r)`) or over the one essential character right after a recording (and that recording was for an earlier right end, whose best start was at or before `a(r)`). When the window first covers at `r`, the shrink loop stops at the first essential character, which is exactly `a(r)`. So every right end where a cover finishes gets its shortest window considered, and the overall minimum is among them.

## Cost

- Time `O(|s| + |t|)`: building `need` reads `t` once; `right` visits each index of `s` once and `left` moves right at most `|s|` times in total across all shrinks.
- Space `O(alphabet)`: the `need` table holds one integer per distinct character.

The brute force is `O(|s|² · alphabet)`.

## Variations you will meet

- **Permutation in String, seen from here.** That problem is the special case "the window covers `t` and has length exactly `len(t)`". You could solve it with this code by checking the length when you record.
- **Smallest window containing all distinct characters of `s` itself.** Set `t` to the set of distinct letters. The same scan works unchanged.
- **Minimum Window Subsequence (LeetCode 727).** The characters must appear *in order*. Coverage is no longer a histogram, so the counter bookkeeping does not apply; the usual approach scans forward to match `t`, then backward to tighten the start.
- **Longest window that does *not* cover `t`, or covers with at most `k` spares.** You flip which side is valid and the loop becomes the "grow, then shrink while invalid" form of problems 3 to 6.

## What to carry forward

Encode a multiset target as a signed balance per character plus one shortfall counter, and a "covers the target" test becomes `missing == 0`; shrinking stops at the first character that is not a spare. The next problem keeps the variable window and its counts but asks for the number of windows with *exactly* `k` distinct values, a condition that is not monotone, and we will rescue it by subtracting two monotone counts.
