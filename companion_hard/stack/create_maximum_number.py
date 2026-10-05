"""
Create Maximum Number (LeetCode 321) - Hard
Chapter: stack
Pattern: Monotonic stack + greedy merge

Given two digit arrays nums1 (length m) and nums2 (length n) and k <= m + n, form the
largest k-digit number by taking digits from both arrays while preserving each array's
relative order; return it as a digit list.
Example: nums1 = [3, 4, 6, 5], nums2 = [9, 1, 2, 5, 8, 3], k = 5 -> [9, 8, 6, 5, 3];
nums1 = [6, 7], nums2 = [6, 0, 4], k = 5 -> [6, 7, 6, 0, 4].
"""


# --- brute force ---
def subsequences(nums, t):
    """Every subsequence of nums with exactly t digits, in their original order."""
    if t == 0:
        return [[]]
    if len(nums) < t:
        return []
    result = []
    for rest in subsequences(nums[1:], t - 1):      # keep nums[0]
        result.append([nums[0]] + rest)
    for rest in subsequences(nums[1:], t):          # skip nums[0]
        result.append(rest)
    return result


def interleavings(a, b):
    """Every merge of a and b that keeps the order inside each list."""
    if len(a) == 0 or len(b) == 0:
        return [a + b]
    result = []
    for rest in interleavings(a[1:], b):            # a's head goes first
        result.append([a[0]] + rest)
    for rest in interleavings(a, b[1:]):            # b's head goes first
        result.append([b[0]] + rest)
    return result


def brute_force(nums1, nums2, k):
    """Try every pick from each array and every interleaving; keep the largest. Exponential."""
    best = []
    low = max(0, k - len(nums2))                    # nums2 alone may be too short
    high = min(k, len(nums1))
    for i in range(low, high + 1):                  # i digits from nums1, k - i from nums2
        for pick1 in subsequences(nums1, i):
            for pick2 in subsequences(nums2, k - i):
                for merged in interleavings(pick1, pick2):
                    if merged > best:               # lists compare digit by digit
                        best = merged
    return best


# --- optimal ---
def pick(nums, t):
    """Largest subsequence of length t: pop smaller digits while drops remain. O(n) time."""
    drop = len(nums) - t                            # digits we may still throw away
    stack = []
    for x in nums:
        while drop > 0 and stack and stack[-1] < x:     # a bigger digit wants this slot
            stack.pop()
            drop -= 1
        stack.append(x)
    return stack[:t]                                # trim if the input was increasing


def merge(a, b):
    """Greedy merge: always take from the list whose remaining tail is larger."""
    i = 0
    j = 0
    out = []
    while i < len(a) or j < len(b):
        if a[i:] > b[j:]:                           # compare whole tails, not just heads
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out


def max_number(nums1, nums2, k):
    """For every split, pick the best digits of each array and merge. O(k * (m + n + k^2)) time."""
    best = []
    low = max(0, k - len(nums2))
    high = min(k, len(nums1))
    for i in range(low, high + 1):                  # i digits from nums1, k - i from nums2
        candidate = merge(pick(nums1, i), pick(nums2, k - i))
        if candidate > best:
            best = candidate
    return best


# --- try the brute force ---
print(brute_force([3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5))   # -> [9, 8, 6, 5, 3]
print(brute_force([6, 7], [6, 0, 4], 5))                  # -> [6, 7, 6, 0, 4]
print(brute_force([3, 9], [8, 9], 3))                     # -> [9, 8, 9]


# --- try the optimal ---
print(max_number([3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5))    # -> [9, 8, 6, 5, 3]
print(max_number([6, 7], [6, 0, 4], 5))                   # -> [6, 7, 6, 0, 4]
print(max_number([3, 9], [8, 9], 3))                      # -> [9, 8, 9]
