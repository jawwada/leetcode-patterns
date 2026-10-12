# Permutation in String

*LeetCode 567 · Medium · Pattern: Fixed-size sliding window with counts · Reading time ~8 min*

## The problem

Return True if some permutation of s1 appears as a contiguous substring of s2.

```text
Example: s1 = "ab", s2 = "eidbaooo" -> True ("ba"); s1 = "ab",
  s2 = "eidboaoo" -> False.
```

## What the problem is really asking

You get a short string `s1` and a longer string `s2`. The question is whether some rearrangement of `s1` appears in `s2` as one unbroken stretch of letters. "Rearrangement" is the important word. We do not care about the order of the letters inside the stretch, only about which letters are there and how many of each.

So the answer is a yes/no, and the object we test is a substring of `s2` whose length is exactly `len(s1)`. Any longer stretch has extra letters and any shorter one is missing some, so only one width is ever worth checking. That makes this a different kind of window from the last six problems: the width is fixed in advance, and only its position changes.

```text
s1 = "ab"            s2 = "e i d b a o o o"
                           0 1 2 3 4 5 6 7
                                 [---]
                                 b a   <- "ba" is a
                                          rearrangement of "ab"
answer: True
```

What makes it hard is that the number of rearrangements of `s1` explodes (`k!` for `k` letters), so generating them is hopeless. The trick is to stop thinking about orderings at all.

## Do it by hand first

Take `s1 = "ab"`, `s2 = "eidbaooo"`. With a pencil you would not write out "ab" and "ba" and search for each. You would make a little tally of what `s1` contains, then slide your finger two letters at a time along `s2` and tally what is under your finger.

```text
s1 tally:   a:1  b:1

finger at 0..1  "ei"   e:1 i:1        no
finger at 1..2  "id"   i:1 d:1        no
finger at 2..3  "db"   d:1 b:1        no
finger at 3..4  "ba"   b:1 a:1        same tally -> yes
```

The thing your hand kept track of is a **tally of letters under the finger**, compared against a fixed target tally. Notice also what your eyes did when the finger moved: they did not re-read both letters. One letter fell off the left, one came in on the right, and you nudged the tally by one in each direction. That nudge is the whole algorithm.

## The first honest attempt

The brute force a strong candidate says out loud: for every start `i` in `s2`, slice `s2[i:i+k]`, sort it, and compare it to `sorted(s1)`. There are `n - k + 1` starts, each costs `O(k log k)` to sort, so the total is `O(n · k log k)`. Counting letters from scratch instead of sorting brings each check to `O(k)`, which is still `O(n · k)`.

Where is the waste? Two neighbouring windows share `k - 1` letters. The brute force throws all that work away and starts over.

```text
s2:      e  i  d  b  a  o  o  o
start 2:       [d  b]              count d, b
start 3:          [b  a]           count b, a   <- b again
start 4:             [a  o]        count a, o   <- a again

with k = 5, each window re-counts 4 letters
it already counted one step ago
```

With `k` around 10^4 and `n` around 10^4 that is 10^8 letter visits, nearly all of them repeats.

## The turning point

**Claim: "some permutation of `s1` is here" is the same as "the letter histogram of this window equals the letter histogram of `s1`", and sliding the window changes the histogram in exactly two cells.**

The first half is a definition in disguise. Two strings are rearrangements of each other exactly when every letter appears the same number of times in both. Order is gone, and what remains is a list of 26 counts. Equality of two such lists is a check of 26 integers, which is a constant no matter how long `s1` is.

The second half is what makes the window slide cheaply. When the window moves one step right, letter `s2[i]` enters and letter `s2[i - k]` leaves. Every other letter stays. So the new histogram is the old one with one cell incremented and one cell decremented.

```text
window [2..3] "db"  ->  window [3..4] "ba"

  have:  b:1 d:1          enter a: a+1
                          leave d: d-1
  have:  a:1 b:1          (2 cells touched, 24 untouched)
```

So we keep two arrays of 26 counts. `need` is built once from `s1` and never changes. `have` describes the current window. For each index `i` in `s2`, add the entering letter; once `i >= k`, subtract the letter at `i - k`, which has just fallen off the left; then compare `have` to `need`. The window is always the `k` letters ending at `i` (or fewer, during the first `k - 1` steps while it fills up).

Compared with problems 2 to 6, the left edge here has no decision to make. It does not wait for a condition to break and then chase it. It is chained to the right edge at distance `k`. That rigidity is what lets us drop the "while invalid, shrink" loop entirely.

## Watch it work

`s1 = "ab"`, `k = 2`, `need = {a:1, b:1}`, `s2 = "eidbaooo"`. The table shows only non-zero cells of `have`.

Frame 1: the window is still filling.

```text
i = 1     e  i  d  b  a  o  o  o
         [e  i]
         L  R
have: e:1 i:1        need: a:1 b:1     equal? no
```

Nothing has left yet because `i < k`; two letters have entered.

Frame 2: first true slide.

```text
i = 2     e  i  d  b  a  o  o  o
            [i  d]
            L  R
enter d (+1), leave s2[0] = e (-1)
have: i:1 d:1                          equal? no
```

The letter at `i - k = 0` left the tally; the window kept width 2.

Frame 3: half a match.

```text
i = 3     e  i  d  b  a  o  o  o
               [d  b]
               L  R
enter b, leave i
have: d:1 b:1                          equal? no
```

`b` matches its target, `d` is a stranger, so the arrays differ.

Frame 4: match.

```text
i = 4     e  i  d  b  a  o  o  o
                  [b  a]
                  L  R
enter a, leave d
have: a:1 b:1        need: a:1 b:1     equal? YES
```

The stranger `d` left at the same moment `a` arrived, and the two histograms line up, so the function returns `True` at `i = 4`.

Across all frames the window held exactly the `min(i + 1, k)` letters ending at `i`, and `have` was always that window's histogram. Each step did two array updates and one 26-cell comparison, never a re-count.

## Why it is correct

The invariant is: after processing index `i`, `have[c]` equals the number of times letter `c` appears in `s2[max(0, i-k+1) .. i]`. It holds at the start (empty window, all zeros). If it holds after `i - 1`, then adding `s2[i]` and, when `i >= k`, removing `s2[i - k]` turns the histogram of `s2[i-k .. i-1]` into the histogram of `s2[i-k+1 .. i]`, so it holds after `i`.

Every length-`k` substring of `s2` is the window at exactly one index `i` (its last index), so every candidate is compared once. A substring is a permutation of `s1` exactly when its histogram equals `need`. Therefore we return `True` if and only if some candidate is a permutation. During the first `k - 1` steps the window is shorter than `k`, so its total count is less than `len(s1)` and it cannot accidentally equal `need`.

If `k > len(s2)` there is no candidate at all, and the code returns `False` up front.

## Cost

- Time `O(26 · n)` = `O(n)`: one pass over `s2`, two updates and a 26-cell comparison per step, plus `O(k)` to build `need`.
- Space `O(1)`: two arrays of 26 integers regardless of input size.

The brute force with sorting is `O(n · k log k)`; with fresh counting it is `O(n · k)`.

## Variations you will meet

- **Find All Anagrams in a String (LeetCode 438).** Same window, but instead of returning on the first match, append `i - k + 1` to a list every time the arrays are equal. Nothing else changes.
- **Large or unknown alphabet.** Comparing two full histograms is no longer `O(1)`. Keep a single integer `matches`, the number of letters whose `have` equals `need`. Each slide touches two letters, so `matches` changes by at most two per step, and the window is a hit when `matches` equals the number of distinct letters. This is the bookkeeping trick that the next problems and Minimum Window Substring rely on.
- **Valid Anagram.** The degenerate case where the window is the whole string: build two histograms once and compare.
- **Words instead of letters.** If the "letters" are fixed-length words, the histogram becomes a `Counter` of words, and the window steps by a whole word. That is the next problem.

## What to carry forward

When the order inside a window does not matter, replace the window with its histogram; a fixed-width slide touches one cell going in and one coming out. The next problem keeps this histogram-equality window but makes each "letter" a whole word, which forces us to choose where the word grid starts.
