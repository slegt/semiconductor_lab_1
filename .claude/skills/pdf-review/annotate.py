#!/usr/bin/env python3
"""Add review comments to a PDF through the headless PdfCraft CLI (Flatpak).

usage: annotate.py <suggestions.json> <clean.pdf> <out.pdf>

<suggestions.json> is a list of {"find": "...", "type": "strikeout"|"highlight", "contents": "...",
"page": N (optional), "all": true (optional), "color": "#RRGGBB" (optional)}. The text in "find" must occur exactly once in the
document, or exactly once on "page" when that is given. <out.pdf> is a copy of <clean.pdf>
(written inside the folder the Flatpak may write to) with the comments added and saved.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

AUTHOR = "Claude"
COLORS = {"strikeout": "#1565C0", "highlight": "#FF9800"}


def norm(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).lower()


def main(suggestions_path, clean, out):
    suggestions = json.load(open(suggestions_path))
    out = os.path.abspath(out)
    out_dir = os.path.dirname(out)
    shutil.copy(clean, out)

    n_pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(
        ["pdfinfo", out], capture_output=True, text=True, check=True).stdout).group(1))
    pages = [norm(subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), out, "-"],
                                 capture_output=True, text=True, check=True).stdout)
             for p in range(1, n_pages + 1)]

    steps = [{"tool": "doc_open", "args": {"path": out}}]
    labels = []
    for s in suggestions:
        needle = norm(s["find"])
        if "page" in s:
            hits = [s["page"]] * pages[s["page"] - 1].count(needle)
        else:
            hits = [p + 1 for p, t in enumerate(pages) for _ in range(t.count(needle))]
        if len(hits) != 1 and not s.get("all"):
            print(f"SKIP ({len(hits)} matches): {s['find']!r}")
            continue
        args = {"doc": 1, "page": hits[0], "type": s["type"], "find": s["find"],
                "contents": s["contents"], "author": AUTHOR,
                "color": s.get("color", COLORS[s["type"]])}
        if s.get("all"):
            args["all"] = True
        steps.append({"tool": "comment_add", "args": args})
        labels.append((hits[0], s["find"]))
    steps.append({"tool": "doc_save", "args": {"doc": 1}})
    steps.append({"tool": "doc_close", "args": {"doc": 1}})

    steps_path = os.path.join(out_dir, ".annotate_steps.json")
    json.dump(steps, open(steps_path, "w"), ensure_ascii=False)
    try:
        run = subprocess.run(
            ["flatpak", "run", f"--filesystem={out_dir}:rw", "--command=pdfcraft-cli",
             "ai.storyteller.pdfcraft", "run", "--script", steps_path, "--root", out_dir,
             "--report"], capture_output=True, text=True)
    finally:
        os.remove(steps_path)
    print(run.stdout[-3000:] if run.returncode else "added", len(labels), "comments to", out)
    if run.returncode:
        print(run.stderr[-2000:])
    try:
        report = json.loads(run.stdout)
        print(json.dumps(report, ensure_ascii=False)[:200])
    except ValueError:
        pass
    return run


if __name__ == "__main__":
    main(*sys.argv[1:4])
