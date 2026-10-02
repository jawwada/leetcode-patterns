# Substring with Concatenation of All Words

*LeetCode 30 · Hard · Pattern: Fixed-size sliding window with counts · Reading time ~12 min*

## What the problem is really asking

You get a string `s` and a list `words`. Every word has the same length `L`, and the list may contain duplicates. Find every index where `s` contains all the words glued together, in any order, each used exactly as many times as it appears in the list, with nothing in between.

Strip away the wording and this is the previous problem one level up. In Permutation in String the alphabet was letters and the window was `len(s1)` letters wide. Here the alphabet is *words*, and a valid window is exactly `m = len(words)` words wide, which is `m · L` characters. "Any order" again means we compare multisets, not sequences.

The answer is a list of start indices. Let us use a running example with a duplicate-free list but a repeated word in `s`, because the repeat is what exercises the interesting part of the algorithm.

```text
words = ["bar", "foo", "the"]     L = 3, m = 3, width = 9

s:  bar foo foo bar the foo bar man
    0   3   6   9   12  15  18  21

            [foo bar the]          start 6
                [bar the foo]      start 9
                    [the foo bar]  start 12

answer: [6, 9, 12]
```

What makes it hard: unlike letters, words do not come pre-separated. Nothing in `s` says where one word ends. A window starting at index 1 would read `arf oof oob ...`, a completely different chopping of the same characters. So before we can count anything we have to decide where the chunk boundaries are.

## Do it by hand first

Take the example above. With a pencil, you would probably not try index 1 or index 2 for long. You would notice that the valid answers start at multiples of 3 here, and that once you start reading at 0 every chunk after it also falls on a multiple of 3. So you would draw tick marks every 3 characters and read the string as a row of tiles.

```text
tiles at offset 0:
| bar | foo | foo | bar | the | foo | bar | man |
   0     1     2     3     4     5     6     7    tile no.
```

Then you would run your finger along the tiles keeping a little tally: "I have one bar, one foo... another foo, that is too many foos, drop tiles from the left until there is only one foo... bar, the, now I have one of each, write down the start." When you hit `man`, which is not a word at all, you would lift your finger and start fresh after it.

Two things were kept track of. First, **which grid of tick marks you were reading on**. Second, **a tally of tiles under your finger** compared to the tally of `words`. The second is exactly the histogram from problem 7. The first is new.

## The first honest attempt

The direct approach: for every start `i` from `0` to `n - m·L`, slice the `m` chunks `s[i : i+L]`, `s[i+L : i+2L]`, and so on, count them in a `Counter`, and compare with `Counter(words)`. That is `n` starts times `m` chunks times `O(L)` per slice, so `O(n · m · L)`.

The waste is the same shape as before, only coarser. Start `i` and start `i + L` read the *same* chunks except for one at each end.

```text
start 0:  [bar foo foo]                count 3 chunks
start 3:      [foo foo bar]            count 3 chunks
start 6:          [foo bar the]        count 3 chunks

each window shares m-1 = 2 tiles with the one
L characters before it, yet recounts all m
```

And start `i + 1` shares nothing useful with start `i`: the tiles are cut in different places. So the starts are not one sequence of overlapping windows. They are `L` separate sequences tangled together.

## The turning point

**Claim: starts that differ by a multiple of `L` see the same tile boundaries, so split the starts into `L` groups by `start mod L`; inside one group the problem is a counting sliding window over a sequence of whole tiles.**

Justify the first half by drawing all three grids for `L = 3`.

```text
s:        b a r f o o f o o b a r t h e ...
index:    0 1 2 3 4 5 6 7 8 9 ...

offset 0: |bar|foo|foo|bar|the|...
offset 1:   |arf|oof|oob|art|...
offset 2:     |rfo|ofo|oba|rth|...
```

Every start index lies on exactly one of these grids, namely grid `start mod L`. Any valid window starting at `i` is a run of `m` consecutive tiles on grid `i mod L`. So we can handle each grid alone, and there are only `L` of them.

On one grid, the string is just a list of tiles, and the question is: which runs of exactly `m` consecutive tiles have the same multiset as `words`? That is Permutation in String with tiles for letters. We could slide a rigid window of width `m` tiles and compare `Counter`s, but comparing two `Counter`s costs `O(m)`. The solution instead slides a **variable** window with three rules that each come from a fact about valid windows:

1. **A tile that is not a word is a wall.** No valid window can contain it, so throw away the whole window and restart just after the wall.
2. **An over-counted word pushes the left edge.** If adding tile `w` makes `have[w] > need[w]`, then every window that contains both this new `w` and the current left edge has too many `w`s. Drop tiles from the left until `have[w]` is back in budget. This is the "while invalid, shrink" loop from problems 3 to 6.
3. **A full window is a hit.** If no word is over budget and the window holds `m` tiles, then the window holds exactly `need[w]` of every `w` (the counts are each at most `need[w]` and they add up to `m`, the sum of all `need[w]`). Record `left`, then drop one tile from the left so the window can keep moving.

Rule 3 is where the `O(m)` comparison disappears. "No word over budget" is maintained by rule 2, and "count equals `m`" is one integer check. Together they prove equality without ever comparing two counters.

The state per grid is small: `left`, a `Counter` called `have`, and an integer `count` of tiles in the window.

## Watch it work

Grid offset 0 on `s = "barfoofoobarthefoobarman"`, `need = {bar:1, foo:1, the:1}`, `m = 3`. The arrow `R` marks the tile just added, `L` the left edge after the step.

Frame 1: the first tile enters.

```text
| bar | foo | foo | bar | the | foo | bar | man |
  0     3     6     9     12    15    18    21
 [bar]
  L,R           have: bar:1           count 1
```

`bar` is a word and within budget, so the window just grows.

Frame 2: a second distinct word.

```text
| bar | foo | foo | bar | the | foo | bar | man |
 [bar   foo]
  L     R       have: bar:1 foo:1     count 2
```

Still within budget everywhere, so the window keeps growing.

Frame 3: a duplicate forces the left edge.

```text
| bar | foo | foo | bar | the | foo | bar | man |
              [foo]
               L,R
add foo -> foo:2 > 1
drop bar (L=3), still foo:2; drop foo (L=6)
                have: foo:1           count 1
```

Rule 2 dropped tiles until the newest `foo` was the only `foo` left.

Frame 4: growing again.

```text
| bar | foo | foo | bar | the | foo | bar | man |
              [foo   bar]
               L     R    have: foo:1 bar:1   count 2
```

No word is over budget and the window is not yet full.

Frame 5: first hit.

```text
| bar | foo | foo | bar | the | foo | bar | man |
              [foo   bar   the]
               L           R      count 3 = m
record 6; drop foo -> L = 9, count 2
```

Count reached `m` with nothing over budget, so start 6 is recorded and the window gives up its leftmost tile.

Frame 6: every following tile completes a new hit.

```text
| bar | foo | foo | bar | the | foo | bar | man |
                    [bar   the   foo]   record 9,  L = 12
                          [the   foo   bar]
                                       record 12, L = 15
```

Adding `foo` at 15 makes the window full again (start 9 recorded); adding `bar` at 18 does the same (start 12 recorded).

Frame 7: a wall.

```text
| bar | foo | foo | bar | the | foo | bar | man |
                                            ^ R
`man` is not a word: clear have, count 0, L = 24
```

No valid window can contain `man`, so everything to its left is forgotten.

Frame 8: the other two grids.

```text
offset 1: |arf|oof|oob|art|hef|oob|arm|   all walls
offset 2: |rfo|ofo|oba|rth|efo|oba|rma|   all walls
```

Every tile on these grids is a wall, so they contribute nothing and the final answer is `[6, 9, 12]`.

Across the frames, `have` always counted exactly the tiles between `L` and `R`, no word ever stayed over budget after a step, and the window never contained a non-word tile.

## Why it is correct

Fix one grid. The invariant after each step is: the window `[left, right + L)` contains only word tiles, `have` is its tile histogram, `count` is its number of tiles, and `have[w] <= need[w]` for every word `w`.

Now argue that no valid start is skipped. A valid window on this grid is a run of `m` word tiles with `have = need`. Suppose it starts at tile `a` and ends at tile `b`. When the scan adds tile `b`, the left edge is at or before `a`: the left edge only moves past a tile when it is a wall (not possible, all tiles from `a` to `b` are words), when that tile must go to fix an over-count (but inside `[a, b]` nothing is over budget, so an over-count caused by a tile up to `b` can always be fixed by dropping tiles before `a`, and the loop stops as soon as it is fixed), or right after recording a full window (which would be a window of `m` tiles ending before `b`, starting before `a`). So when `b` is added, left is at most `a`; and since the window cannot hold more than `m` tiles without some word being over budget, after rule 2 the left edge is exactly `a` and the count is `m`. Rule 3 then records `a`.

Conversely, anything recorded has `count = m` and no word over budget, which forces `have = need` as argued in the turning point. Doing this on all `L` grids covers every possible start.

## Cost

- Time `O(n · L)`: each grid has about `n / L` tiles, every tile is added once and removed at most once, and each add or remove slices and hashes an `L`-character string, so `L` grids × `n/L` tiles × `O(L)` = `O(n · L)`. Notice that `m` has disappeared.
- Space `O(m · L)`: the `need` and `have` counters hold at most `m` distinct words of length `L`.

The brute force is `O(n · m · L)`, so the speed-up is a factor of `m`, the number of words.

## Variations you will meet

- **Permutation in String.** The special case `L = 1`: one grid, and every tile is a letter. Seeing it this way confirms that the grid split is the only new idea.
- **Find All Anagrams in a String.** Same as the variation from problem 7: letters, one grid, record every hit instead of returning early.
- **Words of different lengths.** The grid idea collapses because there is no single tile width. The problem becomes a parsing question (which ways can this stretch be split into words?), and the usual tools are a trie plus dynamic programming, not a sliding window.
- **Return the windows themselves, or count them.** Nothing changes in the scan; only what you do at rule 3 changes.

## What to carry forward

When the units of a string have a fixed width, the only freedom is where the grid starts: run one window per grid offset, and use "nothing over budget and the count is full" instead of comparing whole histograms. The next problem keeps the over-budget bookkeeping but drops the fixed width: the window must *cover* a target with surplus allowed, and we want the shortest such window.
