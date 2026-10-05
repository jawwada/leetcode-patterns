"""
Car Fleet (LeetCode 853) - Medium
Chapter: stack
Pattern: Monotonic stack

n cars drive toward target on a one-lane road; car i starts at position[i] with speed[i].
A faster car that catches a slower one slows down and travels with it as one fleet.
Return the number of fleets that reach the target.
Example: target = 12, position = [10, 8, 0, 5, 3], speed = [2, 4, 1, 1, 3] -> 3.
"""


# --- brute force ---
def brute_force(target, position, speed):
    """A car leads a fleet iff no car ahead arrives at or after it. O(n^2) time, O(1) space."""
    n = len(position)
    fleets = 0
    for i in range(n):
        time_i = (target - position[i]) / speed[i]
        leader = True
        for j in range(n):                          # rescans every car ahead of i
            if position[j] > position[i]:
                time_j = (target - position[j]) / speed[j]
                if time_j >= time_i:
                    leader = False                  # i catches car j, so it joins a fleet
        if leader:
            fleets += 1
    return fleets


# --- optimal ---
def car_fleet(target, position, speed):
    """Sort cars closest-to-target first; stack of fleet arrival times. O(n log n) time, O(n)."""
    cars = []
    for i in range(len(position)):
        cars.append([position[i], speed[i]])
    cars.sort(reverse=True)                         # closest to the target first
    fleets = []                 # arrival time of each fleet leader, increasing
    for car in cars:
        time = (target - car[0]) / car[1]
        if len(fleets) == 0 or time > fleets[-1]:
            fleets.append(time)                     # slower than the fleet ahead: a new fleet
        # else: it catches the fleet ahead and merges into it, adding nothing
    return len(fleets)


# --- try the brute force ---
print(brute_force(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))   # -> 3
print(brute_force(10, [3], [3]))                            # -> 1
print(brute_force(100, [0, 2, 4], [4, 2, 1]))               # -> 1
print(brute_force(10, [6, 8], [3, 2]))                      # -> 2


# --- try the optimal ---
print(car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))   # -> 3
print(car_fleet(10, [3], [3]))                            # -> 1
print(car_fleet(100, [0, 2, 4], [4, 2, 1]))               # -> 1
print(car_fleet(10, [6, 8], [3, 2]))                      # -> 2
