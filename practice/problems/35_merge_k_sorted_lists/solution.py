"""
Merge k Sorted Lists (LeetCode 23) - Medium-Hard
Area: heap
Key operations: heap of the k current heads as (value, list_index, node_index), pop the smallest, push that list's next element

Given k lists, each sorted ascending, merge them into one sorted list. (Plain Python lists stand
in for the linked lists; node_index plays the role of the node pointer.)
Example: [[1, 4, 5], [1, 3, 4], [2, 6]] -> [1, 1, 2, 3, 4, 4, 5, 6]
"""
import heapq
from typing import List


# --- brute force ---
def brute_force(lists: List[List[int]]) -> List[int]:
    """Concatenate everything and sort. O(N log N) for N values in total: a general sort ignores
    that the input is already k sorted runs and re-compares values whose order is already known."""
    return sorted(v for row in lists for v in row)


# --- optimal ---
def solve(lists: List[List[int]]) -> List[int]:
    """Min-heap of the k current heads as (value, list_index, node_index). Pop the globally smallest
    head, then push the next element of the same list so every list keeps one head in the heap.
    O(N log k) time, O(k) heap space."""
    heap = [(row[0], i, 0) for i, row in enumerate(lists) if row]
    heapq.heapify(heap)
    merged = []
    while heap:
        val, i, j = heapq.heappop(heap)
        merged.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return merged


# --- demo ---
def demo():
    return solve([[1, 4, 5], [1, 3, 4], [2, 6]])


# --- bugs ---
BUGS = [
    {
        "replace": "        if j + 1 < len(lists[i]):",
        "with":    "        if j + 1 <= len(lists[i]):",
        "fix": "advance only while j + 1 is a valid index: strict <",
        "why": "With <= the last element of a list is followed by a push of lists[i][len], an IndexError on every input.",
        "decoys": [
            {"line": "            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))", "change": "should push (lists[i][j], i, j + 1)"},
            {"line": "        merged.append(val)", "change": "should append (val, i)"},
            {"line": "    heapq.heapify(heap)", "change": "should be heap.sort(reverse=True)"},
        ],
    },
    {
        "replace": "    heap = [(row[0], i, 0) for i, row in enumerate(lists) if row]",
        "with":    "    heap = [(row[0], i, 0) for i, row in enumerate(lists)]",
        "fix": "skip empty lists when seeding: they have no head",
        "why": "An empty list has no row[0], so [[]] or [[], [1], []] raises IndexError before merging starts.",
        "decoys": [
            {"line": "        val, i, j = heapq.heappop(heap)", "change": "should be heap.pop(0)"},
            {"line": "    while heap:", "change": "should be while any(lists)"},
            {"line": "        if j + 1 < len(lists[i]):", "change": "should be j < len(lists[i])"},
        ],
    },
    {
        "replace": "        val, i, j = heapq.heappop(heap)",
        "with":    "        val, i, j = heap.pop()",
        "fix": "use heapq.heappop: list.pop() takes the last slot, not the min",
        "why": "The last array slot is an arbitrary head, so values come out in the wrong order: the example yields [2, ...] after popping the wrong list first.",
        "decoys": [
            {"line": "            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))", "change": "should be heap.append(...)"},
            {"line": "    merged = []", "change": "should start as [heap[0][0]]"},
            {"line": "    return merged", "change": "should return sorted(merged)"},
        ],
    },
    {
        "replace": "            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))",
        "with":    "            heapq.heappush(heap, (i, lists[i][j + 1], j + 1))",
        "fix": "the value goes first in the tuple so the heap orders by value",
        "why": "The entry is unpacked as (val, i, j), so the list index and the value swap roles: the example raises IndexError when a value is used as a list index, and the heap would order by list, not value, anyway.",
        "decoys": [
            {"line": "    heap = [(row[0], i, 0) for i, row in enumerate(lists) if row]", "change": "should seed with (row[0], 0, i)"},
            {"line": "        merged.append(val)", "change": "should insert at the front"},
            {"line": "        if j + 1 < len(lists[i]):", "change": "should also require lists[i][j + 1] >= val"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
