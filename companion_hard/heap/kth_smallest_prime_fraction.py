"""
K-th Smallest Prime Fraction (LeetCode 786) - Hard
Chapter: heap
Pattern: k-way merge with a heap (merge k sorted feeds)

arr is sorted and contains 1 and distinct primes. Consider every fraction arr[i] / arr[j]
with i < j and return the k-th smallest as [arr[i], arr[j]].
Example: arr = [1,2,3,5], k = 3 -> [2,5] (in order: 1/5, 1/3, 2/5, 1/2, 3/5, 2/3).
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def brute_force(arr, k):
    """Build all n(n-1)/2 fractions, sort them, take the k-th. O(n^2 log n) time, O(n^2) space."""
    fractions = []                             # (value, numerator, denominator)
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            fractions.append((arr[i] / arr[j], arr[i], arr[j]))
    fractions.sort()                           # sorts fractions that can never be in the first k
    value, numerator, denominator = fractions[k - 1]
    return [numerator, denominator]


# --- optimal ---
def kth_smallest_prime_fraction(arr, k):
    """Row i (numerator arr[i]) is sorted from the right; k-way merge the rows. O(k log n)."""
    n = len(arr)
    heap = []                                  # (value, i, j): the root is the smallest fraction
    for i in range(n - 1):
        heapq.heappush(heap, (arr[i] / arr[n - 1], i, n - 1))   # each row's smallest fraction
    for step in range(k - 1):
        value, i, j = heapq.heappop(heap)
        if j - 1 > i:                          # row i's next larger fraction: same numerator
            heapq.heappush(heap, (arr[i] / arr[j - 1], i, j - 1))
    value, i, j = heap[0]                      # after k - 1 pops the root is the k-th smallest
    return [arr[i], arr[j]]


# --- try the brute force ---
print(brute_force([1, 2, 3, 5], 3))   # -> [2, 5]
print(brute_force([1, 7], 1))         # -> [1, 7]
print(brute_force([1, 2, 3, 5], 6))   # -> [2, 3]
print(brute_force([1, 2, 3, 5], 1))   # -> [1, 5]


# --- try the optimal ---
print(kth_smallest_prime_fraction([1, 2, 3, 5], 3))   # -> [2, 5]
print(kth_smallest_prime_fraction([1, 7], 1))         # -> [1, 7]
print(kth_smallest_prime_fraction([1, 2, 3, 5], 6))   # -> [2, 3]
print(kth_smallest_prime_fraction([1, 2, 3, 5], 1))   # -> [1, 5]
