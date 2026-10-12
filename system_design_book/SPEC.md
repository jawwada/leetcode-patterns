# 50 System Designs: chapter format

One book, one PDF: fifty system designs in the rank order of `manifest.json`, built from
`chapters/NN_slug.md` (`NN` = rank, two digits). Titles, subtitles and tiers live only in the
manifest; the build adds the chapter heading. Chapter 1 (`chapters/01_url_shortener.md`) is the
reference: match its voice, structure, depth and density.

The reader is preparing for Google system design interviews. They already own the algorithms
(the companion books *150 Algorithms in Pseudocode / in Python*), and they learn best from a
connected argument in a confident voice with a clear picture of the architecture. Every chapter
should leave them able to run the 45-minute interview for that system on their own.

Run `python3 system_design_book/check.py <rank>`. A chapter is done only when it prints `OK`;
clear the warnings too where reasonable.

## Structure (exact, in this order)

```markdown
---
rank: 1
slug: url_shortener
---

<Opening paragraph, no heading: what the system is, a concrete example, and the two or three
questions that decide the design (the crux).>

### Requirements
### Estimates
### API
### Data Model
### Architecture
### Deep Dives
#### <hardest part 1>
#### <hardest part 2>
#### <optional hardest part 3>
### Scaling and Bottlenecks
### Failure Modes
### Trade-offs and Alternatives
### What Interviewers Probe

*Algorithms:* #100 URL Shortener · #145 Unique ID Generator · #139 Consistent Hashing
```

- **Requirements**: one paragraph of functional requirements (what users can do), one of
  non-functional ones with numbers (scale, latency, availability, consistency, durability), and
  what is out of scope.
- **Estimates**: a ```text block with one derivation per line (traffic, peak, storage, bandwidth,
  memory for the hot set, whatever drives the design), then a paragraph saying what the numbers
  imply. Arithmetic must be right; round sensibly; assumptions stated.
- **API**: a ```text block with the endpoints (or RPCs), request and response shapes and status
  codes, then a paragraph on idempotency, pagination, auth or streaming as relevant.
- **Data Model**: a ```text block with tables/collections, keys and partitioning, then prose on
  the store chosen for each access pattern and why.
- **Architecture**: a ```dot diagram (see below), then paragraphs walking the main paths (write
  path, read path, async path) through the named components.
- **Deep Dives**: two or three `####` subsections on the genuinely hard parts, each a real
  argument: the naive approach and why it fails, the chosen mechanism, its cost. Extra small
  ```dot or ```text figures are welcome here.
- **Scaling and Bottlenecks**, **Failure Modes**, **Trade-offs and Alternatives**: prose, specific
  to this system (which component breaks first, what happens when X fails, which alternative
  design a different requirement would pick).
- **What Interviewers Probe**: the follow-up questions interviewers actually ask, each with a crisp
  answer, written as prose; then what strong candidates raise unprompted.
- Last line: `*Algorithms:*` followed by 1 to 6 entries `#N Exact Title` separated by ` · `, using
  ranks and titles from `algorithms_index.json` (the 150 Algorithms books). List only algorithms
  the design really uses; mention each in the prose too. The manifest's `algorithms` field is a
  suggestion.

## Voice

Flowing paragraphs in a definitive voice, the way chapter 1 reads. No bullet or numbered lists, no
tables, no bold labels, no headings beyond the template and the deep-dive titles. Name real systems
(DynamoDB, Kafka, Redis, Spanner ...) where they help, but state only well-established facts about
them; when unsure of a specific number or behaviour, leave it out or verify it with a web search.
Numbers in the design are stated as assumptions ("assume 100 M new links a day"). Length: 1800 to
3000 words of prose, which prints as 3 to 5 pages.

Cross references: `Chapter N` for another design in this book (rank from the manifest, e.g.
"the fan-out of Chapter 5"); `#N` for an entry of the 150 Algorithms books (e.g. "consistent
hashing (#139)"). Build on earlier chapters instead of repeating them when the brief says so.

## Code blocks

- ```text: estimates, API, data model, small sketches. At most 80 characters per line. Allowed
  non-ASCII characters: ← → ↑ ↓ ↔ ≤ ≥ ≠ ≈ ∞ × · … ² ³ √ ⌊ ⌋ ✓ ✗ ▲ ▼ ● ○ µ ± and box drawing.
  Write powers as `10^9` or `62^7`.
- ```dot: Graphviz diagrams. Write only the body of the graph (no `digraph G { }` wrapper): the
  build adds fonts and colours and expands `class=NAME` into a node style. Classes:
  `client` (users, browsers, apps), `service` (your stateless services; the default),
  `edge` (CDN, load balancer, API gateway), `cache`, `store` (databases, object stores),
  `queue` (Kafka topics, queues, streams), `worker` (batch and stream jobs),
  `external` (third parties: payment providers, APNs/FCM, SMTP, ...).

```dot
rankdir=TB;
user  [label="browser", class=client];
api   [label="API service"];
db    [label="orders DB", class=store];
psp   [label="payment provider", class=external];
user -> api [label=" POST /orders"];
api -> db [label=" insert"];
api -> psp [label=" charge", style=dashed];
{rank=same; db; psp}
```

  Keep diagrams readable on a page: about 8 to 20 nodes, short labels (`\n` for a second line),
  edge labels of a few words with a leading space, `rankdir=TB` when a chain is longer than five
  nodes, `{rank=same; a; b}` to line nodes up, `style=dashed` for asynchronous flows, and
  `subgraph cluster_x { label="Region A"; style="rounded,dashed"; color="#9CA3AF"; ... }` for
  groupings. The laid-out size must stay within about 7 inches wide and 8 inches tall;
  check.py reads it from Graphviz's text output and reports it.
- Never render diagrams or pages to images, and never open image files to check them; that is
  expensive. Verify diagrams with check.py's numbers and by reading the DOT source.

## Correctness bar

Every statement is true: mechanisms of real systems, consistency guarantees, failure behaviour,
protocol details (HTTP status codes, TCP/UDP, WebSocket, DNS), and the arithmetic in Estimates.
The diagram matches the walkthrough (every component named in the prose exists in the diagram and
the arrows go where the prose says). Algorithm references point at the right entries. The design
is coherent end to end: the data model supports the API, the estimates justify the architecture,
and the deep dives address the hardest requirements.
