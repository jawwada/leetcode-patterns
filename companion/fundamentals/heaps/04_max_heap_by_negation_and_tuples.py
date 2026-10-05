"""
Max-Heap by Negation and Tuples - Fundamentals
Chapter: fundamentals/heaps
Key operations: push (-priority, arrival, payload), pop and un-negate, arrival breaks ties

heapq is a min-heap only. To pop the HIGHEST priority first push -priority. To carry a payload
that may not be comparable (a dict, a task object) push the tuple (-priority, arrival, payload):
equal priorities fall back to the arrival counter (first in, first out), so payloads never compare.
Example: [(2, write), (5, deploy), (2, test), (9, fix prod)] -> [fix prod, deploy, write, test]
"""
import heapq   # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def max_push(heap, value):
    """Push the negated value: the smallest negative is the largest original. O(log n)."""
    heapq.heappush(heap, -value)


def max_pop(heap):
    """Pop the smallest negative and un-negate it to get the largest original. O(log n)."""
    return -heapq.heappop(heap)


def pop_in_priority_order(tasks):
    """Push (-priority, arrival, payload): max priority first, FIFO on ties. O(n log n)."""
    heap = []
    arrival = 0
    for priority, payload in tasks:
        heapq.heappush(heap, (-priority, arrival, payload))   # arrival breaks ties, never payload
        arrival += 1
    order = []
    while heap:
        neg_priority, arrival, payload = heapq.heappop(heap)
        order.append(payload)
    return order


# --- try it ---
heap = []
max_push(heap, 3)
max_push(heap, 9)
max_push(heap, 5)
print(heap)            # -> [-9, -3, -5]
print(max_pop(heap))   # -> 9
print(max_pop(heap))   # -> 5
print(pop_in_priority_order([(2, "write"), (5, "deploy"), (2, "test"), (9, "fix prod")]))
# -> ['fix prod', 'deploy', 'write', 'test']
print(pop_in_priority_order([(1, {"id": 1}), (1, {"id": 2})]))   # -> [{'id': 1}, {'id': 2}]
