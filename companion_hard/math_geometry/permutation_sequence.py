"""
Permutation Sequence (LeetCode 60) - Hard
Chapter: math_geometry
Pattern: Factorial number system (direct ranking into blocks)

The permutations of the digits 1..n, listed in lexicographic order, are numbered 1..n!.
Return the k-th one as a string (1 <= n <= 9).
Example: n = 3, k = 3 -> "213" (order: 123, 132, 213, 231, 312, 321); n = 4, k = 9 -> "2314".
"""


# --- brute force ---
def all_permutations(digits):
    """Every arrangement of the (sorted) digits, in lexicographic order. Recursive, n! strings."""
    if len(digits) == 1:
        return [digits[0]]
    result = []
    for i in range(len(digits)):
        rest = digits[:i] + digits[i + 1:]
        for tail in all_permutations(rest):
            result.append(digits[i] + tail)        # smaller first digit comes first
    return result


def brute_force(n, k):
    """List all n! permutations in order and pick the k-th. O(n! * n) time and space."""
    digits = []
    for d in range(1, n + 1):
        digits.append(str(d))
    perms = all_permutations(digits)
    return perms[k - 1]


# --- optimal ---
def permutation_sequence(n, k):
    """Choose each digit by dividing the rank by (n-1)!, (n-2)!, ... O(n^2) time, O(n) space."""
    digits = []
    for d in range(1, n + 1):
        digits.append(str(d))                      # unused digits, ascending
    fact = [1] * n                                 # fact[i] = i!
    for i in range(1, n):
        fact[i] = fact[i - 1] * i
    rank = k - 1                                   # zero-based rank
    out = []
    for i in range(n - 1, -1, -1):                 # i = digits still to place after this one
        index = rank // fact[i]                    # each leading digit owns a block of i! perms
        rank = rank % fact[i]
        out.append(digits.pop(index))
    return "".join(out)


# --- try the brute force ---
print(brute_force(3, 3))                           # -> 213
print(brute_force(4, 9))                           # -> 2314
print(brute_force(3, 1))                           # -> 123
print(brute_force(1, 1))                           # -> 1


# --- try the optimal ---
print(permutation_sequence(3, 3))                  # -> 213
print(permutation_sequence(4, 9))                  # -> 2314
print(permutation_sequence(3, 1))                  # -> 123
print(permutation_sequence(1, 1))                  # -> 1
