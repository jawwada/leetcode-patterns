"""
Find All People With Secret (LeetCode 2092) - Hard
Chapter: graphs
Pattern: Time-grouped union-find with reset of non-informed components

There are n people, 0..n-1. Person 0 tells a secret to firstPerson at time 0. meetings[i] =
[x, y, t] means x and y meet at time t; if either of them knows the secret then, both do, and
within one time t the secret passes instantly along chains of meetings. Return everyone who
knows the secret after all meetings, in ascending order.
Example: n = 6, meetings = [[1,2,5],[2,3,8],[1,5,10]], firstPerson = 1 -> [0, 1, 2, 3, 5]
"""


# --- helpers ---
def meetings_by_time(meetings):
    """Sort the meetings by time and return the groups: one list of (x, y) pairs per time."""
    ordered = []
    for x, y, t in meetings:
        ordered.append((t, x, y))
    ordered.sort()
    groups = []
    last_time = None
    for t, x, y in ordered:
        if t != last_time:             # a new time starts a new group
            groups.append([])
            last_time = t
        groups[-1].append((x, y))
    return groups


# --- brute force ---
def brute_force(n, meetings, first_person):
    """Per time group, re-sweep its meetings until nobody new learns the secret. O(m^2)."""
    knows = [False] * n
    knows[0] = True
    knows[first_person] = True
    for group in meetings_by_time(meetings):
        changed = True
        while changed:                 # each sweep carries the secret only one hop further
            changed = False
            for x, y in group:
                if knows[x] != knows[y]:
                    knows[x] = True
                    knows[y] = True
                    changed = True
    result = []
    for person in range(n):
        if knows[person]:
            result.append(person)
    return result


# --- optimal ---
def find(parent, x):
    """Root of x in the union-find, halving the path on the way up."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def find_all_people_with_secret(n, meetings, first_person):
    """Union each time group, then cut loose everyone not glued to person 0. O(m log m)."""
    parent = list(range(n))
    parent[first_person] = 0           # person 0 is the permanent "knows" root
    for group in meetings_by_time(meetings):
        for x, y in group:
            root_x = find(parent, x)
            root_y = find(parent, y)
            if root_x != root_y:
                parent[root_x] = root_y
        for x, y in group:             # links that never reached 0 must not outlive this time
            if find(parent, x) != find(parent, 0):
                parent[x] = x
            if find(parent, y) != find(parent, 0):
                parent[y] = y
    result = []
    for person in range(n):
        if find(parent, person) == find(parent, 0):
            result.append(person)
    return result


# --- try the brute force ---
print(brute_force(6, [[1, 2, 5], [2, 3, 8], [1, 5, 10]], 1))                  # -> [0, 1, 2, 3, 5]
print(brute_force(4, [[3, 1, 3], [1, 2, 2], [0, 3, 3]], 3))                   # -> [0, 1, 3]
print(brute_force(5, [[3, 4, 2], [1, 2, 1], [2, 3, 1]], 1))                   # -> [0, 1, 2, 3, 4]
print(brute_force(6, [[1, 2, 5], [3, 4, 5], [2, 3, 8], [4, 5, 10]], 1))       # -> [0, 1, 2, 3]


# --- try the optimal ---
print(find_all_people_with_secret(6, [[1, 2, 5], [2, 3, 8], [1, 5, 10]], 1))   # -> [0, 1, 2, 3, 5]
print(find_all_people_with_secret(4, [[3, 1, 3], [1, 2, 2], [0, 3, 3]], 3))       # -> [0, 1, 3]
print(find_all_people_with_secret(5, [[3, 4, 2], [1, 2, 1], [2, 3, 1]], 1))    # -> [0, 1, 2, 3, 4]
meetings_d = [[1, 2, 5], [3, 4, 5], [2, 3, 8], [4, 5, 10]]
print(find_all_people_with_secret(6, meetings_d, 1))                              # -> [0, 1, 2, 3]
