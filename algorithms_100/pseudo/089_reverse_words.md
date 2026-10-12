---
rank: 89
slug: reverse_words
---

Given a string, return its words in reverse order. Words are separated by one or more spaces and the string may start or end with spaces; the result separates the words by single spaces and has none at either end. `"  the sky   is blue "` becomes `"blue is sky the"`.

In Python the library answers in one line, `" ".join(reversed(s.split()))`: `split()` with no argument drops every run of spaces, so trimming and squeezing come for free. That is the answer to give first. The follow-up asks for `O(1)` extra space on a mutable character array (LC 186), and there the trick is two reversals. Reversing the whole array puts the words in the right order but spells each one backwards; reversing each word where it lies then repairs the spelling. Before that, one compaction pass with a read and a write pointer copies the characters forward, keeps only the first space after each word and drops the trailing one, so the words sit at the front separated by single spaces.

Picture the sentence as a strip of tape. Flipping the whole strip end over end carries the last word to the front, but every word now reads mirrored; flipping each word back in place fixes its letters without moving it. The outer flip reverses both the order and the letters, and the inner flips undo the letters alone.

```text
start            "  the sky   is blue "     20 characters
squeeze spaces   "the sky is blue"          length 15
reverse 0..14    "eulb si yks eht"          order flipped, letters backwards
reverse 0..3     "blue si yks eht"
reverse 5..6     "blue is yks eht"
reverse 8..10    "blue is sky eht"
reverse 12..14   "blue is sky the"          every word reads forwards again
```

```pseudo
FUNCTION ReverseWords(s)
    chars ← the characters of s as an array
    length ← SqueezeSpaces(chars)         // the words fill chars[0..length-1]
    Reverse(chars, 0, length - 1)         // order flipped, letters backwards
    start ← 0
    FOR i FROM 0 TO length
        IF i = length OR chars[i] = " "   // a word ends just before i
            Reverse(chars, start, i - 1)  // spell it forwards again
            start ← i + 1
    RETURN chars[0..length - 1] as a string

FUNCTION SqueezeSpaces(chars)
    write ← 0
    FOR read FROM 0 TO len(chars) - 1
        IF chars[read] ≠ " "
            chars[write] ← chars[read]
            write ← write + 1
        ELSE IF write > 0 AND chars[write - 1] ≠ " "
            chars[write] ← " "            // keep one space after a word
            write ← write + 1
    IF write > 0 AND chars[write - 1] = " "
        write ← write - 1                 // drop the trailing space
    RETURN write

FUNCTION Reverse(chars, i, j)
    WHILE i < j
        swap(chars[i], chars[j])
        i ← i + 1
        j ← j - 1
```

Squeezing moves each character once and each of the two reversal passes swaps it at most once, so the time is `O(n)`; on a mutable array the extra space is `O(1)`, while in Python `list(s)` and the final join cost `O(n)` because strings are immutable. The signals are "reverse the order of the words" and in-place rotation: rotating an array right by `k` is the same trick, reversing the whole array and then its first `k` and remaining elements separately. Reversing the letters of each word without moving it (LC 557) is the second pass alone. The classic mistakes are forgetting the last word, which no space follows (the loop runs to `i = length` for exactly that reason), and leaving a trailing space after squeezing, which the full reversal then moves to the front.

*Practice:* LC 151 Reverse Words in a String · LC 186 Reverse Words in a String II · LC 557 Reverse Words in a String III · LC 189 Rotate Array
