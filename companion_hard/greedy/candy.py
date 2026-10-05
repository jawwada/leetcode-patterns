"""
Candy (LeetCode 135) - Hard
Chapter: greedy
Pattern: Two-pass greedy (left-to-right, right-to-left)

Children stand in a line with ratings. Each child gets at least one candy, and a child rated
higher than an immediate neighbour must get more candies than that neighbour. Return the
minimum total number of candies.
Example: ratings = [1,0,2] -> 5 (candies [2,1,2]); ratings = [1,2,2] -> 4 (candies [1,2,1]).
"""


# --- brute force ---
def brute_force(ratings):
    """Give one each, then sweep raising any child below a lower-rated neighbour. O(n^2)."""
    n = len(ratings)
    candies = [1] * n
    changed = True
    while changed:                                # repeat until a full sweep fixes nothing
        changed = False
        for i in range(n):
            for j in (i - 1, i + 1):
                if 0 <= j < n and ratings[i] > ratings[j] and candies[i] <= candies[j]:
                    candies[i] = candies[j] + 1   # one step of the fix; the rest ripples later
                    changed = True
    return sum(candies)


# --- optimal ---
def candy(ratings):
    """One pass left to right for rises, one right to left for falls, take the max. O(n)."""
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):                         # "more than my left neighbour"
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):                # "more than my right neighbour"
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)   # max keeps the first pass true
    return sum(candies)


# --- try the brute force ---
print(brute_force([1, 0, 2]))           # -> 5
print(brute_force([1, 2, 2]))           # -> 4
print(brute_force([5, 4, 3, 2, 1]))     # -> 15
print(brute_force([1, 3, 2, 2, 1]))     # -> 7


# --- try the optimal ---
print(candy([1, 0, 2]))                 # -> 5
print(candy([1, 2, 2]))                 # -> 4
print(candy([5, 4, 3, 2, 1]))           # -> 15
print(candy([1, 3, 2, 2, 1]))           # -> 7
