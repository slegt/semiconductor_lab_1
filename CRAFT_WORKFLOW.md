# Figures and PDF Review with the Craft MCP Servers

How figures (VectorCraft) and PDF review comments (PdfCraft) are handled for the LaTeX reports
(`b7/tex`, same approach for the other lab reports). Both apps are installed as user Flatpaks
through the ArtCraft launcher: `ai.storyteller.pdfcraft` and `ai.storyteller.vectorcraft`. Each
ships a headless CLI (`pdfcraft-cli`, `vectorcraft-cli`) with an opt-in `mcp` subcommand
(JSON-RPC on stdin/stdout, no network port of its own).

Folders in `b7/`:

| Folder | Content |
|---|---|
| `assets/` | figures that `\includegraphics` loads (PDF exported from VectorCraft, PNG) |
| `external/` | editable sources: the `.vectorcraft` files, third-party PDFs |
| `build/` | the user's LaTeX output (`main.pdf`); gitignored, overwritten by every build |

## One-time setup

1. **PdfCraft MCP** in the project's `.mcp.json` (gitignored, so it is not in the repo). Read-only
   access to `b7/` only, because the Flatpak sees nothing but Documents and Downloads by default:

   ```json
   "pdfcraft": {
     "command": "flatpak",
     "args": ["run", "--command=pdfcraft-cli",
              "--filesystem=/home/simon/ProjectsTex/semiconductor_lab/b7:ro",
              "ai.storyteller.pdfcraft", "mcp", "--compact",
              "--root", "/home/simon/ProjectsTex/semiconductor_lab/b7"]
   }
   ```

   Claude Code has to be restarted after editing `.mcp.json`. The server runs in its own process:
   it reads files from disk and is **not** connected to a PdfCraft window.

2. **Latin Modern Math** for Greek letters and math italics in figures. LM Roman has no α, ω, ħ.
   The Flatpak sees `~/.local/share/fonts` but not TeX Live, so copy it once:

   ```sh
   cp /usr/share/texmf-dist/fonts/opentype/public/lm-math/latinmodern-math.otf ~/.local/share/fonts/
   ```

   Start VectorCraft after that, so it picks the font up. (Whether an already running instance sees
   it after `text.rescanFonts` was not tested.)

## Figures: drawing in VectorCraft on a shared canvas

VectorCraft is not registered in `.mcp.json`. The app has to run with a control port and a shared
network namespace, otherwise the Flatpak keeps its loopback private:

```sh
flatpak run --share=network ai.storyteller.vectorcraft --control 7979 &
```

- The port listens on `127.0.0.1` and has **no authentication**. Close the app when the session is
  over. `--share=network` is passed per call; no persistent Flatpak override is needed.
- Claude talks to the app through `vectorcraft-cli mcp --connect 127.0.0.1:7979`. If no app
  listens on the port, this fails with "Connection refused". Without `--connect` the CLI falls back
  to a headless session that nobody sees, so always pass the flag.
- Do not run `vectorcraft --help`: the GUI binary starts the app instead of printing help. Use
  the `*-cli` binaries for anything that is not meant to open a window.
- Both of us edit the same document live. **Before changing anything, check `inspect_document`:**
  the `history` list shows whether the user moved, scaled or pasted objects. If so, change objects
  in place by id and do not redraw.

### Driving the app from Bash (no restart needed)

`vc.py` sends a list of tool calls in one MCP session. The app keeps the state, so each run is
independent. `"$id"` in any argument is replaced by the `id` of the previous result (draw an object,
then style it). Images from `render_preview` are saved as PNG next to the call file.

```python
import base64, json, subprocess, sys

calls = json.load(open(sys.argv[1]))      # [{"name": tool, "arguments": {...}}, ...]
cmd = ["flatpak", "run", "--share=network", "--command=vectorcraft-cli",
       "ai.storyteller.vectorcraft", "mcp", "--connect", "127.0.0.1:7979"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, text=True)

def rpc(i, method, params=None):
    msg = {"jsonrpc": "2.0", "id": i, "method": method}
    if params is not None:
        msg["params"] = params
    p.stdin.write(json.dumps(msg) + "\n"); p.stdin.flush()
    while True:
        line = p.stdout.readline()
        if not line:
            return {"error": "server closed", "stderr": p.stderr.read()}
        d = json.loads(line)
        if d.get("id") == i:
            return d

def sub(o, last_id):
    if o == "$id": return last_id
    if isinstance(o, dict): return {k: sub(v, last_id) for k, v in o.items()}
    if isinstance(o, list): return [sub(v, last_id) for v in o]
    return o

rpc(1, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                      "clientInfo": {"name": "claude-code", "version": "0"}})
p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
p.stdin.flush()
last_id = None
for n, c in enumerate(calls, start=2):
    c = sub(c, last_id)
    r = rpc(n, "tools/call", {"name": c["name"], "arguments": c.get("arguments", {})})
    res = r.get("result", r)
    for k, block in enumerate(res.get("content", []) if isinstance(res, dict) else []):
        if block.get("type") == "image":
            fn = f"{sys.argv[1]}.{n}.{k}.png"
            open(fn, "wb").write(base64.b64decode(block["data"]))
            block["data"] = f"<saved to {fn}>"
    try:
        last_id = json.loads(res["content"][0]["text"]).get("id", last_id)
    except Exception:
        pass
    print(json.dumps(res, ensure_ascii=False))
p.stdin.close(); p.wait(timeout=10)
```

Useful tools: `draw_path` (SVG `d` strings, y points down, origin top-left of the artboard),
`draw_shape`, `add_text`, `inspect_document`, `render_preview`, `export`, and
`run_command` with `file.new`, `stroke.set`, `stroke.setAdvanced`, `text.setRangeStyle`,
`artboard.fitToArt`, `artboard.setProps` (`scaleArt: true`), `edit.clear`. `list_commands` prints
the full catalogue with parameters. Check results visually: `render_preview` with
`max_side` of 2400 and crop with PIL.

### Matching the LaTeX document

The figure is drawn at its final physical size, so that it is included at 1:1 and 10 pt really
means 10 pt:

- **Artboard width = inclusion width in bp.** Page setup is A4, `margin=1in`, 10 pt article:
  `\linewidth` = 452.9679 TeX-pt = **451.276 bp** (TeX pt × 72 / 72.27). A figure for
  `0.6\linewidth` gets an artboard of 270.765 bp. Include it with the same fraction:
  `\includegraphics[width=0.6\linewidth]{../assets/<name>.pdf}`. pdfTeX then logs a natural size
  that equals the requested width.
- **Text:** 10 TeX-pt = 9.963 bp; subscripts 7 TeX-pt = 6.974 bp, lowered by 1.494 bp.
- **Fonts:** `LMRoman10` for digits, parentheses, upright text; `Latin Modern Math` for variables,
  using the Unicode math-italic block (E → U+1D438, f → U+1D453, α → U+1D6FC, ω → U+1D714,
  ħ → U+210F, h → U+210E); subscripts upright in `LMRoman7`, as `\mathrm{...}` in the text. U+2005
  around binary operators and relations. Set the fonts per range with `text.setRangeStyle` (byte
  offsets, so compute them from the UTF-8 length).
- **Notation:** the same symbols as the text (`F_n`, `F_p`, `E_g`, `f_n`, `1 - f_n - f_p`), not
  those of the source figure. Drop panel letters such as "(c)".
- **Strokes:** like the TikZ figures in chapter 4: bands 1.6 pt, solid curves 1.2 pt, axes and
  dashed curves 0.8 pt (dash `[3, 3]`), label pointers 0.6 pt. Arrows `Arrow` with
  `arrowAlign: "tip"` (the tip sits on the end point, otherwise it overshoots) and
  `arrowScale` 170 to 200 %.
- If the user rescales a drawing in the app, `artboard.fitToArt` followed by `artboard.setProps`
  with `scaleArt: true` brings it to the target width; then reset text sizes (stored size times the
  object transform is the effective size).

### Saving and placing

The Flatpak cannot write into the project. Get the bytes through MCP and write them on the host:

1. `export` with `format: "pdf"` and no `path` returns `dataBase64`; decode into
   `b7/assets/<name>.pdf`.
2. `export` with `format: "vectorcraft"` the same way into `b7/external/<name>.vectorcraft`.
   (The user can also save from the app; the file dialog goes through the portal.)
3. Replace the placeholder in the chapter with `\includegraphics`, a real caption using the text's
   notation, and a `\label{fig:...}`. A figure taken from a book gets `\imcite{<bibkey>}`; ask which
   source if unknown (keys are in `b7/tex/literature.bib`).
4. Compile into a scratch folder (`latexmk -pdf -outdir=<tmp> main.tex`), check log and page.

## Review: PDF comments through PdfCraft

1. The user opens `b7/build/main.pdf` in PdfCraft, adds comments (highlights, strike-outs, sticky
   notes) and **saves**. Comments that are only in the open window are invisible to the MCP server.
   A LaTeX build overwrites `build/main.pdf`, which deletes the comments. If they are still needed
   after a rebuild, save a copy first.
2. Claude: `doc_open` with the absolute path, then `comment_list`. If the user saved again, call
   `doc_close` and `doc_open` to see the new state. Close the document when done.
3. `comment_list` rectangles are in points from the **top-left** of the page. Map the comments to
   the source visually: `pdftoppm -f P -l P -r 110 -png main.pdf out` draws the annotations, then
   find the text in the `.tex` files. `text_extract` also takes a top-left `rect`.
4. Meaning of the markup: a strike-out deletes the struck text (a struck heading removes the
   heading only). A highlight with a comment is an instruction for the highlighted text. A sticky
   note is a remark about the nearby object. A highlight without text next to a sticky note belongs
   to it (for example `!=` on a `=` means `\overset{!}{=}`, "must equal").
5. Comment shorthand: `\cref{...}` and `\imcite{*key*}` mean "insert this reference here";
   "paragraph" means `\paragraph{...}` instead of a numbered heading; "does not need [H]" means
   drop the `[H]` float option; "remove the empty line after the equation" means no blank line
   between `\end{equation}` and the following text (a blank line starts a new paragraph).
6. Apply every comment, compile into a scratch folder, check the log and the pages, and report
   per comment what was changed. Say so if a comment was ambiguous or no longer in the file (the
   user deletes comments they have given up on); do not guess.

The page numbers in comments belong to the PDF version that was commented. They shift after edits.
