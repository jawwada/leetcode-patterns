# (Linked list, Level 2). List 1 -> 2 -> 3.
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.cur = None  # acts as the next pointer

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.cur:
            current = current.cur
        current.cur = new_node
        new_node.prev = current

    def next(self, node):
        """Returns the next node after the given node."""
        if node and node.cur:
            return node.cur
        return None

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.cur
        print(" <-> ".join(elements))

# Create the list 1 -> 2 -> 3
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)

dll.display()

prev, cur = None, dll.head
i = 0
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
    i+=1
    if i==1:
        break
