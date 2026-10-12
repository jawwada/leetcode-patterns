---
rank: 59
slug: heapify
---

Rearrange an array in place into a min-heap: a complete binary tree stored level by level, in which every parent is at most its children. The children of index `i` sit at `2i + 1` and `2i + 2`, and its parent at `floor((i - 1) / 2)`. `[9, 5, 6, 2, 3, 7, 1]` becomes `[1, 2, 6, 5, 3, 7, 9]`. Then push and pop on that heap by hand.

Pushing the n values one at a time builds a heap in `O(n log n)`. Heapify builds it in `O(n)` by working from the bottom up with sift-down. A node whose two subtrees are already heaps is repaired by swapping it with its smaller child until neither child is smaller, and then its whole subtree is a heap. Leaves are heaps of one value, so start at the last parent, `floor(n / 2) - 1`, and walk back to the root: every node is sifted after both of its subtrees, so they are heaps by the time its turn comes.

A sift-down costs at most the height of its node, the distance to the bottom, and most nodes live near the bottom. Half of them are leaves and cost nothing, a quarter sit one level up and cost at most one swap, an eighth cost at most two, and the sum `n/4 · 1 + n/8 · 2 + n/16 · 3 + …` stays below n. Building by pushes uses sift-up, whose cost is the depth instead, the distance to the top, and the deep nodes are the many: that is where the extra `log n` comes from.

```text
     start            i = 2            i = 1            i = 0
       9                9                9                1
   5       6        5       1        2       1        2       6
 2   3   7   1    2   3   7   6    5   3   7   6    5   3   7   9
[9 5 6 2 3 7 1]  [9 5 1 2 3 7 6]  [9 2 1 5 3 7 6]  [1 2 6 5 3 7 9]
                 6 swaps with 1   5 swaps with 2   9 sinks 2 levels
```

```pseudo
FUNCTION SiftDown(heap, i, n)              // heap[0..n-1] is the heap
    WHILE true
        smallest ← i
        left ← 2 * i + 1
        right ← 2 * i + 2
        IF left < n AND heap[left] < heap[smallest]
            smallest ← left
        IF right < n AND heap[right] < heap[smallest]
            smallest ← right
        IF smallest = i                    // no child is smaller: done
            RETURN
        swap(heap[i], heap[smallest])
        i ← smallest

FUNCTION Heapify(heap)
    n ← len(heap)
    FOR i FROM floor(n / 2) - 1 DOWNTO 0   // last parent, back to the root
        SiftDown(heap, i, n)

FUNCTION SiftUp(heap, i)
    WHILE i > 0
        parent ← floor((i - 1) / 2)
        IF heap[parent] ≤ heap[i]          // the parent is no larger: done
            RETURN
        swap(heap[i], heap[parent])
        i ← parent

FUNCTION HeapPush(heap, value)
    heap.append(value)
    SiftUp(heap, len(heap) - 1)

FUNCTION HeapPop(heap)
    last ← len(heap) - 1
    swap(heap[0], heap[last])
    top ← heap.removeLast()                // remove the last slot: the old root
    SiftDown(heap, 0, len(heap))
    RETURN top
```

Heapify takes `O(n)` time and `O(1)` extra space; push and pop take `O(log n)`, the height of the tree. Push appends the value as the last leaf and sifts it up, swapping with its parent while it is smaller. Pop swaps the root with the last leaf, removes that last slot, which now holds the old minimum, and sifts the new root down. Every heap in this book rests on these two moves, from Top-K (#19) to Heap Sort (#109), which runs the same build as a max-heap. Reach for heapify when all the values are present at the start: Last Stone Weight heapifies the stones once and then only pops and pushes. The classic mistake is running `i` upward from the root instead of backward from the last parent: the root is sifted before its subtrees are heaps, and the example ends as `[5, 2, 1, 9, 3, 7, 6]`, with 5 sitting above 1.

*Practice:* LC 912 Sort an Array · LC 215 Kth Largest Element in an Array · LC 1046 Last Stone Weight
