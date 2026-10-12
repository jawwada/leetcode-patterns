---
rank: 16
slug: valid_parentheses
---

Given a string made of the brackets `()[]{}`, decide whether it is valid: every opener is closed by a bracket of the same kind, and the bracket opened most recently closes first. `"([]{})"` is valid; `"([)]"` is not, even though each kind is opened once and closed once.

The brute force deletes adjacent matched pairs such as `()` until nothing changes and checks that the string vanished, which costs `O(n²)` when the nesting is deep. The better view is geometric. Draw an arc from every opener to the closer that ends it. A valid string is a set of arcs that nest like boxes inside boxes, never crossing, each joining two brackets of the same kind. Nesting means that a closer always ends the innermost arc still open, the one opened most recently, and "most recent first" is exactly a stack.

So walk the string once. Push every opener. When a closer arrives, the top of the stack must be its partner; popping it closes that arc. A closer that meets an empty stack has no arc to close, and a closer that meets the wrong kind on top would cross an arc that is still open, so either way the answer is `false` on the spot. At the end the stack must be empty, because any opener left on it is an arc that never closed.

```text
 ( [ ] { } )       ch   action                stack after
 │ └─┘ └─┘ │       (    push                  (
 └─────────┘       [    push                  ( [
 arcs nest ✓       ]    top [ matches, pop    (
                   {    push                  ( {
                   }    top { matches, pop    (
                   )    top ( matches, pop    empty  → true

 ( [ ) ]           (    push                  (
 │ └─┼─┘           [    push                  ( [
 └───┘             )    top is [, needs (     → false
 arcs cross ✗
```

```pseudo
FUNCTION IsValid(s)
    partner ← map {')' → '(', ']' → '[', '}' → '{'}  // closer → its opener
    stack ← empty stack                         // openers still waiting
    FOR EACH ch IN s
        IF ch IN partner
            IF len(stack) = 0 OR stack.top() ≠ partner[ch]
                RETURN false                    // nothing open, or wrong kind
            stack.pop()                         // the innermost opener closes
        ELSE
            stack.push(ch)
    RETURN len(stack) = 0                       // leftovers never closed
```

Each character is pushed or popped at most once, so the scan takes `O(n)` time, and the stack can hold all `n` openers, `O(n)` space. Reach for the matching stack whenever things must close in the reverse order of opening: brackets, HTML tags, nested function calls, an encoded string such as `3[a2[c]]`, the groups of an arithmetic expression (#45). With a single bracket kind the stack shrinks to a counter of open brackets, and Minimum Add to Make Parentheses Valid just adds the closers that find the counter at zero to the openers left at the end. Minimum Remove to Make Valid Parentheses pushes indices instead of characters, so it knows exactly which unmatched brackets to delete, and Longest Valid Parentheses also keeps indices, measuring each valid run from the last unmatched index left on the stack. The classic mistakes are returning `true` without checking that the stack is empty, which accepts `"(("`, and reading the top of an empty stack on a leading closer as in `")("`, which crashes instead of returning `false`. Keeping one counter per kind is the third: the counts of `"([)]"` balance perfectly and the crossing goes unseen.

*Practice:* LC 20 Valid Parentheses · LC 921 Minimum Add to Make Parentheses Valid · LC 1249 Minimum Remove to Make Valid Parentheses · LC 32 Longest Valid Parentheses
