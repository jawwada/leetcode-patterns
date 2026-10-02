"""
Compare Version Numbers (LeetCode 165)  — Medium
Pattern: Two-pointer chunk parsing

Problem
-------
Version strings are dot-separated revisions of digits ("1.01", "1.001", "1.0.0"). Compare two
versions revision by revision as integers (so leading zeros are ignored); a missing revision
counts as 0. Return -1 if version1 < version2, 1 if greater, 0 if equal.
Example: "1.01" vs "1.001" -> 0; "1.0" vs "1.0.0" -> 0; "0.1" vs "1.1" -> -1.

Brute force
-----------
Split both strings on '.', pad the shorter list with "0" until both have the same length, map
every chunk through int(), then compare the two integer lists element by element. O(n + m) time
but O(n + m) extra space for two lists of substrings and two lists of ints. The wasted work is
materialising all chunks of both versions before comparing, when the comparison usually decides
on the first differing revision and never needs the rest.

From brute force to optimal
---------------------------
Each revision is consumed left to right and compared immediately, so keep one index into each
string and parse the next integer in place: accumulate x = x*10 + digit until a '.' or the end,
do the same for y, compare, and only if equal advance both past the dot. When one string is
exhausted its pointer simply stays at the end and its parser yields 0, which is exactly the
"missing revision counts as 0" rule for free. Early exit on the first difference, O(1) extra
space, no substrings.

Intuition
---------
Compare like a dictionary but with numeric fields: walk the two strings in lockstep one field at
a time. Leading zeros vanish because we parse to an int, and trailing ".0.0" vanishes because an
exhausted string reads as zeros.

Geometric view
--------------
version1: 1 . 0 1          i parses "1" -> 1, then "01" -> 1
version2: 1 . 0 0 1        j parses "1" -> 1, then "001" -> 1
          ^   ^-----^      pointers land on the same dot boundaries; both run out -> 0
"1.0" vs "1.0.0": after two equal fields i is past the end, yields 0 while j reads "0" -> equal.

Steps
-----
1. i = j = 0.
2. While i < n or j < m: parse x from version1 at i until '.' or end; parse y from version2 at j.
3. If x != y: return -1 or 1.
4. i += 1; j += 1 to skip the dots (harmless past the end).
5. Return 0.

Complexity: O(n + m) time, O(1) space — each character is read once, two integer accumulators.
Pitfalls: comparing chunks as strings ("01" vs "1"); forgetting the missing-revision-is-zero
          rule; advancing past the dot before parsing (skips the first digit).
"""


class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        i = j = 0
        n, m = len(version1), len(version2)
        while i < n or j < m:
            x = 0
            while i < n and version1[i] != ".":
                x = x * 10 + int(version1[i])
                i += 1
            y = 0
            while j < m and version2[j] != ".":
                y = y * 10 + int(version2[j])
                j += 1
            if x != y:
                return -1 if x < y else 1
            i += 1                                   # skip the dot (no-op past the end)
            j += 1
        return 0


def brute_force(version1: str, version2: str) -> int:
    """Split both, pad with zeros, convert every chunk, then compare the lists."""
    a = [int(c) for c in version1.split(".")]
    b = [int(c) for c in version2.split(".")]
    k = max(len(a), len(b))
    a += [0] * (k - len(a))
    b += [0] * (k - len(b))
    return (a > b) - (a < b)


if __name__ == "__main__":
    sol = Solution()
    assert sol.compareVersion("1.01", "1.001") == 0
    assert sol.compareVersion("1.0", "1.0.0") == 0
    assert sol.compareVersion("0.1", "1.1") == -1
    assert sol.compareVersion("1.0.1", "1") == 1
    assert sol.compareVersion("7.5.2.4", "7.5.3") == -1
    assert sol.compareVersion("1", "1.0.0.0.0") == 0          # edge: many trailing zeros
    cases = [("1.01", "1.001"), ("1.0", "1.0.0"), ("0.1", "1.1"), ("1.0.1", "1"),
             ("7.5.2.4", "7.5.3"), ("1", "1.0.0.0.0"), ("1.2", "1.10"), ("0", "0.0")]
    for v1, v2 in cases:
        assert sol.compareVersion(v1, v2) == brute_force(v1, v2), (v1, v2)
    print("ok")
