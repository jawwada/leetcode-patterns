"""
Minimum Window Substring (LeetCode 76)
Return the shortest substring of s that contains every character of t (with counts).
  s = "ADOBECODEBANC", t = "ABC"  ->  "BANC"

Idea: grow the window to the right until it covers t, then shrink from the left
      while it still covers t, recording the smallest. "formed" counts how many
      distinct letters of t currently have enough copies.

Pseudocode:
  need = Counter(t); have = Counter()
  for right, ch in s:
      have[ch] += 1; if have[ch] == need[ch]: formed += 1
      while formed == len(need):
          record window; drop s[left]
          if it falls below need: formed -= 1
          left += 1

Time O(|s| + |t|), space O(alphabet).
"""
from collections import Counter


def min_window(s, t):
    need = Counter(t)
    have = Counter()
    formed = 0                           # letters of t with enough copies
    left = 0
    best_start, best_len = 0, len(s) + 1
    for right, ch in enumerate(s):
        have[ch] += 1                    # expand right
        if ch in need and have[ch] == need[ch]:
            formed += 1
        while formed == len(need):       # window covers t: shrink left
            if right - left + 1 < best_len:
                best_start, best_len = left, right - left + 1
            out = s[left]
            have[out] -= 1
            if out in need and have[out] < need[out]:
                formed -= 1
            left += 1
    return "" if best_len > len(s) else s[best_start:best_start + best_len]


if __name__ == "__main__":
    print(min_window("ADOBECODEBANC", "ABC"))   # BANC
    print(min_window("a", "a"))                 # a
    print(repr(min_window("a", "aa")))          # ''
