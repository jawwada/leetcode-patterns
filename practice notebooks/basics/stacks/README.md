# Stacks

A stack is a list you only touch at one end: push adds on top, pop removes the top, peek looks at it. That single rule, last in first out, is exactly what "undo the most recent thing" and "finish the innermost thing first" need: nested brackets, directory paths, pending operators, anything that resolves inside out. In Python the end of a list is the top; never use index 0 as the top, because `insert(0, x)` and `pop(0)` shift every element.

A queue (first in first out) is built from two stacks: new elements pile up in an *inbox*; the *outbox* is refilled by draining the inbox only when it is empty, which reverses the order once and so turns LIFO into FIFO. Each element crosses from inbox to outbox at most once, so n operations cost O(n) in total even though a single refill may be long.

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| `push` (`append`) | O(1) amortized | the end of the list is the top |
| `pop` | O(1) | raises on an empty stack: guard with `if stack` when "pop if any" is meant |
| `peek` (`stack[-1]`) | O(1) | the most recent unfinished thing |
| `empty` (`not stack`) | O(1) | |
| queue `enqueue` | O(1) | push on inbox |
| queue `dequeue` / `peek` | O(1) amortized | pop from outbox; drain inbox into it only when outbox is empty |
| one left-to-right pass | O(n) | n pushes, at most n pops in total, however the pops are distributed |

## Drawn example: decode "3[a2[c]]"

The stack holds what is *unfinished*: for every open bracket, the text built before it and the count waiting to multiply.

```
read 3        cur ""   k 3
read [        push ("", 3)      stack top->bottom [("", 3)]           cur ""  k 0
read a        cur "a"
read 2        cur "a"  k 2
read [        push ("a", 2)     stack top->bottom [("a", 2), ("", 3)] cur ""  k 0
read c        cur "c"
read ]        pop ("a", 2)      cur = "a" + "c" * 2 = "acc"           stack [("", 3)]
read ]        pop ("", 3)       cur = "" + "acc" * 3 = "accaccacc"    stack []
end           cur "accaccacc"
```

Every `]` finishes exactly the bracket that was opened most recently, which is the one on top. The same picture explains `..` in a Unix path (pop the most recent directory), a pending `*` in a calculator (combine with the most recent term), and an asteroid moving left (fight the most recent right-mover first).

## The invariant to say out loud

"The stack holds the things that are started but not finished, newest on top; the newest thing is always the next one to be finished."

Two slips to watch: popping an empty stack (going above root, an unmatched `]`), and forgetting the final flush at the end of the input (the last number in a calculator, the leftover k deletions after the scan).

## Exercises

| File | Drills |
|---|---|
| `01_array_stack_and_queue_via_two_stacks.py` | the structure itself: push/pop/peek/empty on a list; a FIFO queue from an inbox and an outbox stack, refilled only when the outbox is empty |
| `02_simplify_unix_path.py` | split on `/`, skip `''` and `.`, pop on `..` without going above root, `...` is a normal name |
| `03_decode_string.py` | nested work with one stack of (prefix, count): push on `[`, pop and repeat on `]`, multi-digit counts |
| `04_basic_calculator_ii.py` | operator precedence without recursion: push signed terms, apply `*` and `/` to the top at once, flush at the end, truncate toward zero |
| `05_asteroid_collision.py` | pairwise resolution: push right-movers, a left-mover fights the tops while top > 0 and it survives, equal sizes destroy both |
