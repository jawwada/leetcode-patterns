# Evaluate Reverse Polish Notation (LeetCode 150)

**Area:** stack · **Difficulty:** Medium · **Key operations:** push number, pop two operands (right one first), apply operator, push result

## Problem

You are given an arithmetic expression in postfix (Reverse Polish) notation as a list of string tokens. Each token is an integer or one of `+ - * /`. Evaluate it. Division truncates toward zero, there is no division by zero, and the expression is always valid.

## Example

```
tokens = ["2", "1", "+", "3", "*"]
       = (2 + 1) * 3
       = 9
```

Another: `["4", "13", "5", "/", "+"]` is `4 + 13/5 = 4 + 2 = 6`.

## Brute force

Scan the token list for the first operator. Its operands are the two tokens right before it. Apply the operator, splice the single result back into the list in place of the three tokens, and start scanning again from the front. Stop when one token remains.

O(n²) time, O(n) space: there are about n/2 reductions and each one rescans and rebuilds the list. The wasted work: every pass re-reads the numbers at the front of the list that have not changed since the last pass.

## From brute force to optimal

Look at what the brute force rescans: the numbers before the first operator. Those are exactly the numbers that have been read but not yet consumed, in order. When an operator finally arrives, it consumes the *two most recent* of them. "Most recent first" is LIFO, so a stack holds the unconsumed numbers perfectly.

Walk the tokens once. A number is pushed. An operator pops two numbers, computes, and pushes the result back, which is the brute force's "splice" done in O(1). Every token is touched once.

## Intuition

Postfix was designed for a stack: by the time you read an operator, its operands are the last two things you saw. Picture the stack as a column of pending numbers. A number lands on top. An operator plucks the top two, fuses them into one, and drops it back. At the end exactly one number is left in the column, and that is the answer. The only subtlety is order: the top of the stack is the *right* operand, because it was pushed later.

## Walkthrough

Stack shown top first.

```
token 2    push 2                             stack [2]
token 1    push 1                             stack [1, 2]
token +    pop b=1, pop a=2   2 + 1 = 3       stack [3]
token 3    push 3                             stack [3, 3]
token *    pop b=3, pop a=3   3 * 3 = 9       stack [9]
end: one number left -> 9
```

For `["6", "3", "-"]`: push 6, push 3, then `-` pops b=3 first and a=6 second, giving 6 - 3 = 3.

## Steps

1. `stack = []`.
2. For each token: if it is an operator, pop `b` then `a`, push `a op b`; otherwise push `int(token)`.
3. For `/`, use `int(a / b)` so the result truncates toward zero.
4. Return the single number left on the stack.

## Complexity

O(n) time: each token is pushed once and popped at most once. O(n) space for the stack in the worst case (a long run of numbers before the operators).

## Pitfalls

- **Operand order.** The first pop is the right operand `b`, the second is the left operand `a`. Swapping them turns `6 3 -` into -3.
- **Floor instead of truncation.** Python's `//` floors toward -infinity: `-7 // 2 == -4`. The problem wants -3, so use `int(a / b)`.
- **Detecting operators with `isdigit()`.** `"-7".isdigit()` is False, so a negative number would be treated as an operator and pop from an empty stack. Test membership in the operator set instead.
- **Returning the wrong thing.** With a valid expression exactly one number remains; return it, not the stack.
- **Pushing strings.** Convert with `int(tok)` on the way in; otherwise `+` concatenates and `*` raises.
