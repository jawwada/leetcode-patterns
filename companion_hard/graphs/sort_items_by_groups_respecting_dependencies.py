"""
Sort Items by Groups Respecting Dependencies (LeetCode 1203) - Hard
Chapter: graphs
Pattern: Topological sort (Kahn's BFS) / cycle detection

There are n items; item i belongs to group[i], or to no group when group[i] = -1, with m groups in
total. before_items[i] lists the items that must come before i. Return an ordering of all items in
which items of the same group sit next to each other and every before-constraint holds, or [] if
none exists. Example: n=8, m=2, group=[-1,-1,1,0,0,1,0,-1],
before_items=[[],[6],[5],[6],[3,6],[],[],[]] -> [6,3,4,1,5,2,0,7] (one valid answer).
"""
from collections import deque            # popleft is O(1)
from itertools import permutations       # every ordering of a sequence, as tuples


# --- helpers ---
def is_valid(n, group, before_items, order):
    """True when order holds all n items, respects every constraint and keeps groups together."""
    if sorted(order) != list(range(n)):
        return False
    position = {}                                    # item -> index in order
    for index in range(n):
        position[order[index]] = index
    for item in range(n):
        for earlier in before_items[item]:
            if position[earlier] > position[item]:
                return False
    for g in set(group):
        if g == -1:
            continue
        indices = []
        for item in range(n):
            if group[item] == g:
                indices.append(position[item])
        if max(indices) - min(indices) + 1 != len(indices):
            return False                             # a foreign item sits inside this group's run
    return True


def topological_order(adjacent, in_degree):
    """Kahn's BFS over a graph given as lists; [] when a cycle keeps some node blocked."""
    order = []
    queue = deque()
    for node in range(len(in_degree)):
        if in_degree[node] == 0:
            queue.append(node)
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in adjacent[node]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
    if len(order) != len(in_degree):
        return []
    return order


# --- brute force ---
def brute_force(n, m, group, before_items):
    """Try every permutation of the items and return the first valid one. O(n! * (n + E))."""
    for order in permutations(range(n)):             # n! orders, each checked from scratch
        if is_valid(n, group, before_items, list(order)):
            return list(order)
    return []


# --- optimal ---
def empty_lists(count):
    """[[], [], ...] with count independent empty lists."""
    lists = []
    for _ in range(count):
        lists.append([])
    return lists


def sort_items(n, m, group, before_items):
    """Topologically sort the items and the groups; emit groups in group order. O(n + m + E)."""
    group = group[:]
    for item in range(n):
        if group[item] == -1:                        # a loner gets a fresh group of its own
            group[item] = m
            m += 1
    item_adjacent, item_in_degree = empty_lists(n), [0] * n
    group_adjacent, group_in_degree = empty_lists(m), [0] * m
    for item in range(n):
        for earlier in before_items[item]:
            item_adjacent[earlier].append(item)
            item_in_degree[item] += 1
            if group[earlier] != group[item]:        # a cross-group edge orders whole groups
                group_adjacent[group[earlier]].append(group[item])
                group_in_degree[group[item]] += 1
    item_order = topological_order(item_adjacent, item_in_degree)
    group_order = topological_order(group_adjacent, group_in_degree)
    if not item_order or not group_order:
        return []                                    # a cycle among items or among groups
    members = empty_lists(m)                         # members[g] = group g's items in item order
    for item in item_order:
        members[group[item]].append(item)
    result = []
    for g in group_order:
        result += members[g]
    return result


# --- try the brute force ---
group, before = [-1, -1, 1, 0, 0, 1, 0, -1], [[], [6], [5], [6], [3, 6], [], [], []]
print(is_valid(8, group, before, brute_force(8, 2, group, before)))          # -> True
print(brute_force(8, 2, group, [[], [6], [5], [6], [3], [], [4], []]))        # -> []
print(brute_force(3, 1, [0, -1, 0], [[], [0], [1]]))                          # -> []
print(brute_force(4, 2, [0, 1, 0, 1], [[], [], [1], []]))                     # -> [0, 2, 1, 3]


# --- try the optimal ---
group, before = [-1, -1, 1, 0, 0, 1, 0, -1], [[], [6], [5], [6], [3, 6], [], [], []]
print(is_valid(8, group, before, sort_items(8, 2, group, before)))           # -> True
print(sort_items(8, 2, group, [[], [6], [5], [6], [3], [], [4], []]))         # -> []
print(sort_items(3, 1, [0, -1, 0], [[], [0], [1]]))                           # -> []
print(sort_items(4, 2, [0, 1, 0, 1], [[], [], [1], []]))                      # -> [0, 2, 1, 3]
