"""
Gas Station (LeetCode 134) - Medium
Chapter: greedy
Pattern: Greedy running sum with restart

n gas stations sit on a circle; gas[i] is the fuel at station i and cost[i] the fuel needed to
drive on to station i + 1. Starting with an empty tank, return the unique starting index from
which you can complete a full loop, or -1 if none exists.
Example: gas = [1, 2, 3, 4, 5], cost = [3, 4, 5, 1, 2] -> 3.
"""


# --- brute force ---
def brute_force(gas, cost):
    """Simulate a full loop from every start. O(n^2) time, O(1) space."""
    n = len(gas)
    for start in range(n):
        tank = 0
        completed = True
        for step in range(n):
            i = (start + step) % n           # wrap around the circle
            tank = tank + gas[i] - cost[i]
            if tank < 0:                     # ran dry before the next station
                completed = False
                break
        if completed:
            return start
    return -1


# --- optimal ---
def gas_station(gas, cost):
    """One pass: when the tank runs dry, restart at the next station. O(n) time, O(1) space."""
    total = 0                                # surplus fuel over the whole circle
    tank = 0                                 # fuel since the current candidate start
    start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total = total + diff
        tank = tank + diff
        if tank < 0:                         # no station from start to i can work: skip past i
            start = i + 1
            tank = 0
    if total < 0:                            # not enough fuel on the whole circle
        return -1
    return start


# --- try the brute force ---
print(brute_force([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))   # -> 3
print(brute_force([2, 3, 4], [3, 4, 3]))               # -> -1
print(brute_force([3, 1, 1], [1, 2, 2]))               # -> 0
print(brute_force([1, 2], [2, 1]))                     # -> 1


# --- try the optimal ---
print(gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))   # -> 3
print(gas_station([2, 3, 4], [3, 4, 3]))               # -> -1
print(gas_station([3, 1, 1], [1, 2, 2]))               # -> 0
print(gas_station([1, 2], [2, 1]))                     # -> 1
