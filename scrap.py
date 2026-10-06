# find the non empty subarry with the largest sum in an array of integers. Return the sum. If all numbers are negative, return smallest negative number. Example: [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> 6 (the subarray [4, -1, 2, 1]).


arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

max_sum = float('-inf')
for i in range(len(arr)):
    for j in range(i, len(arr)):
        if sum(arr[i:j+1]) > max_sum:
            max_sum = sum(arr[i:j+1])
            print(arr[i:j+1], sum(arr[i:j+1]))



# what is the optimal solution for this problem?

# The optimal solution for finding the non-empty subarray with the largest sum in an array of integers is known as Kadane's Algorithm. This algorithm runs in O(n) time and uses O(1) space. The idea is to iterate through the array while keeping track of the maximum sum of the subarray that ends at the current position, and also keeping track of the overall maximum sum found so far.

def kadane(arr):
    max_current = max_global = arr[0]

    for i in range(1, len(arr)):
        max_current = max(arr[i], max_current + arr[i])
        if max_current > max_global:
            max_global = max_current

    return max_global