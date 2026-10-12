"""
Evaluate Reverse Polish Notation (LeetCode 150)
Evaluate an expression written in postfix form (division truncates toward zero).
  ["2", "1", "+", "3", "*"]  ->  9   ((2 + 1) * 3)

Idea: numbers wait on a stack; an operator uses the two most recent numbers
      and pushes the result back.

Pseudocode:
  stack = []
  for tok in tokens:
      if tok is an operator:
          b = pop, a = pop          # b is the right operand
          push a op b
      else: push int(tok)
  return stack top

Time O(n), space O(n).
"""


def eval_rpn(tokens):
    stack = []
    for tok in tokens:
        if tok in "+-*/":
            b = stack.pop()              # right operand comes off first
            a = stack.pop()
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # truncate toward zero
        else:
            stack.append(int(tok))       # a number: just wait
    return stack[-1]


if __name__ == "__main__":
    print(eval_rpn(["2", "1", "+", "3", "*"]))   # 9
    print(eval_rpn(["4", "13", "5", "/", "+"]))  # 6
    print(eval_rpn(["7", "-3", "/"]))            # -2
