"""
Maximum XOR With an Element From Array (LeetCode 1707) - Hard
Chapter: bit_manipulation
Pattern: Offline queries + binary trie (max XOR)

Given nums and queries [x, m], answer each query with the largest x XOR nums[j] over the
elements nums[j] <= m, or -1 if no element is <= m. Values are below 10^9 (30 bits).
Example: nums = [0, 1, 2, 3, 4], queries = [[3, 1], [1, 3], [5, 6]] -> [3, 3, 7]
         (3 ^ 0, 1 ^ 2, 5 ^ 2).
"""


# --- helpers ---
BITS = 30  # values < 10^9 < 2^30


# --- brute force ---
def brute_force(nums, queries):
    """For each query try every allowed element. O(Q * N) time, O(1) space."""
    answer = []
    for x, m in queries:
        best = -1
        for value in nums:  # re-filter and re-scan nums for every query
            if value <= m:
                best = max(best, x ^ value)
        answer.append(best)
    return answer


# --- optimal ---
def trie_insert(child, x):
    """Add x to the binary trie, most significant bit first. child[node] = [zero kid, one kid]."""
    node = 0
    for b in range(BITS - 1, -1, -1):
        bit = (x >> b) & 1
        if child[node][bit] == 0:  # 0 means no child yet (the root is node 0, never a child)
            child[node][bit] = len(child)
            child.append([0, 0])
        node = child[node][bit]


def trie_best_xor(child, x):
    """Walk the trie taking the opposite bit of x whenever it exists. O(BITS)."""
    node = 0
    out = 0
    for b in range(BITS - 1, -1, -1):
        want = 1 - ((x >> b) & 1)  # the opposite bit makes bit b of the XOR a 1
        if child[node][want] != 0:
            out |= 1 << b
            node = child[node][want]
        else:
            node = child[node][1 - want]  # forced: only one branch exists
    return out


def maximize_xor(nums, queries):
    """Sort nums and queries by m; insert nums as m grows, greedy trie walk. O((N + Q) * 30)."""
    ordered = sorted(nums)
    by_bound = []  # (m, x, query index) so the queries can be answered in order of m
    for index in range(len(queries)):
        x, m = queries[index]
        by_bound.append((m, x, index))
    by_bound.sort()
    child = [[0, 0]]  # the trie: node 0 is the root
    answer = [-1] * len(queries)
    next_num = 0  # next element of ordered to insert
    for m, x, index in by_bound:
        while next_num < len(ordered) and ordered[next_num] <= m:
            trie_insert(child, ordered[next_num])  # the trie now holds exactly the nums <= m
            next_num += 1
        if next_num > 0:  # at least one allowed element
            answer[index] = trie_best_xor(child, x)
    return answer


# --- try the brute force ---
print(brute_force([0, 1, 2, 3, 4], [[3, 1], [1, 3], [5, 6]]))         # -> [3, 3, 7]
print(brute_force([5, 2, 4, 6, 6, 3], [[12, 4], [8, 1], [6, 3]]))    # -> [15, -1, 5]
print(brute_force([7], [[0, 7], [0, 6]]))                            # -> [7, -1]


# --- try the optimal ---
print(maximize_xor([0, 1, 2, 3, 4], [[3, 1], [1, 3], [5, 6]]))         # -> [3, 3, 7]
print(maximize_xor([5, 2, 4, 6, 6, 3], [[12, 4], [8, 1], [6, 3]]))    # -> [15, -1, 5]
print(maximize_xor([7], [[0, 7], [0, 6]]))                            # -> [7, -1]
