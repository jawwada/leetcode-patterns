# Monotonic stacks

A monotonic stack is an ordinary stack with one rule enforced on every push: the values from bottom to top stay sorted (all decreasing or all increasing). You keep the rule by popping everything that would break it *before* pushing. The popped elements are not lost work: each pop is exactly the moment an answer becomes known.

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| push | O(1) amortized | after popping the offenders |
| pop while top violates the order | O(1) each | every index is popped at most once |
| peek `stack[-1]` | O(1) | the most recent survivor |
| whole pass | O(n) | n pushes, at most n pops |

## Which direction?

The stack is sorted **opposite to what you seek**.

- Next **greater** element: pop while `top < current`. Survivors are decreasing bottom to top. A popped element has just met its next greater element: the current one.
- Next **smaller** element: pop while `top > current`. Survivors are increasing. Used by largest rectangle in a histogram.
- Strictness decides ties: `<` treats equal as "not greater", `<=` treats equal as a resolver. Read the problem statement for which one it wants.

## Drawn example: next greater element of [2, 1, 2, 4, 3]

```
i=0 x=2  stack []      push 0        stack [2]          ans [-1,-1,-1,-1,-1]
i=1 x=1  2 not < 1     push 1        stack [2,1]        ans unchanged
i=2 x=2  1 < 2 pop     ans[1] = 2    stack [2]
         2 not < 2     push 2        stack [2,2]        ans [-1, 2,-1,-1,-1]
i=3 x=4  2 < 4 pop     ans[2] = 4    stack [2]
         2 < 4 pop     ans[0] = 4    stack []
         push 3                      stack [4]          ans [ 4, 2, 4,-1,-1]
i=4 x=3  4 not < 3     push 4        stack [4,3]        ans [ 4, 2, 4,-1,-1]
end: indices 3 and 4 still waiting -> -1
```

## The invariant to say out loud

"Everything on the stack is still waiting for its answer, and the stack is sorted so that the top is the one most likely to be resolved next."

## Exercises

| File | Drills |
|---|---|
| `01_next_greater_element.py` | the base pattern: pop while top < current, record on pop |
| `02_previous_smaller_element.py` | mirror image: increasing stack, pop while top >= current, answer is the survivor under you |
| `03_online_stock_span.py` | spans instead of values: a popped day hands its whole span to today, stack of (price, span) |
| `04_sum_of_subarray_minimums.py` | counting at pop time: popped index is the minimum of (j - left) * (i - j) subarrays, sentinel pass at the end |
| `05_remove_k_digits.py` | greedy with a monotonic stack: pop bigger digits while k remains, cut leftovers from the end, strip zeros |
