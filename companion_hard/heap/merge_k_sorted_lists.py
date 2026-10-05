"""
Merge k Sorted Lists (LeetCode 23) - Hard
Chapter: heap
Pattern: k-way merge with a heap (merge k sorted feeds)

Given an array of k linked lists, each sorted ascending, merge them into one sorted linked
list and return its head.
Example: [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]. Example: [[],[1],[]] -> [1].
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- helpers ---
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values):
    """Python list -> linked list, returns the head (None for an empty list)."""
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def build_lists(arrays):
    """A list of Python lists -> a list of linked-list heads."""
    heads = []
    for values in arrays:
        heads.append(build_list(values))
    return heads


def list_to_array(head):
    """Linked list -> Python list."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


# --- brute force ---
def brute_force(lists):
    """Dump every value into one array, sort it, rebuild a list. O(N log N) time, O(N) space."""
    values = []
    for head in lists:
        node = head
        while node is not None:
            values.append(node.val)
            node = node.next
    values.sort()                      # ignores that each list is already sorted
    return build_list(values)


# --- optimal ---
def merge_k_lists(lists):
    """Min-heap of the k current heads; pop the smallest, push its successor. O(N log k)."""
    heads = list(lists)                # heads[i] = the next unused node of list i
    heap = []                          # (value, list index): the root is the smallest head
    for i in range(len(heads)):
        if heads[i] is not None:
            heapq.heappush(heap, (heads[i].val, i))
    dummy = ListNode(0)
    tail = dummy
    while len(heap) > 0:
        value, i = heapq.heappop(heap)     # the globally smallest remaining node
        node = heads[i]
        tail.next = node
        tail = node
        heads[i] = node.next
        if heads[i] is not None:           # refill the heap from the same list
            heapq.heappush(heap, (heads[i].val, i))
    return dummy.next


# --- try the brute force ---
print(list_to_array(brute_force(build_lists([[1, 4, 5], [1, 3, 4], [2, 6]]))))
# -> [1, 1, 2, 3, 4, 4, 5, 6]
print(list_to_array(brute_force(build_lists([]))))                        # -> []
print(list_to_array(brute_force(build_lists([[], [1], []]))))             # -> [1]
print(list_to_array(brute_force(build_lists([[5], [1, 2, 3], [-1]]))))    # -> [-1, 1, 2, 3, 5]


# --- try the optimal ---
print(list_to_array(merge_k_lists(build_lists([[1, 4, 5], [1, 3, 4], [2, 6]]))))
# -> [1, 1, 2, 3, 4, 4, 5, 6]
print(list_to_array(merge_k_lists(build_lists([]))))                        # -> []
print(list_to_array(merge_k_lists(build_lists([[], [1], []]))))             # -> [1]
print(list_to_array(merge_k_lists(build_lists([[5], [1, 2, 3], [-1]]))))    # -> [-1, 1, 2, 3, 5]
