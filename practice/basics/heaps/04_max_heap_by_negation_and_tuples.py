"""
Max-Heap by Negation and Tuples - Basics
Area: heaps
Key operations: push (-priority, arrival, payload), pop and un-negate, tie-break with the arrival counter so payloads are never compared

heapq is a min-heap only. To pop the HIGHEST priority first push -priority. To carry a payload that
may not be comparable (a dict, a task object) push the tuple (-priority, arrival, payload): equal
priorities fall back to the arrival counter (first in, first out) and the payload is never compared.
solve(tasks) takes (priority, payload) pairs and returns the payloads in pop order.
Example: [(2, "write"), (5, "deploy"), (2, "test"), (9, "fix prod")] -> ["fix prod", "deploy", "write", "test"]
"""
import heapq
from typing import Any, List, Tuple


# --- brute force ---
def brute_force(tasks: List[Tuple[int, Any]]) -> List[Any]:
    """Stable sort by priority descending; stability gives first-in-first-out among ties. O(n log n)."""
    return [payload for _, payload in sorted(tasks, key=lambda t: -t[0])]


# --- optimal ---
def solve(tasks: List[Tuple[int, Any]]) -> List[Any]:
    """Push (-priority, arrival, payload); the min-heap then pops the max priority, FIFO on ties. O(n log n)."""
    heap = []
    for arrival, (priority, payload) in enumerate(tasks):
        heapq.heappush(heap, (-priority, arrival, payload))
    order = []
    while heap:
        neg, arrival, payload = heapq.heappop(heap)
        order.append(payload)
    return order


# --- demo ---
def demo():
    return solve([(2, "write"), (5, "deploy"), (2, "test"), (9, "fix prod")])


# --- bugs ---
BUGS = [
    {
        "replace": "        heapq.heappush(heap, (-priority, arrival, payload))",
        "with":    "        heapq.heappush(heap, (-priority, payload))",
        "fix": "keep the arrival counter between priority and payload so ties never compare payloads",
        "why": "Two dict payloads with equal priority make heapq compare the dicts and raise TypeError; with strings, ties come out alphabetically instead of first-in-first-out.",
        "decoys": [
            {"line": "        neg, arrival, payload = heapq.heappop(heap)", "change": "should be heap.pop()"},
            {"line": "        order.append(payload)", "change": "should append -neg"},
            {"line": "    return order", "change": "should return reversed(order)"},
        ],
    },
    {
        "replace": "    for arrival, (priority, payload) in enumerate(tasks):",
        "with":    "    for arrival, (priority, payload) in enumerate(reversed(tasks)):",
        "fix": "number the tasks in the order they arrive so the counter breaks ties first-in-first-out",
        "why": "Reversing the input gives later tasks the smaller counter, so ties pop last-in-first-out: 'test' before 'write'.",
        "decoys": [
            {"line": "        heapq.heappush(heap, (-priority, arrival, payload))", "change": "should push priority without the minus"},
            {"line": "    heap = []", "change": "should be heapq.heapify(tasks)"},
            {"line": "    while heap:", "change": "should be while len(heap) > 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
