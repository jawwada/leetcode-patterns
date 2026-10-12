"""
Gas Station - Restart After Every Deficit

Station i on a circle gives gas[i] fuel; driving on to the next one burns
cost[i]. Starting with an empty tank, return the station a full lap can start
from (the input promises at most one), or -1:
gas [4, 1, 2, 5, 1], cost [3, 3, 3, 1, 2] -> 3.
"""


# --- algorithm ---
def can_complete_circuit(gas, cost):
    """Check the totals, then skip past every deficit. O(n) time, O(1) space."""
    if sum(gas) < sum(cost):        # not enough fuel for any lap
        return -1
    start = 0
    tank = 0                        # fuel left since leaving start
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                # stranded: start..i are all out
            start = i + 1
            tank = 0
    return start


# --- try it ---
print(can_complete_circuit([4, 1, 2, 5, 1], [3, 3, 3, 1, 2]))   # -> 3
print(can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))   # -> 3
print(can_complete_circuit([2, 3, 4], [3, 4, 3]))               # -> -1
print(can_complete_circuit([5], [4]))                           # -> 0
