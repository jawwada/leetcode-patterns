"""
Longest Substring Without Repeating Characters (LeetCode 3)
Return the length of the longest substring with all distinct characters.
  "abcabcbb"  ->  3   ("abc")

Idea: keep a window s[left..right] of distinct characters. Remember each
      character's last index; on a repeat inside the window, jump left just past it.

Pseudocode:
  last = {}                       # char -> last index
  left = 0
  for right, ch in s:
      if ch in last and last[ch] >= left: left = last[ch] + 1
      last[ch] = right
      best = max(best, right - left + 1)

Time O(n), space O(alphabet).
"""


def length_of_longest_substring(s):
    last = {}                            # char -> index of its last occurrence
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:   # repeat inside the window
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))   # 3
    print(length_of_longest_substring("bbbbb"))      # 1
    print(length_of_longest_substring("abba"))       # 2
