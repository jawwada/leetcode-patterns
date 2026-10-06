"""
Merge Intervals (LeetCode 56)
Merge all overlapping intervals.
  [[1,3],[2,6],[8,10],[15,18]]  ->  [[1,6],[8,10],[15,18]]

Idea: after sorting by start, overlapping intervals sit next to each other.
      Sweep once: each interval either overlaps the last merged one (extend it) or starts a new one.

Pseudocode:
  sort by start
  merged = [first]
  for start, end in the rest:
      if start <= merged[-1].end: merged[-1].end = max(merged[-1].end, end)
      else: merged.append([start, end])

Time O(n log n), space O(n).
"""


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda iv: iv[0])     # sort by start
    merged = [list(intervals[0])]
    for start, end in intervals[1:]:
        last = merged[-1]
        if start <= last[1]:                     # overlaps: extend the end
            last[1] = max(last[1], end)
        else:                                    # gap: open a new interval
            merged.append([start, end])
    return merged


if __name__ == "__main__":
    print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1, 6], [8, 10], [15, 18]]
    print(merge_intervals([[1, 4], [4, 5]]))                     # [[1, 5]]
