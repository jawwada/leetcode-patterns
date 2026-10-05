"""
Find in Mountain Array (LeetCode 1095) - Hard
Chapter: binary_search
Pattern: Binary search on a hidden array (peak, then two sorted halves)

A mountain array strictly increases to one peak and then strictly decreases. You can only read
it through MountainArray.get(i) and MountainArray.length(), with at most 100 get calls allowed.
Return the smallest index whose value equals target, or -1.
Example: arr = [1, 2, 3, 4, 5, 3, 1], target = 3 -> 2 (index 5 also holds 3, but 2 is smaller)
"""


# --- helpers ---
class MountainArray:
    """Stand-in for LeetCode's interface: the array is hidden behind get and length."""

    def __init__(self, values):
        self.values = values
        self.calls = 0

    def get(self, index):
        self.calls += 1
        return self.values[index]

    def length(self):
        return len(self.values)


# --- brute force ---
def brute_force(target, mountain):
    """Read every index from the left until target shows up. O(n) get calls."""
    for i in range(mountain.length()):
        if mountain.get(i) == target:
            return i
    return -1


# --- optimal ---
def fetch(mountain, cache, i):
    """get(i) through a dict, so no index is fetched twice."""
    if i not in cache:
        cache[i] = mountain.get(i)
    return cache[i]


def find_peak(mountain, cache):
    """First index where the array stops climbing. O(log n) get calls."""
    left = 0
    right = mountain.length() - 1
    while left < right:
        mid = (left + right) // 2
        if fetch(mountain, cache, mid) < fetch(mountain, cache, mid + 1):
            left = mid + 1            # still climbing: the peak is to the right
        else:
            right = mid               # at or past the peak
    return left


def search_slope(mountain, cache, target, left, right, ascending):
    """Binary search on one slope; a falling slope flips the direction. O(log n) calls."""
    while left <= right:
        mid = (left + right) // 2
        value = fetch(mountain, cache, mid)
        if value == target:
            return mid
        if ascending:
            go_right = value < target
        else:
            go_right = value > target     # falling slope: bigger values sit on the left
        if go_right:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def find_in_mountain_array(target, mountain):
    """Find the peak, then search the rising side first. O(log n) get calls."""
    cache = {}
    peak = find_peak(mountain, cache)
    index = search_slope(mountain, cache, target, 0, peak, True)
    if index != -1:
        return index                  # the rising side holds the smaller index
    last = mountain.length() - 1
    return search_slope(mountain, cache, target, peak + 1, last, False)


# --- try the brute force ---
print(brute_force(3, MountainArray([1, 2, 3, 4, 5, 3, 1])))   # -> 2
print(brute_force(3, MountainArray([0, 1, 2, 4, 2, 1])))      # -> -1
print(brute_force(5, MountainArray([0, 5, 3, 1])))            # -> 1
print(brute_force(0, MountainArray([3, 5, 3, 2, 0])))         # -> 4


# --- try the optimal ---
print(find_in_mountain_array(3, MountainArray([1, 2, 3, 4, 5, 3, 1])))   # -> 2
print(find_in_mountain_array(3, MountainArray([0, 1, 2, 4, 2, 1])))      # -> -1
print(find_in_mountain_array(5, MountainArray([0, 5, 3, 1])))            # -> 1
print(find_in_mountain_array(0, MountainArray([3, 5, 3, 2, 0])))         # -> 4
