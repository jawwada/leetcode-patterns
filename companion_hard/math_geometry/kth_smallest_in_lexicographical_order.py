"""
K-th Smallest in Lexicographical Order (LeetCode 440) - Hard
Chapter: math_geometry
Pattern: Denary trie traversal with subtree skipping

Return the k-th smallest integer in [1, n] when the integers are ordered as strings
(n and k up to 10^9).
Example: n = 13, k = 2 -> 10, because the order is 1, 10, 11, 12, 13, 2, 3, ..., 9;
n = 1, k = 1 -> 1.
"""


# --- brute force ---
def brute_force(n, k):
    """Write every number as a string, sort, take the k-th. O(n log n) time, O(n) space."""
    strings = []
    for i in range(1, n + 1):
        strings.append(str(i))
    strings.sort()                                 # string order is lexicographic order
    return int(strings[k - 1])


# --- optimal ---
def subtree_size(prefix, n):
    """How many numbers in 1..n start with the digits of prefix (prefix itself included)."""
    low = prefix
    high = prefix + 1                              # [low, high): this prefix, at one depth
    total = 0
    while low <= n:
        total += min(n + 1, high) - low            # clip the level at n
        low = low * 10
        high = high * 10
    return total


def kth_smallest_in_lexicographical_order(n, k):
    """Walk the digit trie in pre-order, skipping whole subtrees. O(log^2 n) time, O(1) space."""
    cur = 1
    k = k - 1                                      # cur is the 1st element, k steps remain
    while k > 0:
        steps = subtree_size(cur, n)
        if steps <= k:
            k -= steps                             # target is past this subtree: next sibling
            cur += 1
        else:
            k -= 1                                 # target is inside: go to the first child
            cur = cur * 10
    return cur


# --- try the brute force ---
print(brute_force(13, 2))                          # -> 10
print(brute_force(1, 1))                           # -> 1
print(brute_force(13, 13))                         # -> 9
print(brute_force(100, 3))                         # -> 100


# --- try the optimal ---
print(kth_smallest_in_lexicographical_order(13, 2))     # -> 10
print(kth_smallest_in_lexicographical_order(1, 1))      # -> 1
print(kth_smallest_in_lexicographical_order(13, 13))    # -> 9
print(kth_smallest_in_lexicographical_order(100, 3))    # -> 100
