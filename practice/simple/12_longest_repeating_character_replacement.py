"""
Longest Repeating Character Replacement (LeetCode 424)
Change at most k letters; return the longest substring that becomes one repeated letter.
  s = "AABABBA", k = 1  ->  4   ("ABBA" -> "BBBB")

Idea: a window is fixable if (length - count of its most common letter) <= k.
      Slide a window right; when it needs more than k changes, shrink from the left.

Pseudocode:
  count = {}, max_freq = 0, left = 0
  for right, ch in s:
      count[ch] += 1; max_freq = max(max_freq, count[ch])
      while window_len - max_freq > k:
          count[s[left]] -= 1; left += 1
      best = max(best, window_len)

Time O(n), space O(26).
"""


def character_replacement(s, k):
    count = {}                            # letter -> count in window
    max_freq = 0                          # most common letter count seen
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1  # add new letter
        max_freq = max(max_freq, count[ch])
        while (right - left + 1) - max_freq > k:   # too many changes needed
            count[s[left]] -= 1           # shrink from the left
            left += 1
        best = max(best, right - left + 1)
    return best


if __name__ == "__main__":
    print(character_replacement("AABABBA", 1))  # 4
    print(character_replacement("ABAB", 2))     # 4
    print(character_replacement("ABCDE", 1))    # 2
