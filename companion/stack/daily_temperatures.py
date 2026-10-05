"""
Daily Temperatures (LeetCode 739) - Medium
Chapter: stack
Pattern: Monotonic stack

Given daily temperatures, return answer[i] = the number of days until a strictly warmer
temperature, or 0 if no warmer day comes.
Example: [73, 74, 75, 71, 69, 72, 76, 73] -> [1, 1, 4, 2, 1, 1, 0, 0].
"""


# --- brute force ---
def brute_force(temperatures):
    """For each day scan forward to the first warmer day. O(n^2) time, O(1) extra space."""
    n = len(temperatures)
    answer = [0] * n
    for i in range(n):
        for j in range(i + 1, n):                   # walks over cooler days that are also waiting
            if temperatures[j] > temperatures[i]:
                answer[i] = j - i
                break
    return answer


# --- optimal ---
def daily_temperatures(temperatures):
    """Stack of days still waiting (temps decreasing); a warmer day resolves them. O(n) time."""
    answer = [0] * len(temperatures)
    waiting = []                # indices of days still waiting for a warmer day
    for i in range(len(temperatures)):
        while len(waiting) > 0 and temperatures[waiting[-1]] < temperatures[i]:
            j = waiting.pop()                       # today is day j's first warmer day
            answer[j] = i - j
        waiting.append(i)
    return answer


# --- try the brute force ---
print(brute_force([73, 74, 75, 71, 69, 72, 76, 73]))   # -> [1, 1, 4, 2, 1, 1, 0, 0]
print(brute_force([30, 40, 50, 60]))                   # -> [1, 1, 1, 0]
print(brute_force([50, 50, 50]))                       # -> [0, 0, 0]
print(brute_force([90, 80, 70]))                       # -> [0, 0, 0]


# --- try the optimal ---
print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))   # -> [1, 1, 4, 2, 1, 1, 0, 0]
print(daily_temperatures([30, 40, 50, 60]))                   # -> [1, 1, 1, 0]
print(daily_temperatures([50, 50, 50]))                       # -> [0, 0, 0]
print(daily_temperatures([90, 80, 70]))                       # -> [0, 0, 0]
