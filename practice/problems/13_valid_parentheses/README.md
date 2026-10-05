# Valid Parentheses (LeetCode 20)

**Area:** stack · **Difficulty:** Medium · **Key operations:** push an opener, on a closer check the top and pop, empty stack at the end

## Problem

Given a string made of the brackets `()[]{}`, decide whether it is valid: every opener is closed by a bracket of the same kind, brackets close in nested order, and nothing is left open.

## Example

```
"([]{})"  ->  True
"([)]"    ->  False   (the ')' arrives while '[' is still open)
"(("      ->  False   (nothing closes them)
"]"       ->  False   (nothing to close)
```

## Brute force

Repeatedly find an adjacent pair `()`, `[]` or `{}`, delete it, and start over. The string is valid iff it shrinks to `""`.

O(n²) time, O(n) space: up to `n/2` deletions, each rescanning and copying the whole string. The wasted work: after a deletion only the characters next to the gap could have formed a new pair, yet every pass rescans from the start.

## From brute force to optimal

A closer is valid only if it matches the most recently opened, still-unclosed bracket, the innermost one. That is last-in, first-out order, so keep the open brackets on a stack. Walk the string once: push openers; on a closer, the stack must be non-empty and its top must be the matching opener, then pop it. At the end the stack must be empty. The stack is exactly the "unfinished business" the brute force kept re-reading; keeping it explicitly makes each character cost O(1).

## Intuition

Picture walking into nested rooms: each opener takes you one room deeper, each closer must be the door of the room you are currently in. The stack is the trail of doors behind you, innermost on top. A closer that does not match the top is a door to a room you are not in; a closer with an empty stack is a door with no room; a non-empty stack at the end means you never walked back out.

## Walkthrough

`^` marks the current character; the stack is shown top first.

```
([]{})
^      '(' opener            -> push    stack ['(']
 ^     '[' opener            -> push    stack ['[', '(']
  ^    ']' closer, top '['   -> pop     stack ['(']
   ^   '{' opener            -> push    stack ['{', '(']
    ^  '}' closer, top '{'   -> pop     stack ['(']
     ^ ')' closer, top '('   -> pop     stack []
end: stack empty -> True
```

The failing case `"([)]"`:

```
([)]
^      '(' opener            -> push    stack ['(']
 ^     '[' opener            -> push    stack ['[', '(']
  ^    ')' closer, top '[' is not '('   -> False
```

## Steps

1. `pairs = {")": "(", "]": "[", "}": "{"}`, `stack = []`.
2. For each character: if it is a closer, return `False` when the stack is empty or its top is not `pairs[ch]`; otherwise pop. If it is an opener, push it.
3. Return `True` iff the stack is empty.

## Complexity

O(n) time: one push or pop per character. O(n) space for the stack in the worst case (all openers).

## Pitfalls

- **Returning `True` at the end unconditionally.** Leftover openers mean something was never closed: `"(("` must be `False`. Return `not stack`.
- **Dropping the empty-stack check.** A closer with nothing open falls through to `stack.pop()` on an empty list and raises; `"]"` must return `False`.
- **`pop(0)` instead of `pop()`.** The match was checked against the top, so the top is what must leave; popping the bottom makes `"([])"` fail on the final `')'`.
- **Matching counts, not kinds.** `"([)]"` has balanced counts of every bracket and is still invalid; the top must be the *same kind* of opener.
- **Mapping the dictionary the wrong way.** With `opener -> closer` you must look up the top's partner; with `closer -> opener` you compare directly. Pick one and be consistent.
