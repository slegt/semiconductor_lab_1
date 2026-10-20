---
name: pdf-review
description: Work through the user's review comments (highlights, strike-outs, sticky notes) in a commented PDF of a LaTeX lab report via the PdfCraft MCP and apply them to the .tex sources. Use when the user says they put comments or annotations into the PDF ("Kommentare in der PDF", "Kommentare einarbeiten", "PDF Review").
---

# PDF review with PdfCraft

The user reviews the compiled report in PdfCraft, saves the comments into the PDF, and asks for them
to be applied. The `pdfcraft` MCP server (entry in the local, gitignored `.mcp.json`, see
`CRAFT_WORKFLOW.md`, "One-time setup") reads files from disk only. Its tools are deferred: load them
with ToolSearch `select:mcp__pdfcraft__doc_open,mcp__pdfcraft__doc_close,mcp__pdfcraft__tool_call,mcp__pdfcraft__text_extract`.

## Procedure

1. **Find the commented PDF.** It lives in `<report>/build/` or `<report>/feedback/` but is not
   always `main.pdf`: a LaTeX build overwrites `main.pdf` and deletes its comments, and the user may
   have commented a copy such as `main_symbols_changes.pdf`. Open the candidates (`ls -lt
   <report>/build/*.pdf <report>/feedback/*.pdf`, newest first) with `doc_open` and take the one
   that has comments. Comments with `author` "Claude" are Claude's own suggestions from an earlier
   round (see below), the user's are "simon". If the comments the user mentions are
   missing, they are probably unsaved in the PdfCraft window: ask them to save, then `doc_close`
   and `doc_open` again.
2. **List the comments.** `comment_list` is a tool, not a command id: call
   `tool_call` with `name: "comment_list"` and `arguments: {"doc": <id>}` (`command_run` rejects it).
   Each entry has `type`, `page`, `contents`, `rect` (points from the **top-left** of the page).
3. **Map every comment to the source.**
   - Text under the comment: `text_extract` with `rect` and `pages` (pad the rect by about 8 pt),
     then `grep -n` a distinctive phrase in `<report>/tex/chapters/*.tex`.
   - Exact extent: the `rect` of a strike-out or highlight is the bounding box of its quads, so a
     strike over two lines always reads x 72 to 523, wherever it really starts and ends. Render and
     look: `pdftoppm -f P -l P -r 200 -x X -y Y -W W -H H -png <pdf> <out>` (pixels = pt x 200/72;
     pdftoppm draws the annotations), then view the PNG.
   - In a marked-up diff build such as `main_symbols_changes.pdf` (blue wavy underline = added
     since git HEAD, red text with strike = removed) the user's strike-outs are red as well. The
     diff's own deletions are red *text*; a strike over black or blue text, or over text that is in
     both versions, is the user's.
4. **Meaning of the markup.**
   - Strike-out: delete the struck text (a struck heading removes the heading only). With `contents`
     or an attached caret reply: replace the struck text with that text.
   - Highlight with a comment: instruction for the highlighted text. A short comment on a gap or
     punctuation mark is an insertion point: `lambda` between two words means insert `$\lambda$`,
     `,` after an equation means a comma at the end of the equation.
   - Sticky note: remark about the nearby object. A highlight without text next to a sticky note
     belongs to it (`!=` on a `=` means `\overset{!}{=}`).
   - A highlight without text and without a sticky note is ambiguous: ask, do not guess.
   - Shorthand: `\cref{...}` and `\imcite{*key*}` mean "insert this reference here"; "paragraph"
     means `\paragraph{...}` instead of a numbered heading; "does not need [H]" means drop the `[H]`
     float option; "remove the empty line after the equation" means no blank line between
     `\end{equation}` and the text (a blank line starts a new paragraph).
   - Comments may be German, the report is English; take wording the user gives verbatim.
5. **Edit the `.tex` files minimally.** After a deletion, repair what the cut leaves behind: a
   dangling comma, a colon before an equation, a missing "and" in a list, an unbalanced
   parenthesis. If the user's wording and the repair differ, keep the repair as small as possible
   and say so in the report.
6. **Compile into a scratch folder**, never into `build/` (that overwrites the user's PDF and its
   comments): `cd <report>/tex && latexmk -pdf -shell-escape -interaction=nonstopmode
   -outdir=<scratchpad>/build main.tex`. Check `main.log` for `^!`, undefined references and
   overfull boxes, and spot-check the edited sentences with `pdftotext`.
7. **Close the documents** (`doc_close`) and **report per comment**: page, what was changed. List
   ambiguous comments and every repair or assumption from step 5 separately. Say so if a comment is
   no longer in the file (the user deletes comments they gave up on).

Page numbers in comments belong to the PDF version that was commented and shift after edits.

## The other direction: Claude reviews the report

For a review round the user can ask Claude to go through the report and write the suggestions as
comments into a PDF, to be approved or discussed and then applied with the procedure above. The
folder is `<report>/feedback/` (gitignored). It holds the archived commented PDF of the previous
round (`main_symbols_changes_commented.pdf`) and the current review PDF (`main_<topic>_review.pdf`).

1. Build the current version in a scratch folder with the engine the user builds with (`build.sh`
   runs XeLaTeX): `cd <report>/tex && latexmk -xelatex -shell-escape -interaction=nonstopmode
   -outdir=<scratchpad>/build main.tex`. Copy `main.pdf` to the scratchpad as the clean source.
2. Read all chapters, collect the findings of the requested kind (for example grammar, spelling,
   wording). Keep every suggestion **atomic**: one word up to a short phrase, no rewritten passages.
   The text to mark must be plain words that occur exactly once on the page, without math, without
   `ff`/`fi`/`ffi` ligature words and without a hyphenation at the line end.
3. Write the findings as a JSON list `[{"find", "type", "contents", "page"?, "all"?}]` and run
   `python3 .claude/skills/pdf-review/annotate.py <list.json> <clean.pdf> <feedback/review.pdf>`.
   It resolves the page of each text, prints `SKIP` for texts that are not found exactly once, adds
   the comments and saves. It runs the headless `pdfcraft-cli run --script` in the Flatpak with
   write access to the feedback folder only, because the `pdfcraft` MCP server is read-only and
   cannot save. Open the result with the MCP (`doc_open`, `comment_list`) to check it.
4. Conventions, so that the next round can be read mechanically:
   - `author` is "Claude". A blue strike-out means: replace the struck text with the text in
     `contents` before the ` | `; the rest is category (Rechtschreibung, Grammatik, Ausdruck,
     Konsistenz, Typografie, Einheit, Terminologie) and a short reason, in German. A strike-out
     whose replacement is empty is a deletion.
   - An orange highlight is a remark or question without a replacement (cross-reference, layout,
     notation); the user decides what to do.
   - To apply the user's answers: untouched suggestions are not approvals; see the reply, the
     review status or a deleted comment, and ask when it is unclear.
