"""
Basic Calculator II (basics: stacks)
Evaluate a string of non-negative integers, + - * / and spaces; division truncates toward zero.
  "3+2*2"  ->  7

Idea: the stack holds signed terms that are summed at the end. When an operator (or the end)
      arrives, apply the PREVIOUS operator to the number just read: + and - push it with its
      sign, * and / combine it with the top term right away (so they bind tighter).

Pseudocode:
  stack = [], num = 0, op = "+"
  for i, ch in s:
      if ch is a digit: num = num * 10 + digit
      if ch is an operator or i is the last index:    # num is complete
          op "+": push num            op "-": push -num
          op "*": push pop() * num    op "/": push int(pop() / num)
          num = 0, op = ch
  return sum(stack)

Time O(n), space O(n).
"""


def calculate(s):
    stack = []                           # signed terms, summed at the end
    num, op = 0, "+"                     # op is the operator in front of num
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)     # one more digit
        if ch in "+-*/" or i == len(s) - 1:  # num is complete: apply op
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)       # * binds tighter
            else:
                stack.append(int(stack.pop() / num))  # truncates toward zero
            num, op = 0, ch
    return sum(stack)


if __name__ == "__main__":
    print(calculate("3+2*2"))            # 7
    print(calculate(" 3/2 "))            # 1
    print(calculate("14-3/2"))           # 13
