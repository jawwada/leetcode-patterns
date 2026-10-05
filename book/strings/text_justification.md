# Text Justification

*LeetCode 68 · Hard · Pattern: Greedy line packing · Reading time ~9 min*

## The problem

Pack words greedily into lines of exactly maxWidth characters. Fully justify each line with extra spaces spread as
evenly as possible (leftover spaces go to the leftmost gaps); the last line, and any line with a single word, is
left-justified and padded.

```text
Example: words =
  ["This","is","an","example","of","text","justification."],
  maxWidth = 16 -> ["This    is    an", "example  of text",
  "justification.  "].
```

## What the problem is really asking

You are given a list of words and a line width `maxWidth`. Lay the words out the way a newspaper column does: every output line is exactly `maxWidth` characters long. Put as many words on each line as fit (greedily, line by line). Then stretch each line to full width by inserting spaces between words, spreading them as evenly as possible; when they cannot be spread evenly, the gaps on the left get one more space than the gaps on the right. Two exceptions: the last line, and any line holding a single word, are left-justified, meaning one space between words and the remaining spaces padded at the end.

The answer is a list of strings, all exactly `maxWidth` long. Nothing here is asymptotically difficult. The difficulty is that the problem has three distinct rules (packing, distributing, and the two exceptions) and each has an off-by-one waiting for you.

```text
 words = This is an example of text justification.
 maxWidth = 16

 |This    is    an|   full: 8 spaces into 2 gaps (4,4)
 |example  of text|   full: 3 spaces into 2 gaps (2,1)
 |justification.  |   last line: left + pad
  ^--------------^
       16 cols
```

## Do it by hand first

Take a ruler of length 16 and the word cards `This(4) is(2) an(2) example(7) of(2) text(4) justification.(14)`.

First line: put down `This`. Width used 4. Can `is` fit? You need one space before it, so 4 + 1 + 2 = 7, yes. `an`: 7 + 1 + 2 = 10, yes. `example`: 10 + 1 + 7 = 18, more than 16, no. The line is `This is an`.

Now stretch it. The letters take 4 + 2 + 2 = 8 columns, so 16 - 8 = 8 columns must be spaces. There are 2 gaps between 3 words. 8 / 2 = 4 each, nothing left over. `This____is____an`.

Second line: `example` (7), `of` (7 + 1 + 2 = 10), `text` (10 + 1 + 4 = 15), `justification.` (15 + 1 + 14 = 30) does not fit. Letters 7 + 2 + 4 = 13, spaces 3, gaps 2. 3 / 2 = 1 remainder 1, so the first gap gets 2 and the second gets 1: `example__of_text`.

Third line: `justification.` alone, and it is also the last line. Left-justify: the word, then 2 trailing spaces.

What did your hand track? Two things that never interfered with each other: a running width while deciding where the line breaks, and, once the line was fixed, a single division of spare spaces by gaps.

## The first honest attempt

Packing is usually done right on the first attempt. Space distribution is where people simulate. The common first version: start each gap at one space; while the line is shorter than `maxWidth`, add one more space to the next gap, cycling from the left; after each addition rebuild the line string and measure it.

```text
 line: example of text   maxWidth 16
 gaps [1,1] -> "example of text"   len 15  < 16
 gaps [2,1] -> "example  of text"  len 16  stop

 line: This is an
 gaps [1,1] len 10 -> [2,1] len 11 -> [2,2] len 12
      -> [3,2] 13 -> [3,3] 14 -> [4,3] 15 -> [4,4] 16
        ^ each step rebuilds and re-measures the line
```

It is correct, because cycling from the left is exactly "leftmost gaps get the extra". But each added space costs a full rebuild of the line, which is `O(maxWidth)`, and there can be `O(maxWidth)` added spaces per line, so a line costs `O(maxWidth^2)`. The repeated work: we re-measure an entire line to answer a question whose answer is pure arithmetic and known before we start: how many spaces in total, and how many gaps.

## The turning point

**Claim: with `spaces` spare columns and `gaps` gaps, gap `k` (counting from 0 on the left) gets `spaces // gaps` spaces, plus one more if `k < spaces % gaps`.**

Why? "As even as possible" means no two gaps differ by more than one; otherwise moving a space from the bigger to the smaller would make it more even. So every gap gets either `q` or `q + 1` for some `q`. If `r` gaps get `q + 1` then `gaps * q + r = spaces` with `0 <= r < gaps`, and that is exactly the definition of `divmod(spaces, gaps)`. "Extras go to the left" says which `r` gaps get them: the first `r`. One division replaces the whole simulation.

```text
 spaces = 3, gaps = 2:   q, r = divmod(3, 2) = 1, 1
   gap 0: q + (0 < 1) = 2
   gap 1: q + (1 < 1) = 1

 spaces = 11, gaps = 4:  q, r = 2, 3
   gaps -> 3 3 3 2
```

The packing half is a greedy two-index scan, and the problem statement itself demands greedy packing, so there is nothing to optimise there beyond doing it in one pass. Let `i` be the first word of the line and `j` the last word placed so far, with `width` the length of `words[i..j]` joined by single spaces. Extend `j` while `width + 1 + len(words[j+1]) <= maxWidth`. The `+ 1` is the minimum space that must precede the next word; forgetting it is the classic packing bug.

```text
 i=0                       width
 This                        4
 This_is                     7   (4 + 1 + 2)
 This_is_an                 10   (7 + 1 + 2)
 This_is_an_example         18   > 16, stop; j stays at "an"
```

Then decide which rule formats the line. Let `gaps = j - i`. If `gaps == 0` (one word) or `j` is the last word index (last line), join with single spaces and pad on the right to `maxWidth`. Otherwise compute `spaces = maxWidth - (sum of word lengths)` and apply the divmod. Note that the single-word case must be handled before the division, both because its rule is different and because dividing by zero gaps would crash. Then set `i = j + 1` and continue.

The two halves are independent: packing never looks at how spaces will be distributed, and distribution never changes which words are on the line. That separation is what makes the problem tractable.

## Watch it work

`words = ["This","is","an","example","of","text","justification."]`, `maxWidth = 16`. State: `i`, `j`, running `width`, and the formatted line.

Frame 1. Pack line 1 from `i = 0`.

```text
 i=0  j: This(4) -> is(7) -> an(10) | example would be 18
 line = [This, is, an]   j=2   gaps=2
```

`example` was rejected by the `+1` test, so line 1 ends at index 2.

Frame 2. Format line 1: not last, more than one word.

```text
 letters = 4+2+2 = 8   spaces = 16-8 = 8
 q, r = divmod(8, 2) = 4, 0
 "This" + 4sp + "is" + 4sp + "an"
 |This    is    an|
```

No remainder, so the gaps are equal.

Frame 3. Pack line 2 from `i = 3`.

```text
 i=3  j: example(7) -> of(10) -> text(15)
      justification. would be 15+1+14 = 30 > 16
 line = [example, of, text]   j=5   gaps=2
```

Frame 4. Format line 2 with a remainder.

```text
 letters = 7+2+4 = 13   spaces = 3
 q, r = divmod(3, 2) = 1, 1
 gap0 = 1+1 = 2   gap1 = 1+0 = 1
 |example  of text|
```

The single extra space went to the leftmost gap.

Frame 5. Pack and format line 3 from `i = 6`.

```text
 i=6  j=6 (last word)   gaps=0, and j is last
 left-justify: "justification." + 2 spaces
 |justification.  |
 i = 7 = len(words) -> done
```

Both exception rules applied here; either one alone would have chosen left-justify.

Through every frame, `width` was the true length of `words[i..j]` with single spaces and never exceeded 16, and every line produced was exactly 16 characters.

## Why it is correct

Packing: the statement defines the layout as greedy, so the only obligation is to implement greedy exactly. The loop invariant is `width == len(" ".join(words[i..j])) <= maxWidth`. It holds when `j = i` (a single word is guaranteed to fit, since every word is at most `maxWidth`), and each extension adds exactly `1 + len(next)` only when the result stays within bounds. When the loop stops, either there are no more words or the next word cannot fit even with a single space, which is the greedy stopping rule.

Distribution: by the argument in the turning point, "as even as possible with extras on the left" has exactly one solution, and divmod computes it. The gap sizes sum to `q * gaps + r = spaces`, so the line length is letters plus spaces, which is `maxWidth`.

Exceptions: the left-justified line has `len(text) <= maxWidth` by the packing invariant, and padding with `maxWidth - len(text)` spaces makes it exactly `maxWidth`.

Every word is placed on exactly one line because `i` jumps to `j + 1` each time.

## Cost

- Time `O(total characters)`: each word is examined once for packing and copied once into output, and each output character (letters and spaces) is written once. Equivalently, `O(lines * maxWidth)`.
- Space `O(maxWidth)` extra for building one line, plus the output itself.

The simulation version was `O(lines * maxWidth^2)`.

## Variations you will meet

- **Minimum raggedness / pretty printing.** If the cost of a line is, say, the square of its trailing spaces and you minimise the total, greedy is no longer optimal; you need dynamic programming over "where does the next line start". Greedy is right here only because the problem mandates it.
- **Center justification.** Same packing; split the slack into left and right padding with `divmod(slack, 2)`, deciding which side gets the extra.
- **Extras on the right instead of the left.** Change the test to `k >= gaps - r`. The divmod is the same.
- **Words longer than `maxWidth`.** The problem rules it out. If allowed, you must decide to split or overflow; the packing loop's base case (one word always fits) no longer holds.

## What to carry forward

Split a fiddly formatting problem into independent decisions, here "which words" (greedy scan) and "how many spaces" (one divmod), and each becomes simple. The next problem leaves parsing behind and asks a structural question about a string: its longest palindromic piece, found by growing outward from every possible middle.
