"""
Max-Heap by Negation and Tuples (basics: heaps)
Given (priority, payload) tasks, return the payloads highest priority first, ties in arrival order.
  [(2, "write"), (5, "deploy"), (2, "test"), (9, "fix prod")]
    ->  ["fix prod", "deploy", "write", "test"]

Idea: heapq only pops the minimum, so push -priority: the biggest priority now pops first.
      Push (-priority, arrival, payload): equal priorities fall back to the arrival counter
      (first in, first out), so the payload itself is never compared (it may be a dict).

Pseudocode:
  for arrival, (priority, payload) in tasks:
      push (-priority, arrival, payload)
  while heap: pop; output its payload

Time O(n log n), space O(n).
"""
import heapq


def highest_priority_first(tasks):
    heap = []
    for arrival, (priority, payload) in enumerate(tasks):
        heapq.heappush(heap, (-priority, arrival, payload))   # negate: max pops first
    order = []
    while heap:
        _, _, payload = heapq.heappop(heap)   # (-priority, arrival, payload)
        order.append(payload)
    return order


if __name__ == "__main__":
    tasks = [(2, "write"), (5, "deploy"), (2, "test"), (9, "fix prod")]
    print(highest_priority_first(tasks))  # ['fix prod', 'deploy', 'write', 'test']
    jobs = [(1, {"id": "a"}), (1, {"id": "b"}), (3, {"id": "c"})]   # dicts can't be compared
    print(highest_priority_first(jobs))   # [{'id': 'c'}, {'id': 'a'}, {'id': 'b'}]
