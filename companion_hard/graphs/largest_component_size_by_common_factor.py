"""
Largest Component Size by Common Factor (LeetCode 952) - Hard
Chapter: graphs
Pattern: Union-Find (disjoint set union)

Given unique positive integers nums, build a graph with an edge between nums[i] and nums[j]
whenever gcd(nums[i], nums[j]) > 1. Return the size of the largest connected component.
Example: [4,6,15,35] -> 4 (4-6 share 2, 6-15 share 3, 15-35 share 5);  [20,50,9,63] -> 2
"""
from math import gcd               # greatest common divisor


# --- helpers ---
def find(parent, x):
    """Root of x in the union-find, halving the path on the way up."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def largest_group(parent, members):
    """How many of the members share the most common root."""
    count = {}
    best = 0
    for x in members:
        root = find(parent, x)
        count[root] = count.get(root, 0) + 1
        if count[root] > best:
            best = count[root]
    return best


# --- brute force ---
def brute_force(nums):
    """Test every pair with gcd and union the ones that share a factor. O(n^2 log max)."""
    n = len(nums)
    parent = list(range(n))            # union-find over indices
    for i in range(n):
        for j in range(i + 1, n):      # every pair re-derives the same prime structure
            if gcd(nums[i], nums[j]) > 1:
                parent[find(parent, i)] = find(parent, j)
    return largest_group(parent, range(n))


# --- optimal ---
def union(parent, a, b):
    """Join the groups of a and b, creating either node on first sight."""
    if a not in parent:
        parent[a] = a
    if b not in parent:
        parent[b] = b
    parent[find(parent, a)] = find(parent, b)


def largest_component_size_by_common_factor(nums):
    """Factor each number once and union it with a hub node per prime factor. O(n * sqrt(max))."""
    parent = {}                        # numbers and prime hubs share one union-find
    for x in nums:
        rem = x
        p = 2
        while p * p <= rem:            # trial division up to the square root
            if rem % p == 0:
                union(parent, x, p)    # number <-> prime hub: two numbers sharing p meet here
                while rem % p == 0:
                    rem //= p
            p += 1
        if rem > 1:
            union(parent, x, rem)      # the leftover is itself a prime
        if x not in parent:
            parent[x] = x              # x == 1 has no prime factor but still counts as a node
    return largest_group(parent, nums)     # count the numbers only, not the hubs


# --- try the brute force ---
print(brute_force([4, 6, 15, 35]))                     # -> 4
print(brute_force([20, 50, 9, 63]))                    # -> 2
print(brute_force([2, 3, 6, 7, 4, 12, 21, 39]))        # -> 8
print(brute_force([1, 2, 3, 5, 7, 11, 13]))            # -> 1


# --- try the optimal ---
print(largest_component_size_by_common_factor([4, 6, 15, 35]))                     # -> 4
print(largest_component_size_by_common_factor([20, 50, 9, 63]))                    # -> 2
print(largest_component_size_by_common_factor([2, 3, 6, 7, 4, 12, 21, 39]))        # -> 8
print(largest_component_size_by_common_factor([1, 2, 3, 5, 7, 11, 13]))            # -> 1
