# Min Stack (LeetCode 155)

**Area:** stack · **Difficulty:** Medium · **Key operations:** push (value, running min), pop the pair, top reads the value, getMin reads the stored min

## Problem

Design a stack that supports `push(val)`, `pop()`, `top()` and `getMin()`, each in O(1) time. The script drives a list of operations such as `("push", -2)`, `("pop",)`, `("top",)`, `("getMin",)` and returns the outputs of `top` and `getMin` in order.

## Example

```
push(-2), push(0), push(-3), getMin(), pop(), top(), getMin()  ->  [-3, 0, -2]
```

## Brute force

A plain list. `push`, `pop` and `top` are O(1); `getMin` scans the whole list with `min()`.

O(n) per `getMin`, O(n) space. The wasted work: the minimum of everything below the top never changes while those entries sit there, because a stack only ever changes at its top. Every `getMin` rescans a prefix whose minimum was already known the moment its top entry was pushed.

## From brute force to optimal

Compute "minimum of everything at or below this entry" once, at push time: `current_min = min(val, min stored on the entry below)`. Store it next to the value as a pair. The entries below never change while this one is on the stack, so the stored min never goes stale. `getMin` reads the top pair's stored min. `pop` removes the pair, and the pair underneath carries the correct earlier minimum, so nothing needs recomputing.

## Intuition

Picture two columns growing upward side by side: the values on the left, "min so far" on the right. Every time you add a row, the right cell is the smaller of the new value and the right cell just below it, so the right column never increases as you go up. Removing the top row removes both cells at once, and the row that is now on top already holds the right answer. A single global `min` variable fails exactly here: after a pop it has no way to recover the previous minimum, but a per-row snapshot does.

## Walkthrough

The stack is drawn top first; each entry is `value (min)`.

```
push -2    top->bottom   -2 (min -2)
push  0    top->bottom    0 (min -2) | -2 (min -2)         min(0, -2) = -2
push -3    top->bottom   -3 (min -3) |  0 (min -2) | -2 (min -2)   min(-3, -2) = -3
getMin  -> -3            read the top pair's min          out [-3]
pop  -3    top->bottom    0 (min -2) | -2 (min -2)         the old min -2 reappears on top
top     ->  0            read the top pair's value        out [-3, 0]
getMin  -> -2            read the top pair's min          out [-3, 0, -2]
result [-3, 0, -2]
```

Duplicates need no special handling: after `push 1, push 1, push 2, pop, pop` the top pair is `1 (min 1)`, so `getMin` is still 1.

## Steps

1. `items = []` of `(value, current_min)` pairs; the top is `items[-1]`.
2. `push(val)`: `current_min = min(val, items[-1][1])` if the stack is non-empty, else `val`; append `(val, current_min)`.
3. `pop()`: remove the top pair.
4. `top()`: return `items[-1][0]`.
5. `getMin()`: return `items[-1][1]`.

## Complexity

O(1) time per operation. O(n) space: one extra integer per entry.

## Pitfalls

- **Comparing with the top's value instead of its stored min.** `min(val, items[-1][0])` forgets smaller entries deeper down: push 1, push 5, push 3 stores min 3 on top.
- **`getMin` reading the wrong field.** `items[-1][0]` is the top value, not the minimum.
- **`pop(0)` instead of `pop()`.** Removing the bottom entry leaves the wrong value on top and invalidates the stored mins above it.
- **A single global min.** It cannot be restored after the minimum is popped. The per-entry snapshot is what makes `pop` O(1).
- **A second "min stack" pushed only on strict decrease.** Duplicates of the minimum then disappear after one pop; push on `<=`, or store the pair as done here.
