# Semiconductor lab reports

LaTeX lab reports and analysis notebooks, one folder per experiment (`a2` to `b7`; `b7` is the
active one). Build a report with `./build.sh <folder>` (for example `./build.sh b7`: xelatex and
biber, artefacts are moved to `<folder>/build/`).

## Workflows

- **PDF review comments** (the user annotated `build/*.pdf` and asks to apply them): skill
  `pdf-review` ([.claude/skills/pdf-review/SKILL.md](.claude/skills/pdf-review/SKILL.md)). Uses the
  `pdfcraft` MCP server; compile into a scratch folder, never into `build/`. The same skill covers
  the other direction: Claude reviews the report and writes suggestions as comments into a PDF in
  `<report>/feedback/` (gitignored).
- **Figures (VectorCraft) and the MCP setup**: [CRAFT_WORKFLOW.md](CRAFT_WORKFLOW.md).
- **Analysis notebooks** (`*/python/task*.ipynb`): [NOTEBOOK_STYLE.md](NOTEBOOK_STYLE.md).
- **Checks on the text**, when asked: agents in [.claude/agents/](.claude/agents/)
  (`latex-check`, `explain-symbols`, `physics-review`, `proofread-grammar`, `proofread-tone`).
