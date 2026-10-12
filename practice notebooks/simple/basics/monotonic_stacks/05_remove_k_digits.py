"""
Remove K Digits (basics: monotonic_stacks)
Remove k digits from the number string num so the number left is as small as possible.
  num = "1432219", k = 3  ->  "1219"

Idea: a bigger digit right before a smaller one should go first: removing it pulls the
      smaller digit into an earlier, more important position. So keep the kept digits
      non-decreasing; deletions still left over at the end come off the tail.

Pseudocode:
  stack = []
  for d in num:
      while k > 0 and stack is not empty and top > d:
          pop;  k -= 1
      push d
  drop the last k digits
  strip leading zeros; return "0" if nothing is left

Time O(n), space O(n).
"""


def remove_k_digits(num, k):
    stack = []                           # kept digits, non-decreasing
    for d in num:
        while k > 0 and stack and stack[-1] > d:   # bigger digit before a smaller one
            stack.pop()
            k -= 1
        stack.append(d)
    stack = stack[:len(stack) - k]       # leftovers off the end (not [:-k]: k may be 0)
    return "".join(stack).lstrip("0") or "0"


if __name__ == "__main__":
    print(remove_k_digits("1432219", 3))  # 1219
    print(remove_k_digits("10200", 1))    # 200
    print(remove_k_digits("10", 2))       # 0
