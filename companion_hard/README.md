# Brute to Optimal: Hard: code files

One runnable file per problem, in the book's reading order. Each file has a brute force and the optimal
solution written in plain Python, and two demos at the bottom that print the same answers. Run a file with
`python3 companion_hard/<chapter>/<problem>.py`, change the inputs, run again. Format: `site/companion/SPEC.md`.

### Arrays and Hashing

1. [First Missing Positive](arrays_hashing/first_missing_positive.py) · LC 41 · Hard · Index as hash (in-place cyclic placement)
2. [Maximum Gap](arrays_hashing/maximum_gap.py) · LC 164 · Hard · Pigeonhole buckets
3. [Contains Duplicate III](arrays_hashing/contains_duplicate_iii.py) · LC 220 · Hard · Sliding window of value buckets
4. [Count of Smaller Numbers After Self](arrays_hashing/count_of_smaller_numbers_after_self.py) · LC 315 · Hard · Merge sort counting
5. [Reverse Pairs](arrays_hashing/reverse_pairs.py) · LC 493 · Hard · Merge sort counting
6. [Create Sorted Array through Instructions](arrays_hashing/create_sorted_array_through_instructions.py) · LC 1649 · Hard · Fenwick tree over values (order-statistics counting)

### Two Pointers

1. [Trapping Rain Water](two_pointers/trapping_rain_water.py) · LC 42 · Hard · Converging two pointers with running maxima
2. [Wildcard Matching](two_pointers/wildcard_matching.py) · LC 44 · Hard · Greedy two pointers with last-star backtrack

### Sliding Window

1. [Substring with Concatenation of All Words](sliding_window/substring_with_concatenation_of_all_words.py) · LC 30 · Hard · Fixed-size sliding window with counts
2. [Minimum Window Substring](sliding_window/minimum_window_substring.py) · LC 76 · Hard · Variable-size sliding window
3. [Subarrays with K Different Integers](sliding_window/subarrays_with_k_different_integers.py) · LC 992 · Hard · Exactly-K = atMost(K) - atMost(K-1)
4. [Sliding Window Maximum](sliding_window/sliding_window_maximum.py) · LC 239 · Hard · Monotonic deque
5. [Shortest Subarray with Sum at Least K](sliding_window/shortest_subarray_with_sum_at_least_k.py) · LC 862 · Hard · Monotonic deque
6. [Sliding Window Median](sliding_window/sliding_window_median.py) · LC 480 · Hard · Two heaps with lazy deletion

### Stacks

1. [Basic Calculator](stack/basic_calculator.py) · LC 224 · Hard · Sign stack for parentheses
2. [Parsing a Boolean Expression](stack/parsing_a_boolean_expression.py) · LC 1106 · Hard · Stack-based expression evaluation
3. [Longest Valid Parentheses](stack/longest_valid_parentheses.py) · LC 32 · Hard · Stack of indices with a barrier
4. [Largest Rectangle in Histogram](stack/largest_rectangle_in_histogram.py) · LC 84 · Hard · Monotonic stack
5. [Maximal Rectangle](stack/maximal_rectangle.py) · LC 85 · Hard · Monotonic stack
6. [Create Maximum Number](stack/create_maximum_number.py) · LC 321 · Hard · Monotonic stack + greedy merge

### Binary Search

1. [Find in Mountain Array](binary_search/find_in_mountain_array.py) · LC 1095 · Hard · Binary search on a hidden array (peak, then two sorted halves)
2. [Split Array Largest Sum](binary_search/split_array_largest_sum.py) · LC 410 · Hard · Binary search on the answer
3. [Maximum Running Time of N Computers](binary_search/maximum_running_time_of_n_computers.py) · LC 2141 · Hard · Binary search on the answer
4. [Kth Smallest Number in Multiplication Table](binary_search/kth_smallest_number_in_multiplication_table.py) · LC 668 · Hard · Binary search on the answer
5. [Find K-th Smallest Pair Distance](binary_search/find_kth_smallest_pair_distance.py) · LC 719 · Hard · Binary search on the answer
6. [Maximum Average Subarray II](binary_search/maximum_average_subarray_ii.py) · LC 644 · Hard · Binary search on the answer
7. [Median of Two Sorted Arrays](binary_search/median_of_two_sorted_arrays.py) · LC 4 · Hard · Binary search on a partition

### Linked Lists

1. [Reverse Nodes in k-Group](linked_list/reverse_nodes_in_k_group.py) · LC 25 · Hard · In-place pointer reversal

### Trees

1. [Binary Tree Maximum Path Sum](trees/binary_tree_maximum_path_sum.py) · LC 124 · Hard · Post-order height with side-channel answer
2. [Vertical Order Traversal of a Binary Tree](trees/vertical_order_traversal_of_a_binary_tree.py) · LC 987 · Hard · DFS with (column, row) coordinates, then group-sort
3. [Closest Binary Search Tree Value II](trees/closest_binary_search_tree_value_ii.py) · LC 272 · Hard · Two lazy inorder iterators (predecessor / successor stacks)
4. [Recover Binary Search Tree](trees/recover_binary_search_tree.py) · LC 99 · Hard · Inorder traversal with previous-node pointer
5. [Recover a Tree From Preorder Traversal](trees/recover_a_tree_from_preorder_traversal.py) · LC 1028 · Hard · Stack of ancestors indexed by depth
6. [Serialize and Deserialize Binary Tree](trees/serialize_and_deserialize_binary_tree.py) · LC 297 · Hard · Preorder with null sentinels
7. [Serialize and Deserialize N-ary Tree](trees/serialize_and_deserialize_n_ary_tree.py) · LC 428 · Hard · Preorder with child counts, consumed by a single cursor
8. [Binary Tree Cameras](trees/binary_tree_cameras.py) · LC 968 · Hard · Greedy post-order with 3-state return

### Tries

1. [Word Search II](tries/word_search_ii.py) · LC 212 · Hard · Trie-guided grid backtracking
2. [Word Squares](tries/word_squares.py) · LC 425 · Hard · Prefix trie + row-by-row backtracking
3. [Prefix and Suffix Search](tries/prefix_and_suffix_search.py) · LC 745 · Hard · Trie over "suffix#word" rotations, max index stored per node
4. [Stream of Characters](tries/stream_of_characters.py) · LC 1032 · Hard · Reversed trie walked backwards over a bounded recent-history buffer
5. [Design Search Autocomplete System](tries/design_search_autocomplete_system.py) · LC 642 · Hard · Trie with per-node frequency map + cursor that follows keystrokes

### Heaps and Priority Queues

1. [Rearrange String k Distance Apart](heap/rearrange_string_k_distance_apart.py) · LC 358 · Hard · Greedy max-heap by remaining count + fixed-length cooldown queue
2. [Merge k Sorted Lists](heap/merge_k_sorted_lists.py) · LC 23 · Hard · k-way merge with a heap (merge k sorted feeds)
3. [K-th Smallest Prime Fraction](heap/kth_smallest_prime_fraction.py) · LC 786 · Hard · k-way merge with a heap (merge k sorted feeds)
4. [Smallest Range Covering Elements from K Lists](heap/smallest_range_covering_elements_from_k_lists.py) · LC 632 · Hard · K-way merge with a min-heap of list pointers (track the running max)
5. [Find Median from Data Stream](heap/find_median_from_data_stream.py) · LC 295 · Hard · Two heaps (balanced max-heap / min-heap)
6. [IPO](heap/ipo.py) · LC 502 · Hard · Sort by threshold + max-heap of unlocked candidates
7. [Minimum Number of Refueling Stops](heap/minimum_number_of_refueling_stops.py) · LC 871 · Hard · Greedy with a max-heap of passed-but-unused options (refuel only when stuck)
8. [Course Schedule III](heap/course_schedule_iii.py) · LC 630 · Hard · Sort by deadline + max-heap of taken durations (swap out the longest)
9. [Maximum Performance of a Team](heap/maximum_performance_of_a_team.py) · LC 1383 · Hard · Sort by the bottleneck (efficiency desc) + min-heap of the top-k other values
10. [Minimize Deviation in Array](heap/minimize_deviation_in_array.py) · LC 1675 · Hard · Max-heap of normalised values, repeatedly shrink the maximum
11. [Meeting Rooms III](heap/meeting_rooms_iii.py) · LC 2402 · Hard · Two heaps (free rooms by id, busy rooms by end time) over a sorted sweep
12. [The Skyline Problem](heap/the_skyline_problem.py) · LC 218 · Hard · Sweep line over events + max-heap with lazy removal
13. [Trapping Rain Water II](heap/trapping_rain_water_ii.py) · LC 407 · Hard · Min-heap frontier expanding inward from the boundary (lowest wall first)

### Backtracking

1. [Unique Paths III](backtracking/unique_paths_iii.py) · LC 980 · Hard · Grid DFS backtracking with in-place visited marking
2. [N-Queens](backtracking/n_queens.py) · LC 51 · Hard · Row-by-row backtracking with column/diagonal sets
3. [Sudoku Solver](backtracking/sudoku_solver.py) · LC 37 · Hard · Constraint backtracking with bitmasks (most-constrained cell first)
4. [Remove Invalid Parentheses](backtracking/remove_invalid_parentheses.py) · LC 301 · Hard · Backtracking with counted removals and balance pruning
5. [Expression Add Operators](backtracking/expression_add_operators.py) · LC 282 · Hard · Backtracking with running value + last operand
6. [24 Game](backtracking/twenty_four_game.py) · LC 679 · Hard · Reduce-the-multiset backtracking (combine two values, recurse on the rest)
7. [Robot Room Cleaner](backtracking/robot_room_cleaner.py) · LC 489 · Hard · Blind DFS with relative coordinates and turn-around backtrack

### Graphs

1. [Word Ladder](graphs/word_ladder.py) · LC 127 · Hard · BFS on implicit graph (wildcard buckets)
2. [Word Ladder II](graphs/word_ladder_ii.py) · LC 126 · Hard · Layered BFS + parents DAG, then backtrack paths
3. [Sliding Puzzle](graphs/sliding_puzzle.py) · LC 773 · Hard · BFS on implicit graph (board-state strings)
4. [Bus Routes](graphs/bus_routes.py) · LC 815 · Hard · BFS on implicit graph (stop -> routes index)
5. [Jump Game IV](graphs/jump_game_iv.py) · LC 1345 · Hard · BFS on implicit graph with value buckets consumed once
6. [K-Similar Strings](graphs/k_similar_strings.py) · LC 854 · Hard · BFS over states with pruned branching (fix the first mismatch)
7. [Shortest Path in a Grid with Obstacles Elimination](graphs/shortest_path_in_a_grid_with_obstacles_elimination.py) · LC 1293 · Hard · BFS over augmented states (position + bitmask/budget)
8. [Shortest Path to Get All Keys](graphs/shortest_path_to_get_all_keys.py) · LC 864 · Hard · BFS over augmented states (position + bitmask/budget)
9. [Shortest Path Visiting All Nodes](graphs/shortest_path_visiting_all_nodes.py) · LC 847 · Hard · BFS over augmented states (position + bitmask/budget)
10. [Minimum Moves to Move a Box to Their Target Location](graphs/minimum_moves_to_move_a_box_to_their_target_location.py) · LC 1263 · Hard · 0-1 BFS (deque shortest path)
11. [Alien Dictionary](graphs/alien_dictionary.py) · LC 269 · Hard · Topological sort (Kahn's BFS) / cycle detection
12. [Parallel Courses III](graphs/parallel_courses_iii.py) · LC 2050 · Hard · Topological order + longest-path relaxation (Kahn)
13. [Sort Items by Groups Respecting Dependencies](graphs/sort_items_by_groups_respecting_dependencies.py) · LC 1203 · Hard · Topological sort (Kahn's BFS) / cycle detection
14. [Reconstruct Itinerary](graphs/reconstruct_itinerary.py) · LC 332 · Hard · Eulerian path (Hierholzer's DFS)
15. [Redundant Connection II](graphs/redundant_connection_ii.py) · LC 685 · Hard · Union-Find (disjoint set union)
16. [Number of Islands II](graphs/number_of_islands_ii.py) · LC 305 · Hard · Union-Find (disjoint set union)
17. [Minimize Malware Spread](graphs/minimize_malware_spread.py) · LC 924 · Hard · Union-Find (disjoint set union)
18. [Largest Component Size by Common Factor](graphs/largest_component_size_by_common_factor.py) · LC 952 · Hard · Union-Find (disjoint set union)
19. [Find All People With Secret](graphs/find_all_people_with_secret.py) · LC 2092 · Hard · Time-grouped union-find with reset of non-informed components
20. [Checking Existence of Edge Length Limited Paths](graphs/checking_existence_of_edge_length_limited_paths.py) · LC 1697 · Hard · Union-Find (disjoint set union)
21. [Remove Max Number of Edges to Keep Graph Fully Traversable](graphs/remove_max_number_of_edges_to_keep_graph_fully_traversable.py) · LC 1579 · Hard · Union-Find (disjoint set union)
22. [Minimum Cost to Make at Least One Valid Path in a Grid](graphs/minimum_cost_to_make_at_least_one_valid_path_in_a_grid.py) · LC 1368 · Hard · 0-1 BFS (deque shortest path)
23. [Swim in Rising Water](graphs/swim_in_rising_water.py) · LC 778 · Hard · Minimax path via min-heap (bottleneck Dijkstra)
24. [Minimum Weighted Subgraph With the Required Paths](graphs/minimum_weighted_subgraph_with_the_required_paths.py) · LC 2203 · Hard · Dijkstra (min-heap shortest paths)
25. [Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree](graphs/find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree.py) · LC 1489 · Hard · Kruskal MST (sorted edges + union-find)
26. [Critical Connections in a Network](graphs/critical_connections_in_a_network.py) · LC 1192 · Hard · Tarjan bridges (DFS low-link)

### Intervals and Sweep Lines

1. [Employee Free Time](intervals/employee_free_time.py) · LC 759 · Hard · K-way merge of sorted interval lists with a min-heap, emitting gaps
2. [Minimum Interval to Include Each Query](intervals/minimum_interval_to_include_each_query.py) · LC 1851 · Hard · Offline queries sorted + sweep by start + min-heap by size with lazy removal
3. [My Calendar III](intervals/my_calendar_iii.py) · LC 732 · Hard · Difference array / prefix-sum sweep
4. [Rectangle Area II](intervals/rectangle_area_ii.py) · LC 850 · Hard · Sweep line over sorted events

### Greedy

1. [Minimum Number of Taps to Open to Water a Garden](greedy/minimum_number_of_taps_to_open_to_water_a_garden.py) · LC 1326 · Hard · Greedy reach (furthest reachable index)
2. [Candy](greedy/candy.py) · LC 135 · Hard · Two-pass greedy (left-to-right, right-to-left)
3. [Minimum Number of Increments on Subarrays to Form a Target Array](greedy/min_number_operations.py) · LC 1526 · Hard · Count only the rises (adjacent-difference greedy)
4. [Super Washing Machines](greedy/super_washing_machines.py) · LC 517 · Hard · Prefix-sum flow bound
5. [Patching Array](greedy/patching_array.py) · LC 330 · Hard · Greedy reach (furthest reachable index)
6. [Set Intersection Size At Least Two](greedy/set_intersection_size_at_least_two.py) · LC 757 · Hard · Greedy by earliest end (interval scheduling)
7. [Couples Holding Hands](greedy/couples_holding_hands.py) · LC 765 · Hard · Union-Find (disjoint set union)
8. [Stamping The Sequence](greedy/stamping_the_sequence.py) · LC 936 · Hard · Reverse greedy (undo the last move first)

### Bit Manipulation

1. [Number of Valid Words for Each Puzzle](bit_manipulation/number_of_valid_words_for_each_puzzle.py) · LC 1178 · Hard · Bitmask counting + submask enumeration
2. [Find Longest Awesome Substring](bit_manipulation/find_longest_awesome_substring.py) · LC 1542 · Hard · Prefix parity mask + first-seen positions
3. [Maximum XOR With an Element From Array](bit_manipulation/maximum_xor_with_an_element_from_array.py) · LC 1707 · Hard · Offline queries + binary trie (max XOR)

### Math and Geometry

1. [Permutation Sequence](math_geometry/permutation_sequence.py) · LC 60 · Hard · Factorial number system (direct ranking into blocks)
2. [K-th Smallest in Lexicographical Order](math_geometry/kth_smallest_in_lexicographical_order.py) · LC 440 · Hard · Denary trie traversal with subtree skipping
3. [Number of Digit One](math_geometry/number_of_digit_one.py) · LC 233 · Hard · Digit counting by position
4. [Poor Pigs](math_geometry/poor_pigs.py) · LC 458 · Hard · Information counting (states per pig, mixed-radix labelling)
5. [Max Points on a Line](math_geometry/max_points_on_a_line.py) · LC 149 · Hard · Anchor point + slope as a reduced fraction
6. [Perfect Rectangle](math_geometry/perfect_rectangle.py) · LC 391 · Hard · Corner parity + area invariant
7. [Erect the Fence](math_geometry/erect_the_fence.py) · LC 587 · Hard · Convex hull (monotone chain)

### Strings: Scanning, Parsing, Canonical Forms

1. [Valid Number](strings/valid_number.py) · LC 65 · Hard · Single-pass state machine with flags
2. [Integer to English Words](strings/integer_to_english_words.py) · LC 273 · Hard · Chunk by thousands + lookup tables
3. [Text Justification](strings/text_justification.py) · LC 68 · Hard · Greedy line packing
4. [Longest Happy Prefix](strings/longest_happy_prefix.py) · LC 1392 · Hard · KMP failure function (longest border)
5. [Shortest Palindrome](strings/shortest_palindrome.py) · LC 214 · Hard · KMP failure function (longest border)
6. [Palindrome Pairs](strings/palindrome_pairs.py) · LC 336 · Hard · Hash map of reversed words + palindrome split
7. [Longest Duplicate Substring](strings/longest_duplicate_substring.py) · LC 1044 · Hard · Binary search on the answer + rolling hash

### Design: Implement a Tracker

1. [LFU Cache](design/lfu_cache.py) · LC 460 · Hard · Frequency buckets of ordered dicts + min-frequency pointer
2. [All O`one Data Structure](design/all_oone_data_structure.py) · LC 432 · Hard · Hash map + doubly linked list of count buckets
3. [Maximum Frequency Stack](design/maximum_frequency_stack.py) · LC 895 · Hard · Frequency buckets as stacks + max pointer
4. [Dinner Plate Stacks](design/dinner_plate_stacks.py) · LC 1172 · Hard · List of stacks + min-heap of "has room" indices with lazy invalidation
5. [Data Stream as Disjoint Intervals](design/data_stream_as_disjoint_intervals.py) · LC 352 · Hard · Sorted disjoint intervals with bisect
6. [Range Module](design/range_module.py) · LC 715 · Hard · Sorted disjoint intervals with bisect
7. [Range Sum Query 2D - Mutable](design/range_sum_query_2d_mutable.py) · LC 308 · Hard · 2D Fenwick tree (binary indexed tree) + inclusion-exclusion
8. [Online Majority Element In Subarray](design/online_majority_element_in_subarray.py) · LC 1157 · Hard · Value -> sorted positions + randomized sampling with bisect verification
9. [Design Movie Rental System](design/design_movie_rental_system.py) · LC 1912 · Hard · Heaps with lazy deletion by version stamp
10. [Design In-Memory File System](design/design_in_memory_file_system.py) · LC 588 · Hard · Trie of directories (path components as edges)
11. [Design Skiplist](design/design_skiplist.py) · LC 1206 · Hard · Multi-level sorted linked list with randomised express lanes
