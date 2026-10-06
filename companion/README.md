# Brute to Optimal: code files

One runnable file per problem, in the book's reading order. Each file has a brute force and the optimal
solution written in plain Python, and two demos at the bottom that print the same answers. Run a file with
`python3 companion/<chapter>/<problem>.py`, change the inputs, run again. Format: `site/companion/SPEC.md`.
`fundamentals/` holds the data structure operations and classic algorithms (sorting, BFS/DFS, topological
sort, union find, Kruskal, Prim, Dijkstra, heaps, tries, KMP ...) in the same style, one algorithm per file.

## Fundamentals

### Arrays and Hashing

- [Insertion Sort](fundamentals/sorting/01_insertion_sort.py) · take the next element, shift larger prefix elements one slot right, fill the gap
- [Merge Sort](fundamentals/sorting/02_merge_sort.py) · split in half, sort each half recursively, merge two sorted runs, left wins ties
- [Quick Sort](fundamentals/sorting/03_quick_sort.py) · Lomuto partition around the last element, swap the pivot to its final slot, recurse
- [Heap Sort](fundamentals/sorting/04_heap_sort.py) · heapify into a max-heap, swap the root with the last heap slot, sift the root down
- [Counting Sort and Bucket Sort](fundamentals/sorting/05_counting_and_bucket_sort.py) · count by value, emit each value count times, bucket by int(x * n), sort buckets
- [Python Sort Keys and Stability](fundamentals/sorting/06_python_sort_keys_and_stability.py) · tuple key, negate a field to flip it, two stable passes with the minor key first

### Stacks

- [Array Stack and Queue via Two Stacks](fundamentals/stacks/01_array_stack_and_queue_via_two_stacks.py) · push, pop, peek, drain inbox into outbox only when outbox is empty
- [Asteroid Collision](fundamentals/stacks/05_asteroid_collision.py) · push right-movers, fight the top while top > 0 and current < 0, pop the loser
- [Next Greater Element](fundamentals/monotonic_stacks/01_next_greater_element.py) · pop while top < current, record answer for popped, push current
- [Previous Smaller Element](fundamentals/monotonic_stacks/02_previous_smaller_element.py) · pop while top >= current, answer is the survivor under the current, push current
- [Online Stock Span](fundamentals/monotonic_stacks/03_online_stock_span.py) · pop while top price <= today, add the popped span to today's, push (price, span)
- [Sum of Subarray Minimums](fundamentals/monotonic_stacks/04_sum_of_subarray_minimums.py) · pop while top >= current (or at the sentinel), count the popped index's subarrays
- [Remove K Digits](fundamentals/monotonic_stacks/05_remove_k_digits.py) · pop while top > digit and k remains, push digit, cut the end, strip leading zeros

### Binary Search

- [Binary Search Variants](fundamentals/searches/01_binary_search_variants.py) · mid = (lo + hi) // 2, keep the half that can hold the answer, lower/upper bound
- [Capacity To Ship Packages Within D Days](fundamentals/searches/02_binary_search_on_answer.py) · monotone can_ship(cap), search [max, sum], hi = mid if feasible else lo = mid + 1

### Linked Lists

- [Build, Print, Insert, Delete](fundamentals/linked_lists/01_build_print_insert_delete.py) · walk index steps from a dummy, splice a node in, unlink the first node with val
- [Reverse a Linked List, Iterative and Recursive](fundamentals/linked_lists/02_reverse_iterative_and_recursive.py) · save next before you cut, point cur back to prev, advance both, hang head behind
- [Middle of the Linked List with Fast and Slow Pointers](fundamentals/linked_lists/03_middle_with_fast_and_slow.py) · slow moves one, fast moves two, stop when fast or fast.next is None
- [Detect a Cycle with Floyd's Tortoise and Hare](fundamentals/linked_lists/04_detect_cycle_floyd.py) · slow and fast meet inside the cycle, reset one pointer to head, step both by one
- [Reverse Nodes in k-Group](fundamentals/linked_lists/07_reverse_nodes_in_k_group.py) · probe k ahead, reverse one group with the next group as prev, re-hook, advance

### Trees

- [Tree Traversals, Recursive and Iterative](fundamentals/trees/01_traversals_recursive_and_iterative.py) · visit before/between/after the children, push right then left, push-left-then-pop
- [Level Order and Height](fundamentals/trees/02_bfs_level_order_and_height.py) · range(len(queue)) drains one level, popleft, push children, levels count as height
- [BST Insert, Search, Delete](fundamentals/trees/03_bst_insert_search_delete.py) · descend by comparison, attach a leaf, splice out a 0/1-child node, successor swap
- [Balanced Binary Tree](fundamentals/trees/04_balanced_and_depth.py) · post-order height, pass -1 upward as soon as a subtree fails, abs(left - right) > 1
- [Serialize and Deserialize Binary Tree](fundamentals/trees/06_serialize_and_deserialize.py) · preorder emit, '#' for None, consume tokens from one queue, build left then right

### Tries

- [Trie: Delete a Word with Pruning](fundamentals/tries/02_trie_delete.py) · path down, clear end flag, prune empty non-end nodes upward, stop at a shared node
- [Autocomplete: Collect Words with a Prefix](fundamentals/tries/03_autocomplete_collect_words_with_prefix.py) · walk to the prefix node, DFS below in sorted child order, emit at each end flag

### Heaps and Priority Queues

- [Heapify by Hand](fundamentals/heaps/01_heapify_by_hand.py) · sift down from last parent to root, pick the smaller child, swap while child < node
- [Heap Push and Pop by Hand](fundamentals/heaps/02_push_and_pop_by_hand.py) · push: append, float up via (i-1)//2; pop: last to root, sink to the smaller child
- [Top K Largest with a Size-k Min-Heap](fundamentals/heaps/03_top_k_with_size_k_min_heap.py) · fill to k, compare with the root, heappushpop replaces it, root is the k-th largest
- [Max-Heap by Negation and Tuples](fundamentals/heaps/04_max_heap_by_negation_and_tuples.py) · push (-priority, arrival, payload), pop and un-negate, arrival breaks ties
- [Heap as a Sorted Stream (Traced)](fundamentals/heaps/05_heap_as_a_sorted_stream.py) · push at a leaf then sift up, pop the root then sift the last leaf down, pull k or pull all
- [Merge K Sorted Arrays](fundamentals/heaps/06_merge_k_sorted_arrays.py) · seed heap with each head (value, array, index), pop the min, push that array's next

### Backtracking

- [Subsets With Duplicates](fundamentals/backtracking/02_subsets_with_duplicates.py) · sort, skip nums[i] == nums[i-1] when i > start, choose, recurse from i+1, unchoose
- [Combinations n Choose k](fundamentals/backtracking/03_combinations_n_choose_k.py) · choose i, recurse from i + 1, prune when numbers left < open slots, unchoose
- [Permutations With Duplicates](fundamentals/backtracking/06_permutations_with_duplicates.py) · sort, skip nums[i] == nums[i-1] unless used[i-1], mark, choose, unmark, unchoose

### Graphs

- [Shortest Path in a 0/1 Grid](fundamentals/searches/03_bfs_grid_shortest_path.py) · queue of cells, mark visited when enqueued, four directions with a bounds check
- [Graph DFS, Recursive and Iterative](fundamentals/searches/04_dfs_recursive_and_iterative.py) · visited set, recurse into unvisited neighbours, stack with neighbours reversed
- [Connected Components](fundamentals/searches/05_connected_components.py) · adjacency list from edges (both directions), BFS from every unvisited node, count
- [01 Matrix](fundamentals/searches/06_multi_source_bfs_01_matrix.py) · enqueue every source first (distance 0), layer-by-layer BFS, mark when enqueued
- [Adjacency List, BFS and DFS](fundamentals/graphs/01_adjacency_list_bfs_dfs.py) · build adjacency list, BFS with a queue and a visited set, DFS with a stack
- [Topological Sort: Kahn and DFS](fundamentals/graphs/02_topological_sort_kahn_and_dfs.py) · count indegrees, queue of indegree-0 nodes, decrement on removal, cycle by count
- [Union-Find (Disjoint Set Union)](fundamentals/graphs/03_union_find.py) · find with path compression, union by size, connected query, component count
- [Kruskal's Minimum Spanning Tree](fundamentals/graphs/04_kruskal_mst.py) · sort edges by weight, union-find accept/reject, stop at n-1 edges
- [Prim's Minimum Spanning Tree](fundamentals/graphs/05_prim_mst.py) · heap of (weight, node, parent), skip a popped node already in the tree, push edges
- [Dijkstra's Shortest Paths](fundamentals/graphs/06_dijkstra.py) · heap of (dist, node), skip stale entries, relax out-edges, final when popped

### Bit Manipulation

- [Get, Set, Clear and Toggle a Bit](fundamentals/bits/01_get_set_clear_toggle_bits.py) · mask = 1 << i, n | mask sets, n & ~mask clears, n ^ mask toggles, n >> i & 1 reads
- [Count Set Bits and the Lowest Set Bit](fundamentals/bits/02_count_bits_and_lowest_set_bit.py) · n & (n-1) drops lowest set bit, n & -n isolates it, power of two iff that leaves 0
- [XOR Tricks: Single Number and Missing Number](fundamentals/bits/03_xor_tricks_single_number_missing_number.py) · xor cancels pairs, xor indices 0..n finds the missing, lowest bit of a^b splits two
- [Bitmask Subset Enumeration](fundamentals/bits/04_bitmask_subset_enumeration.py) · masks 0..2^n-1 = subsets, mask >> i & 1 tests item i, (sub-1) & mask = next submask
- [Reverse Bits and Shifts](fundamentals/bits/05_reverse_bits_and_shifts.py) · bit = n & 1, result = result << 1 | bit, n >>= 1, & 0xFFFFFFFF makes >> logical

### Math and Geometry

- [GCD and LCM with Euclid's Algorithm](fundamentals/math/01_gcd_lcm_euclid.py) · (a, b) -> (b, a % b) until b == 0, lcm = |a| // gcd * |b|
- [Primes: Trial Division and the Sieve of Eratosthenes](fundamentals/math/02_primes_sieve_and_primality.py) · trial divide while d * d <= n, cross off multiples of p from p * p, keep survivors
- [Fast Power and Modular Arithmetic](fundamentals/math/03_fast_power_and_modular_arithmetic.py) · exp & 1 reads the current bit, base = base * base, exp >>= 1, reduce products mod m
- [Reverse Integer and Palindrome Number](fundamentals/math/04_digits_reverse_integer_and_palindrome_number.py) · digit = n % 10 and n //= 10, rev = rev * 10 + digit, 32-bit check, reverse half
- [Base Conversion and Excel Column Titles](fundamentals/math/05_base_conversion_and_excel_columns.py) · n % b and n // b peel the lowest digit, Horner n = n * b + digit, n - 1 for A..Z
- [Random Pick and Reservoir Sampling](fundamentals/math/06_random_pick_and_reservoir_sampling.py) · keep the first k, item i replaces slot j = randrange(i + 1) when j < k, k = 1 pick
- [Search a 2D Matrix II](fundamentals/matrices/04_search_2d_matrix_staircase.py) · start at the top-right corner, move left when too big, move down when too small
- [Game of Life In Place](fundamentals/matrices/05_game_of_life_in_place.py) · count 8 neighbors with & 1, store the next state in bit 1, decode with >> 1
- [Matrix Traversal Patterns](fundamentals/matrices/06_matrix_traversal_patterns.py) · row-major and column-major walks, anti-diagonals by r + c, 4/8 direction vectors

### Strings: Scanning, Parsing, Canonical Forms

- [Two Pointer Palindromes and Reverse Words](fundamentals/strings/02_two_pointer_palindromes_and_reverse_words.py) · lo/hi pointers skipping non-alphanumerics, compare lowercase, reverse a range
- [KMP Prefix Function](fundamentals/strings/03_kmp_prefix_function.py) · build the failure table, fall back with fail[k - 1] on a mismatch, extend on match
- [Rabin-Karp Rolling Hash](fundamentals/strings/04_rabin_karp_rolling_hash.py) · polynomial hash of a window, roll it by dropping the left char, adding the right
- [Encode and Decode Strings](fundamentals/strings/05_encode_decode_strings_and_join.py) · length-prefix each string, collect parts in a list, join once, read length, slice

## Problems

### Arrays and Hashing

1. [Two Sum](arrays_hashing/two_sum.py) · LC 1 · Easy · Hash map complement lookup
2. [Majority Element](arrays_hashing/majority_element.py) · LC 169 · Easy · Boyer-Moore voting
3. [Valid Sudoku](arrays_hashing/valid_sudoku.py) · LC 36 · Medium · Hash set per row/column/box
4. [Group Anagrams](arrays_hashing/group_anagrams.py) · LC 49 · Medium · Canonical key bucketing
5. [Top K Frequent Elements](arrays_hashing/top_k_frequent_elements.py) · LC 347 · Medium · Frequency count + bucket sort
6. [Product of Array Except Self](arrays_hashing/product_of_array_except_self.py) · LC 238 · Medium · Prefix and suffix accumulation
7. [Longest Consecutive Sequence](arrays_hashing/longest_consecutive_sequence.py) · LC 128 · Medium · Hash set with sequence-start detection
8. [Subarray Sum Equals K](arrays_hashing/subarray_sum_equals_k.py) · LC 560 · Medium · Prefix sum + hash map of counts

### Two Pointers

1. [Valid Palindrome](two_pointers/valid_palindrome.py) · LC 125 · Easy · Converging two pointers
2. [Move Zeroes](two_pointers/move_zeroes.py) · LC 283 · Easy · Read/write pointers (stable compaction)
3. [Sort Colors](two_pointers/sort_colors.py) · LC 75 · Medium · Dutch national flag (three-way partition)
4. [Two Sum II - Input Array Is Sorted](two_pointers/two_sum_ii_input_array_is_sorted.py) · LC 167 · Medium · Converging two pointers on sorted input
5. [3Sum](two_pointers/three_sum.py) · LC 15 · Medium · Sort + fixed element + converging two pointers
6. [Container With Most Water](two_pointers/container_with_most_water.py) · LC 11 · Medium · Converging two pointers, move the limiting side

### Sliding Window

1. [Best Time to Buy and Sell Stock](sliding_window/best_time_to_buy_and_sell_stock.py) · LC 121 · Easy · Running minimum sweep
2. [Minimum Size Subarray Sum](sliding_window/minimum_size_subarray_sum.py) · LC 209 · Medium · Variable-size sliding window
3. [Longest Substring Without Repeating Characters](sliding_window/longest_substring_without_repeating_characters.py) · LC 3 · Medium · Variable-size sliding window
4. [Max Consecutive Ones III](sliding_window/max_consecutive_ones_iii.py) · LC 1004 · Medium · Variable-size sliding window
5. [Longest Repeating Character Replacement](sliding_window/longest_repeating_character_replacement.py) · LC 424 · Medium · Variable-size sliding window

### Stacks

1. [Valid Parentheses](stack/valid_parentheses.py) · LC 20 · Easy · Stack matching
2. [Min Stack](stack/min_stack.py) · LC 155 · Medium · Stack with auxiliary state
3. [Evaluate Reverse Polish Notation](stack/evaluate_reverse_polish_notation.py) · LC 150 · Medium · Stack evaluation
4. [Decode String](stack/decode_string.py) · LC 394 · Medium · Stack of nested contexts
5. [Basic Calculator II](stack/basic_calculator_ii.py) · LC 227 · Medium · Stack evaluation
6. [Daily Temperatures](stack/daily_temperatures.py) · LC 739 · Medium · Monotonic stack
7. [Car Fleet](stack/car_fleet.py) · LC 853 · Medium · Monotonic stack

### Queues and Deques

1. [Implement Queue using Stacks](queues/implement_queue_using_stacks.py) · LC 232 · Easy · Two stacks make a queue (lazy transfer)
2. [Design Circular Queue](queues/design_circular_queue.py) · LC 622 · Medium · Ring buffer (circular array with head and count)
3. [Dota2 Senate](queues/dota2_senate.py) · LC 649 · Medium · Round-robin queues (re-enqueue with index + n)

### Binary Search

1. [Binary Search](binary_search/binary_search.py) · LC 704 · Easy · Binary search on a sorted array
2. [Search Insert Position](binary_search/search_insert_position.py) · LC 35 · Easy · Binary search for a boundary (lower / upper bound)
3. [Find First and Last Position of Element in Sorted Array](binary_search/find_first_and_last_position.py) · LC 34 · Medium · Binary search for a boundary (lower / upper bound)
4. [Search a 2D Matrix](binary_search/search_2d_matrix.py) · LC 74 · Medium · Binary search on a sorted array
5. [Find Minimum in Rotated Sorted Array](binary_search/find_min_rotated_sorted_array.py) · LC 153 · Medium · Binary search on a rotated sorted array
6. [Search in Rotated Sorted Array](binary_search/search_rotated_sorted_array.py) · LC 33 · Medium · Binary search on a rotated sorted array
7. [Koko Eating Bananas](binary_search/koko_eating_bananas.py) · LC 875 · Medium · Binary search on the answer

### Linked Lists

1. [Reverse Linked List](linked_list/reverse_linked_list.py) · LC 206 · Easy · In-place pointer reversal
2. [Merge Two Sorted Lists](linked_list/merge_two_sorted_lists.py) · LC 21 · Easy · Dummy head + two-pointer merge
3. [Add Two Numbers](linked_list/add_two_numbers.py) · LC 2 · Medium · Dummy head + carry
4. [Remove Nth Node From End of List](linked_list/remove_nth_from_end.py) · LC 19 · Medium · Two pointers with fixed gap
5. [Linked List Cycle II](linked_list/linked_list_cycle_ii.py) · LC 142 · Medium · Floyd's tortoise and hare (fast/slow pointers)
6. [Intersection of Two Linked Lists](linked_list/intersection_of_two_linked_lists.py) · LC 160 · Easy · Length alignment, then lockstep walk
7. [Palindrome Linked List](linked_list/palindrome_linked_list.py) · LC 234 · Easy · Find middle + reverse second half + interleave
8. [Copy List with Random Pointer](linked_list/copy_list_with_random_pointer.py) · LC 138 · Medium · Interleaved clone (hash map original -> copy, embedded in the list)

### Trees

1. [Maximum Depth of Binary Tree](trees/maximum_depth_of_binary_tree.py) · LC 104 · Easy · Tree recursion (post-order)
2. [Invert Binary Tree](trees/invert_binary_tree.py) · LC 226 · Easy · Tree recursion (post-order)
3. [Symmetric Tree](trees/symmetric_tree.py) · LC 101 · Easy · Simultaneous tree recursion
4. [Balanced Binary Tree](trees/balanced_binary_tree.py) · LC 110 · Easy · Post-order height with side-channel answer
5. [Diameter of Binary Tree](trees/diameter_of_binary_tree.py) · LC 543 · Easy · Post-order height with side-channel answer
6. [Path Sum II](trees/path_sum_ii.py) · LC 113 · Medium · DFS backtracking with a shared path list
7. [Binary Tree Level Order Traversal](trees/binary_tree_level_order_traversal.py) · LC 102 · Medium · BFS by level (queue snapshot)
8. [Binary Tree Inorder Traversal](trees/binary_tree_inorder_traversal.py) · LC 94 · Easy · Iterative traversal with an explicit stack
9. [Validate Binary Search Tree](trees/validate_binary_search_tree.py) · LC 98 · Medium · DFS with (low, high) bounds
10. [Kth Smallest Element in a BST](trees/kth_smallest_element_in_a_bst.py) · LC 230 · Medium · Iterative in-order traversal with early stop
11. [Lowest Common Ancestor of a BST](trees/lowest_common_ancestor_of_a_bst.py) · LC 235 · Medium · BST ordered descent
12. [Lowest Common Ancestor of a Binary Tree](trees/lowest_common_ancestor_of_a_binary_tree.py) · LC 236 · Medium · Post-order "found below me" recursion
13. [Construct Binary Tree from Preorder and Inorder Traversal](trees/construct_binary_tree_from_preorder_and_inorder_traversal.py) · LC 105 · Medium · Recursive tree construction with index map

### Tries

1. [Implement Trie (Prefix Tree)](tries/implement_trie_prefix_tree.py) · LC 208 · Medium · Trie (prefix tree)
2. [Design Add and Search Words Data Structure](tries/design_add_and_search_words_data_structure.py) · LC 211 · Medium · Trie with wildcard DFS

### Heaps and Priority Queues

1. [Kth Largest Element in a Stream](heap/kth_largest_element_in_a_stream.py) · LC 703 · Easy · Size-k heap (keep the k best)
2. [Kth Largest Element in an Array](heap/kth_largest_element_in_an_array.py) · LC 215 · Medium · Quickselect (partition, recurse one side)
3. [K Closest Points to Origin](heap/k_closest_points_to_origin.py) · LC 973 · Medium · Size-k heap (keep the k best)
4. [Task Scheduler](heap/task_scheduler.py) · LC 621 · Medium · Max-heap + cooldown queue simulation
5. [Reorganize String](heap/reorganize_string.py) · LC 767 · Medium · Greedy most-frequent-first with a max-heap

### Backtracking

1. [Subsets](backtracking/subsets.py) · LC 78 · Medium · Backtracking include/exclude decision tree
2. [Permutations](backtracking/permutations.py) · LC 46 · Medium · Backtracking with a used-set
3. [Combination Sum](backtracking/combination_sum.py) · LC 39 · Medium · Backtracking with start index and sum pruning
4. [Combination Sum II](backtracking/combination_sum_ii.py) · LC 40 · Medium · Backtracking with sort + skip-duplicates-at-same-depth
5. [Generate Parentheses](backtracking/generate_parentheses.py) · LC 22 · Medium · Backtracking with validity-preserving constraints (open/close counts)
6. [Word Search](backtracking/word_search.py) · LC 79 · Medium · Grid DFS backtracking with in-place visited marking

### Graphs

1. [Flood Fill](graphs/flood_fill.py) · LC 733 · Easy · Grid flood fill (DFS/BFS)
2. [Number of Islands](graphs/number_of_islands.py) · LC 200 · Medium · Grid flood fill (DFS/BFS)
3. [Rotting Oranges](graphs/rotting_oranges.py) · LC 994 · Medium · Multi-source BFS (level = distance)
4. [Pacific Atlantic Water Flow](graphs/pacific_atlantic_water_flow.py) · LC 417 · Medium · Multi-source reverse BFS/DFS from the boundary
5. [Clone Graph](graphs/clone_graph.py) · LC 133 · Medium · Graph traversal with old->new node map
6. [Course Schedule](graphs/course_schedule.py) · LC 207 · Medium · Topological sort (Kahn's BFS) / cycle detection
7. [Number of Connected Components in an Undirected Graph](graphs/number_of_connected_components.py) · LC 323 · Medium · Union-Find (disjoint set union)
8. [Redundant Connection](graphs/redundant_connection.py) · LC 684 · Medium · Union-Find (disjoint set union)
9. [Network Delay Time](graphs/network_delay_time.py) · LC 743 · Medium · Dijkstra (min-heap shortest paths)
10. [Min Cost to Connect All Points](graphs/min_cost_to_connect_all_points.py) · LC 1584 · Medium · Minimum spanning tree (Prim's with heap)

### Intervals and Sweep Lines

1. [Merge Intervals](intervals/merge_intervals.py) · LC 56 · Medium · Sort by start, sweep and merge
2. [Insert Interval](intervals/insert_interval.py) · LC 57 · Medium · Sort by start, sweep and merge
3. [Non-overlapping Intervals](intervals/non_overlapping_intervals.py) · LC 435 · Medium · Greedy by earliest end (interval scheduling)
4. [Meeting Rooms II](intervals/meeting_rooms_ii.py) · LC 253 · Medium · Sort by start + min-heap of end times

### Greedy

1. [Maximum Subarray](greedy/maximum_subarray.py) · LC 53 · Medium · Greedy running sum (Kadane)
2. [Jump Game](greedy/jump_game.py) · LC 55 · Medium · Greedy reach (furthest reachable index)
3. [Jump Game II](greedy/jump_game_ii.py) · LC 45 · Medium · Greedy reach (furthest reachable index)
4. [Gas Station](greedy/gas_station.py) · LC 134 · Medium · Greedy running sum with restart
5. [Partition Labels](greedy/partition_labels.py) · LC 763 · Medium · Greedy interval merging by last occurrence

### Bit Manipulation

1. [Number of 1 Bits](bit_manipulation/number_of_1_bits.py) · LC 191 · Easy · Clear lowest set bit (n & (n - 1))
2. [Counting Bits](bit_manipulation/counting_bits.py) · LC 338 · Easy · Reuse the count of i >> 1
3. [Reverse Bits](bit_manipulation/reverse_bits.py) · LC 190 · Easy · Bit-by-bit shift and accumulate
4. [Single Number](bit_manipulation/single_number.py) · LC 136 · Easy · XOR cancellation
5. [Missing Number](bit_manipulation/missing_number.py) · LC 268 · Easy · XOR cancellation

### Math and Geometry

1. [Rotate Image](math_geometry/rotate_image.py) · LC 48 · Medium · Transpose + reverse rows (in-place matrix rotation)
2. [Spiral Matrix](math_geometry/spiral_matrix.py) · LC 54 · Medium · Shrinking boundary traversal
3. [Set Matrix Zeroes](math_geometry/set_matrix_zeroes.py) · LC 73 · Medium · In-place markers (reuse first row/column as flags)

### Strings: Scanning, Parsing, Canonical Forms

1. [Valid Anagram](strings/valid_anagram.py) · LC 242 · Easy · Fixed-alphabet frequency count
2. [String to Integer (atoi)](strings/string_to_integer_atoi.py) · LC 8 · Medium · Single-pass state machine with early clamp
3. [Simplify Path](strings/simplify_path.py) · LC 71 · Medium · Stack simulation
4. [Minimum Remove to Make Valid Parentheses](strings/minimum_remove_to_make_valid_parentheses.py) · LC 1249 · Medium · Stack matching
5. [Longest Palindromic Substring](strings/longest_palindromic_substring.py) · LC 5 · Medium · Expand around center

### Design: Implement a Tracker

1. [Moving Average from Data Stream](design/moving_average_from_data_stream.py) · LC 346 · Easy · Sliding window queue with running sum
2. [Logger Rate Limiter](design/logger_rate_limiter.py) · LC 359 · Easy · Hash map of next-allowed timestamps
3. [Design HashMap](design/design_hashmap.py) · LC 706 · Easy · Separate chaining with load-factor resizing
4. [Insert Delete GetRandom O(1)](design/insert_delete_getrandom_o1.py) · LC 380 · Medium · Array + index map (swap-with-last delete)
5. [Time Based Key-Value Store](design/time_based_key_value_store.py) · LC 981 · Medium · Sorted version list + binary search
6. [LRU Cache](design/lru_cache.py) · LC 146 · Medium · Hash map + doubly linked list
