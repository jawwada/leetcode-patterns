"""
Super Washing Machines (LeetCode 517) - Hard
Chapter: greedy
Pattern: Prefix-sum flow bound

n washing machines in a row hold machines[i] dresses. In one move you may pick any number of
machines and have each pass one dress to an adjacent machine, all at the same time. Return the
minimum number of moves to make every machine hold the same count, or -1 if impossible.
Example: [1,0,5] -> 3 ([1,0,5] -> [1,1,4] -> [2,1,3] -> [2,2,2]); [0,3,0] -> 2; [0,2,0] -> -1.
"""
from collections import deque        # popleft is O(1)
from itertools import product        # one choice per machine: -1 left, 0 stay, +1 right


# --- brute force ---
def brute_force(machines):
    """BFS over states; one move = every machine passes 0 or 1 dress to a neighbour. Exponential"""
    n = len(machines)
    if sum(machines) % n != 0:
        return -1
    goal = tuple([sum(machines) // n] * n)
    start = tuple(machines)
    distance = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current == goal:
            return distance[current]              # BFS: the first time we see the goal is shortest
        for choice in product([-1, 0, 1], repeat=n):
            next_state = apply_move(current, choice)
            if next_state is not None and next_state not in distance:
                distance[next_state] = distance[current] + 1
                queue.append(next_state)
    return -1


def apply_move(state, choice):
    """Every machine i passes one dress in direction choice[i]; None if an empty one tries to."""
    n = len(state)
    result = list(state)
    for i in range(n):
        direction = choice[i]
        if direction == 0 or not 0 <= i + direction < n:
            continue
        if state[i] == 0:
            return None                           # an empty machine has nothing to pass
        result[i] -= 1
        result[i + direction] += 1
    return tuple(result)


# --- optimal ---
def super_washing_machines(machines):
    """Answer = max over machines of |dresses crossing its right boundary| and its excess. O(n)."""
    total = sum(machines)
    n = len(machines)
    if total % n != 0:
        return -1
    target = total // n
    best = 0
    balance = 0                                   # net dresses that must cross to the right here
    for load in machines:
        excess = load - target
        balance += excess
        # one dress per move crosses a boundary; a machine gives away one dress per move;
        # a short machine is no bound because it can receive from both sides at once
        best = max(best, abs(balance), excess)
    return best


# --- try the brute force ---
print(brute_force([1, 0, 5]))         # -> 3
print(brute_force([0, 3, 0]))         # -> 2
print(brute_force([0, 2, 0]))         # -> -1
print(brute_force([3, 0, 3]))         # -> 1


# --- try the optimal ---
print(super_washing_machines([1, 0, 5]))   # -> 3
print(super_washing_machines([0, 3, 0]))   # -> 2
print(super_washing_machines([0, 2, 0]))   # -> -1
print(super_washing_machines([3, 0, 3]))   # -> 1
