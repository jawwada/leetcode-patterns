"""
Longest Repeating Character Replacement (LeetCode 424) - Medium
Area: sliding window
Key operations: count the new char, track the max count, shrink while len - max_freq > k, record the window length

Given an uppercase string s and an integer k, you may change at most k characters. Return the
length of the longest substring that can be turned into one repeated letter.
Example: s = "AABABBA", k = 1 -> 4 (change the A in "ABBA" into B: "BBBB")
"""


# --- brute force ---
def brute_force(s: str, k: int) -> int:
    """For every start extend to the right with a letter count; the window works iff its length
    minus its top count is <= k. O(n^2 * 26): every start recounts and every step rescans 26 bins."""
    best = 0
    for i in range(len(s)):
        count = {}
        for j in range(i, len(s)):
            count[s[j]] = count.get(s[j], 0) + 1
            if (j - i + 1) - max(count.values()) <= k:
                best = max(best, j - i + 1)
    return best


# --- optimal ---
def solve(s: str, k: int) -> int:
    """Window s[left..right] with letter counts; it is valid while len - max_freq <= k (the
    non-majority letters are the ones replaced). max_freq never needs to drop: a smaller max
    can only give a shorter window than one already recorded. O(n) time, O(26) space."""
    count = {}
    left = max_freq = best = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        max_freq = max(max_freq, count[ch])
        while right - left + 1 - max_freq > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


# --- demo ---
def demo():
    return solve("AABABBA", 1)


# --- bugs ---
BUGS = [
    {
        "replace": "        while right - left + 1 - max_freq > k:",
        "with":    "        while right - left + 1 - max_freq >= k:",
        "fix": "a window that needs exactly k changes is still valid: shrink only when it needs more than k",
        "why": "With >= the window is shrunk as soon as it needs k changes, so \"AABABBA\" with k = 1 only ever keeps windows of one letter and returns 2 instead of 4.",
        "decoys": [
            {"line": "        max_freq = max(max_freq, count[ch])", "change": "should be recomputed as max(count.values()) after the shrink"},
            {"line": "            left += 1", "change": "should run before the count is decremented"},
            {"line": "        best = max(best, right - left + 1)", "change": "should be inside the while loop"},
        ],
    },
    {
        "replace": "        max_freq = max(max_freq, count[ch])",
        "with":    "        max_freq = count[ch]",
        "fix": "max_freq keeps the largest count seen: max(max_freq, count[ch])",
        "why": "Setting max_freq to the newest letter's count forgets the real majority, so \"AAAAB\" with k = 1 shrinks the window on the B and returns 4 instead of 5.",
        "decoys": [
            {"line": "        count[ch] = count.get(ch, 0) + 1", "change": "should run after the while loop"},
            {"line": "        while right - left + 1 - max_freq > k:", "change": "should be an if"},
            {"line": "    return best", "change": "should return best - k"},
        ],
    },
    {
        "replace": "        while right - left + 1 - max_freq > k:",
        "with":    "        while right - left - max_freq > k:",
        "fix": "the window s[left..right] has right - left + 1 characters",
        "why": "Dropping the +1 under-counts the window length, so windows that need k + 1 changes pass: \"ABCDE\" with k = 1 returns 3 instead of 2.",
        "decoys": [
            {"line": "            count[s[left]] -= 1", "change": "should decrement count[ch]"},
            {"line": "        best = max(best, right - left + 1)", "change": "should be right - left"},
            {"line": "    left = max_freq = best = 0", "change": "max_freq should start at 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
