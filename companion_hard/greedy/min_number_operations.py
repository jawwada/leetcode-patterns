"""
Minimum Number of Increments on Subarrays to Form a Target Array (LeetCode 1526) - Hard
Chapter: greedy
Pattern: Count only the rises (adjacent-difference greedy)

Start from an all-zero array. One operation picks any contiguous subarray and adds 1 to every
element in it. Return the minimum number of operations needed to reach target.
Example: target = [3,1,5,4,2,3,4,2] -> 9; target = [1,2,3,2,1] -> 3.
"""


# --- brute force ---
def brute_force(target):
    """Simulate: while something is short, add 1 across the first run of short spots. O(n max)."""
    n = len(target)
    current = [0] * n
    operations = 0
    while True:
        i = 0
        while i < n and current[i] >= target[i]:  # skip positions that are already done
            i += 1
        if i == n:
            return operations
        while i < n and current[i] < target[i]:   # one stroke across the whole needy run
            current[i] += 1
            i += 1
        operations += 1


# --- optimal ---
def min_number_operations(target):
    """A stroke starts only where the skyline rises; sum the rises. O(n)."""
    operations = target[0]                        # every stroke covering index 0 starts there
    for i in range(1, len(target)):
        if target[i] > target[i - 1]:
            operations += target[i] - target[i - 1]   # new strokes begin here; falls end for free
    return operations


# --- try the brute force ---
print(brute_force([3, 1, 5, 4, 2, 3, 4, 2]))   # -> 9
print(brute_force([1, 2, 3, 2, 1]))            # -> 3
print(brute_force([3, 1, 1, 2]))               # -> 4
print(brute_force([5]))                        # -> 5


# --- try the optimal ---
print(min_number_operations([3, 1, 5, 4, 2, 3, 4, 2]))   # -> 9
print(min_number_operations([1, 2, 3, 2, 1]))            # -> 3
print(min_number_operations([3, 1, 1, 2]))               # -> 4
print(min_number_operations([5]))                        # -> 5
