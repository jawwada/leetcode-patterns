"""
Heap Push and Pop by Hand (basics: heaps)
Implement min-heap push and pop on a plain list without heapq.
  push 5, 3, 8, 1  ->  heap [1, 3, 8, 5];  then pop, pop  ->  1, 3   (heap left: [5, 8])

Idea: the parent of i is (i - 1) // 2, its children 2i+1 and 2i+2. Each operation disturbs one
      element and walks it along one path: push floats the new last leaf UP past bigger parents;
      pop moves the last leaf to the root and sinks it DOWN toward the smaller child.

Pseudocode:
  push(x):  append x; i = last index
            while i > 0:
                parent = (i - 1) // 2
                if heap[parent] <= heap[i]: stop
                swap them; i = parent
  pop():    top = heap[0]; move the last element to the root; i = 0
            while i has a child:
                child = the smaller child
                if heap[i] <= heap[child]: stop
                swap them; i = child
            return top

Time O(log n) per push or pop, space O(1) extra.
"""


def heap_push(heap, x):
    heap.append(x)                       # new leaf at the end
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:      # parent already smaller: done
            break
        heap[i], heap[parent] = heap[parent], heap[i]   # float up one level
        i = parent


def heap_pop(heap):
    top, last = heap[0], heap.pop()      # root is the min; detach the last leaf
    if heap:
        heap[0] = last                   # last leaf fills the hole at the root
    i, n = 0, len(heap)
    while True:
        child = 2 * i + 1
        if child + 1 < n and heap[child + 1] < heap[child]:
            child += 1                   # use the smaller child
        if child >= n or heap[i] <= heap[child]:
            break                        # a leaf, or no bigger than both children
        heap[i], heap[child] = heap[child], heap[i]     # sink one level
        i = child
    return top


if __name__ == "__main__":
    heap = []
    for x in [5, 3, 8, 1]:
        heap_push(heap, x)
    print(heap)                            # [1, 3, 8, 5]
    print(heap_pop(heap), heap_pop(heap))  # 1 3
    print(heap)                            # [5, 8]
