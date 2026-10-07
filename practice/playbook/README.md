# LeetCode Playbook (sources)

The twelve notebooks in `practice/LeetCode_Playbook/` are generated from the markdown sections in this folder:

```bash
uv run python practice/playbook/build.py          # build + run every code cell + embed outputs
uv run jupyter lab practice/LeetCode_Playbook/    # open them
python3 practice/playbook/build_html.py           # the one-page reading copy (artifact.html, not committed)
```

Edit the `.md` files, never the notebooks. `NOTEBOOKS` in `build.py` says which sections go into which
notebook; links like `[Heaps](#s13)` are rewritten to point at the right notebook file. The build also checks
that every code cell has a **Try it** block, that every repo problem sits in exactly one Problem map row,
that every `#sNN` link resolves, and that every `practice/simple/` file is referenced.
To check a few sections in isolation: `build.py --only 06,07 --out /tmp/x.ipynb --folders stack,queues`.

## File format

- One file per section, `NN_slug.md`, starting with `## Title`.
- A ` ```python ` fence becomes a runnable code cell. Cells run top to bottom in one namespace, and the setup
  cell has already imported: `Counter, defaultdict, deque, OrderedDict, cmp_to_key, lru_cache, accumulate,
  combinations, permutations, product, bisect, heapq, math, random, string`. Define every other helper
  (`ListNode`, `TreeNode`, ...) inside your own section; never rely on another section's names.
- Other fences (` ```text `) are shown but not run: use them for ASCII pictures and pseudocode.
- A line `<!-- cell -->` splits a long markdown stretch into two cells.
- Seed randomness (`random.seed(0)`), keep every cell fast (< 1 s) and its output short (< ~25 lines).
- Print results explicitly, with the expected value in a trailing comment: `print(f(x))   # 7`.

## Section recipe (the model is `06_sliding_window.md`)

The notebook's purpose is **turning an idea into an implementation**. Every technique section follows this
order, and the "From idea to code" part is the heart of it.

1. `## Title`, a one-line mental model in a blockquote, **Reach for it when** (clues in the problem
   statement), **In this repo** (topic folder + `practice/simple/...` files that use it).
2. `### The picture`: an ASCII drawing of the data and the motion of the algorithm, then why it is fast
   (what work the brute force repeats and how the technique avoids it).
3. `### From idea to code`: the idea in one sentence; the seven-decision table (**State, Definition,
   Invariant, Step, Record, Init, Return**) answered for this technique; an "In words | In code" table;
   then the template code cell(s), tagged so each decision points at its line: `# STATE`/`# INIT` on the
   structures (with their definition), `# STEP` on the line that folds the new item into the state (not on
   the loop header), `# FIX` on the loop that restores the invariant, `# RECORD` where the answer is updated,
   `# RETURN` on the return. The order of STEP, FIX and RECORD is itself a decision; say why.
4. `### Watch it work`: a small trace that prints the state per step (encouraged, keep it short).
5. `### Where it goes wrong`: numbered implementation traps, each with the fix and a tiny failing input.
6. `### Edge cases to say out loud`: one line of cases, then a code cell of asserts ending with
   `print("edge cases pass")`.
7. `### Variations`: a table (Variation | What changes from the template | Problems), then code cells for
   the most important variations, each introduced by one or two sentences of intuition.
8. `### Say it in the interview`: a short quoted script (brute force, its waste, the optimal idea,
   complexity), plus what to point at while coding.
9. `### Problem map`: `| Problem | Where | Key insight |`, one row per problem. **Where** holds backticked
   repo paths, e.g. `` `sliding_window/fruit_into_baskets.py` · `practice/simple/09_x.py` ``. **Key insight**
   is the single idea that cracks the problem, in under ~20 words. These rows feed the A-Z problem finder.
10. `### Self-check`: 2-4 questions with the answer in `<details><summary>Answer</summary>...</details>`.

**After every code cell** add a markdown block whose first line is `**Try it**`, then 3-4 bullets of
hands-on experiments that teach the main flow and the tricky points: break one line on purpose
(`if` vs `while`, `<` vs `<=`, swap two lines, record in the wrong place) and predict the failure, feed
an edge input, print the state at a chosen point, change a parameter and predict before running.
Any outcome you state must be true. `build.py` lists code cells that lack it.

## Voice

Gentle and learning-oriented: explain *why* before *how*, short paragraphs, concrete tiny examples, pictures
over prose. Write for someone who knows Python but freezes between "I know the idea" and "I know what to
type". Every claim in a code comment or table must be true; every code cell must run.
The notebook speaks in one voice: never mention reviewers, agents, drafts or revision history, and never
attribute an idea to anyone; fold every improvement into the text as if it had always been there.
