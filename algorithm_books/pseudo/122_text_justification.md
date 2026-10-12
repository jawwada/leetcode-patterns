---
rank: 122
slug: text_justification
---

Given a list of words and a width, lay the words out as lines of exactly `max_width` characters. Each line takes as many words as fit with at least one space between neighbors, and its leftover spaces are spread across the gaps as evenly as possible, the leftmost gaps taking one extra when they do not divide evenly. The last line, and any line that holds a single word, is left-justified instead: single spaces between words, then padding on the right. With width `16`, the words `["This", "is", "an", "example", "of", "text", "justification."]` become `"This    is    an"`, `"example  of text"` and `"justification.  "`.

The problem splits into two independent decisions. Which words go on a line is greedy, and the statement demands it: starting from the first word not yet placed, keep taking the next word while the letters so far, plus one space per gap, plus the new word still fit. The running `width` counts exactly that, so the test is `width + 1 + len(words[j]) ≤ max_width`, where the `1` is the space the new word brings with it. How to spread the spaces is arithmetic, not search. A line with `letters` letters and `gaps` gaps must place `spaces = max_width - letters` blanks, so every gap gets `floor(spaces / gaps)` and the first `spaces mod gaps` gaps get one more. A brute force that adds one space at a time, cycling through the gaps and remeasuring the line, reaches the same layout slowly; one division does it at once.

Picture a ruler of length `max_width`. Lay the words of a line end to end and the rest of the ruler is `spaces`; cut it into `gaps` equal pieces and drop the remainder, one unit each, into the leftmost gaps. The last line and a lonely word skip the cutting: the words sit flush left and the remainder becomes one block of trailing spaces.

```text
max_width = 16                                            (· marks a space)
pack: This is an        width 10; adding example → 18 > 16, the line closes
      letters 8, gaps 2, spaces 8 → each 4, extra 0
      This····is····an
pack: example of text   width 15; adding justification. → 30 > 16, it closes
      letters 13, gaps 2, spaces 3 → each 1, extra 1 to the leftmost gap
      example··of·text
pack: justification.    last line: single spaces, pad 2 on the right
      justification.··
```

```pseudo
FUNCTION FullJustify(words, max_width)
    lines ← empty list
    i ← 0
    WHILE i < len(words)
        j ← i + 1                             // the line is words[i..j-1]
        width ← len(words[i])                 // letters plus one space per gap
        WHILE j < len(words) AND width + 1 + len(words[j]) ≤ max_width
            width ← width + 1 + len(words[j])
            j ← j + 1
        is_last ← (j = len(words))
        lines.append(JustifyLine(words, i, j, max_width, is_last))
        i ← j
    RETURN lines

FUNCTION JustifyLine(words, i, j, max_width, is_last)
    IF is_last OR j - i = 1                   // left-justify, pad on the right
        line ← join(words[i..j-1], " ")
        RETURN line + " " × (max_width - len(line))
    letters ← 0
    FOR k FROM i TO j - 1
        letters ← letters + len(words[k])
    gaps ← j - i - 1
    spaces ← max_width - letters              // blanks to place in the gaps
    each ← floor(spaces / gaps)
    extra ← spaces mod gaps                   // leftmost gaps get one more
    pieces ← [words[i]]
    FOR k FROM i + 1 TO j - 1
        gap ← each
        IF k - i ≤ extra                      // gap number k - i, from 1
            gap ← gap + 1
        pieces.append(" " × gap)
        pieces.append(words[k])
    RETURN join(pieces, "")
```

Packing looks at every word a constant number of times and each line is built in `O(max_width)`, so the time is `O(n + L × max_width)` for `n` words and `L` lines, linear in the size of the output. The signals are fixed-width layout of any kind: wrapping text, padding columns, or dealing a total out as evenly as possible. That last move, `each = floor(total / parts)` with the first `total mod parts` parts taking one more, appears far beyond text. The classic mistakes are forgetting to count the separating space when testing whether the next word fits, dividing by zero gaps on a one-word line instead of treating it like the last line, and fully justifying the last line instead of padding it on the right.

*Practice:* LC 68 Text Justification · LC 1592 Rearrange Spaces Between Words · LC 418 Sentence Screen Fitting
