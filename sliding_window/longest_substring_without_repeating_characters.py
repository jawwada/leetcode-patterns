"""
Longest Substring Without Repeating Characters (LeetCode 3)  — Medium
Pattern: Variable-size sliding window

Problem
-------
Given a string s, return the length of the longest substring with all distinct characters.
Example: s = "abcabcbb" -> 3 ("abc"); s = "pwwkew" -> 3 ("wke"); s = "bbbbb" -> 1.

Brute force
-----------
For every start index i, extend j to the right while the characters stay distinct (tracked
in a set), recording the length. O(n^2) time, O(min(n, alphabet)) space. The wasted work:
after start i fails at position j, start i+1 rebuilds the set from scratch even though
s[i+1..j-1] is already known to be distinct.

From brute force to optimal
---------------------------
The redundancy is re-verifying a stretch we already proved distinct. Observation: if the
window s[left..right] is distinct and s[right+1] duplicates s[p] (left <= p <= right), then
every window starting at or before p is doomed, so left can jump straight to p+1. That
requires knowing p instantly: store last[ch] = most recent index of ch. With that map the
left edge never moves backwards, giving a single pass where each index is touched O(1) times.

Intuition
---------
Keep the largest duplicate-free window ending at the current position. When the new
character repeats, the only way to restore distinctness is to cut off everything up to and
including the earlier copy, so jump left there in one step.

Geometric view
--------------
An interval [L, R] slides right over the string. R advances one step per iteration; L only
ever jumps forward, landing just past the earlier copy of s[R]. Because both edges move
monotonically, the window sweeps the string in O(n) total.

Steps
-----
1. last = {} (char -> latest index), left = 0, best = 0.
2. For each right, ch: if ch in last and last[ch] >= left, set left = last[ch] + 1.
3. Record last[ch] = right and best = max(best, right - left + 1).
4. Return best.

Complexity: O(n) time, O(min(n, alphabet)) space — each index enters/leaves the window once.
Pitfalls: Forgetting the `last[ch] >= left` guard (a stale index would move left backwards);
using a set with a while-loop shrink but forgetting to remove s[left]; off-by-one in the
window length.
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}                          # char -> most recent index
        left = best = 0
        for right, ch in enumerate(s):
            if ch in last and last[ch] >= left:
                left = last[ch] + 1        # jump past the earlier copy, never backwards
            last[ch] = right
            best = max(best, right - left + 1)
        return best


def brute_force(s: str) -> int:
    best = 0
    for i in range(len(s)):
        seen = set()                       # rebuilt for every start index
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best


if __name__ == "__main__":
    s = Solution()
    cases = ["abcabcbb", "bbbbb", "pwwkew", "", " ", "abba", "dvdf"]
    assert s.lengthOfLongestSubstring("abcabcbb") == 3
    assert s.lengthOfLongestSubstring("bbbbb") == 1
    assert s.lengthOfLongestSubstring("pwwkew") == 3
    assert s.lengthOfLongestSubstring("") == 0
    assert s.lengthOfLongestSubstring("abba") == 2
    for c in cases:
        assert s.lengthOfLongestSubstring(c) == brute_force(c)
    print("ok")
