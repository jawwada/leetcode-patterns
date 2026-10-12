"""
Monotonic Stack - Next Greater Element

For each day's temperature, return how many days you must wait for a warmer
one, or 0 if no warmer day comes:
[73, 74, 75, 71, 69, 72, 76, 73] -> [1, 1, 4, 2, 1, 1, 0, 0].
"""


# --- algorithm ---
def daily_temperatures(temperatures):
    """Stack of days still waiting; a warmer day answers them. O(n) time."""
    n = len(temperatures)
    answer = [0] * n                # 0 stays for days nothing beats
    stack = []                      # waiting indices, temps never rising
    for i in range(n):
        while len(stack) > 0 and temperatures[stack[-1]] < temperatures[i]:
            j = stack.pop()         # day i is the first warmer day after j
            answer[j] = i - j
        stack.append(i)             # day i waits for its own answer
    return answer


# --- try it ---
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
print(daily_temperatures(temperatures))     # -> [1, 1, 4, 2, 1, 1, 0, 0]
print(daily_temperatures([30, 40, 50]))     # -> [1, 1, 0]
print(daily_temperatures([70, 70, 71]))     # -> [2, 1, 0]
print(daily_temperatures([]))               # -> []
