# Practice bank

Traced, testable scripts for interview drilling. Run any file for a step-by-step trace, add `--quiet` for tests only.
Format: [SPEC.md](SPEC.md). Build/validate: `python3 practice/build_bank.py`. The drill artifact reads `bank.json`.

## Problems

| # | Problem | Area | Difficulty | Key operations | Bugs |
|---|---|---|---|---|---|
| 01 | [Two Sum](practice/problems/01_two_sum/README.md) (LC 1) · [code](practice/problems/01_two_sum/solution.py) | arrays & hashing | Medium | compute the complement, look it up in a dict, insert after the check, return indices | 3 |
| 02 | [Group Anagrams](practice/problems/02_group_anagrams/README.md) (LC 49) · [code](practice/problems/02_group_anagrams/solution.py) | arrays & hashing | Medium | build a 26-count key per word, append the word to the bucket for that key, return the buckets | 3 |
| 03 | [Product of Array Except Self](practice/problems/03_product_of_array_except_self/README.md) (LC 238) · [code](practice/problems/03_product_of_array_except_self/solution.py) | arrays & hashing | Medium | left sweep stamping prefix products, right sweep multiplying in a running suffix product | 3 |
| 04 | [Longest Consecutive Sequence](practice/problems/04_longest_consecutive_sequence/README.md) (LC 128) · [code](practice/problems/04_longest_consecutive_sequence/solution.py) | arrays & hashing | Medium | put the values in a set, skip x when x - 1 is present, walk x, x+1, x+2, ... while present | 3 |
| 05 | [Subarray Sum Equals K](practice/problems/05_subarray_sum_equals_k/README.md) (LC 560) · [code](practice/problems/05_subarray_sum_equals_k/solution.py) | arrays & hashing | Medium | running prefix sum, count lookup of prefix - k, record the prefix in the count dict | 3 |
| 06 | [3Sum](practice/problems/06_three_sum/README.md) (LC 15) · [code](practice/problems/06_three_sum/solution.py) | two pointers | Medium-Hard | sort, fix the anchor i, converge lo/hi on the suffix, skip equal neighbours | 3 |
| 07 | [Container With Most Water](practice/problems/07_container_with_most_water/README.md) (LC 11) · [code](practice/problems/07_container_with_most_water/solution.py) | two pointers | Medium | pointers at both ends, area = shorter wall * width, move the shorter side inward | 3 |
| 08 | [Trapping Rain Water](practice/problems/08_trapping_rain_water/README.md) (LC 42) · [code](practice/problems/08_trapping_rain_water/solution.py) | two pointers | Medium-Hard | compare the two ends, settle the lower side, update that side's running max, add max - height | 3 |
| 09 | [Longest Substring Without Repeating Characters](practice/problems/09_longest_substring_without_repeating_characters/README.md) (LC 3) · [code](practice/problems/09_longest_substring_without_repeating_characters/solution.py) | sliding window | Medium | expand right, look up the last index of the new char, jump left past it, record the window length | 3 |
| 10 | [Minimum Window Substring](practice/problems/10_minimum_window_substring/README.md) (LC 76) · [code](practice/problems/10_minimum_window_substring/solution.py) | sliding window | Medium-Hard | count what is needed, expand right and bump formed, shrink left while every count is met, record the shortest | 3 |
| 11 | [Sliding Window Maximum](practice/problems/11_sliding_window_maximum/README.md) (LC 239) · [code](practice/problems/11_sliding_window_maximum/solution.py) | sliding window | Medium-Hard | pop back while smaller or equal, push index, pop front when it leaves the window, read the max at the front | 3 |
| 12 | [Longest Repeating Character Replacement](practice/problems/12_longest_repeating_character_replacement/README.md) (LC 424) · [code](practice/problems/12_longest_repeating_character_replacement/solution.py) | sliding window | Medium | count the new char, track the max count, shrink while len - max_freq > k, record the window length | 3 |
| 13 | [Valid Parentheses](practice/problems/13_valid_parentheses/README.md) (LC 20) · [code](practice/problems/13_valid_parentheses/solution.py) | stack | Medium | push an opener, on a closer check the top and pop, empty stack at the end | 3 |
| 14 | [Min Stack](practice/problems/14_min_stack/README.md) (LC 155) · [code](practice/problems/14_min_stack/solution.py) | stack | Medium | push (value, running min), pop the pair, top reads the value, getMin reads the stored min | 3 |
| 15 | [Evaluate Reverse Polish Notation](practice/problems/15_evaluate_reverse_polish_notation/README.md) (LC 150) · [code](practice/problems/15_evaluate_reverse_polish_notation/solution.py) | stack | Medium | push number, pop two operands (right one first), apply operator, push result | 3 |
| 16 | [Daily Temperatures](practice/problems/16_daily_temperatures/README.md) (LC 739) · [code](practice/problems/16_daily_temperatures/solution.py) | monotonic stack | Medium | push index, pop while top is colder, answer = i - popped index | 3 |
| 17 | [Largest Rectangle in Histogram](practice/problems/17_largest_rectangle_in_histogram/README.md) (LC 84) · [code](practice/problems/17_largest_rectangle_in_histogram/solution.py) | monotonic stack | Medium-Hard | push index, pop while top is taller, width from the new top, sentinel 0 flushes the stack | 3 |
| 18 | [Search in Rotated Sorted Array](practice/problems/18_search_in_rotated_sorted_array/README.md) (LC 33) · [code](practice/problems/18_search_in_rotated_sorted_array/solution.py) | binary search | Medium | compute mid, decide which half is sorted, test target against the sorted half, move lo or hi | 3 |
| 19 | [Koko Eating Bananas](practice/problems/19_koko_eating_bananas/README.md) (LC 875) · [code](practice/problems/19_koko_eating_bananas/solution.py) | binary search | Medium | hours(speed) by ceiling division, binary search on the answer, hi = mid when feasible, lo = mid + 1 when not | 3 |
| 20 | [Split Array Largest Sum](practice/problems/20_split_array_largest_sum/README.md) (LC 410) · [code](practice/problems/20_split_array_largest_sum/solution.py) | binary search | Medium-Hard | binary search on the answer (a cap), greedy count of pieces under the cap, hi = mid when pieces <= k | 4 |
| 21 | [Reverse Linked List](practice/problems/21_reverse_linked_list/README.md) (LC 206) · [code](practice/problems/21_reverse_linked_list/solution.py) | linked list | Medium | save nxt, flip cur.next to prev, advance prev and cur, return prev | 3 |
| 22 | [Merge Two Sorted Lists](practice/problems/22_merge_two_sorted_lists/README.md) (LC 21) · [code](practice/problems/22_merge_two_sorted_lists/solution.py) | linked list | Medium | dummy head, tail pointer, attach the smaller front node, advance that list, attach the leftover | 3 |
| 23 | [Linked List Cycle II](practice/problems/23_linked_list_cycle_ii/README.md) (LC 142) · [code](practice/problems/23_linked_list_cycle_ii/solution.py) | linked list | Medium | slow/fast race, meeting check by identity, reset one pointer to head, same-speed walk to the entry | 3 |
| 24 | [LRU Cache](practice/problems/24_lru_cache/README.md) (LC 146) · [code](practice/problems/24_lru_cache/solution.py) | linked list / design | Medium-Hard | dict lookup, unlink a node, push front after sentinel head, evict tail.prev | 3 |
| 25 | [Remove Nth Node From End of List](practice/problems/25_remove_nth_node_from_end/README.md) (LC 19) · [code](practice/problems/25_remove_nth_node_from_end/solution.py) | linked list | Medium | dummy head, open a gap of n+1, slide both pointers, splice slow.next = slow.next.next | 3 |
| 26 | [Binary Tree Level Order Traversal](practice/problems/26_binary_tree_level_order_traversal/README.md) (LC 102) · [code](practice/problems/26_binary_tree_level_order_traversal/solution.py) | trees | Medium | queue of the current level, snapshot len(q), popleft and push children, append the level | 3 |
| 27 | [Validate Binary Search Tree](practice/problems/27_validate_binary_search_tree/README.md) (LC 98) · [code](practice/problems/27_validate_binary_search_tree/solution.py) | trees | Medium | pass down an open window (lo, hi), check lo < val < hi, tighten hi going left and lo going right | 3 |
| 28 | [Kth Smallest Element in a BST](practice/problems/28_kth_smallest_element_in_a_bst/README.md) (LC 230) · [code](practice/problems/28_kth_smallest_element_in_a_bst/solution.py) | trees | Medium | push the left spine, pop the next smallest, count down k, step to the right child | 3 |
| 29 | [Lowest Common Ancestor of a BST](practice/problems/29_lowest_common_ancestor_of_a_bst/README.md) (LC 235) · [code](practice/problems/29_lowest_common_ancestor_of_a_bst/solution.py) | trees | Medium | compare both targets with the node, go left if both smaller, go right if both larger, stop at the split | 3 |
| 30 | [Diameter of Binary Tree](practice/problems/30_diameter_of_binary_tree/README.md) (LC 543) · [code](practice/problems/30_diameter_of_binary_tree/solution.py) | trees | Medium | post-order height, candidate = left + right at every node, nonlocal best | 3 |
| 31 | [Implement Trie (Prefix Tree)](practice/problems/31_implement_trie/README.md) (LC 208) · [code](practice/problems/31_implement_trie/solution.py) | tries | Medium | walk one node per character, create the missing child on insert, end flag, prefix walk | 3 |
| 32 | [K Closest Points to Origin](practice/problems/32_k_closest_points_to_origin/README.md) (LC 973) · [code](practice/problems/32_k_closest_points_to_origin/solution.py) | heap | Medium | push (-dist, x, y), evict the root when the heap exceeds k, read the k survivors | 3 |
| 33 | [Task Scheduler](practice/problems/33_task_scheduler/README.md) (LC 621) · [code](practice/problems/33_task_scheduler/solution.py) | heap / greedy | Medium-Hard | pop the most frequent ready task, park it in a cooldown queue with its ready time, re-add when ready, jump the clock over idle gaps | 4 |
| 34 | [Find Median from Data Stream](practice/problems/34_find_median_from_data_stream/README.md) (LC 295) · [code](practice/problems/34_find_median_from_data_stream/solution.py) | heap | Medium-Hard | push into the max-heap low, move its max to the min-heap high, rebalance sizes, read the roots | 4 |
| 35 | [Merge k Sorted Lists](practice/problems/35_merge_k_sorted_lists/README.md) (LC 23) · [code](practice/problems/35_merge_k_sorted_lists/solution.py) | heap | Medium-Hard | heap of the k current heads as (value, list_index, node_index), pop the smallest, push that list's next element | 4 |
| 36 | [Palindrome Partitioning](practice/problems/36_palindrome_partitioning/README.md) (LC 131) · [code](practice/problems/36_palindrome_partitioning/solution.py) | backtracking | Medium | choose a palindromic prefix, recurse on the rest, record at the end, undo the choice | 3 |
| 37 | [Combination Sum II](practice/problems/37_combination_sum_ii/README.md) (LC 40) · [code](practice/problems/37_combination_sum_ii/solution.py) | backtracking | Medium | sort, break when candidate > remaining, skip a duplicate sibling (i > start), append / recurse from i + 1 / pop | 3 |
| 38 | [Letter Combinations of a Phone Number](practice/problems/38_letter_combinations_of_a_phone_number/README.md) (LC 17) · [code](practice/problems/38_letter_combinations_of_a_phone_number/solution.py) | backtracking | Medium | one recursion level per digit, append a letter, recurse to the next digit, pop on return | 3 |
| 39 | [Word Search](practice/problems/39_word_search/README.md) (LC 79) · [code](practice/problems/39_word_search/solution.py) | backtracking | Medium | DFS from every cell, match word[k] at depth k, mark the cell '#' while on the path, restore on return | 3 |
| 40 | [N-Queens](practice/problems/40_n_queens/README.md) (LC 51) · [code](practice/problems/40_n_queens/solution.py) | backtracking | Medium-Hard | one queen per row, attacked = column / diagonal r - c / anti-diagonal r + c sets, add / recurse / remove | 3 |
| 41 | [Number of Islands](practice/problems/41_number_of_islands/README.md) (LC 200) · [code](practice/problems/41_number_of_islands/solution.py) | graphs | Medium | scan for unvisited land, flood fill with a stack, mark visited on push, count the floods | 3 |
| 42 | [Clone Graph](practice/problems/42_clone_graph/README.md) (LC 133) · [code](practice/problems/42_clone_graph/solution.py) | graphs | Medium | BFS from the start node, old -> new dict as the visited set, create a clone on first sight, wire clone -> clone edges | 3 |
| 43 | [Course Schedule](practice/problems/43_course_schedule/README.md) (LC 207) · [code](practice/problems/43_course_schedule/solution.py) | graphs | Medium | adjacency prereq -> course plus indegrees, queue the indegree-0 courses, pop and release dependents, cycle iff taken < n | 3 |
| 44 | [Rotting Oranges](practice/problems/44_rotting_oranges/README.md) (LC 994) · [code](practice/problems/44_rotting_oranges/solution.py) | graphs | Medium | enqueue every rotten source, process one layer per minute, rot fresh neighbours, count fresh left | 3 |
| 45 | [Network Delay Time](practice/problems/45_network_delay_time/README.md) (LC 743) · [code](practice/problems/45_network_delay_time/solution.py) | graphs | Medium | heap pop the closest node, skip stale entries, relax out-edges, push improved arrival times | 3 |
| 46 | [Min Cost to Connect All Points](practice/problems/46_min_cost_to_connect_all_points/README.md) (LC 1584) · [code](practice/problems/46_min_cost_to_connect_all_points/solution.py) | graphs | Medium | heap pop the cheapest outside point, skip stale entries, add it to the tree, push its distances to every outside point | 3 |
| 47 | [Redundant Connection](practice/problems/47_redundant_connection/README.md) (LC 684) · [code](practice/problems/47_redundant_connection/solution.py) | graphs / union find | Medium | find the root of each endpoint, compare roots, union by attaching one root under the other | 3 |
| 48 | [Merge Intervals](practice/problems/48_merge_intervals/README.md) (LC 56) · [code](practice/problems/48_merge_intervals/solution.py) | intervals | Medium | sort by start, compare start with the last merged end, extend end with max, open a new interval | 3 |
| 49 | [Meeting Rooms II](practice/problems/49_meeting_rooms_ii/README.md) (LC 253) · [code](practice/problems/49_meeting_rooms_ii/solution.py) | intervals / heap | Medium | sort by start, pop every end time <= start, push the new end, track the max heap size | 3 |
| 50 | [Longest Palindromic Substring](practice/problems/50_longest_palindromic_substring/README.md) (LC 5) · [code](practice/problems/50_longest_palindromic_substring/solution.py) | strings | Medium | pick a center (odd and even), expand l and r while the ends match, record the best span | 3 |

## Basics

### backtracking · [README](basics/backtracking/README.md)

- [Subsets](practice/basics/backtracking/01_subsets.py) · record the path, choose nums[i], recurse from i + 1, unchoose
- [Subsets With Duplicates](practice/basics/backtracking/02_subsets_with_duplicates.py) · sort first, skip nums[i] == nums[i - 1] when i > start, choose, recurse from i + 1, unchoose
- [Combinations n Choose k](practice/basics/backtracking/03_combinations_n_choose_k.py) · choose i, recurse from i + 1, prune when fewer numbers remain than open slots, unchoose
- [Combination Sum](practice/basics/backtracking/04_combination_sum.py) · sort candidates, choose cands[i], recurse from i (reuse allowed), prune when cands[i] > remaining, unchoose
- [Permutations](practice/basics/backtracking/05_permutations.py) · mark used[i], choose nums[i], recurse with no start index, unmark and unchoose
- [Permutations With Duplicates](practice/basics/backtracking/06_permutations_with_duplicates.py) · sort first, skip nums[i] == nums[i - 1] when used[i - 1] is False, mark used, choose, unmark and unchoose
- [Generate Parentheses](practice/basics/backtracking/07_generate_parentheses.py) · choose an open bracket while opened < n, choose a close bracket while closed < opened, unchoose

### bits · [README](basics/bits/README.md)

- [Get, Set, Clear and Toggle a Bit](practice/basics/bits/01_get_set_clear_toggle_bits.py) · mask = 1 << i, n | mask sets, n & ~mask clears, n ^ mask toggles, n >> i & 1 reads
- [Count Set Bits and the Lowest Set Bit](practice/basics/bits/02_count_bits_and_lowest_set_bit.py) · n & (n - 1) drops the lowest set bit, n & -n isolates it, power of two is n > 0 and n & (n - 1) == 0
- [XOR Tricks: Single Number and Missing Number](practice/basics/bits/03_xor_tricks_single_number_missing_number.py) · acc ^= x cancels pairs, xor with the indices 0..n finds the missing one, lowest set bit of a ^ b splits two singles
- [Bitmask Subset Enumeration](practice/basics/bits/04_bitmask_subset_enumeration.py) · masks 0..2^n - 1 are the subsets, mask >> i & 1 tests item i, sub = (sub - 1) & mask walks the submasks
- [Reverse Bits and Shifts](practice/basics/bits/05_reverse_bits_and_shifts.py) · n & 1 peels the lowest bit, result = result << 1 | bit pushes it in from the right, n >>= 1, mask & 0xFFFFFFFF for logical shifts

### graphs · [README](basics/graphs/README.md)

- [Adjacency List, BFS and DFS](practice/basics/graphs/01_adjacency_list_bfs_dfs.py) · build adjacency list, BFS with a queue and a visited set, DFS with an explicit stack
- [Topological Sort: Kahn and DFS](practice/basics/graphs/02_topological_sort_kahn_and_dfs.py) · count indegrees, queue of indegree-0 nodes, decrement on removal, cycle check by count
- [Union-Find (Disjoint Set Union)](practice/basics/graphs/03_union_find.py) · find with path compression, union by size, connected query, component count
- [Kruskal's Minimum Spanning Tree](practice/basics/graphs/04_kruskal_mst.py) · sort edges by weight, union-find accept/reject, stop at n-1 edges
- [Prim's Minimum Spanning Tree](practice/basics/graphs/05_prim_mst.py) · heap of (weight, node, parent), skip a popped node already in the tree, push crossing edges
- [Dijkstra's Shortest Paths](practice/basics/graphs/06_dijkstra.py) · heap of (dist, node), skip stale entries, relax out-edges, a node is final when popped

### heaps · [README](basics/heaps/README.md)

- [Heapify by Hand](practice/basics/heaps/01_heapify_by_hand.py) · sift down from the last parent to the root, pick the smaller child, swap while child < node
- [Heap Push and Pop by Hand](practice/basics/heaps/02_push_and_pop_by_hand.py) · append then float up via parent (i-1)//2, move the last element to the root, sink toward the smaller child
- [Top K Largest with a Size-k Min-Heap](practice/basics/heaps/03_top_k_with_size_k_min_heap.py) · fill the heap to k, compare a new value with the root, heappushpop to replace the root, read the root as the k-th largest
- [Max-Heap by Negation and Tuples](practice/basics/heaps/04_max_heap_by_negation_and_tuples.py) · push (-priority, arrival, payload), pop and un-negate, tie-break with the arrival counter so payloads are never compared
- [Kth Largest Element in a Stream](practice/basics/heaps/05_kth_largest_in_a_stream.py) · keep a min-heap of exactly k values, heappush then heappop when it overflows, answer is heap[0]
- [Merge K Sorted Arrays](practice/basics/heaps/06_merge_k_sorted_arrays.py) · seed the heap with every array's head as (value, array index, element index), pop the min, push that array's next element

### linked lists · [README](basics/linked_lists/README.md)

- [Build, Print, Insert, Delete](practice/basics/linked_lists/01_build_print_insert_delete.py) · walk index steps from a dummy head, splice a node in, unlink the first node with a value
- [Reverse a Linked List, Iterative and Recursive](practice/basics/linked_lists/02_reverse_iterative_and_recursive.py) · save next before you cut, point cur back to prev, advance prev and cur, unwind recursion and hang head after its old next
- [Middle of the Linked List with Fast and Slow Pointers](practice/basics/linked_lists/03_middle_with_fast_and_slow.py) · slow moves one, fast moves two, stop when fast or fast.next is None
- [Detect a Cycle with Floyd's Tortoise and Hare](practice/basics/linked_lists/04_detect_cycle_floyd.py) · slow and fast meet inside the cycle, reset one pointer to head, step both by one to the entry
- [Merge Two Sorted Lists](practice/basics/linked_lists/05_merge_two_sorted.py) · dummy head, tail pointer, attach the smaller head and advance that list, attach the leftover
- [Palindrome Linked List](practice/basics/linked_lists/06_palindrome_linked_list.py) · fast and slow to the middle, reverse the second half in place, walk both halves and compare
- [Reverse Nodes in k-Group](practice/basics/linked_lists/07_reverse_nodes_in_k_group.py) · probe k nodes ahead, reverse one group with the next group as the initial prev, hook group_prev to the new head, advance group_prev to the old head
- [Add Two Numbers](practice/basics/linked_lists/08_add_two_numbers.py) · walk two lists of unequal length, carry across digits, dummy head + tail, emit the final carry

### math · [README](basics/math/README.md)

- [GCD and LCM with Euclid's Algorithm](practice/basics/math/01_gcd_lcm_euclid.py) · (a, b) -> (b, a % b) until b == 0, lcm = |a| // gcd * |b|
- [Primes: Trial Division and the Sieve of Eratosthenes](practice/basics/math/02_primes_sieve_and_primality.py) · trial divide while d * d <= n, cross off multiples of p starting at p * p, collect the survivors
- [Fast Power and Modular Arithmetic](practice/basics/math/03_fast_power_and_modular_arithmetic.py) · exp & 1 reads the current bit, base = base * base, exp >>= 1, reduce every product mod m
- [Reverse Integer and Palindrome Number](practice/basics/math/04_digits_reverse_integer_and_palindrome_number.py) · digit = n % 10 and n //= 10 (divmod), rev = rev * 10 + digit, sign and 32-bit range check, reverse only half
- [Base Conversion and Excel Column Titles](practice/basics/math/05_base_conversion_and_excel_columns.py) · divmod(n, b) peels the lowest digit, Horner n = n * b + digit, subtract 1 before divmod for 1-based digits
- [Random Pick and Reservoir Sampling](practice/basics/math/06_random_pick_and_reservoir_sampling.py) · keep the first k, item i replaces slot j = randrange(i + 1) when j < k, k = 1 over matching indices

### matrices · [README](basics/matrices/README.md)

- [Rotate Image](practice/basics/matrices/01_rotate_image.py) · transpose by swapping across the diagonal, reverse each row, in place
- [Spiral Matrix](practice/basics/matrices/02_spiral_matrix.py) · four shrinking bounds, emit one side per step, re-check bounds before the bottom and left sides
- [Set Matrix Zeroes](practice/basics/matrices/03_set_matrix_zeroes.py) · record flags for row 0 and column 0 first, mark in the first row/column, zero the inside, finish the borders
- [Search a 2D Matrix II](practice/basics/matrices/04_search_2d_matrix_staircase.py) · start at the top-right corner, move left when too big, move down when too small
- [Game of Life](practice/basics/matrices/05_game_of_life_in_place.py) · count 8 neighbors with & 1, store the next state in bit 1, decode with >> 1
- [Matrix Traversal Patterns](practice/basics/matrices/06_matrix_traversal_patterns.py) · row-major and column-major walks, anti-diagonals by r + c, 4/8 direction vectors with bounds checks

### monotonic stacks · [README](basics/monotonic_stacks/README.md)

- [Next Greater Element](practice/basics/monotonic_stacks/01_next_greater_element.py) · pop while top < current, record answer for popped, push current
- [Previous Smaller Element](practice/basics/monotonic_stacks/02_previous_smaller_element.py) · pop while top >= current, answer is the survivor under the current, push current
- [Online Stock Span](practice/basics/monotonic_stacks/03_online_stock_span.py) · pop while top price <= today, add the popped span to today's, push (price, span)
- [Sum of Subarray Minimums](practice/basics/monotonic_stacks/04_sum_of_subarray_minimums.py) · pop while top >= current (or at the end sentinel), count the subarrays whose minimum is the popped element, push index
- [Remove K Digits](practice/basics/monotonic_stacks/05_remove_k_digits.py) · pop while top > digit and k remains, push digit, cut k leftovers from the end, strip leading zeros

### searches · [README](basics/searches/README.md)

- [Binary Search Variants](practice/basics/searches/01_binary_search_variants.py) · mid = (lo + hi) // 2, keep the half that can still hold the answer, lower_bound (first >= x), upper_bound (first > x)
- [Capacity To Ship Packages Within D Days](practice/basics/searches/02_binary_search_on_answer.py) · monotone feasible(cap), search the answer range [max, sum], hi = mid when feasible, lo = mid + 1 when not
- [Shortest Path in a 0/1 Grid](practice/basics/searches/03_bfs_grid_shortest_path.py) · queue of cells, mark visited when enqueued, four directions with a bounds check, one layer = one step
- [Graph DFS, Recursive and Iterative](practice/basics/searches/04_dfs_recursive_and_iterative.py) · visited set, recurse into each unvisited neighbour, explicit stack with neighbours pushed in reverse, skip a node already visited when popped
- [Connected Components](practice/basics/searches/05_connected_components.py) · adjacency list from an edge list (both directions), BFS from every unvisited node, mark visited when enqueued, one BFS = one component
- [01 Matrix](practice/basics/searches/06_multi_source_bfs_01_matrix.py) · enqueue every source first (distance 0), layer-by-layer BFS, mark a cell when enqueued, first arrival = nearest source

### sorting · [README](basics/sorting/README.md)

- [Insertion Sort](practice/basics/sorting/01_insertion_sort.py) · take the next element, shift larger prefix elements one slot right, drop it into the gap
- [Merge Sort](practice/basics/sorting/02_merge_sort.py) · split in half, sort each half recursively, merge two sorted runs with two pointers taking the left on ties
- [Quick Sort](practice/basics/sorting/03_quick_sort.py) · Lomuto partition around the last element, swap the pivot into its final slot, recurse on both sides
- [Heap Sort](practice/basics/sorting/04_heap_sort.py) · heapify into a max-heap, swap the root with the last unsorted slot, sift the new root down inside the shrunk heap
- [Counting Sort and Bucket Sort](practice/basics/sorting/05_counting_and_bucket_sort.py) · count occurrences by value, emit each value count times, drop floats into n buckets by int(x * n), sort each bucket and concatenate
- [Python Sort Keys and Stability](practice/basics/sorting/06_python_sort_keys_and_stability.py) · key= returning a tuple, negate a number to flip one field, two stable passes with the minor key first

### stacks · [README](basics/stacks/README.md)

- [Array Stack and Queue via Two Stacks](practice/basics/stacks/01_array_stack_and_queue_via_two_stacks.py) · push, pop, peek, drain inbox into outbox only when outbox is empty
- [Simplify Path](practice/basics/stacks/02_simplify_unix_path.py) · split on '/', skip '' and '.', pop on '..', join the survivors
- [Decode String](practice/basics/stacks/03_decode_string.py) · accumulate the count digit by digit, push (prefix, count) on '[', pop and repeat on ']'
- [Basic Calculator II](practice/basics/stacks/04_basic_calculator_ii.py) · build the number digit by digit, apply the pending operator, push a signed term, multiply or divide the top
- [Asteroid Collision](practice/basics/stacks/05_asteroid_collision.py) · push right-movers, fight the top while top > 0 and current < 0, pop the loser

### strings · [README](basics/strings/README.md)

- [Character Counting and Anagrams](practice/basics/strings/01_character_counting_and_anagrams.py) · 26-slot count array, compare count vectors, group by a count tuple key
- [Two Pointer Palindromes and Reverse Words](practice/basics/strings/02_two_pointer_palindromes_and_reverse_words.py) · lo/hi pointers that skip non-alphanumerics, compare lowercase, reverse a range in place, reverse each word back
- [KMP Prefix Function](practice/basics/strings/03_kmp_prefix_function.py) · build the failure table, fall back with fail[k - 1] on a mismatch, extend on a match, record a hit and keep going
- [Rabin-Karp Rolling Hash](practice/basics/strings/04_rabin_karp_rolling_hash.py) · polynomial hash of a window, roll it in O(1) by dropping the left char and adding the right one, verify on a hash hit
- [Encode and Decode Strings](practice/basics/strings/05_encode_decode_strings_and_join.py) · length-prefix each string, collect parts in a list and join once, read length then slice

### trees · [README](basics/trees/README.md)

- [Tree Traversals, Recursive and Iterative](practice/basics/trees/01_traversals_recursive_and_iterative.py) · visit before/between/after the children, push right then left for preorder, push-left-then-pop for inorder
- [Level Order and Height](practice/basics/trees/02_bfs_level_order_and_height.py) · for _ in range(len(q)) drains exactly one level, popleft, push children, one level = one unit of height
- [BST Insert, Search, Delete](practice/basics/trees/03_bst_insert_search_delete.py) · descend by comparison, attach a new leaf, splice out a node with 0 or 1 child, replace a 2-child node by its inorder successor
- [Balanced Binary Tree](practice/basics/trees/04_balanced_and_depth.py) · post-order height, return -1 upward as soon as a subtree is unbalanced, abs(left - right) > 1
- [Lowest Common Ancestor of a Binary Tree](practice/basics/trees/05_lowest_common_ancestor_binary_tree.py) · post-order search, return the found node upward, both sides non-None means this node is the LCA
- [Serialize and Deserialize Binary Tree](practice/basics/trees/06_serialize_and_deserialize.py) · preorder emit with '#' for None, consume tokens with one shared iterator, build left then right

### tries · [README](basics/tries/README.md)

- [Trie: Insert, Search, StartsWith](practice/basics/tries/01_trie_insert_search_prefix.py) · walk or create one child per character, mark the end flag, search checks the end flag, startsWith only needs the path
- [Trie: Delete a Word with Pruning](practice/basics/tries/02_trie_delete.py) · walk down recording the path, clear the end flag, unwind pruning children that are empty and not word ends, stop at a shared node
- [Autocomplete: Collect Words with a Prefix](practice/basics/tries/03_autocomplete_collect_words_with_prefix.py) · walk to the prefix node, DFS below it in sorted child order, emit a word at every end flag
- [Design Add and Search Words Data Structure](practice/basics/tries/04_add_and_search_word_with_wildcard.py) · trie insert, DFS search that follows one child per letter, '.' branches into every child, end flag at the last character
