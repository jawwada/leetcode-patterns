"""
Min Stack (LeetCode 155)
Design a stack with push, pop, top and getMin, all in O(1).
  push(-2), push(0), push(-3), getMin, pop, top, getMin  ->  -3, 0, -2

Idea: store each value together with the minimum of the stack at that moment.
      The top pair always knows the current minimum, even after pops.

Pseudocode:
  push(x): cur_min = min(x, top's min) ; push (x, cur_min)
  pop():   pop the top pair
  top():   top pair's value
  getMin(): top pair's min

Time O(1) per operation, space O(n).
"""


class MinStack:
    def __init__(self):
        self.stack = []                  # pairs (value, min so far)

    def push(self, x):
        cur_min = x if not self.stack else min(x, self.stack[-1][1])
        self.stack.append((x, cur_min))  # value + min at this height

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]


if __name__ == "__main__":
    s = MinStack()
    s.push(-2); s.push(0); s.push(-3)
    print(s.getMin())  # -3
    s.pop()
    print(s.top())      # 0
    print(s.getMin())  # -2
