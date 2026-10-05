"""
Maximum Running Time of N Computers (LeetCode 2141) - Hard
Chapter: binary_search
Pattern: Binary search on the answer

You have n computers and batteries[i] minutes of charge in battery i. A computer runs on one
battery at a time; batteries can be swapped at any whole minute, but charge is never pooled.
Return the most minutes all n computers can run at the same time.
Example: n = 2, batteries = [3, 3, 3] -> 4 (minutes 1-2: A, B; minute 3: A, C; minute 4: B, C)
"""


# --- brute force ---
def brute_force(n, batteries):
    """Simulate minute by minute with the n fullest batteries. O(T * m log m) time."""
    remaining = list(batteries)
    minutes = 0
    while True:
        remaining.sort(reverse=True)          # fullest batteries first
        if len(remaining) < n or remaining[n - 1] == 0:
            return minutes                    # fewer than n batteries still have charge
        for i in range(n):
            remaining[i] -= 1                 # the n fullest each power one computer
        minutes += 1


# --- optimal ---
def can_run(n, batteries, minutes):
    """Can all n computers run for `minutes`? Each battery gives at most `minutes`. O(m)."""
    usable = 0
    for charge in batteries:
        usable += min(charge, minutes)        # one battery powers one computer at a time
    return usable >= n * minutes


def max_run_time(n, batteries):
    """Binary search the largest feasible number of minutes. O(m log(S / n)) time."""
    left = 0
    right = sum(batteries) // n               # no waste at all: every minute of charge used
    while left < right:
        mid = (left + right + 1) // 2         # round up: we keep the LAST feasible value
        if can_run(n, batteries, mid):
            left = mid                        # mid works: try to run longer
        else:
            right = mid - 1
    return left


# --- try the brute force ---
print(brute_force(2, [3, 3, 3]))         # -> 4
print(brute_force(2, [1, 1, 1, 1]))      # -> 2
print(brute_force(3, [10, 10, 3, 5]))    # -> 8
print(brute_force(2, [100, 1]))          # -> 1


# --- try the optimal ---
print(max_run_time(2, [3, 3, 3]))         # -> 4
print(max_run_time(2, [1, 1, 1, 1]))      # -> 2
print(max_run_time(3, [10, 10, 3, 5]))    # -> 8
print(max_run_time(2, [100, 1]))          # -> 1
