"""
Candy - Two Passes: Left, Then Right

Children stand in a line with ratings. Each gets at least one candy, and a
child rated higher than a neighbor gets more candies than that neighbor.
Return the fewest candies in total: [1, 0, 2, 5, 4, 3, 1] -> 15.
"""


# --- algorithm ---
def candy(ratings):
    """Left pass for left neighbors, right pass for right ones. O(n) time."""
    n = len(ratings)
    candies = [1] * n               # everyone gets at least one
    for i in range(1, n):           # left to right
        if ratings[i] > ratings[i - 1]:     # beat a lower left neighbor
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):  # right to left
        if ratings[i] > ratings[i + 1]:     # also beat a lower right neighbor
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)


# --- try it ---
print(candy([1, 0, 2, 5, 4, 3, 1]))     # -> 15
print(candy([1, 0, 2]))                 # -> 5
print(candy([1, 2, 2]))                 # -> 4
print(candy([1, 2, 3, 1]))              # -> 7
