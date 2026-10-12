"""
Task Scheduler - Frame the Most Frequent Task

Each task takes one unit of time, and two runs of the same task need at least
n units between them; the CPU may idle. Return the fewest units for all tasks:
["A", "A", "A", "B", "B", "B"], n = 2 -> 8 (A B idle A B idle A B).
"""


# --- algorithm ---
def least_interval(tasks, n):
    """The most frequent task frames the schedule. O(len(tasks)) time."""
    counts = {}
    for task in tasks:
        counts[task] = counts.get(task, 0) + 1
    max_count = 0
    for task in counts:
        max_count = max(max_count, counts[task])
    tied = 0                        # tasks that also reach max_count
    for task in counts:
        if counts[task] == max_count:
            tied += 1
    frame = (max_count - 1) * (n + 1) + tied    # full rows, then a last row
    return max(frame, len(tasks))   # overflow: rows widen, no idles


# --- try it ---
print(least_interval(["A", "A", "A", "B", "B", "B"], 2))      # -> 8
print(least_interval(["A", "A", "A", "B", "B", "B"], 0))      # -> 6
print(least_interval(["A", "A", "A", "B", "B", "C"], 2))      # -> 7
overflow = ["A", "A", "A", "B", "B", "B", "C", "C", "D", "D"]
print(least_interval(overflow, 2))                            # -> 10
