"""
Longest Common Prefix - Vertical Scan

Return the longest string that is a prefix of every string in the list, or ""
if they share none: ["flower", "flow", "flight"] -> "fl".
"""


# --- algorithm ---
def longest_common_prefix(strs):
    """Scan column by column; stop at the first mismatch or the end of the
    shortest string. O(n * (L + 1)) for n strings and answer length L."""
    if len(strs) == 0:
        return ""
    first = strs[0]
    for col in range(len(first)):
        ch = first[col]
        for word in strs:
            if col == len(word) or word[col] != ch:   # word ended, or mismatch
                return first[0:col]
    return first                        # first is a prefix of all the others


# --- try it ---
print(longest_common_prefix(["flower", "flow", "flight"]))      # -> fl
print(repr(longest_common_prefix(["dog", "racecar", "car"])))   # -> ''
print(longest_common_prefix(["inter", "internet", "interview"]))   # -> inter
print(longest_common_prefix(["flower", "flow"]))                # -> flow
