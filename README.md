# LeetCode Patterns: solutions, Pattern Board, and the Intuition Journey

**📖 [Read the Intuition Journey book](https://jawwada.github.io/leetcode-patterns/site/book_index.html)** · **🧩 [Open the Pattern Board](https://jawwada.github.io/leetcode-patterns/site/index.html)**

294 interview problems (127 Hard), organised by topic, each solved **brute force first, then reasoned to the optimal**, with a diagram of the data structure mid-run. Built for a Google-style loop: data structures, strings, graphs, trees, heaps, "implement a tracker" design problems; dynamic programming kept in its own chapter, outside the brief.

## Two sites

| Site | What it is | Link |
|---|---|---|
| **Pattern Board** | Short form. One page per problem: problem → visual explanation & thinking process → hints → brute-force code → optimal code → pitfalls. Filter by topic/difficulty, practice mode with a 25-minute clock. | [jawwada.github.io/leetcode-patterns/site/index.html](https://jawwada.github.io/leetcode-patterns/site/index.html) |
| **Intuition Journey** | Long form: a book. 19 chapters, each starting from zero (what the structure is, what it costs, the invariant, how to picture it), then every problem in teaching order explained at length with frame-by-frame drawings. | [jawwada.github.io/leetcode-patterns/site/book_index.html](https://jawwada.github.io/leetcode-patterns/site/book_index.html) |

Both sites are single self-contained HTML files (served by GitHub Pages; also open fine locally). Reading progress is saved in your browser.

## Layout

```
<topic>/<slug>.py        one file per problem: docstring (Problem / Brute force / From brute force to
                         optimal / Intuition / Geometric view / Steps / Complexity / Pitfalls),
                         class Solution with LeetCode's signature, brute_force(), __main__ asserts -> "ok"
book/<topic>/            the Intuition Journey chapters (Markdown): 00_background.md, order.json, <slug>.md
site/data/*.json         one structured entry per problem (feeds the Pattern Board)
site/build.py            data/*.json + template.html -> index.html (Pattern Board)
site/build_book.py       book/**/*.md + problems.json + book_template.html -> book_index.html
```

Topics: `arrays_hashing two_pointers sliding_window stack queues binary_search linked_list trees tries heap backtracking graphs intervals greedy bit_manipulation math_geometry strings design dynamic_programming`

## Run

```bash
for f in */*.py; do python3 "$f"; done     # every file prints "ok"
python3 site/build.py                      # rebuild the Pattern Board
python3 site/build_book.py                 # rebuild the Intuition Journey
```

Python 3.13, standard library only.
