---
rank: 63
slug: basic_calculator
---

Evaluate a valid expression made of non-negative integers, the operators `+ - * /`, parentheses and spaces, with the usual precedence. Division truncates toward zero, and a minus sign may also open the expression or a group, as in `-(2 + 3)`. For `"2*(3+4)-10/3"` the answer is 11: the group gives 7, `2 * 7 = 14`, and `10 / 3` truncates to 3.

Precedence looks like it needs a parser, but one level of an expression without parentheses is just a sum of signed terms, and a stack of those terms evaluates it in one pass. Read each number and remember the operator in front of it. When the next operator, a `)` or the end of the string finishes the number, fold it in by that remembered operator: after `+` push it, after `-` push its negation, after `*` or `/` pop the top term, combine it with the number and push the result back. Multiplication and division reach back exactly one term, because the terms on the stack are separated by `+` and `-`, which bind more loosely. When the level ends, its value is the sum of the stack.

Parentheses are recursion. Seen from outside, a group is a single number, so on `(` the function calls itself on the text that follows. The call evaluates that level with its own stack and returns the group's value and the index just past its `)`, where the caller resumes as if it had read one long number. A leading minus needs no special case: `op` starts as `+` and `num` as 0, so the minus in `-(2 + 3)` finishes an invisible 0, and the group's 5 then arrives behind a `-`, giving `0 - 5`.

```text
s = "2*(3+4)-10/3"     (indices 0 to 11)

level 0   '*' ends 2     op in front +   push 2              stack [2]
level 0   '(' at 2       recurse from index 3
level 1     '+' ends 3   op in front +   push 3              stack [3]
level 1     ')' ends 4   op in front +   push 4              stack [3, 4]
level 1     return (3 + 4, 7): value 7, resume at index 7
level 0   '-' ends 7     op in front *   top 2 * 7 = 14      stack [14]
level 0   '/' ends 10    op in front -   push -10            stack [14, -10]
level 0   end ends 3     op in front /   top -10 / 3 = -3    stack [14, -3]
level 0   return 14 + (-3) = 11
```

```pseudo
FUNCTION Calculate(s)
    value, end ← Evaluate(s, 0)
    RETURN value

FUNCTION Evaluate(s, i)             // returns (value, next index to read)
    stack ← empty stack             // signed terms of this level; value = sum
    num ← 0
    op ← '+'                        // the operator in front of num
    WHILE i < len(s)
        ch ← s[i]
        i ← i + 1
        IF ch is a digit
            num ← num * 10 + int(ch)
        ELSE IF ch = '('
            num, i ← Evaluate(s, i)         // a whole group acts as one number
        ELSE IF ch IN "+-*/)"
            ApplyOp(stack, op, num)
            IF ch = ')'
                RETURN (sum(stack), i)
            op ← ch
            num ← 0
    ApplyOp(stack, op, num)
    RETURN (sum(stack), i)

FUNCTION ApplyOp(stack, op, num)
    IF op = '+'
        stack.push(num)
    ELSE IF op = '-'
        stack.push(-num)
    ELSE IF op = '*'
        stack.push(stack.pop() * num)       // * reaches back one term only
    ELSE
        stack.push(truncate(stack.pop() / num))     // toward zero
```

Every character is read once, by the level that owns it, so the run is `O(n)` time, and the stacks plus the recursion hold `O(n)` at worst. Reach for this whenever a string encodes arithmetic or other nesting to resolve from the inside out. Basic Calculator II is one level without parentheses, the stack alone; the original Basic Calculator has only `+ - ( )`, and Basic Calculator III has everything, as here. The recursion is as deep as the nesting, so the original problem is often solved iteratively instead, pushing the running total and sign at `(` and popping them at `)`. Evaluate Reverse Polish Notation is the same stack with precedence already settled by the notation: push numbers and let each operator pop two. The classic mistake is Python's `//`, which rounds toward negative infinity: `-10 // 3` is -4 and turns the example's 11 into 10, while `int(-10 / 3)` truncates to -3. The other is folding a number only when an operator arrives, which loses the last number of the string and the one just before each `)`.

*Practice:* LC 224 Basic Calculator · LC 227 Basic Calculator II · LC 772 Basic Calculator III · LC 150 Evaluate Reverse Polish Notation
