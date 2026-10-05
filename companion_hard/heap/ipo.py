"""
IPO (LeetCode 502) - Hard
Chapter: heap
Pattern: Sort by threshold + max-heap of unlocked candidates

You have capital w and may run at most k projects. Project i needs capital[i] <= your current
capital to start and pays profits[i], added to your capital when done. Pick at most k distinct
projects one after another to maximise final capital.
Example: k = 2, w = 0, profits = [1,2,3], capital = [0,1,1] -> 4.
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def brute_force(k, w, profits, capital):
    """k rounds; each round rescans every project for the best affordable one. O(k n) time."""
    done = [False] * len(profits)
    for round_number in range(k):
        best = -1
        for j in range(len(profits)):
            if done[j] or capital[j] > w:
                continue                       # already picked, or not affordable yet
            if best < 0 or profits[j] > profits[best]:
                best = j
        if best < 0:
            break                              # nothing affordable now, and w will not grow
        done[best] = True
        w += profits[best]
    return w


# --- optimal ---
def find_maximized_capital(k, w, profits, capital):
    """Sort by capital; as w grows, unlock projects into a max-heap of profits. O((n+k) log n)."""
    projects = []                              # (needed capital, profit), sorted by capital
    for i in range(len(profits)):
        projects.append((capital[i], profits[i]))
    projects.sort()
    unlocked = []                              # -profit of affordable projects: root = best profit
    i = 0
    for round_number in range(k):
        while i < len(projects) and projects[i][0] <= w:   # w only grows, so i only moves right
            heapq.heappush(unlocked, -projects[i][1])
            i += 1
        if len(unlocked) == 0:
            break                              # nothing affordable now or ever
        w += -heapq.heappop(unlocked)          # take the largest affordable profit
    return w


# --- try the brute force ---
print(brute_force(2, 0, [1, 2, 3], [0, 1, 1]))   # -> 4
print(brute_force(3, 0, [1, 2, 3], [0, 1, 2]))   # -> 6
print(brute_force(1, 0, [1, 2, 3], [1, 1, 2]))   # -> 0
print(brute_force(2, 5, [4, 9, 1], [10, 2, 3]))  # -> 18


# --- try the optimal ---
print(find_maximized_capital(2, 0, [1, 2, 3], [0, 1, 1]))   # -> 4
print(find_maximized_capital(3, 0, [1, 2, 3], [0, 1, 2]))   # -> 6
print(find_maximized_capital(1, 0, [1, 2, 3], [1, 1, 2]))   # -> 0
print(find_maximized_capital(2, 5, [4, 9, 1], [10, 2, 3]))  # -> 18
