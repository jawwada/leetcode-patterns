"""Merge site/data/*.json into the site template.

Outputs:
  site/index.html     full standalone page (open locally in a browser)
  site/artifact.html  same page without the document skeleton (for publishing)
  site/problems.json  the merged dataset
Also validates every entry against the schema and checks that every referenced
.py file exists.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

REQUIRED = {
    "slug", "title", "leetcode", "difficulty", "topic", "pattern", "file", "problem",
    "brute_force", "optimization", "intuition", "geometric", "visual", "steps",
    "complexity", "pitfalls", "hints", "code", "related",
}


def main() -> int:
    problems, errors = [], []
    for path in sorted(glob.glob(os.path.join(SITE, "data", "*.json"))):
        with open(path) as f:
            data = json.load(f)
        for p in data:
            missing = REQUIRED - set(p)
            if missing:
                errors.append(f"{path}: {p.get('slug')} missing {sorted(missing)}")
            if not os.path.exists(os.path.join(ROOT, p.get("file", ""))):
                errors.append(f"{path}: {p.get('slug')} file not found: {p.get('file')}")
            if len(p.get("hints", [])) != 3:
                errors.append(f"{path}: {p.get('slug')} needs exactly 3 hints")
            if any("\t" in line for line in p.get("visual", "").split("\n")):
                errors.append(f"{path}: {p.get('slug')} visual contains tabs")
        problems.extend(data)

    slugs = [p["slug"] for p in problems]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        errors.append(f"duplicate slugs: {sorted(dupes)}")
    known = set(slugs)
    for p in problems:
        p["related"] = [r for r in p.get("related", []) if r in known and r != p["slug"]]

    if errors:
        print("\n".join(errors))
        return 1

    with open(os.path.join(SITE, "problems.json"), "w") as f:
        json.dump(problems, f, indent=1)

    with open(os.path.join(SITE, "template.html")) as f:
        template = f.read()
    payload = json.dumps(problems).replace("</", "<\\/")
    fragment = template.replace("__DATA__", payload)
    with open(os.path.join(SITE, "artifact.html"), "w") as f:
        f.write(fragment)
    full = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + fragment + "\n</html>\n"
    )
    with open(os.path.join(SITE, "index.html"), "w") as f:
        f.write(full)
    print(f"built {len(problems)} problems -> site/index.html ({len(full)//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
