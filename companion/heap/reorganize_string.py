"""
Reorganize String (LeetCode 767) - Medium
Chapter: heap
Pattern: Greedy most-frequent-first with a max-heap

Rearrange the characters of s so that no two adjacent characters are equal; return any
valid arrangement, or an empty string if impossible.
Example: "aab" -> "aba". Example: "aaab" -> "".
"""
import heapq                           # heappush / heappop keep the smallest item at index 0
from itertools import permutations     # every ordering of a sequence, as tuples


# --- brute force ---
def brute_force(s):
    """Try every permutation and return the first with no equal neighbours. O(n! * n) time."""
    for perm in permutations(s):
        ok = True
        for i in range(len(perm) - 1):
            if perm[i] == perm[i + 1]:      # checked only after the whole permutation is built
                ok = False
                break
        if ok:
            return "".join(perm)
    return ""


# --- optimal ---
def reorganize_string(s):
    """Always place the most frequent letter that was not just placed (max-heap). O(n log 26)."""
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    heap = []                                  # (-count, letter): the root is the most frequent
    for ch in counts:
        if counts[ch] > (len(s) + 1) // 2:
            return ""                          # too many copies of one letter to keep them apart
        heapq.heappush(heap, (-counts[ch], ch))
    out = []
    held = None                                # the letter just placed, kept out for one turn
    while len(heap) > 0:
        neg_count, ch = heapq.heappop(heap)
        out.append(ch)
        if held is not None and held[0] < 0:   # the previous letter still has copies: back in
            heapq.heappush(heap, held)
        held = (neg_count + 1, ch)             # one copy spent
    return "".join(out)


# --- try the brute force ---
print(brute_force("aab"))      # -> aba
print(brute_force("aaab"))     # -> (empty line: impossible)
print(brute_force("vvvlo"))    # -> vlvov
print(brute_force("aaabbc"))   # -> ababac


# --- try the optimal ---
print(reorganize_string("aab"))      # -> aba
print(reorganize_string("aaab"))     # -> (empty line: impossible)
print(reorganize_string("vvvlo"))    # -> vlvov
print(reorganize_string("aaabbc"))   # -> ababac
