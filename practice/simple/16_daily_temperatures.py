"""
Daily Temperatures (LeetCode 739)
For each day, how many days until a warmer temperature (0 if never)?
  [73, 74, 75, 71, 69, 72, 76, 73]  ->  [1, 1, 4, 2, 1, 1, 0, 0]

Idea: keep a stack of days still waiting for a warmer day (temps decreasing).
      A warmer day answers every colder day on top of the stack.

Pseudocode:
  answer = [0] * n, stack = []      # indices of waiting days
  for i, t in temps:
      while stack and temps[stack top] < t:
          j = pop; answer[j] = i - j
      push i
  return answer

Time O(n), space O(n).
"""


def daily_temperatures(temps):
    answer = [0] * len(temps)
    stack = []                           # indices still waiting
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:   # today is warmer
            j = stack.pop()
            answer[j] = i - j            # days waited
        stack.append(i)                  # today now waits too
    return answer


if __name__ == "__main__":
    print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))  # [1, 1, 4, 2, 1, 1, 0, 0]
    print(daily_temperatures([30, 40, 50, 60]))                  # [1, 1, 1, 0]
    print(daily_temperatures([60, 50, 40]))                      # [0, 0, 0]
