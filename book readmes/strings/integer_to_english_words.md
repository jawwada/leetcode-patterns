# Integer to English Words

*LeetCode 273 · Hard · Pattern: Chunk by thousands + lookup tables · Reading time ~9 min*

## The problem

Convert a non-negative integer below 2^31 to English words.

```text
Example: 1234567 -> "One Million Two Hundred Thirty Four
  Thousand Five Hundred Sixty Seven"; 12345 -> "Twelve Thousand
  Three Hundred Forty Five"; 0 -> "Zero"; 1000010 -> "One
  Million Ten".
```

## What the problem is really asking

Given a non-negative integer below `2^31` (so at most about 2.1 billion), write it out in English words with each word capitalised and single spaces between words. `123` is `"One Hundred Twenty Three"`, `12345` is `"Twelve Thousand Three Hundred Forty Five"`, and `0` is `"Zero"`.

The answer is a string, built from a small fixed vocabulary: the words for 1 to 19, the tens words Twenty to Ninety, "Hundred", and the scale words Thousand, Million, Billion. There is no algorithmic cleverness in the asymptotic sense; the input has at most ten digits. The difficulty is entirely in getting every irregular case right on the first try: zero chunks, teens, missing tens, and no stray spaces. It is labelled Hard because most attempts fail on edge cases, not because it is slow.

```text
 2000317  ->  "Two Million Three Hundred Seventeen"

   2 | 000 | 317
   |    |     |
   |    |     +-- "Three Hundred Seventeen"   (no scale)
   |    +-------- empty chunk: say NOTHING, not "Thousand"
   +------------- "Two" + "Million"
```

## Do it by hand first

Say 2,000,317 out loud. You do not read it digit by digit. You first put in the commas, which splits it into groups of three from the right: `2`, `000`, `317`. Then you read each group the same way ("three hundred seventeen") and attach a scale word that depends only on the group's position: the rightmost group gets nothing, the next gets "thousand", then "million", then "billion". And when a group is all zeros, you say nothing at all for it, scale word included. Nobody says "two million zero thousand three hundred seventeen".

Within a group you also follow fixed rules. If the hundreds digit is non-zero, say it and "hundred". Then look at the last two digits as one number: if it is under 20 it has its own name ("seventeen", "eleven", "five"), otherwise say the tens word and then the ones word if the ones digit is non-zero ("forty", "forty five").

What your hand kept track of: the commas (groups of three) and the position of each group. That is base-1000 positional notation, which is how English actually counts.

```text
 English is base 1000 on the outside, base 10 inside:

 | billions | millions | thousands | units |
 |   ddd    |   ddd    |    ddd    |  ddd  |
     each cell read by the same stencil:
     [ONES[h] Hundred] [TENS[t] ONES[o] | TEEN]
```

## The first honest attempt

A reasonable first idea: precompute the English for every chunk value 0 to 999 in a table, using a triple loop over hundreds, tens, and ones digits. Then peel the number into 3-digit chunks with `% 1000` and `// 1000`, look each chunk up, append the scale word, and join.

That is correct. Its cost is fixed at about 1000 string constructions per call, plus a handful of lookups. The waste is easy to see:

```text
 table[0..999] built every call:
   table[0]   = ""
   table[1]   = "One"
   ...
   table[317] = "Three Hundred Seventeen"   <- used
   ...
   table[999] = "Nine Hundred Ninety Nine"
 input 2000317 reads table[317], table[0], table[2]
 -> 3 of 1000 entries used, 997 spelled for nothing
```

Worse, the triple loop does not avoid the hard part. It still has to know that `t == 1` means a teen word, that `t == 0` means no tens word, and that `o == 0` means no ones word. All the irregularity is still encoded, just inside a loop that runs a thousand times. So precomputing saves nothing and costs a lot. The rules that build the table are themselves the solution; we should apply them directly to the three or four chunks that exist.

## The turning point

**Claim: every number is a sequence of 3-digit chunks, each spelled by one function `chunk(n)` for `0 <= n < 1000`, followed by a scale word that depends only on the chunk's position, and zero chunks contribute nothing.**

This is just a precise statement of what you did by hand, and it holds because English names numbers positionally in base 1000 above the hundreds. Once you believe it, the algorithm is two small pieces.

First, the stencil for one chunk. Use two lookup tables. `ONES` lists the names for 0 to 19, with index 0 being the empty string, because "zero" is never spoken inside a larger number. `TENS` lists the names for the tens digit, with indices 0 and 1 empty, because the tens digit 1 is absorbed into the teens and 0 says nothing.

```text
 chunk(n), 0 <= n < 1000:
   n >= 100 ?  emit ONES[n // 100], "Hundred";  n %= 100
   n >= 20  ?  emit TENS[n // 10];              n %= 10
   n > 0    ?  emit ONES[n]          (1..19, teens included)

 ONES: ["", One, ..., Nine, Ten, Eleven, ..., Nineteen]
 TENS: ["", "", Twenty, Thirty, Forty, ..., Ninety]
```

Notice the order of the checks. After removing the hundreds, the remainder is under 100. If it is 20 or more we emit the tens word and keep only the ones digit, which is then under 10. If it was under 20 we skip the tens step entirely and the remainder, still 1..19, indexes `ONES` directly. That is how "Seventeen" comes out as one word and not "Ten Seven". The emptiness of `ONES[0]` is never used because the last step is guarded by `n > 0`; every word emitted is a real word, so joining by single spaces never produces doubles.

Second, the outer loop. Walk the scales `["", "Thousand", "Million", "Billion"]` in order. At each, the current chunk is `num % 1000`. If it is non-zero, build `chunk(num % 1000)` plus the scale word (if any) and put that in front of what you already have, since you are going from low to high. Then `num //= 1000`. Going low to high means the loop never needs to know in advance how many chunks there are; four iterations always suffice for numbers below `2^31`.

The one case the loop cannot express is zero itself: every chunk is empty, so the output would be the empty string. Handle `num == 0` first by returning `"Zero"`. This is the only place the word Zero appears.

## Watch it work

`num = 2000317`. State: the current scale, `num`, the chunk `num % 1000`, and the word list `out`.

Frame 1. Scale "", the lowest chunk.

```text
 num = 2000317   chunk = 317   scale = ""
 chunk(317): 317>=100 -> "Three","Hundred", n=17
             17<20    -> skip tens
             17>0     -> ONES[17]="Seventeen"
 out = [Three Hundred Seventeen]
 num -> 2000
```

The teen path fired: 17 was looked up whole.

Frame 2. Scale "Thousand".

```text
 num = 2000      chunk = 2000 % 1000 = 0
 chunk is 0 -> emit nothing, no scale word
 out = [Three Hundred Seventeen]   (unchanged)
 num -> 2
```

The empty chunk is skipped entirely; that is how "Zero Thousand" is avoided.

Frame 3. Scale "Million".

```text
 num = 2         chunk = 2
 chunk(2): <100, <20, >0 -> ONES[2]="Two"
 out = [Two Million] + [Three Hundred Seventeen]
 num -> 0
```

The new words were prepended, so the higher-order chunk ends up first.

Frame 4. Scale "Billion", and the join.

```text
 num = 0         chunk = 0  -> nothing
 " ".join(out) =
 "Two Million Three Hundred Seventeen"
```

For a second check, 50868: chunk 868 gives `Eight Hundred` then `TENS[6]="Sixty"` then `ONES[8]="Eight"`; chunk 50 gives `TENS[5]="Fifty"` and the ones digit is 0, so nothing more; result `"Fifty Thousand Eight Hundred Sixty Eight"`.

Across the frames, `out` always held the correct words for the low digits already consumed, and every element of `out` was a non-empty word.

## Why it is correct

Two invariants.

For `chunk(n)`: after the hundreds step, the words emitted spell the hundreds digit and `n` holds the last two digits. After the tens step, either `n` was at least 20 and now holds a single digit with the tens word emitted, or `n` was below 20 and is untouched. The final step names whatever is left, which is a value in `1..19` or nothing. Every one of the 1000 inputs follows exactly one path through these three checks, and each path matches the English rule for that range. You can confirm it exhaustively: the solution file compares against a fully precomputed table on hundreds of inputs.

For the outer loop: after processing scale index `s`, `out` is the correct English for `original % 1000^(s+1)`, and `num` equals `original // 1000^(s+1)`. Prepending the next chunk's words with its scale word extends the correct spelling of the lower part to a correct spelling of a larger part, because English places higher groups before lower ones. A zero chunk leaves `out` unchanged, which is also correct, since a zero group is silent. After four steps `num` is 0 and `out` spells the whole number.

## Cost

- Time `O(log n)`, which here is at most 4 chunks and a constant number of table lookups each, so effectively `O(1)`.
- Space `O(1)` beyond the output: two fixed tables and a word list of at most about 20 words.

The brute force was also constant time in theory, but with a constant of 1000 string builds per call against our dozen lookups.

## Variations you will meet

- **British English with "and".** "One Hundred and Five". Insert "and" in `chunk` when the hundreds digit is present and the remainder is non-zero, and, for the lowest chunk only, when a higher chunk exists and the low chunk is below 100.
- **Larger numbers.** Extend `SCALES` with Trillion, Quadrillion; the loop runs until `num` is 0 instead of a fixed four times.
- **Ordinals ("Twenty First").** Spell normally, then rewrite only the last word through a small table (One to First, Two to Second, Twelve to Twelfth, words ending in "y" to "ieth").
- **The reverse: words to integer.** Parse tokens left to right, keeping a current chunk value and a running total: small words add, "Hundred" multiplies the current chunk, a scale word multiplies the chunk by its power of 1000 and adds it to the total. Same base-1000 picture, run backwards.

## What to carry forward

Spell big things by splitting them into fixed-size cells that are each read by one small stencil, and make empty cells silent rather than special-casing them later. The next problem also lays tokens into fixed-width cells, but the cells are lines of text, and the decision of what goes in each cell is greedy.
