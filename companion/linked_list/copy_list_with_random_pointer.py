"""
Copy List with Random Pointer (LeetCode 138) - Medium
Chapter: linked_list
Pattern: Interleaved clone (hash map original -> copy, embedded in the list)

Each node has val, next and random, where random points to any node in the list or None.
Return a deep copy: new nodes whose next and random pointers point to new nodes with the same
structure, leaving the original intact. Lists are written as [value, index of random] pairs.
Example: [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]] -> an identical but independent list
"""


# --- helpers ---
class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def build_random_list(pairs):
    """pairs[i] = [value, index of the random target or None]. Returns the head."""
    nodes = []
    for pair in pairs:
        nodes.append(Node(pair[0]))
    for i in range(len(nodes)):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if pairs[i][1] is not None:
            nodes[i].random = nodes[pairs[i][1]]
    if len(nodes) == 0:
        return None
    return nodes[0]


def random_list_to_array(head):
    """Back to [[value, index of random or None], ...] so a list can be printed."""
    position = {}                  # node -> its index in this list
    node = head
    i = 0
    while node is not None:
        position[node] = i
        node = node.next
        i += 1
    out = []
    node = head
    while node is not None:
        if node.random is None:
            out.append([node.val, None])
        else:
            out.append([node.val, position[node.random]])
        node = node.next
    return out


# --- brute force ---
def position_of(head, target):
    """How many steps it takes to walk from head to target."""
    steps = 0
    node = head
    while node is not target:
        node = node.next
        steps += 1
    return steps


def node_at(head, steps):
    """The node that many steps after head."""
    node = head
    for _ in range(steps):
        node = node.next
    return node


def brute_force(head):
    """Copy by next, then locate every random target by counting steps. O(n^2) time."""
    dummy = Node()
    tail = dummy
    node = head
    while node is not None:                 # pass 1: copy values and next pointers only
        tail.next = Node(node.val)
        tail = tail.next
        node = node.next
    node = head
    clone = dummy.next
    while node is not None:                 # pass 2: random = the clone at the same position
        if node.random is not None:
            steps = position_of(head, node.random)
            clone.random = node_at(dummy.next, steps)
        node = node.next
        clone = clone.next
    return dummy.next


# --- optimal ---
def copy_list_with_random_pointer(head):
    """Weave each clone right after its original, so clone(X) is X.next. O(n) time, O(1) extra."""
    if head is None:
        return None
    node = head
    while node is not None:                 # pass 1: A -> A' -> B -> B' -> ...
        clone = Node(node.val, node.next)
        node.next = clone
        node = clone.next
    node = head
    while node is not None:                 # pass 2: the clone of X.random is X.random.next
        if node.random is not None:
            node.next.random = node.random.next
        node = node.next.next               # step over the clone
    node = head
    new_head = head.next
    while node is not None:                 # pass 3: unweave the two lists again
        clone = node.next
        node.next = clone.next
        if clone.next is not None:
            clone.next = clone.next.next
        node = node.next
    return new_head


# --- try the brute force ---
original = build_random_list([[7, None], [13, 0], [11, 4], [10, 2], [1, 0]])
copied = brute_force(original)
print(random_list_to_array(copied))      # -> [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
print(random_list_to_array(original))    # -> [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
copied = brute_force(build_random_list([[1, 1], [2, 1]]))
print(random_list_to_array(copied))      # -> [[1, 1], [2, 1]]
copied = brute_force(build_random_list([]))
print(random_list_to_array(copied))      # -> []


# --- try the optimal ---
original = build_random_list([[7, None], [13, 0], [11, 4], [10, 2], [1, 0]])
copied = copy_list_with_random_pointer(original)
print(random_list_to_array(copied))      # -> [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
print(random_list_to_array(original))    # -> [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
copied = copy_list_with_random_pointer(build_random_list([[1, 1], [2, 1]]))
print(random_list_to_array(copied))      # -> [[1, 1], [2, 1]]
copied = copy_list_with_random_pointer(build_random_list([]))
print(random_list_to_array(copied))      # -> []
