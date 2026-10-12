"""Build 50 System Designs as one PDF, and the ranked list system_designs.txt.

Usage: python3 system_design_book/build.py [--partial] [--only=1,2,5] [--md-only]
  --partial   skip chapters that are not written yet (default: all 50 must exist)
  --only=...  build only these chapter ranks (implies --partial)
  --md-only   write the combined Markdown and diagrams but do not compile

The compile is also the validation: the LaTeX log of the one build is checked for errors,
missing glyphs and overfull lines, so no second compile is needed.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build")
PDF = os.path.join(HERE, "50_System_Designs.pdf")
LIST_TXT = os.path.join(REPO, "system_designs.txt")
sys.path.insert(0, HERE)
import diagrams  # noqa: E402

TIER_INTRO = {
    1: "These seventeen designs are the ones interviewers reach for first. Each is a family of "
       "its own: the read-heavy service behind a cache, the limiter in front of every API, the "
       "partitioned and replicated store, the cache cluster, the feed, the chat system and its "
       "multi-device cousin, video upload and streaming, file sync, collaborative editing, the "
       "distributed log, geospatial matching and routing, the CDN, autocomplete and the crawler. "
       "Know them well enough to run each interview end to end without notes.",
    2: "The next seventeen come up often and reuse the first tier's building blocks in new "
       "combinations: ranking and voting, media feeds, notifications, ID generation, search, "
       "streaming counts, money movement with exactly-once effects, inventory without "
       "overselling, proximity search, monitoring, scheduling, leaderboards, live video, object "
       "storage and flash sales. Read each one carefully and rehearse its deep dives.",
    3: "The last sixteen round out the set with systems that test depth: audio streaming, real-"
       "time video, the classic distributed file system, a globally consistent database, "
       "coordination services, load balancing, mail, a matching engine, wallets, calendars, "
       "sandboxed code execution, recommendations, logging, feature flags and counting at scale. "
       "Read them once, keep their key ideas, and return to them when a question goes deep.",
}

INTRO = r"""
# How to Read This Book {#how-to-read}

```{=latex}
\markboth{How to Read This Book}{}
```

This book holds fifty system designs in the order to learn them. The order is importance for a system design interview: how often the design is asked, how many other designs reuse its ideas, and how badly a gap in it shows. Tier 1, the first seventeen, are the designs to know cold. Tier 2, the next seventeen, are very common. Tier 3, the last sixteen, are good to know and are where an interview goes when it wants depth.

Every chapter follows the same template, which is also the shape of a good interview. It opens with the system and the two or three questions that decide its design. Then come the requirements, functional and non-functional, with the numbers that matter; back-of-the-envelope estimates, each derivation on its own line; the API; the data model; and the high-level architecture as a diagram, followed by a walk through its main paths. Two or three deep dives take on the genuinely hard parts. The chapter closes with scaling and bottlenecks, failure modes, trade-offs and alternatives, and the follow-up questions interviewers actually ask, with crisp answers. The last line lists the algorithms the design uses.

A reference such as #139 points to entry 139 of the companion books, *150 Algorithms in Pseudocode* and *150 Algorithms in Python*, where consistent hashing is explained down to the code. A reference such as Chapter 5 points to another design in this book and is a link.

In a 45-minute interview, spend about five minutes on requirements and estimates, five to eight on the API and data model, ten on the architecture, fifteen on two deep dives, and the rest on scaling, failures and trade-offs. The chapters give you more than you can say in that time on purpose: the interviewer chooses the deep dives, and you should be ready for any of them.

## Reading the Diagrams

Every architecture diagram uses the same shapes. Solid arrows are synchronous calls on the request path; dashed arrows are asynchronous flows such as events on a queue.

```dot
rankdir=LR;
c [label="client", class=client];
e [label="CDN / gateway", class=edge];
s [label="service", class=service];
k [label="cache", class=cache];
d [label="database", class=store];
q [label="queue / log", class=queue];
w [label="worker / job", class=worker];
x [label="third party", class=external];
c -> e -> s -> k;
s -> d;
s -> q [style=dashed];
q -> w [style=dashed];
w -> x;
{rank=same; k; d; q}
```

## Numbers Worth Knowing

Estimates only need to be right to within a factor of a few, so a handful of conversions carry most of them. A day has 86,400 seconds, close enough to 10^5, and peak traffic usually runs two to three times the daily average.

```text
TRAFFIC                                  STORAGE
1 M requests/day   ≈ 12 per second       2^10 ≈ 10^3   kilo
100 M per day      ≈ 1,200 per second    2^20 ≈ 10^6   mega
1 B per day        ≈ 12,000 per second   2^30 ≈ 10^9   giga
peak               ≈ 2-3 × average       2^40 ≈ 10^12  tera
                                         2^50 ≈ 10^15  peta

LATENCY (the classic table, rounded)
L1 cache reference                       0.5 ns
main memory reference                    100 ns
send 1 KB over a 1 Gbps network          10 µs
read 4 KB at random from SSD             150 µs
read 1 MB sequentially from memory       250 µs
round trip inside a data centre          500 µs
read 1 MB sequentially from SSD          1 ms
disk seek                                10 ms
read 1 MB sequentially from disk         20 ms
packet from California to Europe and back  150 ms
```

Modern hardware has shrunk the memory and SSD rows several times over, but the ratios still hold, and they are what a design needs: memory is about a thousand times faster than a network round trip, a round trip inside a data centre is hundreds of times faster than one across an ocean, and sequential reads beat random ones everywhere.
"""


def load_manifest():
    with open(os.path.join(HERE, "manifest.json")) as f:
        data = json.load(f)
    return data["designs"], data["tiers"]


def md_escape(text):
    return re.sub(r"([\\`*_{}\[\]<>#|~^$])", r"\\\1", text)


def latex_escape(text):
    out = []
    for ch in text:
        if ch in "&%$#_{}":
            out.append("\\" + ch)
        elif ch == "^":
            out.append("\\^{}")
        elif ch == "~":
            out.append("\\~{}")
        elif ch == "\\":
            out.append("\\textbackslash{}")
        else:
            out.append(ch)
    return "".join(out)


def raw_latex(code):
    return "```{=latex}\n" + code + "\n```\n"


def chapter_path(entry):
    return os.path.join(HERE, "chapters", "%02d_%s.md" % (entry["rank"], entry["slug"]))


def read_chapter(entry):
    path = chapter_path(entry)
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n.*?\n---\n(.*)$", text, re.S)
    return m.group(1).strip() if m else text.strip()


def render_diagrams(markdown):
    """Replace every ```dot block with an image of its rendered PDF."""
    out_dir = os.path.join(BUILD, "diagrams")
    os.makedirs(out_dir, exist_ok=True)

    def sub(m):
        body = m.group(1)
        digest = hashlib.sha1(diagrams.wrap(body).encode("utf-8")).hexdigest()[:16]
        rel = "diagrams/%s.pdf" % digest
        path = os.path.join(BUILD, rel)
        if not os.path.exists(path):
            ok, err = diagrams.render(body, "pdf", path)
            if not ok:
                raise SystemExit("diagram failed: " + err)
        return "![](%s)\n" % rel
    return re.sub(r"^```dot\n(.*?)^```\n?", sub, markdown, flags=re.S | re.M)


def chapter_heading(entry):
    plain = "%d. %s" % (entry["rank"], entry["title"])
    meta = "%s · Tier %d" % (entry["subtitle"], entry["tier"])
    return (raw_latex("\\clearpage") + "\n## %s {#d%d}\n\n" % (md_escape(plain), entry["rank"])
            + raw_latex("\\markright{%s}" % latex_escape(plain))
            + "\n[%s]{.meta}\n" % md_escape(meta))


def tier_chapter(tier, name):
    heading = "Tier %d · %s" % (tier, name)
    return ("# %s {#tier%d}\n\n" % (heading, tier)
            + raw_latex("\\markboth{%s}{}" % latex_escape(heading))
            + "\n%s\n" % TIER_INTRO[tier])


def algorithm_appendix(entries):
    index = json.load(open(os.path.join(HERE, "algorithms_index.json")))
    used = {}
    for e in entries:
        body = read_chapter(e)
        m = re.search(r"^\*Algorithms:\*(.*)$", body, re.M)
        if not m:
            continue
        for part in m.group(1).strip().split(" · "):
            mm = re.match(r"^#(\d+) ", part)
            if mm:
                used.setdefault(int(mm.group(1)), []).append(e)
    lines = ["# Where the Algorithms Appear {#algorithm-index}", "",
             raw_latex("\\markboth{Where the Algorithms Appear}{}"),
             "Each algorithm from *150 Algorithms* that a design in this book relies on, with the "
             "chapters that use it. Chapter numbers are links.", "",
             "| Algorithm | Used in |",
             "|:--------------------------------|:----------------------------------------------|"]
    for rank in sorted(used):
        chapters = []
        for e in used[rank]:
            chapters.append("Chapter %d %s" % (e["rank"], md_escape(e["title"])))
        lines.append("| \\#%d %s | %s |" % (rank, md_escape(index[str(rank)]), " · ".join(chapters)))
    return "\n".join(lines) + "\n"


def front_matter():
    return "\n".join([
        "---",
        'title: "50 System Designs"',
        'subtitle: "Ordered by Importance for System Design Interviews"',
        'date: "Requirements · Estimates · API · Data Model · Architecture · Deep Dives"',
        "documentclass: scrbook",
        "classoption: [oneside, 11pt, openany]",
        "papersize: letter",
        "geometry: [margin=0.9in, headheight=14pt]",
        "toc: true",
        "toc-depth: 1",
        "colorlinks: true",
        "linkcolor: accent",
        "urlcolor: accent",
        "toccolor: ink",
        "---",
        "",
    ])


def build_markdown(entries, tiers):
    parts = [front_matter(), INTRO]
    current = None
    for e in entries:
        if e["tier"] != current:
            current = e["tier"]
            parts.append(tier_chapter(current, tiers[str(current)]))
        parts.append(chapter_heading(e))
        parts.append(read_chapter(e) + "\n")
    parts.append(raw_latex("\\clearpage"))
    parts.append(algorithm_appendix(entries))
    return render_diagrams("\n".join(parts))


def write_list(entries, tiers):
    lines = ["50 System Designs, in order of importance", "",
             "Book: system_design_book/50_System_Designs.pdf", ""]
    current = None
    for e in entries:
        if e["tier"] != current:
            current = e["tier"]
            if len(lines) > 4:
                lines.append("")
            lines.append("Tier %d - %s" % (current, tiers[str(current)]))
        lines.append("%d. %s - %s" % (e["rank"], e["title"], e["subtitle"]))
    with open(LIST_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def compile_pdf(md_path):
    """pandoc -> book.tex, LuaLaTeX until references settle, then validate that same log."""
    tex = os.path.join(BUILD, "book.tex")
    cmd = [
        "pandoc", md_path, "-s", "-o", tex,
        "--from", "markdown-tex_math_dollars-raw_tex",
        "--syntax-highlighting", os.path.join(BUILD, "algo.theme"),
        "--lua-filter", os.path.join(BUILD, "sd_filters.lua"),
        "--include-in-header", os.path.join(BUILD, "header.tex"),
    ]
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=BUILD)
    if run.returncode != 0:
        print(run.stderr)
        raise SystemExit("pandoc failed")
    log_path = os.path.join(BUILD, "book.log")
    for attempt in range(3):
        run = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", "book.tex"],
                             capture_output=True, text=True, cwd=BUILD)
        log = open(log_path, encoding="utf-8", errors="replace").read()
        if run.returncode != 0:
            errors = []
            for line in log.split("\n"):
                if line.startswith("!"):
                    errors.append(line)
            raise SystemExit("lualatex failed: " + " | ".join(errors[:3]))
        if attempt >= 1 and "Rerun to get" not in log and "may have changed" not in log:
            break
    pages = re.search(r"Output written on .*?\((\d+) pages", log)
    shutil.move(os.path.join(BUILD, "book.pdf"), PDF)
    print("validated: %s pages, %d missing glyphs, %d overfull lines"
          % (pages.group(1) if pages else "?", log.count("Missing character"),
             log.count("Overfull \\hbox")))


def main(argv):
    entries, tiers = load_manifest()
    only = None
    for arg in argv:
        if arg.startswith("--only="):
            only = set()
            for part in arg[len("--only="):].split(","):
                if part.strip():
                    only.add(int(part))
    present = []
    for e in entries:
        if only is not None and e["rank"] not in only:
            continue
        if read_chapter(e) is not None:
            present.append(e)
        elif "--partial" not in argv and only is None:
            raise SystemExit("chapter %d %s is missing (use --partial)" % (e["rank"], e["slug"]))
    write_list(entries, tiers)
    md_path = os.path.join(BUILD, "book.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(build_markdown(present, tiers))
    if "--md-only" not in argv:
        compile_pdf(md_path)
        print("wrote " + os.path.relpath(PDF, REPO))
    print("wrote %s; %d chapters in the book" % (os.path.relpath(LIST_TXT, REPO), len(present)))


if __name__ == "__main__":
    main(sys.argv[1:])
