"""
Partition Labels (LeetCode 763) - Medium
Chapter: greedy
Pattern: Greedy interval merging by last occurrence

Split the string s into as many parts as possible so that each letter appears in at most one
part, and return the part sizes in order.
Example: "ababcbacadefegdehijhklij" -> [9, 7, 8] ("ababcbaca", "defegde", "hijhklij").
"""


# --- brute force ---
def brute_force(s):
    """Grow the part; rescan the rest of s for any of its letters. O(n^2) time, O(26) space."""
    sizes = []
    start = 0
    for i in range(len(s)):
        part_letters = set(s[start:i + 1])
        appears_later = False
        for j in range(i + 1, len(s)):       # rescan the whole suffix at every step
            if s[j] in part_letters:
                appears_later = True
                break
        if not appears_later:                # no letter of the part shows up again: cut here
            sizes.append(i - start + 1)
            start = i + 1
    return sizes


# --- optimal ---
def partition_labels(s):
    """Precompute each letter's last index, then sweep and cut. O(n) time, O(26) space."""
    last = {}                                # letter -> its final index in s
    for i in range(len(s)):
        last[s[i]] = i
    sizes = []
    start = 0
    end = 0
    for i in range(len(s)):
        if last[s[i]] > end:
            end = last[s[i]]                 # the part must stretch to this letter's last copy
        if i == end:                         # nothing inside points further right: cut here
            sizes.append(end - start + 1)
            start = i + 1
    return sizes


# --- try the brute force ---
print(brute_force("ababcbacadefegdehijhklij"))   # -> [9, 7, 8]
print(brute_force("eccbbbbdec"))                 # -> [10]
print(brute_force("abc"))                        # -> [1, 1, 1]
print(brute_force("abca"))                       # -> [4]


# --- try the optimal ---
print(partition_labels("ababcbacadefegdehijhklij"))   # -> [9, 7, 8]
print(partition_labels("eccbbbbdec"))                 # -> [10]
print(partition_labels("abc"))                        # -> [1, 1, 1]
print(partition_labels("abca"))                       # -> [4]
