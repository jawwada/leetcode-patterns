---
name: brute-to-optimal-companion
description: "Brute to Optimal artifacts (standard 2uod7DD3MdfNtxBDeTzaXH, hard FU9u7QU93gJWEd7GsCUMHq) + companion/ and companion_hard/ code folders in simple Python, built by site/build_companion.py [--edition hard]; Vercel sites brute-to-optimal(.vercel.app) and brute-to-optimal-hard"
metadata:
  node_type: memory
  type: project
  originSessionId: 1c82f467-c4f3-48d2-a8ca-8e7cd3c2dad0
  modified: 2026-10-05T09:04:40.865Z
---

Built 2026-10-05 on the user's request for a short-form companion to the Intuition Journey book: per problem only
two headings (Brute force, Optimal solution), each a short paragraph + runnable Python / pseudocode tabs.
Artifact: https://claude.ai/artifact/2uod7DD3MdfNtxBDeTzaXH (Pyodide 0.26.4 runtime files published next to the
page: pyworker.js, pyodide.js, pyodide.asm.js, pyodide.asm.wasm, pyodide-lock.json, python_stdlib.wasm; on a
republish of the same file path they are kept unless passed as null). Local copies of the runtime are only in a
session scratchpad; re-download from this artifact (Artifact read with `paths`) if they are ever needed again.

Repo pieces: `companion/<chapter>/<slug>.py` (108 problems, selection in `site/companion/selection.json`, no Hard,
no DP) and `companion/fundamentals/<area>/<name>.py` (63 algorithms, `site/companion/fundamentals.json`, rewritten
from `practice/basics/`). Format and the "simple Python" style rules: `site/companion/SPEC.md` (no comprehensions,
lambda, Counter/defaultdict, type hints, class Solution; plain functions, snake_case, short comments).
Build: `python3 site/build_companion.py` (checks every file: runs both demos, same output) → `site/companion.html`
(publish this path) + `site/companion_index.html` + `companion/README.md`. Pseudocode lives in
`site/companion/pseudo/*.json`. Paragraphs/costs come from `site/problems.json`; chapter backgrounds from the
book's 00_background.md (sections What it is / Operations / Invariant / Python toolbox / Mistakes).

Website (2026-10-05): Vercel project `brute-to-optimal` (team ahmed-astock, linked from `site/companion_site/`, which the
build writes: index.html + pyworker.js; deploy with `cd site/companion_site && vercel deploy --prod --yes`). The worker
loads Pyodide from cdn.jsdelivr.net when no runtime files sit next to the page, so the site ships no wasm. The user
wants it on learn.ringnest.ai: ringnest.ai is a Vercel domain of the `ringnest` Next.js project but its nameservers are
at Spaceship, so attaching the subdomain needs `vercel domains add learn.ringnest.ai brute-to-optimal` plus a CNAME
at Spaceship (the auto-mode classifier blocked the domain step; the user does it). Vercel CLI is logged in locally.

Hard edition (2026-10-05): `python3 site/build_companion.py --edition hard` → `companion_hard/<chapter>/<slug>.py` (127 Hard
problems, `site/companion/selection_hard.json`, pseudocode in `site/companion/pseudo_hard/`, limits 70/100 lines), outputs
`site/companion_hard.html` (artifact https://claude.ai/artifact/FU9u7QU93gJWEd7GsCUMHq, runtime files uploaded from local
copies) and `site/companion_hard_site/` (Vercel project `brute-to-optimal-hard`, https://brute-to-optimal-hard.vercel.app).
Its "Fundamentals" group is called Advanced patterns and shows the book backgrounds' Advanced patterns / Signals /
Mistakes sections, no algorithm files. User wants it at learn-hard.ringnest.ai (same CNAME procedure).

**Why:** user's Python is sketchy and they have ~10 days; they want the gist, runnable code to play with, and a
folder they can clone on other machines. They explicitly asked for sorting + top graph algorithms (Kruskal, Prim,
topological sort) "at their fingertips", hence the fundamentals group.

**How to apply:** adding a problem = write `companion/<chapter>/<slug>.py` per SPEC, add the slug to selection.json,
add pseudocode JSON, rebuild, republish `site/companion.html` to the URL above, commit and push. Test in headless
Chrome (puppeteer-core in a scratchpad + installed Google Chrome, serve the page with a wasm-aware server) before
claiming the runtime works. See [[leetcode-repo-layout]], [[practice-bank]], [[google-interview-prep]].
