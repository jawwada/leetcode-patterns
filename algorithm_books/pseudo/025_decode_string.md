---
rank: 25
slug: decode_string
---

Decode a string in which `k[text]` stands for `text` repeated `k` times. Groups may nest, `k` is a positive integer that may have several digits, and digits appear only as repeat counts. `"3[a2[c]]"` decodes to `"accaccacc"`: the inner `2[c]` becomes `cc`, the group then reads `acc`, and the outer 3 writes it three times.

The brute force finds an innermost group, the first `]` and the last `[` before it, expands it in place and starts over, rebuilding the whole string once per group. One left-to-right pass is enough if it can pause a level when a bracket opens and resume it when the bracket closes, and pausing and resuming in last-opened, first-closed order is a stack. Keep `current`, the decoded text of the innermost open level, and `count`, the number being read. On `[` push a frame with the text before the bracket and its count, then start the inner level empty. On `]` the group is finished: pop the frame, and the outer level resumes as `before + current × repeat`. Letters are appended to `current`, and digits build the count as `count * 10 + digit`, so `12` reads as twelve.

Picture each bracket pair as a box. Every open box owns one frame on the stack, holding what its outer level had written before the box opened, and only the innermost open box is being written. Closing a box flattens it into plain text, `repeat` copies of its contents, glued onto the end of the outer level's text, which is exactly the `before` in the frame on top.

```text
3 [ a 2 [ c ] ]
  │     └───┘ │     frame ("a", 2) closes: "a" + "c" × 2 = "acc"
  └───────────┘     frame ("", 3) closes:  "" + "acc" × 3 = "accaccacc"

ch  count  current       frames (before, count)   step
3   3      ""            empty                    count ← 3
[   0      ""            ("", 3)                  park ("", 3)
a   0      "a"           ("", 3)                  append a
2   2      "a"           ("", 3)                  count ← 2
[   0      ""            ("", 3) ("a", 2)         park ("a", 2)
c   0      "c"           ("", 3) ("a", 2)         append c
]   0      "acc"         ("", 3)                  "a" + "c" × 2
]   0      "accaccacc"   empty                    "" + "acc" × 3
```

```pseudo
FUNCTION DecodeString(s)
    stack ← empty stack                 // frames: (text before the '[', count)
    current ← ""                        // decoded text of the innermost level
    count ← 0                           // the repeat count being read
    FOR EACH ch IN s
        IF ch is a digit
            count ← count * 10 + int(ch)        // counts can have many digits
        ELSE IF ch = '['
            stack.push((current, count))        // park the outer level
            current ← ""                        // the inner level starts empty
            count ← 0
        ELSE IF ch = ']'
            before, repeat ← stack.pop()
            current ← before + current × repeat // resume the outer level
        ELSE
            current ← current + ch
    RETURN current
```

The loop reads each input character once, and each `]` builds one string no longer than the output, so the cost is measured by the output length, not the input length: the 10 characters of `9[9[9[a]]]` decode to 729, built as strings of 9, 81 and 729. The trap is a long text followed by many groups, as in `abcdef1[x]1[y]1[z]`, where every `]` recopies the text before it; collecting each level's pieces in a list and joining them once avoids that. The recursive version lets the call stack hold the frames, calling itself after each `[` and getting back the decoded group and the index past its `]`, the same shape as Basic Calculator (#63). Reach for a stack of frames whenever a nested input must suspend an outer level while an inner one is built, as in Number of Atoms, where each frame is a map of element counts and the multiplier follows the `)`. The classic mistake is forgetting to reset `count` after `[`, which reads the inner `2` of `3[a2[c]]` as 32; treating each digit as the whole count turns `12[x]` into `xx`.

*Practice:* LC 394 Decode String · LC 726 Number of Atoms · LC 1190 Reverse Substrings Between Each Pair of Parentheses
