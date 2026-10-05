"""
Maximum Performance of a Team (LeetCode 1383) - Hard
Chapter: heap
Pattern: Sort by the bottleneck (efficiency desc) + min-heap of the top-k other values

n engineers have speed[i] and efficiency[i]. Choose at most k of them; a team's performance
is (sum of speeds) * (minimum efficiency). Return the maximum performance modulo 1e9 + 7.
Example: speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 2 -> 60 (engineers 1 and 4).
"""
import heapq                           # heappush / heappop keep the smallest item at index 0
from itertools import combinations     # every subset of a given size, as tuples


# --- brute force ---
def brute_force(n, speed, efficiency, k):
    """Score every team of size 1..k: sum of speeds * min efficiency. Exponential in k."""
    best = 0
    for size in range(1, k + 1):
        for team in combinations(range(n), size):
            total_speed = 0
            min_efficiency = efficiency[team[0]]
            for i in team:
                total_speed += speed[i]
                min_efficiency = min(min_efficiency, efficiency[i])
            best = max(best, total_speed * min_efficiency)
    return best % (10 ** 9 + 7)


# --- optimal ---
def max_performance(n, speed, efficiency, k):
    """Visit engineers by efficiency desc; keep the k fastest seen in a min-heap. O(n log n)."""
    engineers = []                             # (efficiency, speed), most efficient first
    for i in range(n):
        engineers.append((efficiency[i], speed[i]))
    engineers.sort(reverse=True)
    fastest = []                               # speeds of the current team: root = the slowest
    total_speed = 0
    best = 0
    for current_efficiency, current_speed in engineers:
        heapq.heappush(fastest, current_speed)
        total_speed += current_speed
        if len(fastest) > k:                   # team too big: drop the slowest member
            total_speed -= heapq.heappop(fastest)
        best = max(best, total_speed * current_efficiency)   # this engineer is the bottleneck
    return best % (10 ** 9 + 7)


# --- try the brute force ---
print(brute_force(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2))   # -> 60
print(brute_force(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 3))   # -> 68
print(brute_force(1, [7], [3], 1))                                  # -> 21
print(brute_force(3, [1, 1, 1], [10, 10, 10], 5))                   # -> 30


# --- try the optimal ---
print(max_performance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2))   # -> 60
print(max_performance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 3))   # -> 68
print(max_performance(1, [7], [3], 1))                                  # -> 21
print(max_performance(3, [1, 1, 1], [10, 10, 10], 5))                   # -> 30
