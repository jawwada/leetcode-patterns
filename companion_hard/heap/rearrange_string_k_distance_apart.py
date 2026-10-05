"""
Rearrange String k Distance Apart (LeetCode 358) - Hard
Chapter: heap
Pattern: Greedy max-heap by remaining count + fixed-length cooldown queue

Rearrange string s so that identical characters are at least k positions apart. Return any
valid rearrangement, or an empty string if none exists (k = 0 means no constraint).
Example: s = "aabbcc", k = 3 -> "abcabc". s = "aaabc", k = 3 -> "".
"""
import heapq                       # heappush / heappop keep the smallest item at index 0
from collections import deque      # popleft is O(1)


# --- brute force ---
def place(s, k, counts, out):
    """Fill the next slot with any letter not used in the last k - 1 slots; undo on dead ends."""
    if len(out) == len(s):
        return True
    start = max(0, len(out) - (k - 1))
    recent = set(out[start:])                  # letters still too close to reuse
    for ch in sorted(counts):
        if counts[ch] > 0 and ch not in recent:
            counts[ch] -= 1
            out.append(ch)
            if place(s, k, counts, out):
                return True
            out.pop()                          # backtrack: take the letter back
            counts[ch] += 1
    return False


def brute_force(s, k):
    """Backtracking over every allowed letter at every slot. Exponential time, O(n) space."""
    if k <= 1:
        return s
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    out = []
    if place(s, k, counts, out):
        return "".join(out)
    return ""


# --- optimal ---
def rearrange_string(s, k):
    """Place the most frequent rested letter; a k-slot cooldown queue rests it. O(n log 26)."""
    if k <= 1:
        return s
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    heap = []                                  # (-count, letter): the root is the most frequent
    for ch in counts:
        heapq.heappush(heap, (-counts[ch], ch))
    cooldown = deque()                         # letters placed in the last k slots, in order
    out = []
    for slot in range(len(s)):
        if len(heap) == 0:
            return ""                          # every letter is still cooling down: impossible
        neg_count, ch = heapq.heappop(heap)
        out.append(ch)
        cooldown.append((neg_count + 1, ch))   # one copy spent
        if len(cooldown) == k:                 # the front has waited k slots: it is rested
            neg_count, ch = cooldown.popleft()
            if neg_count < 0:
                heapq.heappush(heap, (neg_count, ch))
    return "".join(out)


# --- try the brute force ---
print(brute_force("aabbcc", 3))     # -> abcabc
print(brute_force("aaabc", 3))      # -> (empty line: impossible)
print(brute_force("abc", 0))        # -> abc
print(brute_force("aa", 2))         # -> (empty line: impossible)


# --- try the optimal ---
print(rearrange_string("aabbcc", 3))     # -> abcabc
print(rearrange_string("aaabc", 3))      # -> (empty line: impossible)
print(rearrange_string("abc", 0))        # -> abc
print(rearrange_string("aa", 2))         # -> (empty line: impossible)
