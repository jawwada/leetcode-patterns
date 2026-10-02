# Decode String

*LeetCode 394 · Medium · Pattern: Stack of nested contexts · Reading time ~7 min*

## What the problem is really asking

A string is encoded with the rule `k[text]`, meaning "text repeated k times". Groups can sit side by side, `3[a]2[bc]`,
or inside each other, `3[a2[c]]`. Digits only ever appear as repeat counts, and a count can have several digits, as in
`10[x]`. Expand everything and return the plain string.

The answer is a string. The difficulty is nesting: to expand the outer group you need the inner group already expanded,
yet you meet the outer group first when reading left to right.

```text
3[a2[c]]

outer: 3 x [ a 2[c] ]
              inner: 2 x [ c ]  -> "cc"
        -> 3 x "acc"
        -> "accaccacc"
```

## Do it by hand first

Read `3[a2[c]]` with a pencil. At `3[` you know you will repeat something three times, but not what yet. You make a note,
"times 3, started with nothing before it", and start a fresh scratch line. You write `a`. At `2[` you make a second note,
"times 2, and there was `a` before it", and start another fresh line. You write `c`.

Now `]`. Which note does it close? The most recent one: times 2, with `a` before. So the scratch line `c` becomes `cc`,
glued after `a`: `acc`. Then the second `]` closes the older note, times 3, with nothing before: `accaccacc`.

```text
notes (newest on top)        scratch line
+------------------+
| before "a",  x2  |         "c"
+------------------+
| before "",   x3  |
+------------------+
first ]  -> pop x2 note: "a" + "c"*2 = "acc"
second ] -> pop x3 note: ""  + "acc"*3
```

The notes were a stack, and each note held two things: the text you had before the bracket opened, and the count to apply
when it closes.

## The first honest attempt

Expand from the inside out by searching. The first `]` in the string always closes an innermost group, one with no
brackets inside. Find it, walk back to its `[` and the digits before that, replace the whole `k[text]` with the repeated
text, and repeat until no brackets remain.

```text
3[a2[c]]        first "]" closes 2[c]   rebuild whole string
3[acc]          first "]" closes 3[acc] rebuild whole string
accaccacc

each rebuild copies EVERYTHING outside the group too:
2[x3[y4[z]]]  -> the "2[x" and "]]" are copied on every pass,
                 and "zzzz" is copied again when y wraps it
```

Every expansion rebuilds the full string, so text outside the innermost group is copied once per level of nesting. The
cost is O(n times output length). The waste is copying text that the current expansion does not touch.

## The turning point

**Claim: on reaching `[`, everything needed to finish the outer level later is two values, the text built so far and the
pending count; park them and start fresh.**

Why only two values? The decoded output of the outer level is "whatever it had built before this group" plus "this
group's expansion" plus "whatever follows". The first part is finished and will not change. The second part needs only
the count and the group's own decoded text. So at `[`, save `(text_so_far, k)`, reset to an empty buffer, and decode the
inside as if it were a whole new string. At the matching `]`, the inside is done: take the saved pair back and set
`cur = saved_text + cur * k`. That is exactly "resume the outer level".

Why a stack of these pairs? Because the `]` always closes the most recently opened `[`, the same LIFO rule as Valid
Parentheses. The difference is what we push: not a bracket character, but a *context*, the state of an unfinished level.

This is recursion made explicit. A recursive decoder would call itself at every `[` and return at every `]`, and the
call stack would hold, for each pending level, its local variables: the text it built so far and its count. The explicit
stack holds exactly those two fields per level and nothing else, and it cannot hit Python's recursion limit.

```text
recursive view                explicit stack view
decode(level 0)               [ ("", 3) ]
  decode(level 1)             [ ("", 3), ("a", 2) ]
    returns "c"               ] -> pop ("a", 2): "acc"
  returns "acc"*3             ] -> pop ("", 3):  "accaccacc"
```

Digits need their own small state, `num`, built as `num = num * 10 + digit` so that `10[` means ten, not one then zero.
It is pushed with the context at `[` and reset to 0.

## Watch it work

Input `3[a2[c]]`. Each frame shows the cursor, the stack of saved `(text, k)` contexts (top at top), the current buffer
`cur` and the pending count `num`.

```text
Frame 1:  3 [ a 2 [ c ] ]     stack            cur   num
            ^                 | ("", 3) |      ""    0
          read 3, then "[": push ("", 3), reset
```

The count 3 was gathered into `num`, and `[` parked it together with the empty prefix.

```text
Frame 2:  3 [ a 2 [ c ] ]     stack            cur   num
                ^             | ("", 3) |      "a"   2
          "a" appended, digit 2 gathered
```

Inside the outer group the buffer grows to `a`, and the next count, 2, is pending.

```text
Frame 3:  3 [ a 2 [ c ] ]     stack            cur   num
                  ^           | ("a", 2) |     ""    0
                              | ("", 3)  |
          "[": push ("a", 2), reset
```

The second `[` parks the outer level's progress, `a`, with its count. The buffer starts empty for the inner group.

```text
Frame 4:  3 [ a 2 [ c ] ]     stack            cur   num
                      ^       | ("", 3) |      "acc" 0
          "c" appended; "]": pop ("a", 2)
          cur = "a" + "c" * 2
```

The inner group closes: its text `c` is repeated twice and glued after the parked `a`. We are back at the outer level.

```text
Frame 5:  3 [ a 2 [ c ] ]     stack            cur
                        ^     (empty)          "accaccacc"
          "]": pop ("", 3); cur = "" + "acc" * 3
```

The outer group closes and the stack is empty, so `cur` is the answer, `accaccacc`. In every frame, the stack held one
context per `[` that had been opened but not closed, and `cur` held the decoded text of the innermost open level only.

## Why it is correct

Invariant: at any point, if the stack holds contexts `(t1, k1), ..., (tm, km)` bottom to top and the buffer is `cur`,
then the full decoding of the prefix read so far, if the open groups were closed right now, would be
`t1 + k1 * (t2 + k2 * ( ... (tm + km * cur) ... ))`. Letters append to `cur`, which is the innermost slot, so they stay in
the right place. A `[` moves `cur` and the pending count into a new context and opens an empty innermost slot, which
leaves the formula's value unchanged in shape. A `]` closes the innermost group by evaluating `tm + km * cur` into the new
`cur`, which is exactly one step of the formula. At the end of a valid string no groups are open, so the formula is just
`cur`, the full decoding.

## Cost

Time O(n + output): each input character is handled once, and each output character is produced by a repeat. Strictly,
a character in a group nested d levels deep gets copied once per enclosing `]`, so the cost is bounded by the sum of
output sizes per level; for interview constraints that is O(output) in practice.
Space O(depth + output): one context per open bracket, plus the strings themselves.

The brute force, by contrast, recopies the entire string on every expansion: O(n times output).

## Variations you will meet

- **Recursive descent.** Write `decode(i)` that returns `(text, next_index)` and recurses at `[`. Same algorithm, with
  Python's call stack holding the contexts; fine until nesting depth reaches about a thousand.
- **Number of atoms (LeetCode 726).** `Mg(OH)2`: counts come *after* the group, so on `)` you pop a whole counter of
  atoms, multiply it by the following number, and merge it into the context below.
- **Brace expansion and similar grammars.** Any "save what I had, start fresh, combine on close" grammar uses the same
  stack of contexts.
- **Huge outputs.** Build with lists of pieces instead of repeated string concatenation, or, if only the k-th character
  is asked (LeetCode 880), never expand at all and work with lengths.

## What to carry forward

At `[`, push the unfinished outer context (text so far, repeat count) and start fresh; at `]`, pop it and resume. That is
recursion with the call stack written out by hand. The next problem leaves brackets behind: newcomers collide with the
top of the stack, and one newcomer can knock off several.
