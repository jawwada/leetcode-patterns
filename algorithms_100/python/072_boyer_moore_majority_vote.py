"""
Boyer-Moore Majority Vote - Different Votes Cancel in Pairs

Given an array, return the value that appears more than n / 2 times, or None
if no value does, in O(n) time and O(1) extra space:
[2, 2, 1, 1, 1, 2, 2] -> 2.
"""


# --- algorithm ---
def majority_candidate(nums):
    """Pair off different values; only a majority must survive. O(n), O(1)."""
    candidate = None
    count = 0                       # candidate votes not yet cancelled
    for x in nums:
        if count == 0:
            candidate = x           # nobody standing: x takes over
            count = 1
        elif x == candidate:
            count += 1              # one more vote for the candidate
        else:
            count -= 1              # x cancels one candidate vote
    return candidate


def majority_element(nums):
    """Second pass: the candidate wins only with more than n / 2 votes."""
    candidate = majority_candidate(nums)
    votes = 0
    for x in nums:
        if x == candidate:
            votes += 1
    if votes * 2 > len(nums):
        return candidate
    return None                     # no value holds a strict majority


# --- try it ---
print(majority_element([2, 2, 1, 1, 1, 2, 2]))  # -> 2
print(majority_element([3, 2, 3]))              # -> 3
print(majority_candidate([1, 2, 3]))            # -> 3
print(majority_element([1, 2, 3]))              # -> None
print(majority_element([1, 2]))                 # -> None
