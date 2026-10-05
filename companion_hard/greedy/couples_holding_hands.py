"""
Couples Holding Hands (LeetCode 765) - Hard
Chapter: greedy
Pattern: Union-Find (disjoint set union)

2n people sit in a row; persons 2k and 2k+1 are a couple. A swap exchanges any two people.
Return the minimum number of swaps so every couple sits side by side on a couch (seats 2i, 2i+1).
Example: row = [0,2,1,3] -> 1 (swap seats 1 and 2); row = [3,2,0,1] -> 0.
"""
from collections import deque   # popleft is O(1)


# --- brute force ---
def brute_force(row):
    """BFS over seatings, one swap per edge; stop at the first seating with all couples paired."""
    start = tuple(row)
    distance = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if all_couples_seated(current):
            return distance[current]              # BFS: first time seen = fewest swaps
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                swapped = list(current)
                swapped[i], swapped[j] = swapped[j], swapped[i]
                swapped = tuple(swapped)
                if swapped not in distance:
                    distance[swapped] = distance[current] + 1
                    queue.append(swapped)
    return -1


def all_couples_seated(seating):
    for i in range(0, len(seating), 2):
        if seating[i] // 2 != seating[i + 1] // 2:   # person p belongs to couple p // 2
            return False
    return True


# --- optimal ---
def couples_holding_hands(row):
    """Couples are nodes, couches are edges: a cycle of k couples costs k - 1 swaps. O(n)."""
    n = len(row) // 2
    parent = list(range(n))                       # union-find over the n couples
    components = n
    for i in range(0, len(row), 2):
        a = find(parent, row[i] // 2)             # couple ids of the two people on this couch
        b = find(parent, row[i + 1] // 2)
        if a != b:
            parent[a] = b                         # two different couples share a couch: link them
            components -= 1
    return n - components                         # sum over cycles of (size - 1)


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]             # path halving keeps the tree flat
        x = parent[x]
    return x


# --- try the brute force ---
print(brute_force([0, 2, 1, 3]))                  # -> 1
print(brute_force([3, 2, 0, 1]))                  # -> 0
print(brute_force([0, 1]))                        # -> 0
print(brute_force([5, 4, 2, 6, 3, 1, 0, 7]))      # -> 2


# --- try the optimal ---
print(couples_holding_hands([0, 2, 1, 3]))                  # -> 1
print(couples_holding_hands([3, 2, 0, 1]))                  # -> 0
print(couples_holding_hands([0, 1]))                        # -> 0
print(couples_holding_hands([5, 4, 2, 6, 3, 1, 0, 7]))      # -> 2
