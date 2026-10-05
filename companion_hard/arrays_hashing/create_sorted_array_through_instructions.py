"""
Create Sorted Array through Instructions (LeetCode 1649) - Hard
Chapter: arrays_hashing
Pattern: Fenwick tree over values (order-statistics counting)

Insert the numbers of instructions one by one into a sorted container. Inserting x costs
min(how many values already present are < x, how many are > x). Return the total cost
modulo 10^9 + 7.
Example: [1, 5, 6, 2] -> 1 (0 + 0 + 0 + min(1, 2): when 2 arrives, 1 is smaller, 5 and 6 larger).
"""


# --- brute force ---
def brute_force(instructions):
    """For each x, scan everything inserted before it. O(n^2) time, O(n) space."""
    placed = []
    cost = 0
    for x in instructions:
        less = 0
        greater = 0
        for value in placed:  # rescans every earlier value
            if value < x:
                less += 1
            elif value > x:
                greater += 1
        cost += min(less, greater)
        placed.append(x)
    return cost % (10 ** 9 + 7)


# --- optimal ---
def fenwick_add(tree, i):
    """Add 1 at value i: walk up the tree. O(log V)."""
    while i < len(tree):
        tree[i] += 1
        i += i & -i  # i & -i is the lowest set bit of i


def fenwick_prefix(tree, i):
    """How many inserted values are <= i: walk down the tree. O(log V)."""
    total = 0
    while i > 0:
        total += tree[i]
        i -= i & -i
    return total


def create_sorted_array(instructions):
    """Count values by VALUE with a Fenwick tree; two prefix sums per insert. O(n log V) time."""
    size = max(instructions)
    tree = [0] * (size + 1)  # 1-indexed: tree[i] covers the values (i - lowbit(i), i]
    cost = 0
    inserted = 0
    for x in instructions:
        less = fenwick_prefix(tree, x - 1)
        greater = inserted - fenwick_prefix(tree, x)  # all inserted so far minus those <= x
        cost += min(less, greater)
        fenwick_add(tree, x)
        inserted += 1
    return cost % (10 ** 9 + 7)


# --- try the brute force ---
print(brute_force([1, 5, 6, 2]))                   # -> 1
print(brute_force([1, 2, 3, 6, 5, 4]))             # -> 3
print(brute_force([1, 3, 3, 3, 2, 4, 2, 1, 2]))    # -> 4
print(brute_force([4, 4, 4, 4]))                   # -> 0


# --- try the optimal ---
print(create_sorted_array([1, 5, 6, 2]))                   # -> 1
print(create_sorted_array([1, 2, 3, 6, 5, 4]))             # -> 3
print(create_sorted_array([1, 3, 3, 3, 2, 4, 2, 1, 2]))    # -> 4
print(create_sorted_array([4, 4, 4, 4]))                   # -> 0
