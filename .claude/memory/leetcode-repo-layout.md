---
name: leetcode-repo-layout
description: "How the Leetcode repo is organized (topic folders, per-problem .py format, Pattern Board site, Intuition Journey book) and where it is published (GitHub jawwada/leetcode-patterns + Pages, two claude.ai artifacts)"
metadata:
  node_type: memory
  type: project
  originSessionId: b9b0c83c-4721-4c82-840e-3593a4746df3
  modified: 2026-10-02T09:27:08.178Z
---

Repo `~/Work/Leetcode` = GitHub **jawwada/leetcode-patterns** (public, created 2026-10-02; GitHub Pages on `main`). One Python file per problem under a topic folder (19 topics incl. `queues/` (split from heaps 2026-10-04) and `dynamic_programming/`, which is outside the interview brief but kept from the user's old Packt folder). Each file: docstring (Problem / Brute force / From brute force to optimal / Intuition / Geometric view / Steps / Complexity / Pitfalls), `class Solution` (or the LeetCode design class), `brute_force()` or `class BruteForce`, `__main__` asserts printing `ok`. 294 problems as of 2026-10-04 (127 Hard).

Two generated sites in `site/`:
- **Pattern Board** (short form): `site/data/*.json` + `template.html` → `python3 site/build.py` → `index.html` (local/Pages) + `artifact.html` (published: https://claude.ai/artifact/SNmABicy9ZmJ7fGcDXFrdE). Problem page leads with "Visual explanation & thinking process".
- **Intuition Journey** (book): `book/<topic>/{00_background.md, order.json, <slug>.md}` → `python3 site/build_book.py` → `book_index.html` + `book.html` (published: https://claude.ai/artifact/8VVxT8oUrNgbu7Yg4U2GFw). Spec for chapter prose lived in the session scratchpad (BOOK_SPEC.md); headings are enforced by build_book.py (backgrounds have 10 `##` sections incl. "Advanced patterns"; order.json may carry a `see_also` list of slugs from other chapters).
- Pages URLs: https://jawwada.github.io/leetcode-patterns/site/index.html and .../site/book_index.html.

**Why:** User asked for topic-organised solutions, brute-force-first explanations, a pattern site, then a long-form intuition book, all pushed to their GitHub.

**How to apply:** Adding a problem = .py in topic folder + JSON entry in `site/data/` + book chapter .md and `order.json` entry, then rebuild both sites, republish both artifacts (same file paths), commit and push. Book readings show the problem statement (from problems.json) in a box under the title. Test the sites in headless Chrome (puppeteer-core + installed Google Chrome) before claiming a fix. See [[google-interview-prep]].
