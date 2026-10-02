# Partition Labels

*LeetCode 763 · Medium · Pattern: Greedy interval merging by last occurrence · Reading time ~7 min*

## What the problem is really asking

Cut a string into consecutive pieces so that no letter appears in two different pieces, and make as many pieces as
possible. Return the lengths of the pieces in order.

The answer is a list of sizes, which is the same as a set of cut positions. Cutting more is always the goal, so the
question is really "where are you allowed to cut?". A cut between positions `k` and `k + 1` is legal exactly when no letter
appears on both sides of it. What makes it tricky is that one letter far to the right can veto a cut that looks fine
locally.

```text
index:  0 1 2 3 4 5 6 7 8 9
s:      a b a c b c d e d f
        [----------]|[----]|[]
          "abacbc"    "ded"  "f"    -> [6, 3, 1]
```

## Do it by hand first

Read `abacbcdedf` with a finger. You see `a` at 0. Can you cut right after it? Only if `a` never appears again; scanning
ahead, it appears at 2. So the first piece must reach at least 2. Along the way you pass `b` at 1, which appears again at
4, so the piece must reach 4. At 3 you meet `c`, whose last appearance is 5: the piece must reach 5. At 4 and 5 nothing
pushes further. Your finger is now standing on the boundary it was told to reach, and everything inside is accounted for.
Cut. First piece: 6 letters.

```text
s:      a b a c b c | d e d | f
a must reach  -> 2
b must reach  -> 4
c must reach  -> 5      finger at 5 == must-reach -> cut
d must reach  -> 8
e must reach  -> 7      finger at 8 == must-reach -> cut
f must reach  -> 9      finger at 9 -> cut
```

Your hand tracked one number: "this piece must extend at least to here". And for each letter it needed to know one fact,
the position of that letter's last appearance.

## The first honest attempt

Grow the current piece one character at a time. After each extension, take the set of letters in the piece and scan the
rest of the string to see if any of them shows up again. If none does, cut. That is O(n^2) time (each position triggers a
scan of the remaining suffix), O(26) extra space.

The waste is the suffix scan. The same question, "does `a` occur after here?", is answered over and over by reading the
same tail:

```text
s:  a b a c b c d e d f
i=0  piece {a}       scan  b a c b c d e d f
i=1  piece {a,b}     scan    a c b c d e d f
i=2  piece {a,b}     scan      c b c d e d f
                                 ^^^^^^^^^^^ the same tail,
                     rescanned to learn facts that never change
```

"Where does `a` last appear?" has one answer for the whole string. It does not depend on where the piece started or which
other letters are in it.

## The turning point

Claim: a piece that contains position `i` must extend at least to `last[s[i]]`, and a cut right after position `i` is
legal exactly when `i` is at least `last[c]` for every letter `c` seen so far in the current piece.

Justify it. If the piece containing `s[i]` stopped before `last[s[i]]`, that letter would appear in this piece and in a
later one, which is forbidden. Conversely, if every letter seen in the piece has its last occurrence at or before `i`,
none of them appears to the right, so the cut after `i` separates nothing.

Geometrically, each letter owns a bar from its first to its last occurrence. A piece must swallow the whole bar of every
letter it touches. Overlapping bars chain into one block, and cuts go exactly in the gaps where no bar crosses:

```text
index:  0 1 2 3 4 5 6 7 8 9
s:      a b a c b c d e d f
a:      [---]
b:        [-----]
c:            [---]
d:                  [---]
e:                    []
f:                        []
cuts:              ^     ^ ^   (after 5, 8, 9)
```

So the algorithm is: precompute `last` in one pass. Then sweep with `end = max(end, last[s[i]])`; whenever `i == end`, the
sweep has caught up with every bar it has touched, so cut there, record `end - start + 1`, and start the next piece at
`i + 1`. The update must happen before the comparison; otherwise you could cut right after a letter whose bar continues.

This is the reach invariant from the Jump Game problems, run in the other direction: there the frontier said how far you
CAN go, here it says how far you MUST go.

## Watch it work

`s = "abacbcdedf"`.

Frame 1

```text
index:  0 1 2 3 4 5 6 7 8 9
s:      a b a c b c d e d f
last:   a:2  b:4  c:5  d:8  e:7  f:9
start = 0, end = 0, sizes = []
```

The first pass records each letter's final position; later indices overwrite earlier ones.

Frame 2

```text
s:      a b a c b c d e d f
        ^ ^ ^ i = 0, 1, 2
end:    2 4 4               end = 4 after i=2
piece:  [a b a . .]         i < end: no cut
```

`a` pushes the boundary to 2, then `b` pushes it to 4; the second `a` adds nothing.

Frame 3

```text
s:      a b a c b c d e d f
              ^ ^ ^ i = 3, 4, 5
end:          5 5 5
piece:  [a b a c b c]       i = 5 == end -> cut, size 6
start = 6, sizes = [6]
```

`c` extends the boundary to 5, and the sweep reaches it: the first piece closes.

Frame 4

```text
s:      a b a c b c d e d f
                    ^ ^ ^ i = 6, 7, 8
end:                8 8 8
piece:              [d e d] i = 8 == end -> cut, size 3
start = 9, sizes = [6, 3]
```

`d` sets the boundary at 8; `e` (last at 7) lies inside it and does not move it.

Frame 5

```text
s:      a b a c b c d e d f
                          ^ i = 9
end:                      9  i == end -> cut, size 1
sizes = [6, 3, 1]
```

`f` appears once, so its bar is one cell and the piece closes immediately.

In every frame, `end` was the largest `last` value among letters in the current piece, so `[start, end]` was the shortest
stretch that could contain the piece. A cut happened exactly when the sweep caught up with it.

## Why it is correct

**Every cut is legal.** At a cut after `i`, `end == i`, and `end` is the maximum of `last[c]` over every letter in the
current piece. So no letter in this piece appears after `i`. Letters in earlier pieces were already finished before this
piece began (that was true at their own cut). So no letter is split.

**No legal cut is missed (an exchange-style argument).** Suppose some valid partition has a cut after position `k` inside
what greedy treats as one piece `[start, end]` with `start <= k < end`. As the sweep went from `start` to `k`, the value of `end` at step `k` was still greater than `k`
(otherwise greedy would have cut there). So some letter at a position in `[start, k]` has its last occurrence beyond `k`.
That letter appears on both sides of the cut at `k`, so that cut is illegal. Contradiction. Therefore every legal cut is a
cut greedy makes.

Since greedy makes every legal cut and only legal cuts, it produces the maximum number of pieces. Put as an invariant:
after each step, the pieces closed so far are exactly the pieces of the finest legal partition of `s[0..i]` that can be
extended to the whole string.

## Cost

- **Time O(n):** one pass to fill `last`, one sweep; constant work per character.
- **Space O(1):** the map has at most 26 keys (O(alphabet) in general), plus the output list.

The brute force is O(n^2) time from rescanning the suffix at every position.

## Variations you will meet

- **Merge intervals (LeetCode 56).** Exactly the bar picture: if you are handed `[first, last]` intervals directly, sort
  by start and merge overlaps. Partition labels skips the sort because the sweep along the string visits starts in order.
- **Return the pieces, not the sizes.** Record `(start, end)` at each cut and slice the string.
- **Fewest pieces with a different constraint.** If each piece must instead contain at most `k` distinct letters, the
  greedy becomes "extend while legal, cut when forced" (a sliding-window flavour), and the proof flips to a "stays ahead"
  argument.
- **Max chunks to make sorted (LeetCode 769).** The same sweep: track the maximum value seen so far, and cut whenever it
  equals the current index. "Last occurrence" becomes "largest value that must land at or before here".

## What to carry forward

Each letter's last occurrence is a promise the current piece must keep; carry the furthest promise and cut when the sweep
reaches it. The next problem leaves single-direction sweeps behind: each child is constrained by both neighbours, and the
fix is to sweep once in each direction and combine.
