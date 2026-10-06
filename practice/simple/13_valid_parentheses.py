"""
Valid Parentheses (LeetCode 20)
Return True if every bracket in s is closed by the matching type in the right order.
  s = "([]{})"  ->  True        s = "([)]"  ->  False

Idea: the most recently opened bracket must be closed first -> a stack.
      Push openers; on a closer, the top of the stack must be its partner.

Pseudocode:
  stack = []
  for ch in s:
      if ch is an opener: push ch
      else if stack empty or top != partner(ch): return False
      else: pop
  return stack is empty

Time O(n), space O(n).
"""


def is_valid(s):
    partner = {")": "(", "]": "[", "}": "{"}   # closer -> opener
    stack = []
    for ch in s:
        if ch not in partner:            # opener: remember it
            stack.append(ch)
        elif not stack or stack[-1] != partner[ch]:
            return False                 # nothing to close, or wrong type
        else:
            stack.pop()                  # matched pair
    return not stack                     # leftovers were never closed


if __name__ == "__main__":
    print(is_valid("([]{})"))  # True
    print(is_valid("([)]"))    # False
    print(is_valid("(("))      # False
