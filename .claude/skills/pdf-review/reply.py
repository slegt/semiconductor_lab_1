#!/usr/bin/env python3
"""Add replies to existing comments of a PDF through the headless PdfCraft CLI (Flatpak).

usage: reply.py <replies.json> <review.pdf>

<replies.json> is a list of {"id": "<comment id from comment_list>", "text": "..."}. The PDF is
changed in place (incremental save, the user's comments and replies stay), so close it in the
PdfCraft window and in the MCP before running this.
"""
import json
import os
import subprocess
import sys

AUTHOR = "Claude"


def main(replies_path, pdf):
    replies = json.load(open(replies_path))
    pdf = os.path.abspath(pdf)
    out_dir = os.path.dirname(pdf)

    steps = [{"tool": "doc_open", "args": {"path": pdf}}]
    for r in replies:
        steps.append({"tool": "comment_reply",
                      "args": {"doc": 1, "id": r["id"], "text": r["text"], "author": AUTHOR}})
    steps.append({"tool": "doc_save", "args": {"doc": 1}})
    steps.append({"tool": "doc_close", "args": {"doc": 1}})

    steps_path = os.path.join(out_dir, ".reply_steps.json")
    json.dump(steps, open(steps_path, "w"), ensure_ascii=False)
    try:
        run = subprocess.run(
            ["flatpak", "run", f"--filesystem={out_dir}:rw", "--command=pdfcraft-cli",
             "ai.storyteller.pdfcraft", "run", "--script", steps_path, "--root", out_dir,
             "--report"], capture_output=True, text=True)
    finally:
        os.remove(steps_path)
    if run.returncode:
        print(run.stdout[-3000:])
        print(run.stderr[-2000:])
    else:
        print("added", len(replies), "replies to", pdf)
    return run


if __name__ == "__main__":
    main(*sys.argv[1:3])
