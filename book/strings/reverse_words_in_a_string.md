# Reverse Words in a String
*LeetCode 151 · Medium · Pattern: In-place reverse, then reverse each word · Reading time ~8 min*

## What the problem is really asking

You get a sentence in which words are separated by one or more spaces, possibly with spaces at the front and back. Return the words in reverse order, joined by exactly one space, with nothing at either end. The answer is a new string. The words themselves keep their spelling. Only their order flips, and the spacing is normalised.

```text
 input:   _ _ h i _ _ y o u _ o k _        (_ = space)
 words:       [hi]    [you]  [ok]
 output:  o k _ y o u _ h i
          [ok] [you] [hi]
```

In Python this is a one-liner. The real question is the follow-up: "Your language has mutable strings. Do it in place with O(1) extra memory." That rules out a list of words, and the problem becomes one about moving characters around inside a single array.

## Do it by hand first

Write `"  hi  you ok "` on squared paper, one character per square. To reverse the words by hand you would probably cross out the extra spaces first. Then you would copy the last word to the front, the middle word next, and so on. With only one row of squares and no scratch paper, that copying is painful, because moving "ok" to the front overwrites "hi".

There is a trick you may notice by accident. Read the cleaned sentence `hi you ok` backwards, letter by letter: `ko uoy ih`. The words are now in the right order. Each one is just spelled backwards.

```text
 cleaned:          h i _ y o u _ o k
 read backwards:   k o _ u o y _ i h
                   [ok] [you] [hi]   <- order right,
                                        letters mirrored
```

Your hand kept track of **word boundaries**, meaning where each run of letters starts and ends, and it used **two ends moving toward each other** to read backwards.

## The first honest attempt

`" ".join(reversed(s.split()))`. `split()` with no argument drops all the empty pieces, `reversed` flips the word list, and `join` puts single spaces between the words. It runs in O(n) time and O(n) space and is genuinely optimal in Python. Say it first.

The waste the interviewer wants you to see is the allocation. The method builds a list of k word objects, each a fresh copy, then a reversed iterator, and then a third copy in the joined output. In C, Java with a `char[]`, or Go with a `[]byte`, the follow-up wants zero extra arrays.

```text
 original buffer:   [_ _ h i _ _ y o u _ o k _]
 word list copy:    ["hi"] ["you"] ["ok"]       <- extra
 output copy:       [o k _ y o u _ h i]         <- extra
```

## The turning point

**Reversing the whole array and then reversing each word restores every spelling while keeping the reversed order.**

Why it works: reversal is its own inverse, and it composes. Reversing the whole sentence does two things at once. It moves word *k* from the front to the back, which is what we want, and it mirrors every word's letters, which we do not want. Reversing each word in place undoes the second effect without touching the first, because a word's position does not change when you reverse its letters inside the same span.

```text
 A B C           (words)
 reverse all ->  C' B' A'    (' = spelled backwards)
 reverse each -> C  B  A
```

Each reversal is the classic converging two-pointer swap: `L` at the left end, `R` at the right, swap and step inward until they meet.

Spaces need one more pass before any of this, and it is also two-pointer: **read/write compaction**. A read pointer `r` visits every character. A write pointer `w` (always `w ≤ r`) writes a character only if it is a letter, or if it is a space and the last written character was not a space. A leading space is never written because `w == 0`. At the end, if the last written character is a space, drop it. This leaves words separated by exactly one space, so in the word-reversal pass a single space is a reliable boundary.

The three passes are compact, reverse all, then reverse each word. The extra memory is the array itself plus a few integers.

## Watch it work

`s = "  hi  you ok "`, positions 0..12, `_` = space.

**Frame 1.** Compaction begins. The two leading spaces are skipped because `w == 0`. `h` and `i` are written to slots 0 and 1.
```text
 read:  _ _ h i _ _ y o u _ o k _
            ^ r=2..3
 write: h i
            ^ w=2
```

**Frame 2.** The space at r=4 is written, since the last written character was `i`. The space at r=5 is skipped, since the last written character is now a space.
```text
 read:  _ _ h i _ _ y o u _ o k _
                  ^ r=5
 write: h i _
              ^ w=3
```

**Frame 3.** The rest is copied. The final space is written at r=12 (w=10) and then trimmed, so w=9.
```text
 write: h i _ y o u _ o k
                         ^ w=9  (trailing '_' trimmed)
```

**Frame 4.** Reverse the whole array with L=0 and R=8 converging.
```text
 before: h i _ y o u _ o k
         L->           <-R
 after:  k o _ u o y _ i h
```

**Frame 5.** Walk left to right. At each space, or at the end, reverse the span since the last start.
```text
 k o _ u o y _ i h
 [0,1]  -> o k
 [3,5]  -> y o u
 [7,8]  -> h i
 result: o k _ y o u _ h i   = "ok you hi"
```

In each pass the region left of the pointer was finished and never touched again. During compaction, `chars[0:w]` was always the normalised prefix of what `r` had read so far. Every character was swapped at most twice, once in each reversal pass.

## Why it is correct

**Compaction.** Invariant: `chars[0:w]` equals the input prefix `s[0:r]` with leading spaces removed and every run of spaces collapsed to one. A letter is always appended. A space is appended only when it starts a new run after some letter. Because `w ≤ r`, writing never destroys a character not yet read. Trimming one trailing space then makes it "words joined by single spaces".

**Reversals.** Write the compacted array as `W1 _ W2 _ … _ Wk`. Reversing it gives `rev(Wk) _ … _ rev(W1)`, since the reverse of a concatenation is the concatenation of the reverses in opposite order. The spaces are still single spaces. The second pass finds each maximal non-space run, which is exactly some `rev(Wi)`, and reverses it to `Wi`. The result is `Wk _ … _ W1`.

## Cost

- **Time O(n)**: three linear passes. Each reversal swaps each position at most once.
- **Space**: O(1) extra in a language with mutable strings. In Python, `list(s)` is an O(n) copy we cannot avoid, but there is no extra word list.
- The split/reverse/join one-liner is also O(n) time and O(n) space, with higher constant memory.

## Variations you will meet

- **Reverse Words in a String II (LeetCode 186).** The input is already a `char[]` with single spaces, so skip compaction. The double reversal is the entire solution.
- **Rotate Array (LeetCode 189).** The same composition trick on numbers: rotating right by k is reverse all, reverse the first k, reverse the rest.
- **Reverse Words in a String III (LeetCode 557).** Keep the word order and reverse each word's letters. That is just the second pass.
- **"Do it in one pass."** Scan from the right with an end pointer, find each word's start, and append it to the output. You get O(n) time with an output buffer instead of in-place work, and it is a good contrast to discuss.

## What to carry forward

Reverse the whole, then reverse each part: an outer reversal you keep and inner reversals you undo. Read/write compaction is the in-place way to delete or collapse characters. The next problem keeps two pointers but puts one on each of two strings, walking them in lockstep while parsing numbers out of the text.
