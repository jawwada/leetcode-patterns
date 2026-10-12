"""
Partition Labels - Extend to the Last Occurrence

Cut a string into as many parts as possible so that each letter appears in at
most one part, and return the part sizes in order:
"ababcbacadefegdehijhklij" -> [9, 7, 8].
"""


# --- algorithm ---
def partition_labels(s):
    """Record each letter's last index; cut where i meets part_end. O(n)."""
    last = {}                       # letter -> index of its last copy
    for i in range(len(s)):
        last[s[i]] = i
    sizes = []
    start = 0                       # first index of the current part
    part_end = 0                    # the part must reach at least here
    for i in range(len(s)):
        part_end = max(part_end, last[s[i]])    # this letter drags it along
        if i == part_end:           # nothing inside reaches past i: cut
            sizes.append(i - start + 1)
            start = i + 1
    return sizes


# --- try it ---
print(partition_labels("ababcbacadefegdehijhklij"))   # -> [9, 7, 8]
print(partition_labels("eccbbbbdec"))                 # -> [10]
print(partition_labels("abac"))                       # -> [3, 1]
print(partition_labels(""))                           # -> []
